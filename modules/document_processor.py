"""
文档处理模块
负责文档上传、文本提取、分块和向量化
"""

import io
import tempfile
from typing import List
import streamlit as st

# 文档处理库
try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

try:
    from docx import Document
except ImportError:
    Document = None

# LangChain 和向量存储
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

def extract_text_from_pdf(file) -> str:
    """从 PDF 文件提取文本"""
    if PyPDF2 is None:
        raise ImportError("请安装 PyPDF2: pip install PyPDF2")
    
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text_parts = []
        
        for page_num, page in enumerate(pdf_reader.pages):
            text = page.extract_text()
            if text.strip():
                text_parts.append(f"[Page {page_num + 1}]
{text}")
        
        return "\n\n".join(text_parts)
    except Exception as e:
        raise Exception(f"PDF 处理错误: {str(e)}")

def extract_text_from_docx(file) -> str:
    """从 DOCX 文件提取文本"""
    if Document is None:
        raise ImportError("请安装 python-docx: pip install python-docx")
    
    try:
        doc = Document(file)
        text_parts = []
        
        for para in doc.paragraphs:
            if para.text.strip():
                text_parts.append(para.text)
        
        return "\n\n".join(text_parts)
    except Exception as e:
        raise Exception(f"DOCX 处理错误: {str(e)}")

def extract_text_from_txt(file) -> str:
    """从 TXT/MD 文件提取文本"""
    try:
        # 尝试多种编码
        encodings = ['utf-8', 'gbk', 'gb2312', 'latin-1']
        
        for encoding in encodings:
            try:
                file.seek(0)
                text = file.read().decode(encoding)
                return text
            except (UnicodeDecodeError, AttributeError):
                continue
        
        # 如果所有编码都失败
        file.seek(0)
        return file.read().decode('utf-8', errors='ignore')
        
    except Exception as e:
        raise Exception(f"文本文件处理错误: {str(e)}")

def process_uploaded_files(files, api_key: str):
    """
    处理上传的文件并创建向量数据库
    
    Args:
        files: Streamlit 上传的文件列表
        api_key: Google API Key
    
    Returns:
        Chroma 向量数据库实例
    """
    if not files:
        raise ValueError("没有上传文件")
    
    if not api_key:
        raise ValueError("请提供 API Key")
    
    documents = []
    
    # 处理每个文件
    for file in files:
        file_name = file.name
        file_extension = file_name.split('.')[-1].lower()
        
        try:
            # 根据文件类型提取文本
            if file_extension == 'pdf':
                text = extract_text_from_pdf(file)
            elif file_extension == 'docx':
                text = extract_text_from_docx(file)
            elif file_extension in ['txt', 'md']:
                text = extract_text_from_txt(file)
            else:
                st.warning(f"不支持的文件格式: {file_name}")
                continue
            
            if not text.strip():
                st.warning(f"文件为空或无法提取文本: {file_name}")
                continue
            
            # 文本分块
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                separators=["\n\n", "\n", "。", "！", "？", ".", "!", "?", " ", ""],
                length_function=len
            )
            
            chunks = text_splitter.split_text(text)
            
            # 为每个块添加元数据
            for i, chunk in enumerate(chunks):
                documents.append({
                    "content": chunk,
                    "metadata": {
                        "source": file_name,
                        "chunk_id": i,
                        "total_chunks": len(chunks)
                    }
                })
            
            st.success(f"✅ {file_name}: {len(chunks)} 个文档块")
            
        except Exception as e:
            st.error(f"❌ 处理文件失败 {file_name}: {str(e)}")
            continue
    
    if not documents:
        raise ValueError("没有成功处理任何文档")
    
    # 创建 Embeddings
    try:
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",
            google_api_key=api_key
        )
    except Exception as e:
        raise Exception(f"创建 Embeddings 失败: {str(e)}")
    
    # 创建向量数据库
    try:
        # 使用临时目录
        persist_directory = tempfile.mkdtemp(prefix="chroma_")
        
        vectorstore = Chroma.from_texts(
            texts=[doc["content"] for doc in documents],
            metadatas=[doc["metadata"] for doc in documents],
            embedding=embeddings,
            persist_directory=persist_directory
        )
        
        return vectorstore
        
    except Exception as e:
        raise Exception(f"创建向量数据库失败: {str(e)}")

def get_vectorstore_stats(vectorstore) -> dict:
    """获取向量数据库统计信息"""
    try:
        collection = vectorstore._collection
        total_chunks = collection.count()
        
        # 获取所有元数据
        all_data = collection.get()
        sources = set()
        
        if all_data and 'metadatas' in all_data:
            for metadata in all_data['metadatas']:
                if metadata and 'source' in metadata:
                    sources.add(metadata['source'])
        
        return {
            "total_chunks": total_chunks,
            "num_documents": len(sources),
            "sources": list(sources)
        }
    except Exception as e:
        return {
            "total_chunks": 0,
            "num_documents": 0,
            "sources": [],
            "error": str(e)
        }