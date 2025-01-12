import openai
import os
import glob

# Load the OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("The OpenAI API key is not set. Please set it as an environment variable: OPENAI_API_KEY.")


def load_all_training_data(data_folder):
    """
    Load training data from multiple files in a given folder.

    Args:
        data_folder (str): Path to the folder containing training data files.

    Returns:
        str: Consolidated training data from all files.
    """
    training_data = []
    try:
        # Get all files matching the pattern in the specified folder
        file_paths = glob.glob(f"{data_folder}/training_data*.txt")
        for file_path in file_paths:
            with open(file_path, "r") as file:
                training_data.append(file.read())
    except Exception as e:
        print(f"An error occurred while loading training data: {e}")
        return f"Error loading training data: {e}"

    # Combine all the training data into a single string
    return "\n\n".join(training_data)


def generate_code_for_query(natural_language_query, training_data):
    """
    Generate Python code for a natural language query using GPT-4o with loaded training data.

    Args:
        natural_language_query (str): The natural language query to process.
        training_data (str): The training data loaded from multiple files.

    Returns:
        str: Generated Python code or error message.
    """
    # Create the prompt by appending the query to the training data
    prompt = f"{training_data}\nInput: \"{natural_language_query}\"\nOutput:"

    try:
        # Use OpenAI API to generate the code with the specified model
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # Replace with your desired model
            messages=[
                {"role": "system", "content": "You are an assistant that converts natural language queries into Python code for querying a NetworkX graph."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.0,  # Deterministic output
        )
        # Correct way to access the message content in the new SDK
        return response.choices[0].message.content.strip()

    except Exception as e:
        # Print and return the exception details
        print(f"An error occurred: {e}")
        return f"Error: {e}"


def main():
    """
    Main function to interactively generate Python code for user-provided natural language queries.
    """
    # Folder containing training data files
    training_data_folder = "datasets"
    
    # Load all training data
    training_data = load_all_training_data(training_data_folder)
    if "Error" in training_data:
        print(training_data)
        return

    print("Training Engine Initialized. Enter a natural language query to generate Python code.")
    print("Type 'exit' to quit.\n")
    
    while True:
        # Get input query from the user
        natural_language_query = input("Enter your query: ").strip()
        if natural_language_query.lower() == "exit":
            print("Exiting the training engine.")
            break
        
        # Generate the Python code for the input query
        generated_code = generate_code_for_query(natural_language_query, training_data)
        
        # Display the generated code
        print("\nGenerated Python Code:\n")
        print(generated_code)
        print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    main()
