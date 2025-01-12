import openai
import os

# Set the OpenAI API key from an environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("The OpenAI API key is not set. Please set it as an environment variable: OPENAI_API_KEY.")

# Fetch and print the list of available models
try:
    models = openai.models.list()  # Get the list of models
    print("Available models:")
    for model in models:
        print(f"- {model.id}")
except openai.APIError as e:
    print(f"OpenAI API returned an error: {e.message}")
except openai.APIConnectionError as e:
    print(f"Failed to connect to OpenAI API: {e}")
except openai.RateLimitError as e:
    print(f"Rate limit exceeded: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")


