import sqlite3
conn = sqlite3.connect('calendar.db')
cursor =conn.cursor()

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
    column = int(input ('select which column you are searching in: 1. date\n2.time\n3.person '))
    if column == 1:
        dates=[]
        dat =input ('enter date/s, when finished input done ')
        
        while dat != 'done':
            dates.append(dat)
            dat =input ('enter date/s, when finished input done ')
        placeholders=','.join(['?']*len(dates))
        query = f'''
        SELECT * FROM day
        WHERE date IN ({placeholders})
        '''
        rows = read_record_for_date(query,dates,)
        for row in rows:
            print(row)
    elif column == 2:
        tim=input('enter the time of the meeting: ')
        rows = read_record_for_day(tim);
        for row in rows:
            print(row)
    elif column == 3:
        pers=input('who are you looking for: ')
        rows = read_record_for_person(pers,)
        for row in rows:
            print(row)


def read_record_for_date(query,dates,):
    cursor.execute(query,dates)
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

def add_record():
    dat=input('enter the date of the meeting: ')
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
        elif choice =='4':
            print('goodbye!')
            break
        else:
            print('invalid input.')
            choice=input('select one of the 4 start options ')