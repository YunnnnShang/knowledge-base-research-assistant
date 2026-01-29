"""
配置文件 - 研究引擎参数配置
"""

# ========================================
# 模型配置常量
# ========================================
MODEL_NAMES = {
    "embedding": "models/text-embedding-004",      # 向量嵌入模型
    "evaluation": "gemini-1.5-flash",              # 评估模型（快速）
    "synthesis": "gemini-1.5-pro",                 # 合成模型（质量）
    "reranker_default": "BAAI/bge-reranker-v2-m3", # 默认Reranker模型
}

# ========================================
# 检索配置
# ========================================
RETRIEVAL_CONFIG = {
    # 基础参数
    "default_k": 10,                    # 默认检索文档数（增加到10）
    "similarity_threshold": 0.7,        # 相似度阈值
    
    # 高级检索开关
    "use_reranker": True,               # 启用本地Reranker（推荐）
    "use_query_expansion": True,        # 启用查询扩展（推荐）
    "use_hyde": False,                  # HyDE（可选，增加延迟）
    
    # Reranker配置
    "reranker_model": "BAAI/bge-reranker-v2-m3",  # 最佳中文模型
    "reranker_top_k": 8,                # 重排后保留前8个
    
    # 查询扩展配置
    "num_expanded_queries": 2,          # 扩展查询数量
}

# ========================================
# 文档处理配置
# ========================================
DOCUMENT_CONFIG = {
    # 分块参数（优化版）
    "chunk_size": 1500,                 # 块大小（从1000增加到1500）
    "chunk_overlap": 300,               # 重叠大小（20%）
    
    # 分块策略
    "use_semantic_chunking": False,     # 语义分块（实验性）
    
    # PDF处理
    "use_pdfplumber_for_tables": True,  # 表格提取
    "use_docling_for_ocr": False,       # OCR（需要时启用）
}

# ========================================
# 研究引擎配置
# ========================================
RESEARCH_CONFIG = {
    # 模型选择
    "evaluation_model": "gemini-1.5-flash",  # 评估模型（快速）
    "synthesis_model": "gemini-1.5-pro",     # 合成模型（质量）
    
    # 覆盖度评估
    "coverage_threshold": 90,           # 覆盖度阈值（低于此值触发外部研究）
    "use_cot_evaluation": True,         # 使用CoT评估（更准确）
    
    # Deep Research
    "deep_research_timeout": 300,       # 超时时间（秒）
    "deep_research_agent": "deep-research-pro-preview-12-2025",
    
    # 报告合成
    "default_kb_weight": 80,            # 知识库权重
    "report_temperature": 0.3,          # 生成温度
}

# ========================================
# Reranker模型选项
# ========================================
RERANKER_MODELS = {
    "best_chinese": "BAAI/bge-reranker-v2-m3",          # 最佳中文（推荐）
    "balanced": "cross-encoder/ms-marco-electra-base",   # 平衡性能
    "lightweight": "cross-encoder/ms-marco-MiniLM-L-6-v2",  # 轻量级
    "multilingual": "BAAI/bge-reranker-v2-m3",          # 多语言
}

# ========================================
# ChromaDB优化配置
# ========================================
CHROMADB_CONFIG = {
    # HNSW索引优化（提升检索速度）
    "hnsw_space": "cosine",              # 距离度量：cosine（推荐）、l2、ip
    "hnsw_construction_ef": 200,         # 构建时的搜索深度（越大越准确，但构建慢）
    "hnsw_search_ef": 50,                # 搜索时的深度（越大越准确，但搜索慢）
    "hnsw_M": 16,                        # 每个节点的连接数（推荐16-64）
    
    # 量化压缩（减少内存和磁盘占用）
    "enable_quantization": False,        # 是否启用量化（实验性）
    "quantization_type": "scalar",       # 量化类型：scalar, product
    
    # 批处理优化
    "batch_size": 100,                   # 批量添加文档的批次大小
    "max_batch_size": 5000,              # 最大批次大小
}

# ========================================
# 缓存配置
# ========================================
CACHE_CONFIG = {
    "enabled": True,                     # 是否启用缓存
    "cache_dir": ".cache/queries",       # 缓存目录
    "ttl": 3600,                         # 缓存有效期（秒），默认1小时
    "max_size": 1024 * 1024 * 100,       # 最大缓存大小（字节），默认100MB
}

# ========================================
# 性能优化配置
# ========================================
PERFORMANCE_CONFIG = {
    # 缓存
    "enable_query_cache": False,        # 查询结果缓存（可选）
    "cache_ttl": 3600,                  # 缓存有效期（秒）
    
    # 并发
    "max_concurrent_queries": 3,        # 最大并发查询数
    
    # 批处理
    "batch_size": 32,                   # embedding批处理大小
}

# ========================================
# UI配置
# ========================================
UI_CONFIG = {
    "show_advanced_metrics": True,      # 显示高级指标
    "show_query_type": True,            # 显示查询类型
    "show_confidence": True,            # 显示置信度
    "enable_debug_mode": False,         # 调试模式
}


def get_config(category: str = "all") -> dict:
    """
    获取配置
    
    Args:
        category: 配置类别 ("retrieval", "document", "research", "performance", "ui", "all")
    
    Returns:
        配置字典
    """
    configs = {
        "retrieval": RETRIEVAL_CONFIG,
        "document": DOCUMENT_CONFIG,
        "research": RESEARCH_CONFIG,
        "performance": PERFORMANCE_CONFIG,
        "ui": UI_CONFIG,
    }
    
    if category == "all":
        return configs
    
    return configs.get(category, {})
