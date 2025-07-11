import json
from datetime import date
import sqlite3
from hello import string
from openai import AzureOpenAI
from dotenv import load_dotenv
import os


# A simple chatbot class that stores conversation history and responds differently when asked to remember input.
class Chatbot:
    def __init__ (self):
        self.memory = []
    
    def store_user_input(self, user_input):
        self.memory.append({"role": "user", "content": user_input});

    def store_system_response(self, system_response):
        self.memory.append({"role": "assistant", "content": system_response});

    def respond(self, user_input):
        if 'remember' in user_input.lower():
            self.memory.append(user_input)
            return f'I remember you said: {', '.join(self.memory)}'
        return f'you said: {user_input}. anything else? '
    


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

#allows the chatbot to create meetings that go directly into the calendar
def insert_meeting(date, start_time, duration, person, job_role, meeting):
    conn=sqlite3.connect('calendar.db')
    cursor=conn.cursor()
    cursor.execute('''
            INSERT INTO day (date, start_time, duration, person, job_role, meeting)
            VALUES (?,?,?,?,?,?)
            ''',(date,start_time,duration,person,job_role,meeting))
    conn.commit()
    conn.close()
#a function that is put into the prompts so the chatbot knows the date
def Todays_date():
    today= date.today()
    return str(today)

#string is imported from the hello file, and is a function that turns all current records into strings so they can be added to the prompts
records_text=string()
#a variable of the date function so it can be put into the prompts
today_str= Todays_date()
#the out put of the chatbot
print("Chatbot: Hello! How can I assist you today? Type 'exit' to end the conversation.")
#an object of the chatbot class
chatbot = Chatbot()
#an array of the prompts given to the chatbot eg: the records and the date
prompts = [
                {"role": "system", "content": 'You are a helepful assistant. dates are formatted dd.mm.yy.'},
                {"role": "system", "content": f'here are the calendar records:\n{records_text}'},
                {"role": "system", "content": f'here is todays date:\n{today_str}'},
                {"role": "system", "content": "if the user wants to add a meeting, return the details as JSON like this\n"+
                                                '{"date": "08.07.25","start_time":"10.00","duration":"30","person":"Mel Davis","job_role":"Marketing Manager","meeting":"intro to marketing"}'},
            ]

# Start an infinite loop to keep the chatbot running
while True:
    # Prompt the user for input
    user_input = input("You: ")
    # Check if the user wants to exit the conversation
    if user_input.lower() == "exit":
        print("Chatbot: Ending the conversation. Have a great day!")
        break
    
    # Store the user's input into the chatbot's memory
    chatbot.store_user_input(user_input)

    try:
        # Make a call to the Azure OpenAI model with the current conversation history
        response = client.chat.completions.create(
            model=AZURE_OPENAI_MODEL_NAME,      # Use the specified Azure OpenAI model
            messages=prompts + chatbot.memory,  # Combine system prompts and conversation memory
            max_tokens=200                      # Limit the number of tokens in the response
            )

         # Extract the chatbot's response text from the API result
        response_text = response.choices[0].message.content.strip()

        # Store the chatbot's response in memory and print it
        chatbot.store_system_response(response_text)
        print('chat bot:',response_text)
    except:
        # If there's an error during the API call, silently ignore it (not recommended for production)
        pass
    try:
        # Attempt to parse the chatbot's response as JSON
        data = json.loads(response_text)
        
        # Insert the extracted meeting details into the database
        insert_meeting(
            data['date'],
            data['start_time'],
            data['duration'],
            data['person'],
            data['job_role'],
            data['meeting']
        )
        print('meeting added to database. ')
        print('inserting: ',data)
    
    except json.JSONDecodeError as e:
        print(' ')
    except Exception as e:
        print(f'unexpected error: {e}')
    except KeyError as e:
        print(f'missing one or more required feilds in the response {e}')
