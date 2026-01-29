"""
高级文档处理模块
使用 Docling 进行高质量文档解析
支持 PDF, DOCX, PPTX, HTML, 图片等多种格式
"""

import os
import tempfile
from typing import List, Dict, Optional
from pathlib import Path

class AdvancedDocumentProcessor:
    """高级文档处理器（使用 Docling）"""
    
    def __init__(self, use_ocr: bool = True, use_table_structure: bool = True):
        """
        初始化文档处理器
        
        Args:
            use_ocr: 是否启用 OCR
            use_table_structure: 是否启用表格结构识别
        """
        self.use_ocr = use_ocr
        self.use_table_structure = use_table_structure
        self.converter = None
        
        # 尝试导入 Docling
        try:
            from docling.document_converter import DocumentConverter
            self.converter = DocumentConverter()
        except ImportError:
            print("Warning: Docling not installed. Using fallback methods.")
    
    def process_document(self, file_path: str) -> Dict:
        """
        处理单个文档
        
        Args:
            file_path: 文档路径
            
        Returns:
            包含文本、表格、元数据的字典
        """
        if self.converter:
            return self._process_with_docling(file_path)
        else:
            return self._process_with_fallback(file_path)
    
    def _process_with_docling(self, file_path: str) -> Dict:
        """使用 Docling 处理文档"""
        try:
            result = self.converter.convert(file_path)
            
            return {
                'text': result.document.export_to_markdown(),
                'tables': [table.to_dict() for table in result.document.tables],
                'metadata': {
                    'source': os.path.basename(file_path),
                    'page_count': len(result.document.pages) if hasattr(result.document, 'pages') else 0,
                    'has_tables': len(result.document.tables) > 0,
                    'format': Path(file_path).suffix
                }
            }
        except Exception as e:
            raise Exception(f"Docling 处理失败: {str(e)}")
    
    def _process_with_fallback(self, file_path: str) -> Dict:
        """降级处理方法"""
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == '.pdf':
            return self._fallback_pdf(file_path)
        elif file_ext == '.docx':
            return self._fallback_docx(file_path)
        elif file_ext in ['.txt', '.md']:
            return self._fallback_text(file_path)
        else:
            raise ValueError(f"不支持的文件格式: {file_ext}")
    
    def _fallback_pdf(self, file_path: str) -> Dict:
        """PDF 降级处理"""
        try:
            import PyPDF2
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n\n"
                
                return {
                    'text': text,
                    'tables': [],
                    'metadata': {
                        'source': os.path.basename(file_path),
                        'page_count': len(reader.pages),
                        'format': '.pdf'
                    }
                }
        except Exception as e:
            raise Exception(f"PDF 处理失败: {str(e)}")
    
    def _fallback_docx(self, file_path: str) -> Dict:
        """DOCX 降级处理"""
        try:
            from docx import Document
            doc = Document(file_path)
            text = "\n\n".join([para.text for para in doc.paragraphs if para.text.strip()])
            
            return {
                'text': text,
                'tables': [],
                'metadata': {
                    'source': os.path.basename(file_path),
                    'format': '.docx'
                }
            }
        except Exception as e:
            raise Exception(f"DOCX 处理失败: {str(e)}")
    
    def _fallback_text(self, file_path: str) -> Dict:
        """文本文件降级处理"""
        try:
            encodings = ['utf-8', 'gbk', 'gb2312', 'latin-1']
            text = None
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        text = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            
            if text is None:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
            
            return {
                'text': text,
                'tables': [],
                'metadata': {
                    'source': os.path.basename(file_path),
                    'format': Path(file_path).suffix
                }
            }
        except Exception as e:
            raise Exception(f"文本文件处理失败: {str(e)}")
    
    def process_uploaded_file(self, uploaded_file) -> Dict:
        """处理 Streamlit 上传的文件
        
        Args:
            uploaded_file: Streamlit UploadedFile 对象
            
        Returns:
            处理结果字典
        """
        # 保存到临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name
        
        try:
            result = self.process_document(tmp_path)
            result['metadata']['original_filename'] = uploaded_file.name
            return result
        finally:
            # 清理临时文件
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def batch_process(self, file_paths: List[str]) -> List[Dict]:
        """批量处理文档
        
        Args:
            file_paths: 文件路径列表
            
        Returns:
            处理结果列表
        """
        results = []
        for file_path in file_paths:
            try:
                result = self.process_document(file_path)
                results.append(result)
            except Exception as e:
                print(f"处理 {file_path} 失败: {str(e)}")
                results.append({
                    'text': '',
                    'tables': [],
                    'metadata': {'source': os.path.basename(file_path), 'error': str(e)}
                })
        return results


def create_processor(use_docling: bool = True) -> AdvancedDocumentProcessor:
    """创建文档处理器
    
    Args:
        use_docling: 是否尝试使用 Docling
        
    Returns:
        AdvancedDocumentProcessor 实例
    """
    return AdvancedDocumentProcessor(use_ocr=True, use_table_structure=True)


# 使用示例
if __name__ == "__main__":
    processor = create_processor()
    result = processor.process_document("example.pdf")
    print(f"提取文本长度: {len(result['text'])}")
    print(f"表格数量: {len(result['tables'])}")
