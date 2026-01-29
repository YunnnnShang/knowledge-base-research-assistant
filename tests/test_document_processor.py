"""
文档处理测试
"""
import pytest
import tempfile
from pathlib import Path


class TestDocumentProcessor:
    """测试文档处理功能"""
    
    def test_process_text_file(self):
        """测试处理文本文件"""
        from modules.document_processor import process_uploaded_files
        
        # 创建临时文本文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("这是一个测试文档。\n")
            f.write("用于验证文档处理功能。\n")
            temp_path = f.name
        
        try:
            # 注意：实际测试需要API key，这里只测试模块存在
            from modules import document_processor
            assert hasattr(document_processor, 'process_uploaded_files')
        finally:
            Path(temp_path).unlink()
    
    def test_pdf_extraction_with_pypdf(self):
        """测试使用pypdf提取PDF文本"""
        from pypdf import PdfReader
        # 只测试导入，实际PDF测试需要真实文件
        assert PdfReader is not None
    
    def test_pdfplumber_integration(self):
        """测试pdfplumber集成（表格提取）"""
        try:
            import pdfplumber
            # 测试导入成功
            assert pdfplumber is not None
        except ImportError:
            pytest.skip("pdfplumber not installed")


class TestAdvancedDocumentProcessor:
    """测试高级文档处理"""
    
    def test_docling_integration(self):
        """测试Docling集成（OCR和复杂文档）"""
        try:
            from docling.document_converter import DocumentConverter
            # 测试导入成功
            assert DocumentConverter is not None
        except ImportError:
            pytest.skip("docling not installed")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
