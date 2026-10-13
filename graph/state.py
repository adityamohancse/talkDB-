# graph/state.py

from typing import TypedDict, List


class State(TypedDict):
    # Input
    user_question: str

    # Classification
    query_type: str  # simple_query, sales_analysis, inventory_question, full_report, follow_up

    # SQL
    sql_query: str
    sql_results: str
    sql_results_raw: list  # actual data for grounding checks

    # Analysis
    analysis: str
    chart_code: str
    final_answer: str

    # Error handling
    error_message: str
    retry_count: int

    # Conversation memory
    conversation_history: list

    # Execution trace (for UI transparency)
    execution_trace: list