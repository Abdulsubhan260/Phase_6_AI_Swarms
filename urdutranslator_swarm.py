# psudo code starting

# importing dotenv,ddgo,type dict,dependencies

# class recipe(state)
# node Chef
# returns recipe
# node translatoir
# translate into urdu by usini ai model llm
# then setting graph plumbing 
# workflow edges ebtery pints cinditional edges and then if approved show output to user

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from typing import TypedDict
from langgraph.graph import StateGraph,END

load_dotenv()
llm1=ChatGroq(model="llama-3.1-8b-instant", temperature=0.7)
llm2=ChatGroq(model="llama-3.1-8b-instant",temperature=0.5)
class RecipieState(TypedDict):
    food_item:str
    english_recipe:str
    urdu_recipe:str

def chef_node(state:RecipieState):
    print("Chef Thinking about recipe")
    food_recipie=state.get("food_item"," ")
    prompt=f"Please write recipie for making {food_recipie} in simple english and in 3 steps only "
    response=llm1.invoke(prompt)
    return {
        "english_recipe":response.content
    }
def translator_node(state:RecipieState):
    print("Translating recipie into Urdu")
    translator_recipe=state.get("english_recipe"," ")
    prompt=f"please transalte {translator_recipe} into roman urdu "
    response=llm2.invoke(prompt)
    return {
        "urdu_recipe":response.content
    }

workflow=StateGraph(RecipieState)
workflow.add_node("chef",chef_node)
workflow.add_node('translator',translator_node)
workflow.set_entry_point("chef")
workflow.add_edge("chef","translator")
app=workflow.compile()

if __name__ == "__main__":
    initial_state = {
        "food_item": "Karachi-Biryani",
        "english_recipe": "",
        "urdu_recipe": ""
        
    }
print("\n--- STARTING SWARM ---")
final_state = app.invoke(initial_state)
print("\n--- FINAL STATE ---")
print(final_state["urdu_recipe"])





