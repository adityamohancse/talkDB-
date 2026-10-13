# graph/workflow.py

from langgraph.graph import StateGraph
from graph.state import State
from graph.nodes import (
    classifier_node,
    sql_node,
    analyst_node,
    inventory_node,
    visualizer_node,
    report_node,
    simple_answer_node,
    error_node,
)
from graph.routing import (
    route_after_classifier,
    route_after_sql,
    route_after_analysis,
    route_after_inventory,
    route_after_visualizer,
)


def build_workflow():
    """Build and compile the LangGraph workflow."""

    graph = StateGraph(State)

    # Add all nodes
    graph.add_node("classifier_node", classifier_node)
    graph.add_node("sql_node", sql_node)
    graph.add_node("analyst_node", analyst_node)
    graph.add_node("inventory_node", inventory_node)
    graph.add_node("visualizer_node", visualizer_node)
    graph.add_node("report_node", report_node)
    graph.add_node("simple_answer_node", simple_answer_node)
    graph.add_node("error_node", error_node)

    # Entry point
    graph.set_entry_point("classifier_node")

    # Edges
    graph.add_conditional_edges("classifier_node", route_after_classifier)
    graph.add_conditional_edges("sql_node", route_after_sql)
    graph.add_conditional_edges("analyst_node", route_after_analysis)
    graph.add_conditional_edges("inventory_node", route_after_inventory)
    graph.add_conditional_edges("visualizer_node", route_after_visualizer)

    # Finish points — these nodes end the pipeline
    graph.set_finish_point("simple_answer_node")
    graph.set_finish_point("report_node")
    graph.set_finish_point("error_node")

    # Compile
    return graph.compile()