# evaluate.py

import sys
from evaluation.grader import run_evaluation
from evaluation.llm_judge import run_llm_judge


if __name__ == "__main__":
    # Check if user wants to run limited tests
    max_cases = None
    if len(sys.argv) > 1:
        try:
            max_cases = int(sys.argv[1])
        except ValueError:
            pass

    # Run code-based evaluation
    results = run_evaluation(max_cases=max_cases)

    # Ask if user wants LLM judge
    print("\n" + "-" * 70)
    run_judge = input("Run LLM-as-Judge evaluation? (y/n): ").strip().lower()
    if run_judge == "y":
        run_llm_judge(results)

    print("\n✅ Evaluation complete!")