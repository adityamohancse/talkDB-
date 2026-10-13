# test_workflow.py

from graph.workflow import build_workflow


def test_question(agent, question):
    """Run a question through the full pipeline."""
    print("=" * 60)
    print(f"🗣️  {question}")
    print("=" * 60)

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

    # Show execution trace
    print("\n📍 Execution Trace:")
    for step in result.get("execution_trace", []):
        print(f"   {step}")

    # Show SQL
    if result.get("sql_query"):
        print(f"\n💻 SQL: {result['sql_query']}")

    # Show answer
    print(f"\n📊 Answer:\n{result['final_answer']}")
    print()


if __name__ == "__main__":
    print("Building TalkDB agent...\n")
    agent = build_workflow()

    # Test 1: Simple query
    test_question(agent, "How many customers do we have?")

    # Test 2: Sales analysis
    test_question(agent, "What are the top 3 product categories by total revenue?")

    # Test 3: Inventory
    test_question(agent, "Which products need restocking urgently?")

    # Test 4: Comparison
    test_question(agent, "Compare sales performance across all store locations")