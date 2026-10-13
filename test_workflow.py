
# test_workflow.py

import pytest
from graph.workflow import build_workflow


@pytest.fixture
def agent():
    """Build the TalkDB workflow for testing."""
    return build_workflow()


@pytest.fixture
def question():
    """Provide a sample question for the workflow."""
    return "Show me the total sales for each product"


def test_question(agent, question):
    """Run a question through the workflow."""
    result = agent.invoke({
        "user_question": question,
        "query_type": "",
        "sql_query": "",
        "sql_results": "",
        "sql_results_raw": [],
        "analysis": "",
        "chart_code": "",
        "final_answer": "",
        "error_message": "",
        "retry_count": 0,
        "conversation_history": [],
        "execution_trace": [],
    })

    assert result is not None
    assert isinstance(result, dict)
    print("Workflow executed successfully")
    print("Final answer:", result.get("final_answer", ""))
