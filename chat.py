import numpy as np
from numpy import dot
from numpy.linalg import norm

import json
from datetime import datetime, timedelta, date
import sqlite3
from hello import string
from openai import AzureOpenAI
from dotenv import load_dotenv
import os

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

def insert_meeting(date, start_time, duration, person, job_role, meeting):
    conn=sqlite3.connect('calendar.db')
    cursor=conn.cursor()
    cursor.execute('''
            INSERT INTO day (date, start_time, duration, person, job_role, meeting)
            VALUES (?,?,?,?,?,?)
            ''',(date,start_time,duration,person,job_role,meeting))
    conn.commit()
    conn.close()

def Todays_date():
    today= date.today()
    return str(today)

records_text=string()
today_str= Todays_date()

print("Chatbot: Hello! How can I assist you today? Type 'exit' to end the conversation.")

chatbot = Chatbot()

prompts = [
                {"role": "system", "content": 'You are a helpful assistant. dates are formatted dd.mm.yy'},
                {"role": "system", "content": f'here are the calendar records:\n{records_text}'},
                {"role": "system", "content": f'here is todays date:\n{today_str}'},
                {"role": "system", "content": "if the user wants to add a meeting, return the details as JSON like this\n"+
                                                '{"date": "08.07.25","start_time":"10.00","duration":"30","person":"Mel Davis","job_role":"Marketing Manager","meeting":"intro to marketing"}'},
            ]

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Chatbot: Ending the conversation. Have a great day!")
        break
    
    chatbot.store_user_input(user_input)

    try:
        response = client.chat.completions.create(
            model=AZURE_OPENAI_MODEL_NAME,
            messages=prompts + chatbot.memory,
            max_tokens=200
            )

        response_text = response.choices[0].message.content.strip()

        chatbot.store_system_response(response_text)
        print('chat bot:',response_text)
    except:
        pass
    try:
        data = json.loads(response_text)
        
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
