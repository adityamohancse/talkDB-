# graph/routing.py


def route_after_classifier(state):
    """All query types go to SQL first."""
    return "sql_node"


def route_after_sql(state):
    """After SQL: retry, continue to analysis, or return simple answer."""
    error = state.get("error_message", "")
    retry_count = state.get("retry_count", 0)
    query_type = state.get("query_type", "simple_query")

    # If there's an error and we haven't retried too many times
    if error and retry_count < 3:
        return "sql_node"  # RETRY — loop back

    # If error and max retries reached
    if error:
        return "error_node"  # GIVE UP gracefully

    # Success — route based on query type
    if query_type == "simple_query":
        return "simple_answer_node"
    elif query_type == "inventory_question":
        return "inventory_node"
    else:
        # sales_analysis, full_report, follow_up all go to analyst
        return "analyst_node"


def route_after_analysis(state):
    """After analysis, generate chart and report for complex queries."""
    query_type = state.get("query_type", "")

    if query_type == "full_report":
        return "visualizer_node"  # full report gets charts
    else:
        return "report_node"  # others skip to report


def route_after_inventory(state):
    """After inventory analysis, go to report."""
    return "report_node"


def route_after_visualizer(state):
    """After chart generation, go to report."""
    return "report_node"