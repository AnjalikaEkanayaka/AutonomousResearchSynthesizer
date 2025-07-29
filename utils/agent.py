from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent
from langchain.agents.agent_types import AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.tools import paper_search_tool, summarize_tool, gap_analysis_tool, methodology_tool
import os
from dotenv import load_dotenv

load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GEMINI_API_KEY"))

#Add memory to store past interactions
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

tools = [paper_search_tool, summarize_tool, gap_analysis_tool, methodology_tool]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="chat-conversational-react-description",
    memory=memory,
    verbose=True
)
