
from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline
from huggingface_hub import login
from typer import prompt

login('HF_API_KEY')
# Create HuggingFace pipeline
pipe = pipeline(
    "text-generation",
    #model = "Qwen/Qwen2-0.5B-Instruct",
    #model = "mistralai/Mistral-7B-Instruct-v0.2",
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    max_new_tokens=500,
    temperature=0.001,
    return_full_text=False
)

llm = HuggingFacePipeline(pipeline=pipe)

if __name__ == "__main__":
    prompt = """
        "What is Gen AI?"
        """
    response = llm.invoke(prompt)
    print(response)
