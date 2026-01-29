"""
RAG评估模块
使用RAGAS (RAG Assessment)进行自动化质量评估
GitHub: https://github.com/explodinggradients/ragas (14.5K stars)
"""

from typing import Dict, List, Optional
import warnings
import logging

# 抑制RAGAS的警告
warnings.filterwarnings("ignore", category=FutureWarning)

logger = logging.getLogger(__name__)


class RAGEvaluator:
    """
    RAG评估器
    使用RAGAS框架评估检索和生成质量
    
    评估指标：
    - Faithfulness: 答案是否忠实于上下文（幻觉检测）
    - Answer Relevancy: 答案与问题的相关性
    - Context Precision: 上下文的精确度
    - Context Recall: 上下文的召回率
    - Answer Correctness: 答案正确性（需要ground truth）
    """
    
    def __init__(self, api_key: str):
        """
        初始化评估器
        
        Args:
            api_key: Google API Key
        """
        self.api_key = api_key
        self.metrics_available = False
        
        try:
            from ragas import evaluate
            from ragas.metrics import (
                faithfulness,
                answer_relevancy,
                context_precision,
                context_recall,
            )
            from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
            
            self.evaluate = evaluate
            self.faithfulness = faithfulness
            self.answer_relevancy = answer_relevancy
            self.context_precision = context_precision
            self.context_recall = context_recall
            
            # 初始化LLM和Embeddings
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=api_key,
                temperature=0
            )
            self.embeddings = GoogleGenerativeAIEmbeddings(
                model="models/text-embedding-004",
                google_api_key=api_key
            )
            
            self.metrics_available = True
            
        except ImportError:
            logger.warning("RAGAS未安装，评估功能不可用。运行: pip install ragas")
        except Exception as e:
            logger.error(f"RAGAS初始化失败: {str(e)}", exc_info=True)
    
    def evaluate_response(
        self,
        question: str,
        answer: str,
        contexts: List[str],
        ground_truth: Optional[str] = None
    ) -> Dict:
        """
        评估单个问答对
        
        Args:
            question: 用户问题
            answer: 生成的答案
            contexts: 检索到的上下文列表
            ground_truth: 标准答案（可选，用于计算正确性）
        
        Returns:
            评估结果字典
        """
        if not self.metrics_available:
            return {
                "error": "RAGAS不可用",
                "metrics": {},
                "overall_score": 0.0
            }
        
        try:
            from datasets import Dataset
            
            # 准备数据
            data = {
                "question": [question],
                "answer": [answer],
                "contexts": [contexts],
            }
            
            if ground_truth:
                data["ground_truth"] = [ground_truth]
            
            dataset = Dataset.from_dict(data)
            
            # 选择评估指标
            metrics = [
                self.faithfulness,
                self.answer_relevancy,
                self.context_precision,
            ]
            
            if ground_truth:
                metrics.append(self.context_recall)
            
            # 执行评估
            result = self.evaluate(
                dataset,
                metrics=metrics,
                llm=self.llm,
                embeddings=self.embeddings
            )
            
            # 提取结果
            scores = {
                "faithfulness": result.get("faithfulness", 0.0),
                "answer_relevancy": result.get("answer_relevancy", 0.0),
                "context_precision": result.get("context_precision", 0.0),
            }
            
            if ground_truth:
                scores["context_recall"] = result.get("context_recall", 0.0)
            
            # 计算总分
            overall_score = sum(scores.values()) / len(scores)
            
            return {
                "metrics": scores,
                "overall_score": round(overall_score, 3),
                "interpretation": self._interpret_score(overall_score)
            }
            
        except Exception as e:
            return {
                "error": f"评估失败: {str(e)}",
                "metrics": {},
                "overall_score": 0.0
            }
    
    def evaluate_batch(
        self,
        questions: List[str],
        answers: List[str],
        contexts_list: List[List[str]],
        ground_truths: Optional[List[str]] = None
    ) -> Dict:
        """
        批量评估
        
        Args:
            questions: 问题列表
            answers: 答案列表
            contexts_list: 上下文列表的列表
            ground_truths: 标准答案列表（可选）
        
        Returns:
            批量评估结果
        """
        if not self.metrics_available:
            return {
                "error": "RAGAS不可用",
                "metrics": {},
                "overall_score": 0.0
            }
        
        try:
            from datasets import Dataset
            
            # 准备数据
            data = {
                "question": questions,
                "answer": answers,
                "contexts": contexts_list,
            }
            
            if ground_truths:
                data["ground_truth"] = ground_truths
            
            dataset = Dataset.from_dict(data)
            
            # 选择评估指标
            metrics = [
                self.faithfulness,
                self.answer_relevancy,
                self.context_precision,
            ]
            
            if ground_truths:
                metrics.append(self.context_recall)
            
            # 执行评估
            result = self.evaluate(
                dataset,
                metrics=metrics,
                llm=self.llm,
                embeddings=self.embeddings
            )
            
            # 提取结果
            scores = {
                "faithfulness": result.get("faithfulness", 0.0),
                "answer_relevancy": result.get("answer_relevancy", 0.0),
                "context_precision": result.get("context_precision", 0.0),
            }
            
            if ground_truths:
                scores["context_recall"] = result.get("context_recall", 0.0)
            
            # 计算总分
            overall_score = sum(scores.values()) / len(scores)
            
            return {
                "metrics": scores,
                "overall_score": round(overall_score, 3),
                "sample_count": len(questions),
                "interpretation": self._interpret_score(overall_score)
            }
            
        except Exception as e:
            return {
                "error": f"批量评估失败: {str(e)}",
                "metrics": {},
                "overall_score": 0.0
            }
    
    def _interpret_score(self, score: float) -> str:
        """
        解释评分
        
        Args:
            score: 总体评分 (0-1)
        
        Returns:
            评分解释
        """
        if score >= 0.8:
            return "🟢 优秀 - RAG系统表现出色"
        elif score >= 0.6:
            return "🟡 良好 - RAG系统表现尚可，有改进空间"
        elif score >= 0.4:
            return "🟠 一般 - RAG系统需要优化"
        else:
            return "🔴 较差 - RAG系统需要重大改进"


