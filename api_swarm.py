## LLMOPS STARTING HERE IN THIS FILE

import os
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from typing import TypedDict
from langgraph.graph import StateGraph, END

load_dotenv()

# ==========================================
# 1. FASTAPI & PYDANTIC SETUP (The Receptionist)
# ==========================================
api = FastAPI(title="AI Joke Swarm API")

class JokeRequest(BaseModel):
    topic:str
    # TODO: Define 'topic' as a string here
    

# ==========================================
# 2. LANGGRAPH SETUP (The Factory)
# ==========================================

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
app=workflow.compile()

# ==========================================
# 3. FASTAPI ENDPOINT
# =========================================
@api.post("/generate-joke")
async def generate_joke_endpoint(request: JokeRequest):
    print(f"--- API Received Request for Topic: {request.topic} ---")
    
    # 1. Setup the starting folder for LangGraph
    # Warning: Read from Pydantic using dot-notation (request.topic)
    initial_state = {
        "topic": request.topic,  
        "joke": "",
        "feedback": "",
        "approved": False
    }
    
    # 2. TODO: Invoke your LangGraph 'app' with the initial_state
    final_state=app.invoke(initial_state)
    
    # 3. TODO: Extract the final joke from the LangGraph output 
    # (Remember bracket notation for dictionaries!)
    extracted_joke=final_state["joke"]
    
    # 4. Return the JSON response to the user
    return {
        "requested_topic": request.topic,
        "final_joke": extracted_joke
    }

# ==========================================
# 4. SERVER START
# ==========================================
if __name__ == "__main__":
    # Starts the local web server
    uvicorn.run(api, host="127.0.0.1", port=8000)