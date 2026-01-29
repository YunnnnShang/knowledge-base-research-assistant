# 🔄 升级迁移指南

本指南提供详细的步骤来帮助你将项目升级到推荐的最新版本。

---

## 📋 准备工作

### 1. 备份现有环境

```bash
# 1. 导出当前依赖
pip freeze > requirements-old-backup.txt

# 2. 备份向量数据库（如果已有数据）
cp -r ./chroma_db ./chroma_db_backup

# 3. 创建Git分支
git checkout -b upgrade-dependencies
```

### 2. 创建新的虚拟环境（推荐）

```bash
# 创建新环境避免冲突
python -m venv venv-upgraded
source venv-upgraded/bin/activate  # Linux/Mac
# 或
venv-upgraded\Scripts\activate     # Windows
```

---

## 🚀 阶段1: 基础升级（必需，低风险）

### 步骤1: 安装升级后的依赖

```bash
pip install -r requirements-upgraded.txt
```

### 步骤2: 验证安装

```bash
python -c "import streamlit; print(f'Streamlit: {streamlit.__version__}')"
python -c "import langchain; print(f'LangChain: {langchain.__version__}')"
python -c "import chromadb; print(f'ChromaDB: {chromadb.__version__}')"
```

预期输出:
```
Streamlit: 1.40.2
LangChain: 0.3.16
ChromaDB: 0.5.30
```

### 步骤3: 测试基本功能

```bash
# 启动应用检查是否有导入错误
streamlit run app.py --server.headless true &
sleep 5
pkill -f streamlit
```

---

## 🔧 阶段2: 代码适配（LangChain 0.3.x）

### 需要修改的文件

#### 1. `modules/rag_retriever.py`

**变更点**: LangChain 0.3.x的链式调用语法

**原代码** (LangChain 0.1.x):
```python
from langchain.chains import RetrievalQA
from langchain.chains.question_answering import load_qa_chain

# 旧的链式调用
chain = load_qa_chain(llm, chain_type="stuff")
result = chain.run(input_documents=docs, question=query)
```

**新代码** (LangChain 0.3.x):
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# LCEL (LangChain Expression Language) 风格
prompt = ChatPromptTemplate.from_template(
    "根据以下文档回答问题:\n\n{context}\n\n问题: {question}"
)

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

result = chain.invoke(query)
```

#### 2. `modules/hybrid_research.py`

**变更点**: Google Generative AI集成方式

**原代码**:
```python
from langchain.llms import GoogleGenerativeAI

llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)
```

**新代码**:
```python
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    google_api_key=api_key,
    temperature=0.7,
    convert_system_message_to_human=True
)
```

#### 3. `modules/reranker_retriever.py`

**变更点**: Retriever接口更新

**原代码**:
```python
retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
docs = retriever.get_relevant_documents(query)
```

**新代码** (保持兼容):
```python
retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
# invoke 和 get_relevant_documents 都支持
docs = retriever.invoke(query)
```

---

## 📄 阶段3: 文档处理升级

### 步骤1: 更新 `modules/document_processor.py`

#### 替换 PyPDF2 为 pypdf

**原代码**:
```python
from PyPDF2 import PdfReader

def extract_pdf_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text
```

**新代码**:
```python
from pypdf import PdfReader

def extract_pdf_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text
```

**说明**: pypdf API几乎完全兼容PyPDF2，只需修改import即可。

### 步骤2: （可选）集成Docling进行高级处理

创建新文件 `modules/docling_processor.py`:

```python
"""
高级文档处理器 - 使用Docling
支持表格、公式、OCR
"""

from docling.document_converter import DocumentConverter
from pathlib import Path

def process_with_docling(file_path: str) -> dict:
    """
    使用Docling处理文档
    
    Args:
        file_path: 文档路径
        
    Returns:
        dict: 包含文本、表格、元数据
    """
    converter = DocumentConverter()
    result = converter.convert(file_path)
    
    return {
        "text": result.document.export_to_markdown(),
        "tables": result.document.tables,
        "metadata": result.document.metadata
    }
```

在 `requirements-upgraded.txt` 中取消注释:
```bash
# 取消注释这行
docling==2.15.0
```

重新安装:
```bash
pip install docling==2.15.0
```

---

## 🔍 阶段4: ChromaDB 0.5.x适配

### 主要变化

ChromaDB 0.5.x向后兼容0.4.x，但有一些性能优化的新特性。

#### 1. 持久化配置更新

**原代码**:
```python
import chromadb
from chromadb.config import Settings

client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="./chroma_db"
))
```

**新代码** (推荐):
```python
import chromadb

# 0.5.x 使用更简单的API
client = chromadb.PersistentClient(path="./chroma_db")
```

#### 2. 向量搜索距离函数

**新增选项**:
```python
collection = client.create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"}  # 可选: "l2", "ip", "cosine"
)
```

---

## ✅ 阶段5: 测试和验证

### 1. 创建测试脚本

创建 `tests/test_upgrade.py`:

```python
"""
升级后的功能测试
"""

import pytest
from modules import (
    process_uploaded_files,
    retrieve_from_knowledge_base,
    hybrid_research
)

def test_import_modules():
    """测试所有模块能否正常导入"""
    assert True

def test_streamlit_version():
    """测试Streamlit版本"""
    import streamlit as st
    version = st.__version__
    major, minor = version.split('.')[:2]
    assert int(major) >= 1
    assert int(minor) >= 40

