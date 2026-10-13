# test_agents.py

from agents.classifier import classify_question
from agents.sql_agent import generate_sql_query
from agents.analyst import analyze_data
from database.connection import run_query
from database.security import validate_sql


def test_full_flow(question):
    """Test the full flow: classify → generate SQL → execute → analyze."""
    print("=" * 60)
    print(f"Question: {question}")
    print("=" * 60)

    # Step 1: Classify
    print("\n📋 Step 1: Classifying...")
    query_type = classify_question(question)
    print(f"   Type: {query_type}")

    # Step 2: Generate SQL
    print("\n🔧 Step 2: Generating SQL...")
    sql = generate_sql_query(question)
    print(f"   SQL: {sql}")

    # Step 3: Validate SQL
    print("\n🔒 Step 3: Validating SQL...")
    is_safe, reason = validate_sql(sql)
    print(f"   Safe: {is_safe} ({reason})")

    if not is_safe:
        print("   ❌ SQL blocked for security reasons")
        return

    # Step 4: Execute SQL
    print("\n⚡ Step 4: Executing SQL...")
    result = run_query(sql)
    if result["success"]:
        print(f"   Rows returned: {result['row_count']}")
        # Show first 3 rows
        for row in result["data"][:3]:
            print(f"   {row}")
    else:
        print(f"   ❌ Error: {result['error']}")
        return

    # Step 5: Analyze (only for non-simple queries)
    if query_type.strip() != "simple_query":
        print("\n📊 Step 5: Analyzing...")
        analysis_input = f"""Question: {question}

SQL Results:
{result['data'][:20]}"""
        analysis = analyze_data(analysis_input)
        print(f"   {analysis}")

    print("\n✅ Done!")
    print()


if __name__ == "__main__":
    # Test 1: Simple query
    test_full_flow("How many products do we have?")

    # Test 2: Sales analysis
    test_full_flow("What are the top 5 best selling products?")

    # Test 3: Inventory
    test_full_flow("Which products are below reorder level and need restocking?")