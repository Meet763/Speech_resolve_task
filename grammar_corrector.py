import requests
import streamlit as st

# Load environment variables from .env file

def correct_grammar(user_sentence):
    # Azure OpenAI connection details
    azure_openai_key = st.secrets["openai"]["api_key"]  # Ensure the key is set in your .env
    azure_openai_endpoint = st.secrets["openai"]["api_endpoint"]  # Ensure the endpoint is set in your .env

    if azure_openai_key and azure_openai_endpoint:
        if user_sentence:  # Check if the input sentence is not empty
            try:
                # Setting up headers for the API request
                headers = {
                    "Content-Type": "application/json",
                    "api-key": azure_openai_key
                }
                
                # Data to be sent to Azure OpenAI
                data = {
                    "messages": [
                        {
                            "role": "user",
                            "content": f"Please correct the grammar of the following sentence: '{user_sentence}' and in output only give me corrected sentence not any additional text like this is your corrected text"
                        }
                    ],
                    "max_tokens": 100  # Adjust token limit as needed
                }
                
                # Making the POST request to the Azure OpenAI endpoint
                response = requests.post(azure_openai_endpoint, headers=headers, json=data)
                
                # Check if the request was successful
                if response.status_code == 200:
                    result = response.json()  # Parse the JSON response
                    full_response = result["choices"][0]["message"]["content"].strip()  # Get full response

                    # Extract the part between single or double quotes
                    if "'" in full_response:
                        corrected_sentence = full_response.split("'")[1]  # Extract text between quotes
                    elif '"' in full_response:
                        corrected_sentence = full_response.split('"')[1]  # Handle double quotes
                    else:
                        corrected_sentence = full_response  # Fallback, in case no quotes were used

                    # Return only the corrected sentence
                    return corrected_sentence
                else:
                    return f"Error: {response.status_code} - {response.text}"
            except Exception as e:
                return f"Error: {str(e)}"
        else:
            return "No sentence provided for correction."
    else:
        return "API key or endpoint missing."
