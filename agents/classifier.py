# agents/classifier.py

from sdk.llm_service import llm_task

CLASSIFIER_PROMPT = """You are a query classifier for a retail database system.

Classify the user's question into ONE of these categories:

- simple_query: Needs one SQL query with a direct answer.
  Examples: "What's the stock of iPhone cases?", "How many customers do we have?"

- inventory_question: About stock levels, restocking, reorder alerts.
  Examples: "Which products need restocking?", "What's running low?"

- sales_analysis: About revenue, trends, comparisons, performance.
  Examples: "Compare Riyadh vs Jeddah sales", "What's our best selling product?"

- full_report: Needs comprehensive analysis across multiple dimensions.
  Examples: "Give me a complete business overview", "Monthly performance report"

- follow_up: References previous conversation context like "they", "those", "it".
  Examples: "What did they buy?", "Show me more details about that"

Respond with ONLY the category name. Nothing else."""


@llm_task(system_prompt=CLASSIFIER_PROMPT)
def classify_question(question):
    return question