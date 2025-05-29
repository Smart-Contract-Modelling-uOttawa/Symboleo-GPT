from openai import OpenAI;
import os;
import sys;
import random;
# from dotenv import load_dotenv

# Load environment variables from .env file
# load_dotenv()

#  TODO: Enter you API KEY for Open AI . In my case I added Prof API key
# Access the API key
API_KEY = "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"
# API_KEY = os.getenv("API_KEY")
# Define all your prompt-generation functions (they look good)

def generate_main_prompt(errors, contract_content, symboleo_syntax):
    """Generates a ChatGPT prompt to fix errors in the Symboleo contract."""
    print("Creating Prompt ....")
    prompt = f"""
    Based on the Symboleo syntax, correct the contract below.
    Symboleo Syntax:
    {symboleo_syntax}
    You are an expert in the Symboleo contract language. Your task is to analyze the given Symboleo contract and fix only the errors present. Below is the extracted contract along with the identified errors.

    Do not make unnecessary changes to the contract. If a part of the contract does not contain errors, leave it unchanged. Only modify the sections where errors are explicitly mentioned.

    Ensure that you do not alter any variables, functions, or other elements unless an error related to them is specified. The errors include line numbers—only make changes to the specified lines if required, and avoid modifying any other lines.

    Errors:
    {errors}

    Incorrect Symboleo Contract:
    {contract_content}

    Please review the contract and:
    1. Identify issues based on the errors mentioned.
    2. Correct any mistakes while preserving the structure.
    3. Ensure the contract follows proper Symboleo syntax and semantics.

    Return only the corrected contract. Do not include explanations.
    """
    print("Prompt creation done")
    return prompt

def generate_prompt_signature(errors, contract_content, symboleo_syntax):
    return f"""
    [Signature Prompt]
    You are an expert in Symboleo contract language. Your task is to fix the errors in the contract below, based on the provided Symboleo syntax.

    Symboleo Syntax:
    {symboleo_syntax}

    Errors:
    {errors}

    Contract:
    {contract_content}

    Ensure the contract follows the correct Symboleo syntax. Only fix the errors mentioned and leave other parts unchanged. Return the corrected contract without any explanations.
    """

def generate_prompt_chain_of_thought(errors, contract_content, symboleo_syntax):
    return f"""
    [Chain of Thought Prompt]
    Think step by step before correcting the errors in the contract. Your task is to analyze the contract and fix only the errors mentioned. You should break down the process logically before providing the corrections.

    Errors:
    {errors}

    Contract:
    {contract_content}

    Steps:
    1. Read and analyze the errors.
    2. Break down the contract line by line, considering each error.
    3. Apply the corrections logically based on the provided errors, ensuring no changes are made beyond the identified issues.
    4. Return only the corrected contract without unnecessary explanations.
    """

# def generate_prompt_few_shot(errors, contract_content, symboleo_syntax):
#     return f"[Few-shot Prompt]\nExample:\nError: Line 4 - missing colon\nFix: trigger Payment:\n---\nErrors:\n{errors}\nContract:\n{contract_content}"

# Update generate_prompt() function
def generate_prompt(errors, contract_content, symboleo_syntax, iteration, log_file_path=None):
    print(f"\n🧠 Creating Prompt for Iteration {iteration}...")

    prompt_styles = [
        generate_main_prompt,
        generate_prompt_signature,
        generate_prompt_chain_of_thought,
        # generate_prompt_few_shot,
    ]

    prompt_names = [
        "Signature + Chain of thought",
        "Signature",
        "Chain of Thought",
        # "Few-shot",
    ]

    log_message = ""

    if iteration < len(prompt_styles):
        prompt_func = prompt_styles[iteration - 1]
        prompt_name = prompt_names[iteration - 1]
        log_message = f"✅ Iteration {iteration} → Using Prompt Style: {prompt_name}"
        print(log_message)
        selected_prompt = prompt_func(errors, contract_content, symboleo_syntax)
    else:
        # Randomly mix two styles for iterations > 3
        selected_funcs = random.sample(prompt_styles, 2)
        selected_names = [prompt_names[prompt_styles.index(func)] for func in selected_funcs]
        prompt_name = f"Mixed_{selected_names[0]}+{selected_names[1]}"  
        log_message = (
            f"🔁 Iteration {iteration} → Using Mixed Prompt Styles: "
            f"{selected_names[0]} + {selected_names[1]}"
        )
        print(log_message)
        part1 = selected_funcs[0](errors, contract_content, symboleo_syntax)
        part2 = selected_funcs[1](errors, contract_content, symboleo_syntax)
        selected_prompt = f"{part1}\n\n--- Additional Guidance ---\n\n{part2}"

    # Optional: Save the log message to a file
    if log_file_path:
        try:
            with open(log_file_path, "a") as log_file:
                log_file.write(log_message + "\n")
        except Exception as e:
            print(f"⚠️ Failed to write log: {e}")
    # print(f'Selected Prompt IS ',selected_prompt)
    return selected_prompt, prompt_name


