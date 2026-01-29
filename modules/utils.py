"""
工具函数模块
提供通用的辅助功能
"""

import time
import streamlit as st
from google import genai


def init_session_state():
    """初始化 Streamlit 会话状态"""
    if 'vectorstore' not in st.session_state:
        st.session_state.vectorstore = None
    
    if 'research_result' not in st.session_state:
        st.session_state.research_result = None
    
    if 'uploaded_file_names' not in st.session_state:
        st.session_state.uploaded_file_names = []
    
    if 'research_query' not in st.session_state:
        st.session_state.research_query = ""


def clear_session_state():
    """清空会话状态"""
    st.session_state.vectorstore = None
    st.session_state.research_result = None
    st.session_state.uploaded_file_names = []
    st.session_state.research_query = ""


def wait_for_interaction_completion(
    client: genai.Client,
    interaction_id: str,
    timeout: int = 300
) -> object:
    """
    等待 Gemini Interaction 完成
    
    Args:
        client: Gemini Client
        interaction_id: Interaction ID
        timeout: 超时时间（秒）
    
    Returns:
        完成的 Interaction 对象
    """
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    elapsed = 0
    check_interval = 3
    
    while elapsed < timeout:
        try:
            interaction = client.interactions.get(interaction_id)
            
            if interaction.status != "in_progress":
                progress_bar.progress(100)
                status_text.success(f"✅ 完成！状态: {interaction.status}")
                time.sleep(1)
                status_text.empty()
                progress_bar.empty()
                return interaction
            
            # 更新进度
            elapsed += check_interval
            progress = min(95, int((elapsed / timeout) * 100))
            progress_bar.progress(progress)
            status_text.text(f"⏳ Deep Research 进行中... ({elapsed}秒)")
            
            time.sleep(check_interval)
            
        except Exception as e:
            status_text.error(f"检查状态时出错: {str(e)}")
            time.sleep(check_interval)
            elapsed += check_interval
    
    # 超时后最后检查一次
    try:
        interaction = client.interactions.get(interaction_id)
        progress_bar.empty()
        status_text.empty()
        return interaction
    except Exception as e:
        progress_bar.empty()
        status_text.empty()
        return None
