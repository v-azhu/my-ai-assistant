# My AI Assistant

> A personal AI assistant with long-term memory, built with Python.

中文版请见下方。

---

# English

## Vision

Most AI assistants today are stateless. They can answer questions, but they usually do not truly remember the user, understand personal preferences, or grow through long-term interaction.

**My AI Assistant** aims to build a personal AI assistant with long-term memory.

The goal is not only to provide intelligent answers, but also to gradually understand:

- User preferences
- Communication style
- Long-term projects
- Learning goals
- Personal workflows
- Important experiences and decisions

Over time, this assistant should become a personalized partner that grows together with the user.

---

## Project Goals

### Phase 1 - Basic AI Chat

Build a simple AI assistant framework.

Goals:

- Connect with Large Language Models (LLMs)
- Support OpenAI API
- Build a basic Python chat application
- Manage configuration securely
- Create a clean and extensible architecture

---

### Phase 2 - Long-Term Memory

Add long-term memory capability.

Goals:

- Integrate Mem0 as the memory layer
- Store meaningful user information
- Retrieve relevant memories before conversations
- Automatically summarize important information
- Separate short-term conversation context and long-term memory

Example:

Instead of:

> "I don't know anything about this user."

The assistant can gradually understand:

> "This user prefers direct communication, values critical thinking, enjoys building projects, and prefers honest feedback instead of simple agreement."

---

### Phase 3 - Personal AI Assistant

Expand the system into a complete personal AI assistant.

Possible features:

- Multiple LLM providers
- Local models support (Ollama, etc.)
- Voice input and output
- Personal knowledge management
- Document understanding
- RAG (Retrieval-Augmented Generation)
- Tool calling
- Personal workflow automation
- Long-term project management

---

# Architecture Overview

The system will follow a modular architecture:
User
|
|
Chat Interface
|
|
AI Assistant Core
|
+----------------+
| |
LLM Provider Memory Layer
| |
GPT / Ollama Mem0
|
|
Tools & Knowledge

Main components:

### LLM Layer

Responsible for generating responses.

Possible providers:

- OpenAI GPT models
- Local models through Ollama
- Other future LLM providers

---

### Memory Layer

Responsible for long-term memory management.

Technology:

- Mem0

Responsibilities:

- Store important memories
- Retrieve relevant information
- Update user profile
- Build personalized understanding

---

### Application Layer

Responsible for:

- Conversation management
- User interaction
- Configuration
- Workflow control

---

# Project Structure
my-ai-assistant/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
│
├── docs/
│ └── architecture.md
│
├── src/
│ ├── main.py
│ ├── chat.py
│ ├── memory.py
│ └── config.py
│
└── tests/

---

# Design Principles

## 1. Memory First

Memory is a core capability, not an additional feature.

The assistant should gradually understand the user through meaningful interactions.

---

## 2. Model Independent

The system should not depend on a single AI model.

Possible future support:

- OpenAI
- Ollama
- Other LLM providers

---

## 3. Modular Architecture

Each component should be replaceable.

Examples:

- Replace GPT with local models
- Replace memory backend
- Add new tools

---

## 4. Incremental Development

Build step by step:

1. Make it work
2. Make it reliable
3. Make it intelligent
4. Make it personal

---

# Roadmap

## Completed

- [x] Create GitHub repository
- [x] Define project vision

---

## In Progress

- [ ] Create project structure
- [ ] Build basic Python chat interface
- [ ] Connect OpenAI API
- [ ] Integrate Mem0 memory layer

---

## Future

- [ ] Support Ollama local models
- [ ] Add voice interaction
- [ ] Build personal knowledge system
- [ ] Create desktop/mobile interface
- [ ] Develop autonomous assistant capabilities

---

# Long-Term Vision

The ultimate goal is to build a true personal AI assistant.

An assistant that:

- Remembers important conversations
- Understands personal preferences
- Helps manage long-term projects
- Supports learning and creativity
- Evolves together with the user

This project is not just about building a chatbot.

It is about building a long-term intelligent companion.

---

<br>

# 中文版

# My AI Assistant

> 一个基于 Python 构建的具有长期记忆能力的个人 AI 助手。

---

## 项目愿景

目前大多数 AI 助手都是"无状态"的。

它们可以回答问题，但是无法真正长期理解一个用户：

- 用户喜欢什么
- 用户习惯怎样交流
- 用户正在进行什么长期项目
- 用户的思考方式是什么
- 用户的重要经历和决策是什么

**My AI Assistant** 的目标，是打造一个具有长期记忆能力的个人 AI 助手。

它不仅仅是一个聊天机器人，而是一个能够随着时间不断成长、逐渐理解用户的智能伙伴。

---

# 项目目标

## 第一阶段：基础 AI 对话能力

目标：

- 接入大型语言模型
- 支持 OpenAI API
- 创建 Python 聊天程序
- 建立清晰的软件架构
- 为未来扩展做好基础

---

## 第二阶段：长期记忆系统

目标：

引入 Mem0 作为长期记忆层。

实现：

- 保存重要信息
- 自动提取用户偏好
- 根据上下文检索相关记忆
- 区分短期聊天记录和长期记忆

例如：

普通聊天机器人：

> "我不知道这个用户是谁。"

长期记忆 AI：

> "这个用户喜欢直接交流，希望得到真实反馈，不喜欢简单迎合；喜欢研究技术，并且正在构建个人 AI 助手项目。"

---

## 第三阶段：完整个人 AI 助手

未来扩展：

- 支持多个 AI 模型
- 支持 Ollama 本地模型
- 支持语音交互
- 支持个人知识库
- 支持 RAG
- 支持工具调用
- 支持自动化任务
- 支持长期项目管理

---

# 核心设计思想

## 1. 记忆是核心能力

记忆不是附加功能。

一个真正的个人 AI 助手，需要通过长期交流逐渐理解用户。

---

## 2. 模型无关

系统不绑定某一个 AI 模型。

未来可以自由切换：

- OpenAI GPT
- Ollama 本地模型
- 其他大语言模型

---

## 3. 模块化设计

每个模块都可以独立替换。

例如：

- 更换 AI 模型
- 更换记忆数据库
- 增加新的工具能力

---

## 4. 持续迭代

开发过程：

1. 先实现功能
2. 保证稳定
3. 增强智能
4. 实现个性化

---

# 项目长期目标

最终希望打造一个真正属于个人的 AI 助手。

它能够：

- 记住长期交流内容
- 理解用户习惯
- 协助学习和开发
- 管理长期项目
- 成为不断成长的智能伙伴

这个项目的目标，不只是制造一个聊天机器人。

而是探索如何打造一个长期陪伴用户成长的个人 AI 系统。

---

# License

To be decided.