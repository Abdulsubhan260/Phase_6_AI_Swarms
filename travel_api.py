import os
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from typing import TypedDict
from langgraph.graph import StateGraph, END
load_dotenv()
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.7)
api=FastAPI(title="Travel AI")
class TrippRequest(BaseModel):
    city:str
    days:int


class TripState(TypedDict):
    city:str
    days:int
    itinerary:str
    budget:str

def planner_node(State:TripState):
    print("Creating Plan....")
    current_city=State.get("city","")
    current_days=State.get("days","")
    prompt=f"write a full itinearary of trip of{current_city}.{current_days}"
    
    response=llm.invoke(prompt)
    ai_text=response.content
    return{"itinerary":ai_text}

def budget_node(State:TripState):
    print("Processing Budget")
    current_itinerary=State.get("itinerary")
    prompt=f"write 1-line estimate budget of {current_itinerary}"
    response=llm.invoke(prompt)
    ai_text=response.content
    return{"budget":ai_text}

workflow=StateGraph(TripState)
workflow.add_node("plan",planner_node)
workflow.add_node("budget",budget_node)
workflow.set_entry_point("plan")
workflow.add_edge("plan","budget")
workflow.add_edge("budget",END)
app=workflow.compile()

@api.post("/plan-trip")
async def genrate_plane_and_budget(request:TrippRequest):
    initial_state={
        "city":request.city,
        "days":request.days

    }

    final_state=app.invoke(initial_state)
    extracted_plan=final_state["itinerary"]
    extracted_budget=final_state["budget"]
    return{
        "city":request.city,
        "days":request.days,
        "itenerary":extracted_plan,
        "budget":extracted_budget
    }
if __name__ == "__main__":
    uvicorn.run(api, host="0.0.0.0", port=7860) 