def get_fixed_contract(prompt):
    """Sends the prompt to ChatGPT API and returns the corrected contract."""
    print("Running Fixing")
    if not prompt:
        return "No errors detected, so no correction needed."
    
    # Sending the syntax and prompt to LLM (chatgpt) 
    try:
        print("Sending syntax and prompt to Chatgpt .....")
        client = OpenAI(api_key=API_KEY)
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  # Ensure this model is available to you
            messages=[
            {"role": "user", "content": prompt}
            ]
        )
        print("Got the response back from LLM (Chatgpt)")
        return completion.choices[0].message.content  

    except Exception as e:
        return f"Error occurred: {e}"

def read_symboleo_syntax_file(file_path):
    """Reads a text file and returns its content without newlines and tabs."""
    try:
        print("Reading the symboleo syntax ....")
        with open(file_path, "r", encoding="utf-8") as file:
            print("Successfully Read the symboleo syntax")
            return file.read()
    except FileNotFoundError:
        return "Error: File not found."
    except Exception as e:
        return f"Error: {e}"
    
def read_txt_file(file_path):
    """Reads the file and extracts errors and contract content separately."""
    try:
        print("Reading the current errors and contract or symboleo contract....")
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        # Splitting the content into errors and contract parts
        parts = content.split("Contract Content:")
        errors = parts[0].replace("Errors:", "").strip() if len(parts) > 0 else "No errors found."
        contract_content = parts[1].strip() if len(parts) > 1 else "No contract content found."
        print("Successfully Reading Done")
        return errors, contract_content

    except FileNotFoundError:
        print("Error: File not found.")
        return None, None
    except Exception as e:
        print(f"Error: {e}")
        return None, None
  
def save_to_file(content, filename_prefix, directory, iteration):
    """Saves the provided content to a specified directory."""
    try:
        print("Saving the corrected file at the location specified ......")
        # Ensure the directory exists, if not, create it
        os.makedirs(directory, exist_ok=True)
        
        # Construct full file path
        filename = f"{filename_prefix}-{iteration}.symboleo"
        full_path = os.path.join(directory, filename)

        # Save the file
        with open(full_path, 'w', encoding="utf-8") as file:
            file.write(content)
        
        print(f"Contract successfully saved to {full_path}")
    
    except Exception as e:
        print(f"Failed to save the contract: {e}")

def remove_first_and_last_line(text):
    lines = text.split("\n")
    return "\n".join(lines[1:-1]) if len(lines) > 2 else ""


# TODO :Set the correct file path , depends on where the files are
file_path = "/Users/gurdarshansingh/Desktop/Masters_Project/runtime-EclipseApplication/workspace_output.txt"  # Replace with your workspace_output.txt file
syntax_file_path = "/Users/gurdarshansingh/Desktop/Masters_Project/Python/symboleo_syntax.txt" # Replace with the symboleo_syntax.txt file
log_file_path = "/Users/gurdarshansingh/Desktop/prompt_logs.txt"
# Read the file and extract content
errors, contract = read_txt_file(file_path) # Reading the workspace_output.txt file to extract current errors and contract
symboleo_syntax = read_symboleo_syntax_file(syntax_file_path) # Reading the symboleo_syntax.txt file to get the symboleo syntax so that we can send to LLM (chatgpt)

# TODO Save the response (corrected contract) from the chatgpt in this location : The file with name corrected_contract.txt would be there at the location mentioned
directory = "/Users/gurdarshansingh/Desktop/runtime-EclipseApplication/meatsale/"

# print(f"Errors are: {errors}")
print(f"####################################################:\nErrors are: {errors}")


iteration = int(sys.argv[1])
# This is the code to generate the prompt, then send that prompt to chatgpt and get the response and save it to a file named corrected_contract.txt
# It runs only when there are errors in the file
if errors.lower() != "no errors found.":
    #Generate the Chatgpt prompt
    # prompt = generate_prompt(errors, contract,symboleo_syntax, iteration, log_file_path)
    # print(f'Error:', errors)
    # print(f'Contract:', contract)
    # print(f'Symboleo Syntax:', symboleo_syntax)
    print(f'Iteration From Code is :', iteration)
    # prompt = generate_main_prompt(errors, contract)
    for iteration in range(0, iteration):
        prompt, prompt_type = generate_prompt(errors, contract, symboleo_syntax, iteration, log_file_path)
        # print(f'Final Prompt is',prompt)
        # # Send the Prompt to ChatGPT API
        corrected_contract = get_fixed_contract(prompt)
        corrected_contract = remove_first_and_last_line(corrected_contract)
        # Save the corrected contract to a file
        filename_prefix = f"corrected_contract_{prompt_type.replace(' ', '_')}"
        # filename_prefix = f"corrected_contract_"
        save_to_file(corrected_contract, filename_prefix, directory, iteration)

    # save_to_file(corrected_contract, 'corrected_contract.txt', directory, iteration)
else:
    print("No errors detected, skipping contract correction.")