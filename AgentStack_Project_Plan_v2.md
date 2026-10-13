# 🤖 AgentStack — Full Project Plan (v2 — Refined)

> Turn any database into a conversational AI analyst.
> Ask questions in plain English. Get answers with charts.

---

## What is AgentStack?

An open-source framework that lets non-technical users query ANY database using natural language. It auto-discovers your schema, plans multi-step queries, self-corrects errors, and generates interactive dashboards — all through conversation.

**The pain point it solves:** Every company has data locked in databases that only SQL-literate people can access. Business users wait hours or days for analysts to pull data. AgentStack eliminates that friction.

---

## Key Features (Star-Worthy Differentiators)

### 1. Auto Schema Discovery
No manual schema writing. Point AgentStack at any PostgreSQL database and it automatically:
- Reads all tables, columns, data types
- Discovers foreign key relationships
- Samples data to understand value patterns
- Uses a cheap LLM call to generate business-friendly column descriptions

```python
# User just does this:
agent = AgentStack(database_url="postgresql://localhost/mydb")
# Framework auto-discovers everything
```

### 2. Semantic Mapping (Column Translation)
Database columns are often cryptic (e.g., `cust_ltv_scr` instead of "Customer Lifetime Value"). AgentStack auto-generates a `metadata.yaml` that translates DB jargon into business terms.

```yaml
# Auto-generated metadata.yaml (user can refine)
tables:
  products:
    description: "Product catalog with pricing and stock levels"
    columns:
      sku: "Stock Keeping Unit — unique product identifier"
      cost_price: "Price the merchant pays to the supplier"
      selling_price: "Price the customer pays"
      reorder_level: "Minimum stock before restock alert triggers"
```

The SQL agent uses this metadata in its system prompt, producing much better queries.

### 3. Multi-Step Query Planner
Most Text-to-SQL tools try to answer everything in one query. Complex business questions need multiple steps.

```
User: "Which category has highest margin but lowest sales?"

Query Planner breaks into:
    Step 1: Calculate avg margin by category (from products table)
    Step 2: Calculate total sales volume by category (from sales table)
    Step 3: Join and rank — highest margin + lowest volume

Each step is a separate SQL query, executed in sequence.
Results from all steps are synthesized by the Analyst agent.
```

### 4. Self-Correcting Pipeline with Transparency
Every step is visible to the user in the Streamlit UI:

```
✅ Schema loaded (4 tables, 22 columns)
✅ Classified as: complex_analysis
✅ Query plan: 3 steps
✅ Step 1 SQL executed (0.3s)
⚠️ Step 2 SQL failed — self-correcting...
✅ Step 2 SQL corrected and executed (0.8s)
✅ Step 3 SQL executed (0.2s)
✅ Analysis generated — numbers verified ✓
✅ Dashboard ready
```

### 5. Conversational Memory (Follow-Up Questions)
The agent remembers context from previous turns:

```
User: "Who are my top 5 customers?"
Agent: Shows top 5 customers by total purchases

User: "What did they buy last month?"
Agent: Remembers "they" = the 5 customers from previous answer
       Queries their purchases for last month
```

Implementation: conversation history stored in LangGraph state. Each turn appends to the history. The SQL agent sees previous questions + results as context.

### 6. Human-in-the-Loop (Review Mode)
For complex multi-step queries, the user can review the plan before execution:

```
🧠 Query Plan (click to expand):
    Step 1: Get revenue by region for Q1 2025
    Step 2: Get revenue by region for Q4 2024
    Step 3: Calculate quarter-over-quarter change

    [Execute All]  [Edit Plan]  [Cancel]
```

This builds trust and looks impressive in the demo.

### 7. Security Layer
- Read-only database connections by default
- SQL validator blocks destructive commands (DROP, DELETE, UPDATE, ALTER, TRUNCATE)
- No raw SQL injection — all queries go through parameterized execution
- API key authentication for the FastAPI backend

```python
# security/sql_validator.py
BLOCKED_KEYWORDS = ['DROP', 'DELETE', 'UPDATE', 'ALTER', 'TRUNCATE', 'INSERT']

def validate_sql(sql: str) -> bool:
    sql_upper = sql.upper().strip()
    for keyword in BLOCKED_KEYWORDS:
        if keyword in sql_upper:
            return False
    return True
```

### 8. Provider-Agnostic SDK
Switch LLM providers with one config change:

```python
# config.py
DEFAULT_PROVIDER = "gemini"    # or "openai", "claude", "ollama"
DEFAULT_MODEL = "gemini-pro"
FALLBACK_PROVIDER = "openai"   # automatic failover
```

