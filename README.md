# 🧠 知识库驱动的研究助手 + PPT 生成器

**上传文档 → 智能检索 → Deep Research → 自动生成PPT**

## 🌟 功能特性

### 核心功能
- 📚 **智能知识库管理** - 支持 PDF/DOCX/TXT/Markdown 多格式文档上传
- 🔍 **混合检索策略** - RAG 向量检索 + Deep Research 网络搜索
- 🎯 **Rerank 精排** - 两阶段检索提升准确率 15-30%
- 📊 **自动 PPT 生成** - 一键生成专业演示文稿
- 🧠 **智能分块** - 自适应文档类型和语言的分块策略
- 💡 **高级 Prompt** - Chain of Thought + 结构化输出

### 技术优势

| 特性 | 标准版 | Pro 版 |
|------|--------|--------|
| 文档分块 | 固定 1000 字符 | 自适应 1500-2000 |
| 重叠策略 | 20% | 20-25%（智能调整） |
| 检索方��� | 单阶段向量检索 | 两阶段（粗排+精排） |
| Rerank | ❌ | ✅ LLM Rerank |
| Prompt 工程 | 基础模板 | CoT + Few-shot |

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Google API Key ([获取地址](https://ai.google.dev/))

### 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/YunnnnShang/knowledge-base-research-assistant.git
cd knowledge-base-research-assistant

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置 API Key（可选）
cp .env.example .env
# 编辑 .env 文件，添加你的 GOOGLE_API_KEY

# 4. 启动应用
streamlit run app.py              # 标准版
# 或
streamlit run app_advanced.py     # Pro 版（推荐）
```

## 📂 项目结构

```
knowledge-base-research-assistant/
├── app.py                              # 标准版应用
├── app_advanced.py                     # Pro 版应用（推荐）
├── modules/
│   ├── __init__.py
│   ├── document_processor.py           # 标准文档处理
│   ├── advanced_document_processor.py  # 智能文档处理
│   ├── rag_retriever.py                # RAG 检索
│   ├── reranker_retriever.py           # Rerank 检索
│   ├── hybrid_research.py              # 混合研究引擎
│   ├── ppt_generator.py                # PPT 生成器
│   ├── advanced_prompts.py             # 高级 Prompt 模板
│   └── utils.py                        # 工具函数
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 📖 使用指南

### 基础工作流

1. **上传文档** - 支持 PDF/DOCX/TXT/MD
2. **配置参数** - 设置知识库权重、相似度阈值
3. **输入问题** - 描述研究主题
4. **获取报告** - 自动生成结构化报告
5. **导出 PPT** - 一键生成演示文稿

## 🔧 技术栈

- **前端**: Streamlit
- **LLM**: Google Gemini 1.5 Pro/Flash
- **Embedding**: text-embedding-004
- **向量数据库**: ChromaDB
- **RAG 框架**: LangChain
- **PPT 生成**: python-pptx

## 📈 升级指南

项目已完成全面的技术栈分析和升级建议，详见以下文档：

- 📋 **[升级分析报告.md](./升级分析报告.md)** - 执行摘要（5分钟快速阅读）
- 📊 **[UPGRADE_RECOMMENDATIONS.md](./UPGRADE_RECOMMENDATIONS.md)** - 详细升级建议和GitHub最新技术方案
- 🔄 **[MIGRATION_GUIDE.md](./MIGRATION_GUIDE.md)** - 分阶段迁移指南
- 📉 **[TECHNOLOGY_COMPARISON.md](./TECHNOLOGY_COMPARISON.md)** - 技术方案深度对比
- 📦 **[requirements-upgraded.txt](./requirements-upgraded.txt)** - 升级后的依赖清单

### 快速升级

```bash
# 创建新环境并升级
python -m venv venv-upgraded
source venv-upgraded/bin/activate  # Linux/Mac
pip install -r requirements-upgraded.txt
```

预期收益：**性能提升40%**，**稳定性大幅改进**，**成本降低90%**

---

## 📄 许可证

MIT License

---

Made with ❤️ by YunnnnShang
