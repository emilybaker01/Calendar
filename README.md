# Calendar

The calendar is specifically for tracking meetings and schedualling new meetings. It uses a data base and SQL commands to create and view records.

At the moment it has 4 main commands:

* creates the table
* adds records
* views the whole table
* views specific records

_the table should not be created if already exists._
_new records cannot be created if they have the same date and time._

_09.07.25_ this program now includes openai!
https://techcommunity.microsoft.com/blog/educatordeveloperblog/building-a-basic-chatbot-with-azure-openai/4373018

## __here are some examples of ai adding in records__
__You:__ add a meeting to my calendar on wednesday 9th at 10.30 for an Intro to BD, with Martin Green, Business Development, for 30 minutes


__chat bot:__ {"date": "09.07.25","start_time":"10.30","duration":"30","person":"Martin Green","job_role":"Business Development","meeting":"Intro to BD"}
meeting added to database. 
inserting:  {'date': '09.07.25', 'start_time': '10.30', 'duration': '30', 'person': 'Martin Green', 'job_role': 'Business Development', 'meeting': 'Intro to BD'}

__You:__ add a meeting with Simon Holderness, Development Director on Friday 11th at midday for a discussion on cricket to last an hour


__chat bot:__ {"date": "11.10.25","start_time":"12.00","duration":"60","person":"Simon Holderness","job_role":"Development Director","meeting":"discussion on cricket"}
meeting added to database. 
inserting:  {'date': '11.10.25', 'start_time': '12.00', 'duration': '60', 'person': 'Simon Holderness', 'job_role': 'Development Director', 'meeting': 'discussion on cricket'}

as you can see the date automatically saved to the month of october, i will try and fix that using datetime and calendar