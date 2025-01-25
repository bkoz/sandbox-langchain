# https://python.langchain.com/docs/tutorials/llm_chain/
import getpass
import os
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

os.environ["LANGSMITH_TRACING"] = "true"
if os.environ.get("LANGSMITH_TRACING"):
  if not os.environ["LANGSMITH_API_KEY"]:
   os.environ["LANGSMITH_API_KEY"]= getpass.getpass("Enter LANGSMITH_API_KEY: ")

if not os.environ.get("OPENAI_API_KEY"):
  os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

model = ChatOpenAI(model="gpt-4o-mini")

messages = [
    SystemMessage("Translate the following from English into Italian"),
    HumanMessage("hi!"),
]

r = model.invoke(messages)
print(r.content)