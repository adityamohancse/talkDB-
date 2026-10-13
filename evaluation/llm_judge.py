# evaluation/llm_judge.py

import json
from sdk.llm_service import llm_task


JUDGE_PROMPT = """You are an expert evaluator for an AI data analyst system.

You will receive:
- The original question
- The SQL query that was generated
- The final answer/report

Grade the response on these criteria (1-5 each):

1. CORRECTNESS: Does the answer accurately reflect what the SQL results would show?
2. COMPLETENESS: Does it fully answer the question asked?
3. CLARITY: Is it well-written and easy to understand?
4. ACTIONABILITY: Does it provide useful, actionable insights?

Respond in EXACTLY this JSON format and nothing else:
{"correctness": 4, "completeness": 5, "clarity": 4, "actionability": 3, "overall": 4, "reason": "Brief explanation"}"""


@llm_task(system_prompt=JUDGE_PROMPT)
def judge_response(evaluation_input):
    return evaluation_input


def run_llm_judge(results):
    """Run LLM-as-judge on completed evaluation results."""
    print("\n" + "=" * 70)
    print("🤖 LLM-as-Judge Evaluation")
    print("=" * 70)

    scores = []

    for detail in results["details"]:
        if detail.get("status") == "❌ ERROR":
            continue

        question = detail["question"]
        sql = detail.get("sql_generated", "N/A")

        print(f"\n  Judging: {question[:50]}...", end=" ")

        judge_input = f"""Question: {question}
SQL Generated: {sql}
Final Answer: {detail.get('answer', 'N/A')}"""

        try:
            response = judge_response(judge_input)
            # Parse JSON from response
            response_clean = response.strip()
            if response_clean.startswith("```"):
                response_clean = response_clean.replace("```json", "").replace("```", "").strip()

            score = json.loads(response_clean)
            scores.append(score)
            print(f"Overall: {score.get('overall', 'N/A')}/5")

        except Exception as e:
            print(f"Failed: {str(e)[:50]}")

    # Print summary
    if scores:
        avg_correctness = sum(s.get("correctness", 0) for s in scores) / len(scores)
        avg_completeness = sum(s.get("completeness", 0) for s in scores) / len(scores)
        avg_clarity = sum(s.get("clarity", 0) for s in scores) / len(scores)
        avg_actionability = sum(s.get("actionability", 0) for s in scores) / len(scores)
        avg_overall = sum(s.get("overall", 0) for s in scores) / len(scores)

        print(f"""
┌─────────────────────────┬──────────┐
│ LLM Judge Metric        │ Avg Score│
├─────────────────────────┼──────────┤
│ Correctness             │ {avg_correctness:.1f}/5    │
│ Completeness            │ {avg_completeness:.1f}/5    │
│ Clarity                 │ {avg_clarity:.1f}/5    │
│ Actionability           │ {avg_actionability:.1f}/5    │
│ Overall                 │ {avg_overall:.1f}/5    │
└─────────────────────────┴──────────┘
        """)

    return scores