def quick_evaluate(
    question: str,
    answer: str,
    contexts: List[str],
    api_key: str,
    ground_truth: Optional[str] = None
) -> Dict:
    """
    快速评估函数（便捷接口）
    
    Args:
        question: 用户问题
        answer: 生成的答案
        contexts: 检索到的上下文列表
        api_key: Google API Key
        ground_truth: 标准答案（可选）
    
    Returns:
        评估结果
    """
    evaluator = RAGEvaluator(api_key)
    return evaluator.evaluate_response(question, answer, contexts, ground_truth)


# 评估指标说明
METRICS_DESCRIPTION = {
    "faithfulness": {
        "name": "忠实度 (Faithfulness)",
        "description": "衡量答案是否忠实于给定的上下文，检测幻觉",
        "range": "0.0 - 1.0",
        "good_threshold": 0.7,
        "interpretation": {
            "high": "答案完全基于上下文，无幻觉",
            "medium": "答案大部分基于上下文，有轻微偏差",
            "low": "答案包含未在上下文中出现的信息（幻觉）"
        }
    },
    "answer_relevancy": {
        "name": "答案相关性 (Answer Relevancy)",
        "description": "衡量答案与问题的相关程度",
        "range": "0.0 - 1.0",
        "good_threshold": 0.7,
        "interpretation": {
            "high": "答案直接回答了问题",
            "medium": "答案部分回答了问题",
            "low": "答案偏离了问题主题"
        }
    },
    "context_precision": {
        "name": "上下文精确度 (Context Precision)",
        "description": "衡量检索到的上下文中相关信息的比例",
        "range": "0.0 - 1.0",
        "good_threshold": 0.7,
        "interpretation": {
            "high": "检索的上下文高度相关",
            "medium": "检索的上下文部分相关",
            "low": "检索的上下文包含大量无关信息"
        }
    },
    "context_recall": {
        "name": "上下文召回率 (Context Recall)",
        "description": "衡量所有必需信息是否都被检索到（需要ground truth）",
        "range": "0.0 - 1.0",
        "good_threshold": 0.7,
        "interpretation": {
            "high": "所有必需信息都被检索到",
            "medium": "大部分必需信息被检索到",
            "low": "缺失重要信息"
        }
    }
}
