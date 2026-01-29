# 测试指南

本目录包含项目的自动化测试。

## 🚀 快速开始

### 安装测试依赖

```bash
pip install pytest pytest-cov pytest-asyncio
```

### 运行所有测试

```bash
# 基础测试
pytest

# 详细输出
pytest -v

# 查看测试覆盖率
pytest --cov=modules --cov-report=html

# 生成覆盖率报告后，打开 htmlcov/index.html 查看
```

## 📋 测试文件说明

### test_dependencies.py
测试所有依赖版本是否符合要求：
- ✅ Streamlit >= 1.40
- ✅ LangChain >= 0.3
- ✅ langchain-community >= 0.3.27 (安全补丁)
- ✅ langchain-core >= 0.3.81 (安全补丁)
- ✅ ChromaDB >= 0.5
- ✅ pypdf >= 5.0
- ✅ sentence-transformers >= 3.0

### test_document_processor.py
测试文档处理功能：
- PDF提取（pypdf + pdfplumber）
- DOCX提取
- TXT/MD提取
- 文档分块

### test_reranker.py
测试本地Reranker功能：
- sentence-transformers导入
- Cross-Encoder模型
- 重排序性能

## 🔧 运行特定测试

```bash
# 只运行依赖测试
pytest tests/test_dependencies.py

# 只运行文档处理测试
pytest tests/test_document_processor.py

# 只运行特定测试类
pytest tests/test_dependencies.py::TestDependencies

# 只运行特定测试函数
pytest tests/test_dependencies.py::TestDependencies::test_langchain_version
```

## 📊 测试覆盖率目标

- **目标**: >= 80% 代码覆盖率
- **当前**: 运行 `pytest --cov=modules` 查看

## ⚠️ 注意事项

1. **API Key**: 部分测试需要 `GOOGLE_API_KEY` 环境变量
2. **网络**: 某些测试需要下载模型，首次运行可能较慢
3. **跳过测试**: 可选依赖未安装时，相关测试会自动跳过

## 🐛 常见问题

### ImportError: No module named 'pytest'
```bash
pip install pytest pytest-cov
```

### 模块导入失败
确保从项目根目录运行测试：
```bash
cd /path/to/knowledge-base-research-assistant
pytest
```

### 测试超时
某些测试（如模型下载）可能需要较长时间，增加超时：
```bash
pytest --timeout=300
```

## 📚 扩展阅读

- [pytest文档](https://docs.pytest.org/)
- [pytest-cov文档](https://pytest-cov.readthedocs.io/)
- [Python测试最佳实践](https://docs.python-guide.org/writing/tests/)
