import os
from typing import TypedDict
from dotenv import load_dotenv
from langgraph.graph import StateGraph,END,MessagesState
from langchain_groq import ChatGroq
load_dotenv()
llm=ChatGroq(model="llama-3.1-8b-instant",temperature=0.7)

class JokeState(TypedDict):
    topic:str
    joke:str
    feedback:str
    approved:bool

def comedian_node(state:JokeState):
    print("Comedian Thinking......")
    current_topic=state.get("topic","")
    current_feedback=state.get("feedback","")
    prompt=f'write a 1-sentence joke about {current_topic}.{current_feedback}'
    response=llm.invoke(prompt)
    ai_text=response.content
    return {"joke":ai_text}

def critics_node(state:JokeState):
    print("Critics reviewing......")
    current_joke=state.get("joke","")
    print(f"Joke : {current_joke}" )

    if "chicken"in current_joke.lower():
        return {"approved":True,
                "feedback":""}
    else:
        return {"approved":False,
                "feedback":"you must include the word chicken "}
    
def router(state: JokeState):
    if state["approved"]==True:
        return END
    else:
        return "comedian"

workflow = StateGraph(JokeState)
workflow.add_node("comedian",comedian_node)
workflow.add_node("critics",critics_node)
workflow.set_entry_point("comedian")
workflow.add_edge("comedian","critics")
workflow.add_conditional_edges("critics",router)
app = workflow.compile()


if __name__ == "__main__":
    initial_state = {
        "topic": "Space Travel",
        "joke": "",
        "feedback": "",
        "approved": False
    }
    
    print("\n--- STARTING SWARM ---")
    final_state = app.invoke(initial_state)
    print("\n--- FINAL JOKE ---")
    print(final_state["joke"])









