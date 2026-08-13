# 改动说明：接入 Mem0（本地/云端可切换）

这一轮把 `memory.py` 里的占位实现（关键词交集匹配、内存中存储、重启即丢）
换成了真正的 Mem0，并且像 `providers/` 对 LLM 的处理一样，做了一层
"本地自托管 / 云端托管"可切换的抽象，对应你之前问的"以后能不能迁移到
云端"——现在只需要改 `.env` 里的 `MEMORY_BACKEND` 一个值。

## 新增的 memory_backends/ 包

- `memory_backends/base.py`：抽象接口 `MemoryBackend`（`add` / `search` /
  `get_all`），以及统一异常 `MemoryBackendError`。
- `memory_backends/local_backend.py`：`LocalMemoryBackend`，本地自托管
  Mem0，用你已经装好的 Ollama 做记忆抽取（LLM）和向量化（embedding），
  向量库用 Chroma（存在本地文件夹里，不需要额外装数据库服务）。
- `memory_backends/cloud_backend.py`：`CloudMemoryBackend`，用 Mem0
  Platform（云端托管），需要去 https://app.mem0.ai 注册拿一个 API Key。
- `memory_backends/_utils.py`：`normalize_mem0_results`，统一处理 Mem0
  不同版本里 `search()`/`get_all()` 返回结果格式不完全一致的问题
  （有的版本返回 `{"results": [...]}`，有的版本返回列表；条目里的文本
  字段有的叫 `memory`，有的叫 `content`）。
- `memory_backends/__init__.py`：`get_memory_backend()` 工厂函数，根据
  `config.MEMORY_BACKEND` 决定用哪个后端，懒加载缓存。

## 修改的文件

### config.py
新增：
- `MEMORY_BACKEND`（`local` 或 `cloud`，默认 `local`）
- `MEM0_API_KEY`（云端模式需要）
- `MEM0_USER_ID`（默认 `default_user`——这个项目目前是单用户 CLI 工具，
  所有记忆都挂在这一个固定用户名下；以后如果要支持多用户，需要把真实
  的用户标识传进来替换这个常量）
- `MEM0_VECTOR_STORE_PATH`（本地 Chroma 数据存放路径，默认 `./mem0_data`）
- `MEM0_COLLECTION_NAME`（Chroma 集合名）
- `OLLAMA_EMBED_MODEL`（默认 `nomic-embed-text`——注意这跟对话用的
  `OLLAMA_MODEL` 是两个不同的模型，聊天模型不具备生成 embedding 的能力）

`validate()` 新增了对 `MEMORY_BACKEND` 的校验：选 `cloud` 时检查
`MEM0_API_KEY` 是否已填；选 `local` 时不检查 Ollama 是否真的在跑（因为
状态可能随时变化，交给实际调用时的报错更合适，跟 Ollama LLM provider
的处理方式保持一致）。

### memory.py
整个重写为 `MemoryManager` 包装 `get_memory_backend()`：
- `add_memory(user_message, assistant_response)`：现在每轮对话都会调用，
  把这轮的 user+assistant 消息交给 Mem0，由 Mem0 自己的 LLM 抽取管线决定
  "这段话里有没有值得长期记住的信息"。这正是你在最早的 `chat.py` 里
  注释写的"Future: Replace with Mem0 automatic extraction"，现在算是
  真正实现了。
- `search_memory` / `get_all_memories`：转调对应后端方法，失败时优雅
  降级（返回空列表），不影响主对话流程。

### chat.py
- 删掉了原来 `_looks_like_preference` 那个中英文关键词匹配的占位逻辑——
  不再需要了，Mem0 自己判断该记什么。
- `send_message` 现在无条件调用 `memory_manager.add_memory(user_message,
  response)`，而不是只在命中关键词时才存。

### requirements.txt / .env.example
- 新增 `mem0ai` 依赖。
- 新增上面提到的 Mem0 相关配置项。

## 使用前需要做的准备（本地模式）

1. `pip install -r requirements.txt`（会装上 `mem0ai`，它可能会连带装
   `chromadb`，如果报错提示缺 `chromadb`，单独 `pip install chromadb`
   即可）
2. 确认 Ollama 在跑，并且拉了两个模型：
   ```
   ollama pull llama3.2          # 或你在用的 gemma4:latest 等对话模型
   ollama pull nomic-embed-text  # 专门用于 embedding，Mem0 检索必需
   ```
3. `.env` 里确认：
   ```
   MEMORY_BACKEND=local
   OLLAMA_MODEL=你的对话模型名      # 跟 LLM_PROVIDER=ollama 时用的一致即可
   OLLAMA_EMBED_MODEL=nomic-embed-text
   ```
4. 运行 `python src/main.py`，跟之前一样对话。第一次运行时 Mem0 会在
   `MEM0_VECTOR_STORE_PATH` 指定的文件夹下自动建库，不需要手动建。

## 如何切换到云端

```
MEMORY_BACKEND=cloud
MEM0_API_KEY=你在 app.mem0.ai 拿到的 key
```
不需要改任何代码。

## 已做的验证 / 尚未验证的部分

- 用 mock 后端跑了完整的端到端流程：确认 `search()` 参数正确、检索到的
  记忆正确注入了 system prompt、`add()` 每轮都会带上 user+assistant 两条
  消息调用，不再受旧的关键词过滤限制。
- **没有**在沙盒里跑通真实的 Mem0 + Ollama + Chroma 全链路——沙盒里没装
  Ollama，也没有外网装 `mem0ai` 包。Mem0 的 `search()`/`get_all()`
  参数格式（`user_id=` vs `filters={"user_id": ...}`）在不同版本之间有
  过变化，代码里已经做了 try/except 兼容两种写法，但如果你本地实际跑
  起来后 `[Memory not saved: ...]` 或检索报错里提到某个方法签名不对，
  把完整报错发给我，我再针对你本地这个 `mem0ai` 版本调整。
- 建议先跑几轮真实对话验证：说一句包含个人信息的话（比如"我对坚果过敏"），
  重启程序（这次是真的重启进程），再问一句相关的问题，看记忆是否真的
  跨进程持久化下来了——这是这一轮改动要解决的核心问题。
