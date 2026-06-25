from dotenv import load_dotenv

from langchain_huggingface import (
    HuggingFaceEndpoint,
    ChatHuggingFace
)

load_dotenv()

llm_endpoint = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-72B-Instruct",
    task="text-generation",
    max_new_tokens=2048,
    temperature=0.2
)

llm = ChatHuggingFace(
    llm=llm_endpoint
)