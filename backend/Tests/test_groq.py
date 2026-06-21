from langchain_groq import ChatGroq
from dotenv import load_dotenv
import time

load_dotenv()

llm=ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)

start=time.time()
response=llm.invoke(
    "What did kratos do to baldur in god of war?"
)

print(response.content)
print(f"Time taken:{time.time()-start:.2f}seconds")