### 9. Built-in Evaluation Framework
```bash
python evaluate.py

# Output:
# ┌──────────────────────┬──────────┐
# │ Metric               │ Score    │
# ├──────────────────────┼──────────┤
# │ SQL Accuracy          │ 93%     │
# │ Hallucination Rate    │ 4%      │
# │ Avg Latency (simple)  │ 2.8s    │
# │ LLM Judge Score       │ 4.3/5   │
# └──────────────────────┴──────────┘
```

### 10. Beautiful Interactive Dashboard
Plotly charts with hover, zoom, export. Generated SQL visible in expandable tabs. Step-by-step execution trace. Data tables with sorting.

---

## Tech Stack (All Free)

| Component | Tool | Cost |
|-----------|------|------|
| Database | PostgreSQL on Supabase | Free (500MB) |
| LLM (primary) | Google Gemini API | Free (60 req/min) |
| LLM (fallback) | OpenAI (optional) | Free trial credits |
| LLM-as-Judge | Gemini (same free tier) | Free |
| Agent framework | LangGraph | Free (open source) |
| Backend | FastAPI | Free (open source) |
| Frontend | Streamlit | Free (open source) |
| Hosting | Streamlit Cloud | Free (1 public app) |
| Charts | Plotly | Free (open source) |
| Containerization | Docker | Free (personal use) |
| Version control | GitHub | Free (public repos) |

**Total cost: $0**

---

## Agent Architecture (6 Agents)

```
USER: "Why did revenue drop last quarter in the South region?"
        │
        ↓
SCHEMA DISCOVERY (auto-reads DB on startup)
    - Tables, columns, types, relationships
    - Generates semantic descriptions
    - Cached — runs once per session
        │
        ↓
AGENT 1: CLASSIFIER
    Decides query type:
    - simple_query (one SQL, direct answer)
    - multi_step (needs query planner)
    - follow_up (uses conversation memory)
        │
        ↓
AGENT 2: QUERY PLANNER (for multi-step only)
    Breaks complex question into ordered steps:
    Step 1: "Get Q1 revenue by region"
    Step 2: "Get Q4 revenue by region for comparison"
    Step 3: "Calculate change and identify South specifically"
    
    Human-in-the-loop: user can review plan before execution
        │
        ↓
AGENT 3: SQL AGENT (runs for each step)
    - Generates SQL using schema + metadata + few-shot examples
    - Validation: separate LLM call checks SQL logic
    - Execution: Python runs query against PostgreSQL
    - Self-correction: errors fed back, retry up to 3x
    - Security: blocks destructive SQL before execution
        │
        ↓
AGENT 4: ANALYST
    - Synthesizes results from all steps
    - Calculates metrics (margins, lifts, trends)
    - Grounding check: Python code verifies numbers
    - Uses conversation history for follow-up context
        │
        ↓
AGENT 5: VISUALIZER
    - Decides best chart type based on data shape
    - Generates Plotly code
    - Comparison → grouped bar chart
    - Trend → line chart
    - Composition → pie chart
    - Detailed → sortable data table
        │
        ↓
AGENT 6: REPORT GENERATOR
    - Key findings (2-3 bullets)
    - Interactive chart
    - Generated SQL (expandable, for transparency)
    - Execution trace (expandable)
    - Recommendation
        │
        ↓
STREAMLIT DASHBOARD displays everything
```

### Flow Paths

```
SIMPLE QUERY:
    Classifier → SQL Agent → Visualizer → Display (~3s)

MULTI-STEP ANALYSIS:
    Classifier → Query Planner → [Review] → SQL Agent (×N steps)
    → Analyst → Visualizer → Report → Display (~10-15s)

FOLLOW-UP QUESTION:
    Classifier (detects follow-up) → reads conversation memory
    → SQL Agent (with previous context) → continues as normal
```

### Self-Correction Loop

```
SQL Agent generates SQL
        ↓
Security Check (block DROP/DELETE/UPDATE)
        ↓                    ↓
    SAFE                  BLOCKED → return error, don't retry
        ↓
Validation Node (separate LLM checks logic)
        ↓                    ↓
    VALID                INVALID → feed reason → SQL Agent retries
        ↓
Execute SQL (try/except)
        ↓                    ↓
    SUCCESS              DB ERROR → feed error → SQL Agent retries
        ↓
Grounding Check (Python verifies numbers in analysis)
        ↓                    ↓
    PASSED               WRONG → feed correct numbers → Analyst retries
```

---

## LangGraph State Definition

