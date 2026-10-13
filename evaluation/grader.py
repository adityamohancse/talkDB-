# evaluation/grader.py

import json
import time
import logging
from graph.workflow import build_workflow

logging.basicConfig(level=logging.WARNING)


def load_golden_dataset(path="evaluation/golden_dataset.json"):
    """Load test cases from JSON file."""
    with open(path, "r") as f:
        data = json.load(f)
    return data["test_cases"]


def grade_classifier(result, expected_type):
    """Check if classifier got the right type."""
    actual = result.get("query_type", "").strip().lower()
    expected = expected_type.strip().lower()
    return actual == expected


def grade_sql(result, expected_contains):
    """Check if generated SQL contains expected keywords."""
    sql = result.get("sql_query", "").upper()
    if not sql:
        return False, []

    missing = []
    for keyword in expected_contains:
        if keyword.upper() not in sql:
            missing.append(keyword)

    return len(missing) == 0, missing


def grade_answer(result, expected_contains):
    """Check if final answer contains expected content."""
    answer = result.get("final_answer", "").lower()
    if not answer:
        return False, []
    if not expected_contains:
        return True, []  # no expected content to check

    missing = []
    for keyword in expected_contains:
        if keyword.lower() not in answer:
            missing.append(keyword)

    return len(missing) == 0, missing


def run_evaluation(max_cases=None):
    """Run the full evaluation pipeline."""
    print("=" * 70)
    print("🧪 TalkDB Evaluation Pipeline")
    print("=" * 70)

    # Load test cases
    test_cases = load_golden_dataset()
    if max_cases:
        test_cases = test_cases[:max_cases]

    print(f"\nRunning {len(test_cases)} test cases...\n")

    # Build agent
    agent = build_workflow()

    # Track results
    results = {
        "total": len(test_cases),
        "classifier_correct": 0,
        "sql_correct": 0,
        "sql_executed": 0,
        "answer_correct": 0,
        "errors": 0,
        "total_latency": 0,
        "details": []
    }

    for i, test in enumerate(test_cases):
        print(f"  [{i+1}/{len(test_cases)}] {test['question'][:50]}...", end=" ")
        start = time.time()

        try:
            result = agent.invoke({
                "user_question": test["question"],
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

            latency = time.time() - start

            # Grade classifier
            classifier_pass = grade_classifier(result, test["expected_query_type"])
            if classifier_pass:
                results["classifier_correct"] += 1

            # Grade SQL
            sql_pass, sql_missing = grade_sql(result, test["expected_sql_contains"])
            if sql_pass:
                results["sql_correct"] += 1

            # Check if SQL executed successfully
            if result.get("sql_results"):
                results["sql_executed"] += 1

            # Grade answer
            answer_pass, answer_missing = grade_answer(result, test["expected_answer_contains"])
            if answer_pass:
                results["answer_correct"] += 1

            results["total_latency"] += latency

            # Status emoji
            if classifier_pass and sql_pass and answer_pass:
                status = "✅"
            elif sql_pass:
                status = "⚠️"
            else:
                status = "❌"

            print(f"{status} ({latency:.1f}s)")

            # Save details
            results["details"].append({
                "id": test["id"],
                "question": test["question"],
                "category": test["category"],
                "classifier_pass": classifier_pass,
                "sql_pass": sql_pass,
                "sql_missing": sql_missing,
                "answer_pass": answer_pass,
                "answer_missing": answer_missing,
                "latency": latency,
                "sql_generated": result.get("sql_query", ""),
                "status": status
            })

        except Exception as e:
            print(f"❌ ERROR: {str(e)[:50]}")
            results["errors"] += 1
            results["details"].append({
                "id": test["id"],
                "question": test["question"],
                "category": test["category"],
                "status": "❌ ERROR",
                "error": str(e)
            })

    # Print results
    print_results(results)
    return results


def print_results(results):
    """Print a formatted evaluation report."""
    total = results["total"]
    
    print("\n" + "=" * 70)
    print("📊 EVALUATION RESULTS")
    print("=" * 70)

    print(f"""
┌─────────────────────────┬──────────┬──────────┐
│ Metric                  │ Score    │ Pct      │
├─────────────────────────┼──────────┼──────────┤
│ Classifier Accuracy     │ {results['classifier_correct']}/{total}     │ {results['classifier_correct']/total*100:.0f}%      │
│ SQL Keyword Accuracy    │ {results['sql_correct']}/{total}     │ {results['sql_correct']/total*100:.0f}%      │
│ SQL Execution Success   │ {results['sql_executed']}/{total}     │ {results['sql_executed']/total*100:.0f}%      │
│ Answer Accuracy         │ {results['answer_correct']}/{total}     │ {results['answer_correct']/total*100:.0f}%      │
│ Errors                  │ {results['errors']}/{total}      │ {results['errors']/total*100:.0f}%      │
│ Avg Latency             │ {results['total_latency']/total:.1f}s    │          │
└─────────────────────────┴──────────┴──────────┘""")

    # Show failures
    failures = [d for d in results["details"] if d["status"] != "✅"]
    if failures:
        print(f"\n⚠️  Issues ({len(failures)}):")
        for f in failures:
            print(f"  [{f['id']}] {f['question'][:50]}")
            if f.get("sql_missing"):
                print(f"       Missing SQL keywords: {f['sql_missing']}")
            if f.get("answer_missing"):
                print(f"       Missing answer keywords: {f['answer_missing']}")

    # Show by category
    categories = {}
    for d in results["details"]:
        cat = d.get("category", "unknown")
        if cat not in categories:
            categories[cat] = {"total": 0, "passed": 0}
        categories[cat]["total"] += 1
        if d["status"] == "✅":
            categories[cat]["passed"] += 1

    print(f"\n📁 Results by Category:")
    for cat, stats in sorted(categories.items()):
        pct = stats['passed'] / stats['total'] * 100
        bar = "█" * int(pct / 10) + "░" * (10 - int(pct / 10))
        print(f"  {cat:20s} {bar} {stats['passed']}/{stats['total']} ({pct:.0f}%)")


if __name__ == "__main__":
    run_evaluation()