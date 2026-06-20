import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# 1. NEW IMPORTS FOR TOOLS
from langgraph.graph import StateGraph, END, MessagesState
from langgraph.prebuilt import ToolNode
from langchain_community.tools import DuckDuckGoSearchResults

load_dotenv()

# 2. Define the Tool and the LLM
web_search_tool = DuckDuckGoSearchResults()
tools_list = [web_search_tool]

# Initialize LLM and "bind" the tools to it (so Llama-3 knows it has a browser)
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
llm_with_tools = llm.bind_tools(tools_list)

# 3. Define the Agent Node
# Notice we pass MessagesState. It automatically tracks the conversation history!
def agent_node(state: MessagesState):
    print("--- AGENT THINKING ---")
    
    # The state["messages"] is a list of all chat history. We pass it directly to the LLM.
    response = llm_with_tools.invoke(state["messages"])
    
    # Return the new message to be appended to the state
    return {"messages": [response]}

# 4. Define the Router
def router(state: MessagesState):
    print("--- ROUTER CHECKING ---")
    # Get the very last message in the state (which is the one the AI just generated)
    last_message = state["messages"][-1]
    
    # If the AI decided it needs to use the web search tool, it will have this attribute
    if last_message.tool_calls:
        print("-> Routing to Web Search Tool")
        return "tools"
    
    print("-> Routing to END")
    return END

# 5. Build the Graph
workflow = StateGraph(MessagesState)

# Add the agent node
workflow.add_node("agent", agent_node)

# Add the pre-built ToolNode (It handles the execution of the Python tool automatically!)
tool_node = ToolNode(tools_list)
workflow.add_node("tools", tool_node)

# Set Entry and Edges
workflow.set_entry_point("agent")

# The router decides if we go to 'tools' or END
workflow.add_conditional_edges("agent", router)

# Once the tool finishes searching, ALWAYS go back to the agent to read the results
workflow.add_edge("tools", "agent")

app = workflow.compile()

# 6. Test it with something the AI could not possibly know without the internet
if __name__ == "__main__":
    from langchain_core.messages import HumanMessage
    
    print("\n--- STARTING WEB AGENT ---")
    # Ask about a recent event (e.g., current year is 2026)
    user_input = "Who is imran khan?"
    
    # We initialize the state with a single HumanMessage
    initial_state = {"messages": [HumanMessage(content=user_input)]}
    
    final_state = app.invoke(initial_state)
    
    print("\n--- FINAL ANSWER ---")
    print(final_state["messages"][-1].content)