```python
from typing import TypedDict, List, Optional

class QueryStep(TypedDict):
    step_number: int
    description: str          # "Get Q1 revenue by region"
    sql: str                  # generated SQL
    results: str              # query results
    status: str               # pending, success, failed, retrying

class ConversationTurn(TypedDict):
    question: str
    answer: str
    sql_queries: List[str]
    key_entities: List[str]   # ["top 5 customers", "South region"]

class State(TypedDict):
    # Input
    user_question: str
    
    # Schema context
    schema_info: str              # auto-discovered schema
    metadata: str                 # semantic column descriptions
    
    # Classification
    query_type: str               # simple_query, multi_step, follow_up
    
    # Query planning
    query_plan: List[QueryStep]   # ordered steps for multi-step
    current_step: int             # which step we're on
    
    # Execution
    sql_query: str                # current SQL being executed
    sql_results: str              # current results
    all_results: str              # accumulated results from all steps
    
    # Quality
    error_message: str
    retry_count: int
    validation_status: str        # valid, invalid
    grounding_status: str         # passed, failed
    
    # Analysis
    analysis: str
    chart_code: str
    final_report: str
    
    # Memory
    conversation_history: List[ConversationTurn]
    
    # Execution trace (for transparency UI)
    execution_trace: List[str]    # ["✅ Schema loaded", "✅ Classified as..."]
```

---

## File Structure

```
agentstack/
├── agentstack/
│   ├── __init__.py
│   ├── config.py                    # all settings (DB, LLM, retries)
│   │
│   ├── sdk/                         # central LLM infrastructure
│   │   ├── __init__.py
│   │   ├── llm_service.py           # @llm_task decorator
│   │   ├── providers.py             # gemini, openai provider functions
│   │   └── response.py              # LLMResponse class
│   │
│   ├── database/                    # data layer
│   │   ├── __init__.py
│   │   ├── connection.py            # PostgreSQL connection
│   │   ├── schema_discovery.py      # auto-read tables, columns, types
│   │   ├── semantic_mapper.py       # LLM generates column descriptions
│   │   ├── query_executor.py        # safe SQL execution with security
│   │   └── security.py             # SQL validator (block destructive SQL)
│   │
│   ├── agents/                      # the 6 agents
│   │   ├── __init__.py
│   │   ├── classifier.py            # query type classification
│   │   ├── query_planner.py         # breaks complex Qs into steps
│   │   ├── sql_agent.py             # generates SQL + system prompt
│   │   ├── validator.py             # separate LLM validates SQL logic
│   │   ├── analyst.py               # business analysis + grounding check
│   │   └── visualizer.py            # auto-chart with Plotly
│   │
│   ├── graph/                       # LangGraph orchestration
│   │   ├── __init__.py
│   │   ├── state.py                 # State TypedDict (above)
│   │   ├── nodes.py                 # node functions
│   │   ├── routing.py               # conditional routing functions
│   │   └── workflow.py              # build and compile the graph
│   │
│   └── evaluation/                  # quality assurance
│       ├── __init__.py
│       ├── golden_dataset.json      # 30-50 test cases
│       ├── grader.py                # code-based grading
│       └── llm_judge.py             # LLM-as-judge
│
├── demo/                            # demo data for instant setup
│   ├── schema.sql                   # CREATE TABLE statements
│   ├── seed_data.py                 # populate with retail data
│   └── sample_questions.md          # example questions to try
│
├── app.py                           # Streamlit dashboard (beautiful UI)
├── api.py                           # FastAPI backend
├── main.py                          # entry point
├── evaluate.py                      # run evaluation from CLI
├── Dockerfile                       # containerization
├── requirements.txt                 # dependencies
└── README.md                        # polished documentation
```

---

## Demo Dataset (Retail — Rewaa-Inspired)

### Data volume:
- 500 products across 8 categories
- 50,000 sales transactions over 12 months
- 1,000 customers
- 3 store locations (Riyadh, Jeddah, Dammam)
- Inventory movements (restocks, returns, damages)

### Categories:
Electronics, Clothing, Food & Beverage, Beauty, Home & Kitchen,
Sports, Books & Stationery, Toys

### Realistic patterns baked into seed data:
- Seasonal trends (Ramadan spike in food, Eid spike in clothing)
- Some products below reorder level (triggers restock alerts)
- Different margins by category (electronics high, food low)
- Different store performance (Riyadh highest, Dammam lowest)
- Some customers with high frequency, some dormant

---

## Evaluation Framework

### Golden Dataset Categories:
```
Category                    Count    Example Question
───────────────────────────────────────────────────────────
Simple lookup               8       "What's the stock of iPhone cases?"
Aggregation                 5       "Total sales last month"
Comparison                  5       "Compare Riyadh vs Jeddah revenue"
Time-range                  4       "Sales trend over last 6 months"
Multi-step reasoning        4       "Highest margin but lowest volume category"
Inventory-specific          4       "Which products need restocking?"
Follow-up questions         3       "Who are top customers?" then "What did they buy?"
Edge cases                  2       "Show me everything" (too broad — should ask to narrow)
───────────────────────────────────────────────────────────
TOTAL                       35
```

