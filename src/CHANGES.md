# 改动说明：加入 Groq Provider

新增第四个可选的 LLM provider —— Groq，免费、不需要绑卡，托管的是
Llama 3.3 70B 这类真正有实力的开源大模型，速度也比本地 Ollama 快很多
（专用 LPU 硬件）。

## 新增/修改的文件

- `providers/groq_provider.py`（新增）：`GroqProvider`。因为 Groq 的 API
  跟 OpenAI 格式完全兼容，这里直接复用官方 `openai` SDK，只是把
  `base_url` 指向 `https://api.groq.com/openai/v1`，代码量很小，
  跟 `openai_provider.py` 几乎一样。
- `providers/__init__.py`：工厂函数加了 `"groq"` 分支。
- `config.py`：
  - `SUPPORTED_PROVIDERS` 加入 `"groq"`
  - 新增 `GROQ_API_KEY`、`GROQ_MODEL`（默认 `llama-3.3-70b-versatile`）
  - `validate()` 新增对应校验：选 `groq` 时检查 `GROQ_API_KEY` 是否填写
- `.env.example`：新增 Groq 配置示例，顶部说明也更新为四个可选值。

## 如何使用

1. 去 https://console.groq.com/keys 用邮箱注册（不需要绑卡）
2. 生成一个 API Key（格式类似 `gsk_...`）
3. 编辑 `.env`：
   ```
   LLM_PROVIDER=groq
   GROQ_API_KEY=gsk_你的key
   GROQ_MODEL=llama-3.3-70b-versatile
   ```
4. 重新运行 `python src/main.py`

不需要装任何新的 Python 依赖——`requirements.txt` 里已有的 `openai` 包
就够用了，因为 Groq 走的是同一套 SDK。

## 免费额度

- 不需要绑卡，注册即可用
- 限制是频率：每分钟 30 次请求、每天 14,400 次，**用不完不会过期**
  （跟 OpenAI/Anthropic/DeepSeek 那种"一次性代币"不是一回事）
- 如果遇到限流，`GroqProvider` 会抛出清晰的 `LLMError` 提示，而不是
  裸露的底层异常

## 可选的其他模型

`GROQ_MODEL` 除了默认的 `llama-3.3-70b-versatile`，还可以试：
- `openai/gpt-oss-120b`（OpenAI 开源出来的模型）
- `qwen/qwen3-32b`
具体以 Groq 控制台当前支持的模型列表为准，模型名可能会随时间调整。

## 已做的验证

沙盒里没有外网装真实的 `openai` 包，所以用了一个最小化的本地 stub 模拟
其接口，验证了：
- `GROQ_API_KEY` 缺失时 `config.validate()` 能正确报错
- 通过 `get_llm_provider()` 能正确路由到 `GroqProvider`
- `base_url` 确实指向了 Groq 而不是 OpenAI 官方地址
- 默认模型名读取正确

**没有**用真实的 Groq API Key 做在线调用测试，建议你拿到 Key 后实际跑
一轮对话验证响应速度和质量。
