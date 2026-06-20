# langraph practice with single agent
import os
from typing import TypedDict
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq

# 1. Load the API Key safely
load_dotenv()

# 2. Initialize the Groq LLM (Llama 3 is extremely fast and free on Groq)
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.7)

# 3. Define State
class AgentState(TypedDict):
    topic: str
    draft: str
    editor_feedback: str
    approved: bool

# 4. Define Nodes
def researcher_node(state: AgentState):
    print("--- RESEARCHER AI THINKING ---")
    current_topic = state.get("topic", "")
    current_feedback = state.get("editor_feedback", "")
    
    # Construct the instruction for the AI
    prompt = f"Write a 1-sentence fun fact about {current_topic}. {current_feedback}"
    
    # TODO: Invoke the LLM 
    # Syntax: response = llm.invoke(prompt)
    response=llm.invoke(prompt)
    
    # TODO: Extract the string text from the LLM's response
    # Syntax: ai_text = response.content
    ai_text=response.content
    
    # TODO: Return a dictionary updating the "draft" with the AI's text
    return {"draft":ai_text}

def editor_node(state: AgentState):
    print("--- EDITOR WORKING ---")
    current_draft = state.get("draft", "")
    print(f"Current Draft: {current_draft}\n")
    
    if "APPLE" in current_draft.upper():
        return {"approved":True,"editor_feedback":"perfect"}
    else:
        return {"approved":False,"editor_feedback":"you MUST include exact word 'APPLE' in next draft"}
    # TODO: Write python logic to check if the word "APPLE" is in current_draft.upper()
    # TODO: If yes, return {"approved": True, "editor_feedback": "Perfect."}
    # TODO: If no, return {"approved": False, "editor_feedback": "You MUST include the exact word APPLE in your next draft!"}
    

# 5. Define Router
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