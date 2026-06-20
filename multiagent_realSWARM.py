# langraph practicing with 2 diffrent ai agents
import os
from typing import TypedDict
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq

load_dotenv()

# 1. TWO Different Brains!
junior_llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.7)

senior_llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.0)

class AgentState(TypedDict):
    topic: str
    draft: str
    editor_feedback: str
    approved: bool

def researcher_node(state: AgentState):
    print("--- JUNIOR AI (LLAMA-3) WRITING ---")
    current_topic = state.get("topic", "")
    current_feedback = state.get("editor_feedback", "")
    
    prompt = f"Write a 1-sentence historical fact about {current_topic}. {current_feedback}"
    
    # TODO: Invoke junior_llm here
    response = junior_llm.invoke(prompt)
    
    return {"draft": response.content}

def editor_node(state: AgentState):
    print("--- SENIOR AI (MIXTRAL) EVALUATING ---")
    current_draft = state.get("draft", "")
    print(f"Draft to evaluate: {current_draft}\n")
    
    prompt = f"You are a strict editor. Review this draft: '{current_draft}'. If it contains a specific four-digit year (like 1903), reply EXACTLY with the word 'APPROVED'. If it does not contain a year, reply with 'REJECTED: You must include the specific year.'"
    
    # TODO: Invoke senior_llm here
    response = senior_llm.invoke(prompt)
    evaluation = response.content
    print(f"Senior AI says: {evaluation}\n")
    if evaluation=="APPROVED":
        return { "approved" : True}
    else:
        return {"approved":False,"editor_feedback":evaluation}

    
    # TODO: If "APPROVED" in evaluation: return approved=True
    # TODO: Else: return approved=False, editor_feedback=evaluation
def router(state: AgentState):
        if state["approved"]==True:
            return END
        else:
            return "researcher"
    # TODO: check state["approved"]
    # If True, return END
    # Else, return "researcher"
    

# 6. Build Graph
workflow = StateGraph(AgentState)
workflow.add_node("researcher",researcher_node)
workflow.add_node("editor",editor_node)
workflow.set_entry_point("researcher")
workflow.add_edge("researcher","editor")
workflow.add_conditional_edges("editor",router)

# TODO: Add the two nodes: "researcher" and "editor"
# TODO: Set entry point to "researcher"
# TODO: Add standard edge from "researcher" to "editor"
# TODO: Add conditional edges from "editor" using the router function

app = workflow.compile()

# 7. Run it
if __name__ == "__main__":
    initial_state = {
        "topic": "Isaac Newton",
        "draft": "",
        "editor_feedback": "",
        "approved": False
    }
    
    print("\n--- STARTING SWARM ---")
    final_state = app.invoke(initial_state)
    print("\n--- FINAL STATE ---")
    print(final_state["draft"])
    

# ... (Router and Graph plumbing stays exactly the same as your last script) ...