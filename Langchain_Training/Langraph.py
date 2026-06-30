# ─────────────────────────────────────────────────────────────────────────────
# HANDS-ON: Build Your First LangGraph
# Demonstrates: State, Nodes, Edges, Conditional routing, Compile & Invoke
# ─────────────────────────────────────────────────────────────────────────────

# Step 1 — Install (run once)
# !pip install langgraph

# ─── Imports ─────────────────────────────────────────────────────────────────
from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, START, END

# ─── Step 2: Define State (shared memory across all nodes) ───────────────────
class AgentState(TypedDict):
    input:    str           # original user question
    response: str           # answer built up by nodes
    steps:    Annotated[list[str], operator.add]   # log of what happened

# ─── Step 3: Define Nodes (each is a Python function) ────────────────────────
def greet_node(state: AgentState) -> dict:
    """Node A — acknowledge the input."""
    msg = f"Received your question: '{state['input']}'"
    print(f"[greet_node] {msg}")
    return {"response": msg, "steps": ["greet_node ran"]}

def check_node(state: AgentState) -> dict:
    """Node B — decide how to answer."""
    if "weather" in state["input"].lower():
        answer = "The weather today is sunny ☀️"
    elif "time" in state["input"].lower():
        import datetime
        answer = f"Current time: {datetime.datetime.now().strftime('%H:%M:%S')}"
    else:
        answer = "Great question! I will need to look that up."
    print(f"[check_node] answer = {answer}")
    return {"response": answer, "steps": ["check_node ran"]}

def respond_node(state: AgentState) -> dict:
    """Node C — format the final response."""
    final = f"✅ FINAL ANSWER: {state['response']}"
    print(f"[respond_node] {final}")
    return {"response": final, "steps": ["respond_node ran"]}

# ─── Step 4: Define conditional routing ─────────────────────────────────────
def route_after_check(state: AgentState) -> str:
    """Edge function — returns the name of the next node to visit."""
    if "look that up" in state["response"]:
        return "respond_node"   # generic response, skip straight to end
    return "respond_node"       # same here — extend this for real branches

# ─── Step 5: Build the Graph ─────────────────────────────────────────────────
builder = StateGraph(AgentState)

# Add nodes
builder.add_node("greet_node",   greet_node)
builder.add_node("check_node",   check_node)
builder.add_node("respond_node", respond_node)

# Add edges
builder.add_edge(START,          "greet_node")    # entry point
builder.add_edge("greet_node",   "check_node")    # always go to check
builder.add_conditional_edges(                    # conditional branch
    "check_node",
    route_after_check,
    {"respond_node": "respond_node"}
)
builder.add_edge("respond_node", END)             # exit point

# Compile
graph = builder.compile()
print("✅ Graph compiled successfully!\n")

# ─── Step 6: Invoke the Graph ─────────────────────────────────────────────────
for question in ["What is the weather today?", "What time is it?", "Tell me about AI"]:
    print(f"\n{'─'*55}")
    print(f"Question: {question}")
    initial_state = {"input": question, "response": "", "steps": []}
    result = graph.invoke(initial_state)
    print(f"Steps taken: {result['steps']}")
    print(f"{result['response']}")