# Title: Implement State Persistence (MemorySaver) and Thread IDs

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from langgraph.graph import StateGraph, END, MessagesState
from langchain_core.messages import HumanMessage
# 1. NEW IMPORT: The Checkpointer
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

# Initialize LLM
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

# 2. Define the Node
def chat_node(state: MessagesState):
    print("--- AI THINKING ---")
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# 3. Build the Graph
workflow = StateGraph(MessagesState)
workflow.add_node("chat", chat_node)
workflow.set_entry_point("chat")
workflow.add_edge("chat", END)

# 4. Initialize the Memory Checkpointer
memory=MemorySaver()
# TODO: Initialize MemorySaver() and assign it to a variable named `memory`


# 5. Compile the Graph WITH Memory
# TODO: Compile the workflow, passing checkpointer=memory as an argument
# Syntax: app = workflow.compile(checkpointer=your_memory_variable)
app=workflow.compile(checkpointer=memory)

# 6. Run the Graph Multiple Times
if __name__ == "__main__":
    
    # 7. Define the Thread Configuration (This is how the AI knows it's YOU)
    # TODO: Create a dictionary named `config`. 
    # It must have this exact structure: {"configurable": {"thread_id": "1"}}
    config={
        "configurable":{"thread_id":"1"}
    }
    
    # --- CONVERSATION TURN 1 ---
    print("\n--- TURN 1 ---")
    user_input_1 = "Hi, my name is Ali and my favorite number is 7."
    
    # We pass the input AND the config to the graph
    # TODO: invoke the app passing {"messages": [HumanMessage(content=user_input_1)]} AND your config
    # Syntax: state_1 = app.invoke(your_input_dict, config=your_config_dict)
    state_1=app.invoke({"messages": [HumanMessage(content=user_input_1)]},config=config)

    
    # TODO: Print the AI's response (state_1["messages"][-1].content)
    print(state_1['messages'][-1].content)
    
    # --- CONVERSATION TURN 2 ---
    print("\n--- TURN 2 ---")
    user_input_2 = "What is my name, and what is my favorite number?"
    
    # Notice we don't pass the old history. We JUST pass the new message!
    # The checkpointer will automatically pull the old history from the filing cabinet.
    
    # TODO: invoke the app passing {"messages": [HumanMessage(content=user_input_2)]} AND your exact same config
    # TODO: Print the AI's response. It should remember your name!
    state_2=app.invoke({"messages":[HumanMessage(content=user_input_2)]},config=config)
    print(state_2['messages'][-1].content)
    