import sqlite3
from datetime import datetime
conn = sqlite3.connect('calendar.db')
cursor =conn.cursor()
def date_verification(date_str,fmt='%d.%m.%y'):
    try:
        datetime.strptime(date_str,fmt)
        return True
    except ValueError:
        return False

    
def create_table():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS day (
        date INTEGER,
        start_time INTEGER,
        duration INTEGER,
        person TEXT NOT NULL,
        job_role TEXT NOT NULL,
        meeting TEXT NOT NULL,
        UNIQUE(date, start_time)
    )
    ''')

def read_table():
    cursor.execute('SELECT * FROM day')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def read_record():
    column = int(input ('select which column you are searching in:\n1. date\n2.time\n3.person '))
    if column == 1:
        dates=[]
        dat =input ('enter date/s (dd.mm.yy), when finished input done ')
        
        while dat != 'done':
            dates.append(dat)
            dat =input ('enter date/s, when finished input done ')
            
        rows = read_record_for_date(dates,)
        entries=[]
        for row in rows:
            entry=CalendarEntry(*row)
            entries.append(entry)
        for entry in entries:
            print (entry)
            
    elif column == 2:
        tim=input('enter the time of the meeting: ')
        rows = read_record_for_day(tim);
        entries=[]
        for row in rows:
            entry=CalendarEntry(*row)
            entries.append(entry)
        for entry in entries:
            print (entry)
            
    elif column == 3:
        pers=input('who are you looking for: ')
        rows = read_record_for_person(pers,)
        entries=[]
        for row in rows:
            entry=CalendarEntry(*row)
            entries.append(entry)
        for entry in entries:
            print (entry)
            
def add_record():
    while True:
        dat=input('enter the date of the meeting: ')
        if date_verification(dat):
            break
        else:
            print('invalid date. try again.')
    
    tim=input('enter the time of the meeting: ')
    length=input('enter the duration of the meeting: ')
    pers=input('enter the person holding the meeting: ')
    job=input('enter their job title: ')
    meet=input('enter the outline of the meeting: ')
    cursor.execute('''
    INSERT INTO day (date, start_time, duration, person, job_role, meeting)
    VALUES (?,?,?,?,?,?)
    ''',(dat,tim,length,pers,job,meet))
    conn.commit()
    conn.close()

def read_record_for_date(dates,):
    placeholders=','.join(['?']*len(dates))
    query = f'''
    SELECT * FROM day
    WHERE date IN ({placeholders})
    '''
    cursor.execute(query,dates,)
    rows = cursor.fetchall()
    return rows;

def read_record_for_person(pers,):
    cursor.execute('SELECT * FROM day WHERE person =?',(pers,))
    rows = cursor.fetchall()
    return rows;

def read_record_for_day(tim):
    cursor.execute('SELECT * FROM day WHERE start_time=?',(tim,))
    rows = cursor.fetchall()
    return rows;

def delete_record():
    #cursor.execute('DELETE FROM day WHERE person =?',(person,))
    #conn.commit()
    pass

def string():
    entries=[]
    cursor.execute('SELECT * FROM day')
    rows = cursor.fetchall()
    for row in rows:
        entry=CalendarEntry(*row)
        entries.append(str(entry))
    return '\n'.join(entries)

class CalendarEntry:
    def __init__(self, date, Starttime, duration, person, jobrole, meeting):
        self.date = date 
        self.Starttime = Starttime
        self.duration = duration
        self.person = person
        self.jobrole = jobrole
        self.meeting = meeting

    def __str__(self):
        return f'On {self.date}, there is a {self.meeting} meeting at {self.Starttime} with {self.person}, {self.jobrole}. It is {self.duration} minutes long.'
    
    

if __name__ == '__main__':
    create_table()
    print('*****WELCOME TO YOUR MEETING CALENDAR*****')
    print('PLEASE SELECT ONE OF THE FOLLOWING START OPTIONS')
    print('1.view whole table\n2.view specific records\n3.add new record\n4.exit')
    choice=input()
    while choice!='':
        if choice == '1':
            read_table()
            choice=input('select one of the 4 start options ')
        elif choice == '2':
            read_record()
            choice=input('select one of the 4 start options ')
        elif choice == '3':
            add_record()
            choice=input('select one of the 4 start options ')
        elif choice =='4' or 'exit':
            print('goodbye!')
            break

        else:
            print('invalid input.')
            choice=input('select one of the 4 start options ')