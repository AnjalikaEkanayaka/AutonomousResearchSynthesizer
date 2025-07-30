from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import Tool
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.tools import paper_search_tool, summarize_tool, gap_analysis_tool, methodology_tool, pdf_reader_tool

import os

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GEMINI_API_KEY"))

#Add memory to store past interactions
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

tools = [paper_search_tool,
        summarize_tool,
        gap_analysis_tool,
        methodology_tool,
        pdf_reader_tool
    ]

# Create prompt template 
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI research assistant. You use tools when needed."),
    ("user", "{input}")
])

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="chat-conversational-react-description", #AgentType.OPENAI_FUNCTIONS
    memory=memory,
    verbose=True
)
