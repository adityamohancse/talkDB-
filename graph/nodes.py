# graph/nodes.py

import logging
from agents.classifier import classify_question
from agents.sql_agent import generate_sql_query
from agents.analyst import analyze_data
from agents.inventory_agent import analyze_inventory
from agents.visualizer import generate_chart
from agents.report_agent import generate_report
from database.connection import run_query
from database.security import validate_sql

logger = logging.getLogger(__name__)


def classifier_node(state):
    """Classify the question type."""
    question = state["user_question"]
    query_type = classify_question(question).strip().lower()
    
    trace = state.get("execution_trace", [])
    trace.append(f"✅ Classified as: {query_type}")
    
    return {
        "query_type": query_type,
        "execution_trace": trace
    }


def sql_node(state):
    """Generate SQL, validate, and execute."""
    question = state["user_question"]
    error = state.get("error_message", "")
    retry_count = state.get("retry_count", 0)
    trace = state.get("execution_trace", [])

    # Generate SQL (with error context if retrying)
    try:
        sql = generate_sql_query(question, error_context=error)
    except Exception as e:
        trace.append(f"❌ SQL generation failed: {str(e)}")
        return {
            "error_message": str(e),
            "retry_count": retry_count + 1,
            "execution_trace": trace
        }

    # Validate SQL for security
    is_safe, reason = validate_sql(sql)
    if not is_safe:
        trace.append(f"🔒 SQL blocked: {reason}")
        return {
            "sql_query": sql,
            "error_message": f"Security: {reason}",
            "retry_count": retry_count + 1,
            "execution_trace": trace
        }

    trace.append(f"✅ SQL generated and validated")

    # Execute SQL
    result = run_query(sql)

    if result["success"]:
        trace.append(f"✅ SQL executed — {result['row_count']} rows returned")
        return {
            "sql_query": sql,
            "sql_results": str(result["data"][:50]),  # limit for prompt size
            "sql_results_raw": result["data"],
            "error_message": "",
            "retry_count": retry_count,
            "execution_trace": trace
        }
    else:
        trace.append(f"⚠️ SQL error — retrying... ({retry_count + 1}/3)")
        return {
            "sql_query": sql,
            "error_message": result["error"],
            "retry_count": retry_count + 1,
            "execution_trace": trace
        }


def analyst_node(state):
    """Analyze SQL results for sales/comparison queries."""
    trace = state.get("execution_trace", [])

    analysis_input = f"""Question: {state['user_question']}

SQL Query used: {state['sql_query']}

SQL Results:
{state['sql_results']}"""

    analysis = analyze_data(analysis_input)
    trace.append("✅ Analysis complete")

    return {
        "analysis": analysis,
        "execution_trace": trace
    }


def inventory_node(state):
    """Analyze inventory-specific data."""
    trace = state.get("execution_trace", [])

    inventory_input = f"""Question: {state['user_question']}

SQL Query used: {state['sql_query']}

Inventory Data:
{state['sql_results']}"""

    analysis = analyze_inventory(inventory_input)
    trace.append("✅ Inventory analysis complete")

    return {
        "analysis": analysis,
        "execution_trace": trace
    }


def visualizer_node(state):
    """Generate Plotly chart code."""
    trace = state.get("execution_trace", [])

    viz_input = f"""Analysis: {state['analysis']}

Raw Data:
{state['sql_results']}

Create an appropriate Plotly chart for this data."""

    chart_code = generate_chart(viz_input)
    trace.append("✅ Chart generated")

    return {
        "chart_code": chart_code,
        "execution_trace": trace
    }


def report_node(state):
    """Generate final executive report."""
    trace = state.get("execution_trace", [])

    report_input = f"""Question: {state['user_question']}

Analysis:
{state['analysis']}

Data:
{state['sql_results']}"""

    report = generate_report(report_input)
    trace.append("✅ Report generated")

    return {
        "final_answer": report,
        "execution_trace": trace
    }


def simple_answer_node(state):
    """For simple queries, format the SQL results directly."""
    trace = state.get("execution_trace", [])
    
    results = state.get("sql_results_raw", [])
    
    if len(results) == 0:
        answer = "No results found for your query."
    elif len(results) == 1:
        # Single value result like COUNT
        answer = str(results[0])
    else:
        # Format as readable text
        answer = f"Found {len(results)} results:\n"
        for row in results[:20]:
            answer += f"  {row}\n"
        if len(results) > 20:
            answer += f"  ... and {len(results) - 20} more rows"

    trace.append("✅ Answer ready")

    return {
        "final_answer": answer,
        "execution_trace": trace
    }


def error_node(state):
    """Handle unrecoverable errors gracefully."""
    trace = state.get("execution_trace", [])
    trace.append("❌ Failed after all retries")

    return {
        "final_answer": f"Sorry, I couldn't process your question. Error: {state.get('error_message', 'Unknown error')}. Please try rephrasing your question.",
        "execution_trace": trace
    }