### Metrics:
- Classifier accuracy (%)
- SQL execution accuracy (%)
- SQL result accuracy (%)
- Multi-step plan quality (LLM judge, 1-5)
- Numerical accuracy (code-based, %)
- Hallucination rate (%)
- LLM judge average score (1-5)
- Avg latency by query type (seconds)

---

## Build Schedule (8 Days)

### Day 1: Database + Schema Discovery
- Set up free PostgreSQL on Supabase
- Create schema.sql with all 4 tables
- Write seed_data.py (500 products, 50K sales, 1K customers)
- Build schema_discovery.py — reads tables/columns/types automatically
- Test: print discovered schema in readable format

### Day 2: Semantic Mapper + Security
- Build semantic_mapper.py — LLM generates column descriptions
- Build security.py — SQL validator blocks destructive commands
- Build query_executor.py — safe execution with try/except
- Build connection.py — PostgreSQL connection handler
- Test: discover schema → generate metadata → execute sample queries

### Day 3: SDK (Decorator + Providers)
- Build config.py
- Build sdk/response.py (LLMResponse class)
- Build sdk/providers.py (Gemini function)
- Build sdk/llm_service.py (@llm_task with retry + fallback)
- Test: simple decorated function works end-to-end

### Day 4: Core Agents (Classifier + SQL + Validator)
- Build agents/classifier.py
- Build agents/sql_agent.py with auto-discovered schema in prompt
- Build agents/validator.py (separate LLM checks SQL logic)
- Test: 10 questions → correct SQL generated and executed

### Day 5: Advanced Agents (Planner + Analyst + Visualizer)
- Build agents/query_planner.py (multi-step decomposition)
- Build agents/analyst.py (with grounding check)
- Build agents/visualizer.py (auto-chart selection + Plotly)
- Test: complex multi-step question works end-to-end

### Day 6: LangGraph + Conversational Memory
- Build graph/state.py (State TypedDict)
- Build graph/nodes.py (all node functions)
- Build graph/routing.py (conditional edges + retry loops)
- Build graph/workflow.py (compile the full graph)
- Add conversation history to state for follow-up questions
- Test: full pipeline — simple, complex, and follow-up queries

### Day 7: Streamlit Dashboard + FastAPI
- Build app.py — beautiful Streamlit UI with:
  - Chat interface
  - Execution trace sidebar
  - Expandable SQL viewer
  - Interactive Plotly charts
  - Human-in-the-loop plan review
  - Conversation history
- Build api.py — FastAPI endpoints (/query, /health, /schema)
- Test: end-to-end through the UI

### Day 8: Evaluation + Docker + README + Deploy
- Create golden_dataset.json (35 test cases)
- Build grader.py and llm_judge.py
- Run evaluation, document results in README
- Write Dockerfile
- Deploy to Streamlit Cloud
- Write polished README with screenshots/GIFs
- Push to GitHub

---

## GitHub Star Strategy

### README must have:
- Eye-catching title with emoji
- One-line description
- Live demo link
- 3 GIF screenshots (schema discovery, multi-step query, dashboard)
- "Quick Start in 3 commands" section
- Architecture diagram
- Evaluation results table
- Feature comparison vs alternatives (Vanna, SQLChat, etc.)

### Share on:
- Reddit: r/MachineLearning, r/LangChain, r/Python
- Twitter/X: tag LangChain, LangGraph maintainers
- LinkedIn: post with demo GIF
- Hacker News: "Show HN: Turn any database into a conversational AI"
- Dev.to: write a tutorial article

### Topics/Tags on GitHub:
llm, langchain, langgraph, text-to-sql, ai-agent, multi-agent,
natural-language-sql, database-assistant, streamlit, fastapi

---

## Interview Pitch (2 Minutes)

"I built AgentStack — an open-source framework that turns any database into a conversational AI analyst. Point it at a PostgreSQL database, and it auto-discovers the schema, generates semantic descriptions of columns, and lets users query the data in plain English.

What makes it different from simple Text-to-SQL tools is the multi-step query planner. Complex business questions like 'Which category has the highest margin but lowest sales?' can't be answered in one SQL query. AgentStack breaks it into steps — calculate margins, calculate volumes, combine and rank — each step visible to the user for transparency.

The LLM infrastructure uses a decorator-based SDK pattern. All LLM calls go through a central decorator with retry, exponential backoff, and automatic provider fallback. Switching from Gemini to OpenAI is a one-line config change.

Quality assurance has three layers — SQL validation before execution, database error self-correction, and code-based grounding checks for numerical accuracy. I evaluate the system using a golden dataset of 35 test cases with both code-based grading and LLM-as-judge.

Security is built in — read-only connections, destructive SQL blocking, and API key authentication. The frontend is a Streamlit dashboard with interactive Plotly charts, execution traces, and human-in-the-loop plan review for complex queries.

It's deployed on Streamlit Cloud with a pre-loaded retail dataset so anyone can try it immediately. Three commands to set up locally."
