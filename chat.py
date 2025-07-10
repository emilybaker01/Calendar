from openai import AzureOpenAI
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Retrieve environment variables
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_MODEL_NAME = os.getenv("AZURE_OPENAI_MODEL_NAME")
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    base_url=f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_CHAT_DEPLOYMENT_NAME}"
)

print("Chatbot: Hello! How can I assist you today? Type 'exit' to end the conversation.")
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Chatbot: Ending the conversation. Have a great day!")
        break
    response = client.chat.completions.create(
        model=AZURE_OPENAI_MODEL_NAME,
        messages=[
            {"role": "system", "content": 'You are a helpful assistant. On 08.07.25, there is a intro to marketing meeting at 10.00 with Mel Davis, Marketing Manager. It is 30 minutes long.'
            'On 08.07.25, there is a intro to training meeting at 10.30 with Di Austin, Training Manager. It is 30 minutes long.'
            'On 08.07.25, there is a intro to testing meeting at 11.00 with George Smyth, CTO. It is 30 minutes long.'
            'On 08.07.25, there is a intro to tech docs meeting at 11.30 with Chris Callaghan, Technical Writer. It is 30 minutes long.'
            'On 09.07.25, there is a Campaigning Team Workshop meeting at 10.00 with Adam Robertson, Campaigning Tech Lead. It is 30 minutes long.'
            'On 09.07.25, there is a Intro to Tech Services meeting at 11.00 with Craig Walker, Tech Services Manager. It is 30 minutes long.'
            'On 10.07.25, there is a Intro to Development meeting at 15.30 with Stuart Williams, Software Producer. It is 30 minutes long.'},
            {"role": "user", "content": user_input}
        ],
        max_tokens=200
    )
    print("Chatbot:", response.choices[0].message.content.strip())