# 🗣️ TalkDB

> Turn any database into a conversational AI analyst.  
> Ask questions in plain English. Get answers with charts.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Streamlit](https://img.shields.io/badge/Streamlit-Live_Demo-red.svg)](https://talkdb.streamlit.app)

---

## ✨ What is TalkDB?

TalkDB is an open-source framework that lets non-technical users query **any** database using natural language. It auto-discovers your schema, generates SQL, self-corrects errors, analyzes results, and produces interactive reports — all through a conversational interface.

**The problem it solves:** Every company has data locked in databases that only SQL-literate people can access. Business users wait hours for analysts to pull data. TalkDB eliminates that friction.

---

## 🎯 Key Features

🔍 **Auto Schema Discovery** — Point TalkDB at any PostgreSQL database. It reads tables, columns, types, and relationships automatically. No manual schema writing.

🧠 **Multi-Agent Architecture** — 6 specialized AI agents (Classifier, SQL Agent, Analyst, Inventory Agent, Visualizer, Report Generator) orchestrated via LangGraph with conditional routing.

🔄 **Self-Correcting SQL** — When generated SQL fails, the error feeds back into the agent for automatic retry. Three layers of quality checks: SQL validation, execution error handling, and numerical grounding.

📊 **Interactive Charts** — Auto-generated Plotly visualizations. The system chooses the right chart type based on your data.

🔌 **Provider-Agnostic SDK** — Central decorator pattern wraps all LLM calls. Switch between Groq (Llama 3.3), Google Gemini, or OpenAI with a one-line config change. Built-in retry with exponential backoff and automatic provider fallback.

🔒 **Security First** — Read-only database connections. SQL validator blocks destructive commands (DROP, DELETE, UPDATE). No SQL injection.

📏 **Built-in Evaluation** — Golden dataset with 20 test cases. Code-based grading + LLM-as-Judge scoring. Measure classifier accuracy, SQL accuracy, and answer quality.

🐳 **Docker Ready** — Containerized for easy deployment anywhere.

---

## 🚀 Quick Start

### 3 commands to run locally:

```bash
git clone https://github.com/shadabakhtar/talkdb.git
cd talkdb
pip install -r requirements.txt
```

### Set up your environment:

Create a `.env` file: