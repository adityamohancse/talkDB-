# TalkDB — Multi-Agent Conversational AI Data Analyst

> Ask questions about business data in natural language and turn database results into readable analysis, inventory insights, and recommendations.

**Live Demo:** https://talkdb.onrender.com  
**Source Code:** https://github.com/adityamohancse/talkDB-

TalkDB is a Streamlit-based conversational analytics application that connects natural-language questions to a PostgreSQL database. It uses a LangGraph-orchestrated workflow to classify questions, generate and validate SQL, execute read queries, and present results with analysis and recommendations.

> **Note:** TalkDB is a portfolio project using a sample retail database. Validate analytical recommendations against the underlying data before using them for real business decisions.

## Table of Contents

- [Overview](#overview)
- [Highlights](#highlights)
- [Example Questions](#example-questions)
- [How It Works](#how-it-works)
- [Technology Stack](#technology-stack)
- [Database Schema](#database-schema)
- [Repository Structure](#repository-structure)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [Initialize the Database](#initialize-the-database)
- [Run Locally](#run-locally)
- [Run with Docker](#run-with-docker)
- [Deploy on Render](#deploy-on-render)
- [Testing](#testing)
- [Security Considerations](#security-considerations)
- [Troubleshooting](#troubleshooting)
- [Known Limitations](#known-limitations)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

## Overview

Business teams often need SQL expertise to answer everyday questions about products, sales, inventory, and customers. TalkDB aims to make that workflow more accessible by letting a user ask a question in plain English instead of manually writing SQL.

The application provides an interactive Streamlit chat interface and an execution-trace sidebar. The trace helps users understand workflow stages, while the generated SQL panel makes the query being executed more transparent.

### The problem it addresses

- Business questions often require manual SQL writing and repeated analysis.
- Query results are not always easy for non-technical users to interpret.
- Inventory and sales data can be difficult to turn into actionable summaries.
- AI-generated database answers need visibility into the SQL and execution process.

## Highlights

- **Conversational data exploration:** Ask questions in natural language.
- **Multi-agent workflow:** LangGraph-based orchestration coordinates task processing.
- **SQL generation and validation:** Generated SQL is validated before execution.
- **PostgreSQL integration:** Query a relational database containing retail-style data.
- **Sales analysis:** Summarize sales by product or store where supported.
- **Inventory insights:** Identify products whose stock is below configured reorder levels.
- **Report generation:** Present findings, details, and recommendations for supported analysis flows.
- **Execution trace:** Show workflow stages, generated SQL, query status, and timing.
- **LLM integrations:** The repository includes Groq and Google Gemini provider code; active provider/model depends on configuration.
- **Containerization:** A Dockerfile is included for deployment.

Verify each capability against the current code before describing it as production-ready. The exact active agents, supported query categories, and provider/model combinations should be checked in the source.

## Example Questions

The interface includes examples such as:

- How many products do we have?
- What are the top 5 best-selling products?
- Which products need restocking?
- Compare sales across store locations.
- What's the revenue trend by month?
- Show me profit margins by category.
- Which payment method is most popular?
- Who are our top 10 customers?

Results depend on the database contents, schema, model response, and current implementation. Treat generated recommendations as decision support rather than a substitute for validating the underlying data.

## How It Works

```mermaid
flowchart TD
    A[User asks a business question] --> B[Streamlit chat interface]
    B --> C[LangGraph workflow]
    C --> D[Classify question and select workflow]
    D --> E[Generate SQL using schema context]
    E --> F[Validate SQL and apply safety checks]
    F --> G[Execute read query]
    G --> H[Analyze query results]
    H --> I[Generate findings and recommendations]
    I --> J[Render response, SQL, trace and charts]
    G <--> K[(PostgreSQL)]
    E <--> L[Configured LLM provider]
    H <--> L
```

This is a high-level view; check `graph/`, `agents/`, `sdk/`, and `app.py` to ensure every stage and connection matches the current implementation.

1. **Question intake:** The user submits a natural-language question.
2. **Classification and routing:** The workflow determines the question type and selects a processing path.
3. **SQL generation:** The SQL-generation component uses available schema context.
4. **Validation:** The application checks the generated query against its safety rules.
5. **Execution:** The query is sent to PostgreSQL.
6. **Analysis:** Returned rows are analyzed where the workflow supports it.
7. **Report generation:** Findings and recommendations are generated from available result data.
8. **Presentation:** The interface displays the answer, execution trace, generated SQL, and visualizations where supported.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application and workflow implementation |
| Streamlit | Interactive web interface |
| LangGraph | Workflow orchestration |
| PostgreSQL | Relational data storage |
| psycopg2 | PostgreSQL connectivity |
| Groq | LLM provider integration |
| Google Gemini | LLM provider integration |
| Plotly | Charts and visualizations |
| Docker | Containerized execution and deployment |
| pytest | Automated testing, where configured |

Confirm versions and active usage against the repository before treating this as a complete dependency inventory.

## Database Schema

The sample schema defines these tables.

### `products`

| Column | Description |
|---|---|
| `product_id` | Primary key |
| `name` | Product name |
| `category` | Product category |
| `sku` | Unique stock-keeping unit |
| `cost_price` | Cost per unit |
| `selling_price` | Selling price per unit |
| `stock_quantity` | Current stock quantity |
| `reorder_level` | Inventory threshold for restocking |
| `supplier` | Supplier name |

### `sales`

| Column | Description |
|---|---|
| `sale_id` | Primary key |
| `product_id` | References `products.product_id` |
| `quantity_sold` | Units sold |
| `total_amount` | Amount for the sales record |
| `sale_date` | Date of sale |
| `store_location` | Store or sales location |
| `payment_method` | Payment method |

### `inventory_log`

| Column | Description |
|---|---|
| `log_id` | Primary key |
| `product_id` | References `products.product_id` |
| `movement_type` | Type of inventory movement |
| `quantity` | Quantity moved |
| `reason` | Reason for movement |
| `log_date` | Date of movement |

### `customers`

| Column | Description |
|---|---|
| `customer_id` | Primary key |
| `name` | Customer name |
| `phone` | Optional phone number |
| `total_purchases` | Recorded purchase total |
| `visit_count` | Recorded visit count |
| `last_visit` | Most recent recorded visit |

### Relationships

```mermaid
erDiagram
    PRODUCTS ||--o{ SALES : has
    PRODUCTS ||--o{ INVENTORY_LOG : records
    PRODUCTS {
        int product_id PK
        string name
        string category
        string sku UK
        decimal cost_price
        decimal selling_price
        int stock_quantity
        int reorder_level
        string supplier
    }
    SALES {
        int sale_id PK
        int product_id FK
        int quantity_sold
        decimal total_amount
        date sale_date
        string store_location
        string payment_method
    }
    INVENTORY_LOG {
        int log_id PK
        int product_id FK
        string movement_type
        int quantity
        string reason
        date log_date
    }
    CUSTOMERS {
        int customer_id PK
        string name
        string phone
        decimal total_purchases
        int visit_count
        date last_visit
    }
```

The supplied schema defines foreign-key relationships from `sales` and `inventory_log` to `products`. The `customers` table has no declared foreign-key relationship in that schema.

## Repository Structure

Simplified overview; confirm exact files in the current repository.

```text
TalkDB/
├── agents/              # Agent implementations
├── api/                 # API-related code, if used
├── database/
│   ├── connection.py    # PostgreSQL connection and query execution
│   ├── schema.sql       # Database schema
│   ├── schema_discovery.py
│   ├── security.py      # SQL/database safety helpers
│   └── seed_data.py     # Sample-data seeding
├── evaluation/          # Evaluation assets and utilities
├── graph/               # Workflow state, routing and orchestration
├── sdk/                 # LLM/provider abstractions and response types
├── app.py               # Streamlit application entry point
├── config.py            # Application configuration
├── Dockerfile
├── requirements.txt
├── test_agents.py
├── test_sdk.py
├── test_workflow.py
└── README.md
```

## Getting Started

### Prerequisites

- Git
- Python version compatible with the dependencies and Dockerfile
- Access to a PostgreSQL database
- API key for the configured LLM provider
- Docker, if using the containerized version

The included Dockerfile uses Python 3.11. For local development, use a Python version supported by the project's dependencies.

### 1. Clone the repository

```bash
git clone https://github.com/adityamohancse/talkDB-.git
cd talkDB-
```

### 2. Create a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If dependency resolution fails, inspect the reported conflict and align package versions rather than randomly upgrading individual packages.

## Environment Variables

Create a local `.env` file in the project root. Never commit it.

```dotenv
DATABASE_URL=postgresql://USER:PASSWORD@HOST:5432/DATABASE
GROQ_API_KEY=your_groq_api_key
GOOGLE_API_KEY=your_google_api_key
```

Use only the provider credentials required by your selected configuration. Confirm exact variable names in `config.py` and the provider implementation before running the application.

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |
| `GROQ_API_KEY` | Groq API key, if Groq is selected |
| `GOOGLE_API_KEY` | Google Gemini API key, if Gemini is selected |

Do not put real credentials in source code, README examples, GitHub issues, or public logs. Configure production secrets through the deployment platform's environment-variable settings.

## Initialize the Database

The project includes `database/schema.sql` and `database/seed_data.py`.

1. Create a PostgreSQL database.
2. Set `DATABASE_URL` to that database's connection string.
3. Apply `database/schema.sql` using the initialization method supported by the repository.
4. Inspect `database/seed_data.py` to identify its actual entry point and whether it can safely run more than once.
5. Run the verified seed command only after confirming it targets the intended database.

Do not assume a seeding function name. The command must match the actual code. Seeding a cloud database inserts records directly into that database; it does not require a GitHub push.

Confirm the target database before seeding. Do not run schema resets or destructive commands against a database containing data you need.

## Run Locally

From the project root:

```bash
streamlit run app.py
```

If the current repository defines a different startup command, use the verified project configuration. Streamlit typically prints a local URL in the terminal.

## Run with Docker

Build the image:

```bash
docker build -t talkdb .
```

Run it with environment variables:

```bash
docker run --rm -p 8501:8501 --env-file .env talkdb
```

Open `http://localhost:8501`.

The current Dockerfile exposes Streamlit on port `8501`. For Render, ensure the application listens on the port assigned by the platform. If the container command hardcodes a port, update it to use the platform's `PORT` variable with a local default and verify the configuration before deploying.

## Deploy on Render

Live demo: **https://talkdb.onrender.com**

1. Push reviewed code to the connected GitHub branch.
2. Open the TalkDB Web Service in Render.
3. Confirm it is configured to use the repository's Dockerfile.
4. Configure `DATABASE_URL` with the correct Render PostgreSQL connection string. Prefer the internal database URL when the service and database are in the same Render region and supported by the platform.
5. Add required LLM API keys in Render environment settings.
6. Ensure the service binds to `0.0.0.0` and listens on the port expected by Render.
7. Deploy and inspect build and runtime logs.
8. Test product count, sales analysis, and inventory questions in the live UI.

Never publish database passwords or API keys. Keep production credentials in Render environment settings, not in Git.

A successful deployment confirms that the service starts; it does not automatically prove every query, report, or visualization is correct.

## Testing

Run the existing test suite:

```bash
python -m pytest -v
```

Run individual files if they exist:

```bash
python -m pytest -v test_agents.py
python -m pytest -v test_sdk.py
python -m pytest -v test_workflow.py
```

Tests may require environment variables, database access, or provider configuration. Review test setup before interpreting failures.

Recommended additional coverage:

- SQL validation rejects write and DDL statements.
- Database connections and cursors close on success and error.
- Empty results and null values render correctly.
- Numeric and currency formatting is consistent.
- Report claims can be traced to query results.
- Provider failures produce useful errors without exposing secrets.
- Schema discovery handles the actual database schema.

## Security Considerations

TalkDB executes AI-generated SQL against a database, so database safety is essential.

- Use a dedicated database role with minimum required permissions.
- Prefer a read-only role for analytical queries.
- Validate generated SQL before execution.
- Block write operations and DDL unless explicitly required and separately secured.
- Use query timeouts and row limits where appropriate.
- Never expose database credentials or provider keys in the UI or logs.
- Keep `.env` out of version control.
- Avoid unrestricted public access to sensitive production data.
- Validate generated findings before relying on them for business decisions.

Application-level SQL validation does not replace database-level permissions. Enforce read-only access at the PostgreSQL role level as well.

## Troubleshooting

### `relation "products" does not exist`

- Confirm the app is connected to the intended PostgreSQL database.
- Check whether `database/schema.sql` was applied to that database.
- Verify schema and table names using a PostgreSQL client.
- Confirm the web service's `DATABASE_URL` matches the database where schema and sample data were created.

### Database connection fails

- Check `DATABASE_URL` in the environment where the app runs.
- Verify hostname, database name, username, password, and port.
- Check network access rules and hosting platform connection instructions.
- Avoid printing the full connection string because it may contain a password.

### LLM provider errors

- Confirm the selected provider's API key is configured.
- Check that the model identifier is supported.
- Inspect errors without exposing credentials.
- Check provider status, rate limits, and account access.

### Dependency installation fails

- Find the first actual dependency conflict in the build logs.
- Check package compatibility and Python-version constraints.
- Remove unrelated development packages from production dependencies where appropriate.
- Rebuild from a clean environment after resolving the conflict.

### Render deployment fails or the service does not start

- Inspect the first error in deployment logs.
- Confirm the Dockerfile copies required files and installs dependencies.
- Confirm the app binds to `0.0.0.0` and uses Render's expected port.
- Verify required environment variables.
- Test the Docker image locally where possible.

### The app starts but reports confusing results

- Inspect generated SQL in the execution trace.
- Verify the query directly against the database.
- Check that report numbers come from returned data.
- Review schema context, SQL validation, retry logic, and result formatting.

## Known Limitations

- Results depend on the quality and completeness of the underlying database.
- LLM-generated SQL and narrative analysis can be incorrect and must be validated.
- Provider availability, rate limits, and model behavior can affect responses.
- The public demo uses sample data and should not be treated as a production service for sensitive data.
- Free hosting plans may spin down after inactivity, increasing first-request latency.
- Supported question types and chart behavior depend on the current implementation.

Update this section as limitations are fixed or discovered.

## Roadmap

Potential future improvements, subject to implementation and testing:

- More readable and consistent answer formatting.
- Stronger grounding checks between report claims and SQL results.
- More comprehensive tests for SQL safety and report correctness.
- Improved chart labels, formatting, and empty states.
- Query latency and token-usage observability.
- Better schema selection for databases with many tables.
- Role-based access and user authentication for multi-user deployments.
- CI checks for dependency installation, tests, and container builds.

These are planned improvements, not claims about existing functionality.

## Contributing

1. Fork the repository.
2. Create a focused feature branch.
3. Make a small, clearly scoped change.
4. Add or update tests when appropriate.
5. Run the test suite.
6. Review the diff for secrets and unrelated files.
7. Open a pull request with a clear summary and testing notes.

Do not include credentials, private datasets, or production connection strings in issues or pull requests.

## License

See the repository's [`LICENSE`](LICENSE) file for the applicable license terms. Review that file before redistributing or using the project.

## Author

**Aditya Mohan Jha**  
Software Engineer | Full-Stack Development | AI-Integrated Applications

- GitHub: https://github.com/adityamohancse
- LinkedIn: https://linkedin.com/in/adityamohancse

---

*Built as a portfolio project exploring conversational analytics, agent orchestration, SQL safety, and AI-assisted business reporting.*
