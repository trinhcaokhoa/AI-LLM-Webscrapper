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
    """
    Sends the DOM chunks and parse description to the Ollama model via Langchain OllamaLLM.
    """
    # Create the prompt using the template
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model  # Combine the prompt template with the model

    parsed_results = []

    # Reduce chunk size if necessary
    small_chunks = [chunk[:500] for chunk in dom_chunks]  # Limit each chunk to 500 characters

    # Iterate through each chunk and send it to the model
    for i, chunk in enumerate(small_chunks, start=1):
        print(f"Sending chunk {i}/{len(small_chunks)} to the model.")

        # Pass the chunk and description to the model with a timeout
        try:
            response = chain.invoke(
                {"dom_content": chunk, "parse_description": parse_description},

            )
            print(f"Parsed batch {i} successfully.")

            # Check if response is empty
            if response.strip():
                parsed_results.append(response)  # Collect the result from the model
            else:
                parsed_results.append(f"No relevant data found for batch {i}.")
        except Exception as e:
            print(f"Error parsing batch {i}: {str(e)}")
            parsed_results.append(f"Error in batch {i}: {str(e)}")

    # Join all results into a single string output
    return "\n".join(parsed_results)
