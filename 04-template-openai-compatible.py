# https://python.langchain.com/docs/tutorials/llm_chain/
import getpass
import os
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import OpenAI

os.environ["LANGSMITH_TRACING"] = "true"
if os.environ.get("LANGSMITH_TRACING"):
  if not os.environ["LANGSMITH_API_KEY"]:
   os.environ["LANGSMITH_API_KEY"]= getpass.getpass("Enter LANGSMITH_API_KEY: ")

cserve_host = os.getenv("CSERVE_HOST", "http://cserve:8080")
print(f'cserve_host: {cserve_host}')
model = OpenAI(base_url=f'{cserve_host}/openai/v1/', model="google/gemma-2b-it")

from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template("How to say {input} in {output_language}:\n")

chain = prompt | model
r = chain.invoke(
    {
        "output_language": "German",
        "input": "I love programming.",
    }
)

print(prompt)
print(r)