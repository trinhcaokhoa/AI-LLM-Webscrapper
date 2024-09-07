from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import os

# Define the template for the prompt
template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

# Use the Ollama API URL running in Docker
ollama_api_url = os.getenv("OLLAMA_API_URL", "http://ollama:11434")

# Initialize the model using the base_url for Ollama running in Docker
model = OllamaLLM(model="llama3.1", base_url=ollama_api_url)


def parse_with_ollama(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        print(f"Parsing batch: {i} of {len(dom_chunks)}")
        response = chain.invoke(
            {"dom_content": chunk, "parse_description": parse_description}
        )
        print(f"Parsed batch: {i} of {len(dom_chunks)}")
        parsed_results.append(response)

    return "\n".join(parsed_results)
