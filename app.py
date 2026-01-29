"""
知识库研究助手 - 主应用
基于 RAG + Deep Research 的智能研究工具
"""

import os
import streamlit as st
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 导入模块
from modules import (
    init_session_state,
    clear_session_state,
    process_uploaded_files,
    get_vectorstore_stats,
    hybrid_research,
    generate_ppt
)

# 页面配置
st.set_page_config(
    page_title="知识库研究助手",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化会话状态
init_session_state()

# 标题
st.title("🔬 知识库研究助手")
st.markdown("**基于 RAG + Google Deep Research 的智能研究工具**")
st.markdown("---")

# 侧边栏 - API Key 配置
with st.sidebar:
    st.header("⚙️ 配置")
    
    api_key = st.text_input(
        "Google API Key",
        value=os.getenv("GOOGLE_API_KEY", ""),
        type="password",
        help="从 https://ai.google.dev/ 获取"
    )
    
    if not api_key:
        st.warning("⚠️ 请输入 API Key")
    else:
        st.success("✅ API Key 已配置")
    
    st.markdown("---")
    
    # 高级设置
    with st.expander("🔧 高级设置"):
        enable_external = st.checkbox(
            "启用外部研究",
            value=True,
            help="当知识库信息不足时，使用 Deep Research 补充"
        )
        
        similarity_threshold = st.slider(
            "检索相似度阈值",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.05,
            help="越高越严格"
        )
        
        kb_weight = st.slider(
            "知识库权重 (%)",
            min_value=50,
            max_value=100,
            value=80,
            step=5,
            help="知识库内容在最终报告中的权重"
        )
    
    st.markdown("---")
    
    if st.button("🗑️ 清空所有数据", type="secondary"):
        clear_session_state()
        st.rerun()

# 主界面 - 标签页
tab1, tab2, tab3 = st.tabs(["📁 文档管理", "🔍 研究分析", "📊 结果展示"])

# Tab 1: 文档上传与管理
with tab1:
    st.header("📁 文档上传与知识库构建")
    
    uploaded_files = st.file_uploader(
        "上传文档（支持 PDF, DOCX, TXT, MD）",
        type=["pdf", "docx", "txt", "md"],
        accept_multiple_files=True,
        help="可以同时上传多个文档"
    )
    
    if uploaded_files and api_key:
        if st.button("🚀 处理文档并构建知识库", type="primary"):
            with st.spinner("处理中，请稍候..."):
                try:
                    vectorstore = process_uploaded_files(uploaded_files, api_key)
                    st.session_state.vectorstore = vectorstore
                    st.session_state.uploaded_file_names = [f.name for f in uploaded_files]
                    
                    # 显示统计信息
                    stats = get_vectorstore_stats(vectorstore)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("文档数量", stats['num_documents'])
                    with col2:
                        st.metric("文档块数量", stats['total_chunks'])
                    with col3:
                        st.metric("平均块大小", f"{stats['total_chunks'] // max(stats['num_documents'], 1)}")
                    
                    st.success("✅ 知识库构建完成！")
                    
                except Exception as e:
                    st.error(f"❌ 处理失败: {str(e)}")
    
    # 显示当前知识库状态
    if st.session_state.vectorstore:
        st.success("✅ 知识库已就绪")
        
        with st.expander("查看已上传的文档"):
            for filename in st.session_state.uploaded_file_names:
                st.markdown(f"- 📄 {filename}")

# Tab 2: 研究分析
with tab2:
    st.header("🔍 智能研究分析")
    
    if not st.session_state.vectorstore:
        st.info("💡 请先在「文档管理」标签页上传文档并构建知识库")
    else:
        research_query = st.text_area(
            "输入您的研究问题",
            value=st.session_state.research_query,
            height=100,
            placeholder="例如：分析人工智能在医疗领域的应用现状和未来趋势...",
            help="尽可能详细地描述您的研究需求"
        )
        
        st.session_state.research_query = research_query
        
        if st.button("🚀 开始研究", type="primary", disabled=not research_query):
            if not api_key:
                st.error("❌ 请先配置 API Key")
            else:
                with st.spinner("研究进行中，这可能需要几分钟..."):
                    try:
                        result = hybrid_research(
                            query=research_query,
                            vectorstore=st.session_state.vectorstore,
                            api_key=api_key,
                            enable_external=enable_external,
                            similarity_threshold=similarity_threshold,
                            kb_weight=kb_weight
                        )
                        
                        st.session_state.research_result = result
                        st.success("✅ 研究完成！")
                        
                    except Exception as e:
                        st.error(f"❌ 研究失败: {str(e)}")

# Tab 3: 结果展示
with tab3:
    st.header("📊 研究结果")
    
    if not st.session_state.research_result:
        st.info("💡 暂无研究结果，请在「研究分析」标签页执行研究")
    else:
        result = st.session_state.research_result
        
        # 显示研究元数据
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("知识库覆盖度", f"{result['kb_coverage']}%")
        
        with col2:
            st.metric("检索文档块", result['num_kb_chunks'])
        
        with col3:
            st.metric("内部来源", len(set(result['internal_sources'])))
        
        with col4:
            external_status = "✅ 已使用" if result['has_external'] else "❌ 未使用"
            st.metric("外部研究", external_status)
        
        st.markdown("---")
        
        # 显示报告
        st.markdown("### 📝 研究报告")
        st.markdown(result['report'])
        
        st.markdown("---")
        
        # 导出选项
        col1, col2 = st.columns(2)
        
        with col1:
            # 下载 Markdown
            st.download_button(
                label="📥 下载 Markdown",
                data=result['report'],
                file_name="research_report.md",
                mime="text/markdown"
            )
        
        with col2:
            # 生成并下载 PPT
            if st.button("🎨 生成 PPT"):
                with st.spinner("生成 PPT 中..."):
                    try:
                        ppt_path = generate_ppt(
                            report_text=result['report'],
                            query=st.session_state.research_query
                        )
                        
                        with open(ppt_path, "rb") as f:
                            st.download_button(
                                label="📥 下载 PPT",
                                data=f,
                                file_name="research_report.pptx",
                                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                            )
                         
                        st.success("✅ PPT 生成成功！")
                        
                    except Exception as e:
                        st.error(f"❌ PPT 生成失败: {str(e)}")

# 页脚
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        <p>🔬 知识库研究助手 v1.0 | Powered by Google Gemini & Deep Research</p>
    </div>
    """,
    unsafe_allow_html=True
)