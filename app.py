# app.py

import streamlit as st
import plotly.express as px
import pandas as pd
import time
from graph.workflow import build_workflow


# Page config
st.set_page_config(
    page_title="TalkDB",
    page_icon="🗣️",
    layout="wide"
)

# Custom CSS for clean design
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #888;
        margin-top: 0;
    }
    .metric-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    }
    .trace-step {
        padding: 4px 0;
        font-size: 0.9rem;
    }
    .stChatMessage {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)


# Initialize the agent (cached so it only builds once)
@st.cache_resource
def get_agent():
    return build_workflow()


agent = get_agent()


# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<p class="main-header">🗣️ TalkDB</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Turn any database into a conversational AI analyst</p>', unsafe_allow_html=True)
with col2:
    st.markdown("")
    st.markdown("")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.traces = []
        st.rerun()


# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "traces" not in st.session_state:
    st.session_state.traces = []


# Sidebar — execution trace and info
with st.sidebar:
    st.markdown("### 📍 Execution Trace")
    st.markdown("See what happens behind the scenes")
    st.divider()

    if st.session_state.traces:
        # Show latest trace
        latest = st.session_state.traces[-1]
        for step in latest.get("trace", []):
            st.markdown(f"<div class='trace-step'>{step}</div>", unsafe_allow_html=True)

        st.divider()

        # Show SQL
        if latest.get("sql"):
            st.markdown("### 💻 Generated SQL")
            st.code(latest["sql"], language="sql")

        # Show query type
        if latest.get("query_type"):
            st.markdown(f"**Query Type:** `{latest['query_type']}`")

        # Show latency
        if latest.get("latency"):
            st.markdown(f"**Total Time:** `{latest['latency']:.1f}s`")
    else:
        st.markdown("*Ask a question to see the trace*")

    st.divider()
    st.markdown("### 💡 Try These Questions")
    example_questions = [
        "How many products do we have?",
        "What are the top 5 best selling products?",
        "Which products need restocking?",
        "Compare sales across store locations",
        "What's the revenue trend by month?",
        "Show me profit margins by category",
        "Which payment method is most popular?",
        "Who are our top 10 customers?",
    ]
    for q in example_questions:
        if st.button(q, key=q, use_container_width=True):
            st.session_state.pending_question = q
            st.rerun()


# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # Show chart if available
        if message.get("chart_code"):
            try:
                exec_globals = {"px": px, "pd": pd}
                exec(message["chart_code"], exec_globals)
                if "fig" in exec_globals:
                    st.plotly_chart(exec_globals["fig"], use_container_width=True)
            except Exception:
                pass  # chart failed, skip silently


# Handle pending question from sidebar buttons
if "pending_question" in st.session_state:
    question = st.session_state.pending_question
    del st.session_state.pending_question
else:
    question = st.chat_input("Ask anything about your data...")


# Process question
if question:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # Run the agent
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            start_time = time.time()

            result = agent.invoke({
                "user_question": question,
                "query_type": "",
                "sql_query": "",
                "sql_results": "",
                "sql_results_raw": [],
                "analysis": "",
                "chart_code": "",
                "final_answer": "",
                "error_message": "",
                "retry_count": 0,
                "conversation_history": [],
                "execution_trace": [],
            })

            total_time = time.time() - start_time

        # Display the answer
        answer = result.get("final_answer", "Sorry, I couldn't process that.")
        st.markdown(answer)

        # Try to render chart
        chart_code = result.get("chart_code", "")
        if chart_code:
            try:
                exec_globals = {"px": px, "pd": pd}
                exec(chart_code, exec_globals)
                if "fig" in exec_globals:
                    st.plotly_chart(exec_globals["fig"], use_container_width=True)
            except Exception as e:
                st.caption(f"Chart could not be rendered: {str(e)[:100]}")

        # Save to session state
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "chart_code": chart_code
        })

        # Save trace
        st.session_state.traces.append({
            "trace": result.get("execution_trace", []),
            "sql": result.get("sql_query", ""),
            "query_type": result.get("query_type", ""),
            "latency": total_time
        })

        # Rerun to update sidebar trace
        st.rerun()