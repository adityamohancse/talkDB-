# agents/sql_agent.py

from sdk.llm_service import llm_task
from database.schema_discovery import discover_schema, schema_to_prompt_text

# Discover schema once when the module loads
_schema = None

def get_schema_text():
    """Load schema once and cache it."""
    global _schema
    if _schema is None:
        schema = discover_schema()
        _schema = schema_to_prompt_text(schema)
    return _schema


def build_sql_prompt():
    """Build the full system prompt with auto-discovered schema."""
    schema_text = get_schema_text()

    return f"""You are a senior SQL expert for a retail business database (PostgreSQL).

{schema_text}

BUSINESS RULES:
- payment_method values: 'cash', 'card', 'mada', 'apple_pay'
- store_location values: 'Riyadh', 'Jeddah', 'Dammam'
- category values: 'Electronics', 'Clothing', 'Food & Beverage', 'Beauty', 
  'Home & Kitchen', 'Sports', 'Books & Stationery', 'Toys'
- Margin = (selling_price - cost_price) / selling_price
- Products need restocking when stock_quantity < reorder_level

RULES:
- Write PostgreSQL-compatible SQL
- NEVER write DELETE, UPDATE, DROP, ALTER, or TRUNCATE
- Always use exact column names from the schema
- Use JOINs when data is needed from multiple tables
- For "last month" calculate from current date
- For "top" questions, use ORDER BY with LIMIT
- Return ONLY the SQL query, no explanation, no markdown formatting"""


@llm_task(system_prompt="")  # placeholder, we'll set it dynamically
def generate_sql(question):
    return question


# We need to override the decorator for dynamic prompts
# So let's use a direct approach instead
from sdk.providers import PROVIDERS
from config import DEFAULT_PROVIDER, DEFAULT_MODEL
import logging

logger = logging.getLogger(__name__)

def generate_sql_query(question, error_context=""):
    """Generate SQL from a natural language question."""
    system_prompt = build_sql_prompt()

    if error_context:
        user_input = f"""Previous SQL had an error: {error_context}
Fix the query.

Question: {question}
Return ONLY the SQL query."""
    else:
        user_input = question

    llm_function = PROVIDERS[DEFAULT_PROVIDER]
    response = llm_function(system_prompt, user_input, DEFAULT_MODEL)

    if response.success:
        # Clean the SQL — remove markdown formatting if any
        sql = response.text.strip()
        sql = sql.replace("```sql", "").replace("```", "").strip()
        logger.info(f"Generated SQL: {sql}")
        return sql
    else:
        logger.error(f"SQL generation failed: {response.error}")
        raise Exception(f"SQL generation failed: {response.error}")