def test_langchain_version():
    """测试LangChain版本"""
    import langchain
    version = langchain.__version__
    major, minor = version.split('.')[:2]
    assert int(major) >= 0
    assert int(minor) >= 3

def test_chromadb_version():
    """测试ChromaDB版本"""
    import chromadb
    version = chromadb.__version__
    major, minor = version.split('.')[:2]
    assert int(major) >= 0
    assert int(minor) >= 5

# 添加更多功能测试...
```

### 2. 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行测试并查看覆盖率
pytest tests/ --cov=modules --cov-report=html
```

### 3. 手动端到端测试

```bash
# 启动应用
streamlit run app.py

# 测试清单:
# ✅ 1. 上传PDF文档
# ✅ 2. 构建知识库
# ✅ 3. 执行研究查询
# ✅ 4. 生成PPT
# ✅ 5. 查看结果
```

---

## 🐛 常见问题和解决方案

### 问题1: LangChain导入错误

**错误信息**:
```
ImportError: cannot import name 'load_qa_chain' from 'langchain.chains'
```

**解决方案**:
```python
# 不要使用已废弃的load_qa_chain
# 改用LCEL风格的链式调用（见阶段2）
```

### 问题2: ChromaDB持久化路径问题

**错误信息**:
```
ValueError: Could not connect to tenant default_tenant
```

**解决方案**:
```python
# 删除旧的数据库文件重新创建
import shutil
shutil.rmtree("./chroma_db", ignore_errors=True)

# 使用新的API
client = chromadb.PersistentClient(path="./chroma_db")
```

### 问题3: Google Generative AI认证错误

**错误信息**:
```
google.api_core.exceptions.Unauthenticated
```

**解决方案**:
```python
# 确保API key正确设置
import os
os.environ["GOOGLE_API_KEY"] = "your-api-key"

# 或在代码中显式传递
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    google_api_key="your-api-key"
)
```

### 问题4: pypdf提取文本为空

**解决方案**:
```python
# 某些PDF可能需要OCR
# 安装OCR支持
pip install pdfplumber

# 使用pdfplumber作为备用
import pdfplumber

def extract_pdf_text_robust(file):
    try:
        # 先尝试pypdf
        from pypdf import PdfReader
        reader = PdfReader(file)
        text = "".join(page.extract_text() or "" for page in reader.pages)
        if text.strip():
            return text
    except:
        pass
    
    # 备用: pdfplumber
    with pdfplumber.open(file) as pdf:
        text = "".join(page.extract_text() or "" for page in pdf.pages)
    
    return text
```

---

## 📊 性能对比测试

创建 `benchmarks/compare_performance.py`:

```python
"""
对比升级前后的性能
"""

import time
import tempfile
from pathlib import Path

def benchmark_document_processing(file_path):
    """测试文档处理速度"""
    from modules.document_processor import process_uploaded_files
    
    start = time.time()
    # 处理文档
    vectorstore = process_uploaded_files([file_path], api_key="test")
    end = time.time()
    
    return end - start

def benchmark_retrieval(vectorstore, query):
    """测试检索速度"""
    from modules.rag_retriever import retrieve_from_knowledge_base
    
    start = time.time()
    results = retrieve_from_knowledge_base(query, vectorstore)
    end = time.time()
    
    return end - start

# 运行基准测试
if __name__ == "__main__":
    print("🔄 性能基准测试")
    print("=" * 50)
    
    # TODO: 添加测试文档和查询
    print("✅ 测试完成")
```

---

## 🎯 回滚计划

如果升级出现问题，按以下步骤回滚:

```bash
# 1. 切换回原分支
git checkout main

# 2. 恢复旧的虚拟环境
deactivate
source venv/bin/activate  # 原来的环境

# 3. 恢复向量数据库备份
rm -rf ./chroma_db
cp -r ./chroma_db_backup ./chroma_db

# 4. 验证应用正常运行
streamlit run app.py
```

---

## ✨ 升级后的新特性

### 1. LangChain LCEL

```python
# 更灵活的链式调用
from langchain_core.runnables import RunnableParallel

chain = RunnableParallel({
    "context": retriever,
    "question": RunnablePassthrough()
}) | prompt | llm | parser
```

### 2. ChromaDB性能增强

```python
# 支持更多查询选项
collection.query(
    query_texts=["query"],
    n_results=10,
    where={"source": "pdf"},  # 元数据过滤
    where_document={"$contains": "AI"}  # 文档内容过滤
)
```

### 3. Streamlit新组件

```python
import streamlit as st

# 对话框
@st.dialog("确认操作")
def confirm_dialog():
    st.write("确定要继续吗？")
    if st.button("确定"):
        st.rerun()

# 更好的状态管理
if "counter" not in st.session_state:
    st.session_state.counter = 0
```

---

## 📞 获取帮助

如果遇到问题:

1. **查看日志**:
   ```bash
   streamlit run app.py --logger.level=debug
   ```

2. **社区支持**:
   - LangChain Discord: https://discord.gg/langchain
   - Streamlit Forum: https://discuss.streamlit.io/
   - GitHub Issues: 在项目仓库提issue

3. **文档**:
   - [LangChain 0.3 迁移指南](https://python.langchain.com/docs/versions/v0_3)
   - [ChromaDB文档](https://docs.trychroma.com/)
   - [Streamlit文档](https://docs.streamlit.io/)

---

**升级完成后，记得提交代码并更新README！** 🎉
