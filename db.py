import sqlite3
db_name = 'quiz.db'
conn = None
curor = None

def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

def close():
    cursor.close()
    conn.close()

def do(query):
    cursor.execute(query)
    conn.commit()

def clear_db_tables():
    ''' delete all tables '''
    open()
    query = '''DROP TABLE IF EXISTS quiz_content'''
    do(query)
    query = '''DROP TABLE IF EXISTS question'''
    do(query)
    query = '''DROP TABLE IF EXISTS quiz'''
    do(query)
    close()

def create_schema_tables():

    open()

    table_quiz = """CREATE TABLE IF NOT EXISTS quiz 
    (id INTEGER PRIMARY KEY, name VARCHAR)"""
    cursor.execute(table_quiz)

    table_question = """CREATE TABLE IF NOT EXISTS question 
    (id INTEGER PRIMARY KEY, 
    question VARCHAR,
    answer VARCHAR,
    wrong1 VARCHAR,
    wrong2 VARCHAR,
    wrong3 VARCHAR)"""
    cursor.execute(table_question)

    cursor.execute('''PRAGMA foreign_keys=on''') 

    table_quiz_content = """CREATE TABLE IF NOT EXISTS quiz_content (
    id INTEGER PRIMARY KEY,
    quiz_id INTEGER,
    question_id INTEGER,
    FOREIGN KEY (quiz_id) REFERENCES quiz (id),
    FOREIGN KEY (question_id) REFERENCES question (id))"""
    cursor.execute(table_quiz_content)

    conn.commit()

    
def fill_data_to_tables():
    open()
    # quizes = [
    #     ('Own game', ),
    #     ('Who wants to be a millionaire?', ),
    #     ('The smartest', )
    # ]

    # questions = [
    #     ('How many months in a year have 28 days?', 'All', 'One', 'None','Two'),
    #     ('What will the green cliff look like if it falls into the Red Sea?', 'Wet', 'Red', 'Will not change', 'Purple'),
    #     ('Which hand is better to stir tea with?', 'With a spoon', 'Right', 'Left', 'Any'),
    #     ('What has no length, depth, width, or height, but can be measured?', 'Time', 'Stupidity', 'The sea','Air'),
    #     ('When is it possible to draw out water with a net?', 'When the water is frozen', 'When there are no fish', 'When the goldfish swim away', 'When the net breaks'),
    #     ('What is bigger than an elephant and weighs nothing?', 'Shadow of elephant','A balloon','A parachute', 'A cloud')
    # ]

    # quiz_content = [
    #     (1, 1,),
    #     (1, 2,),
    #     (2, 3,),
    #     (2, 4,),
    #     (3, 5,),
    #     (3, 6,)
    # ]

    # cursor.executemany('''INSERT INTO quiz 
    #                 (name) 
    #                 VALUES (?)''', quizes)
    # cursor.executemany('''INSERT INTO question 
    #                 (question, answer, wrong1, wrong2, wrong3) 
    #                 VALUES (?,?,?,?,?)''', questions)
    # cursor.executemany('''INSERT INTO quiz_content 
    #                 (quiz_id, question_id) 
    #                 VALUES (?,?)''', quiz_content)
    # conn.commit()

    # Menambahkan 3 tipe kuis baru
    tech_quizes = [
        ('Golang Fundamentals', ),
        ('Python & Django Mastery', ),
        ('Web Development Basics', )
    ]

    # Format: (question, answer, wrong1, wrong2, wrong3)
    tech_questions = [
        # Pertanyaan seputar Go (ID 7, 8)
        ('What keyword is used to create a concurrent goroutine in Go?', 'go', 'thread', 'run', 'start'),
        ('Which of these is NOT a valid numeric data type in Go?', 'float128', 'float64', 'int32', 'complex128'),
        
        # Pertanyaan seputar Python & Django (ID 9, 10)
        ('In Python, which keyword is used to define a function?', 'def', 'function', 'func', 'define'),
        ('Which architectural pattern does Django primarily follow?', 'MVT (Model-View-Template)', 'MVC (Model-View-Controller)', 'MVVM', 'MVP'),
        
        # Pertanyaan seputar HTML, CSS, JS (ID 11, 12, 13)
        ('What does CSS stand for?', 'Cascading Style Sheets', 'Colorful Style Sheets', 'Computer Style Sheets', 'Creative Style Sheets'),
        ('Which HTML tag is used to define an internal style sheet?', '<style>', '<css>', '<script>', '<link>'),
        ('How do you write "Hello World" in an alert box using JavaScript?', 'alert("Hello World");', 'msg("Hello World");', 'msgBox("Hello World");', 'alertBox("Hello World");')
    ]

    # Asumsi: ID kuis sebelumnya 1-3, jadi kuis baru memiliki ID 4, 5, 6.
    # Asumsi: ID pertanyaan sebelumnya 1-6, jadi pertanyaan baru memiliki ID 7-13.
    # Format: (quiz_id, question_id)
    tech_quiz_content = [
        # Relasi untuk kuis Golang
        (4, 7),  
        (4, 8),  
        
        # Relasi untuk kuis Python & Django
        (5, 9),  
        (5, 10), 
        
        # Relasi untuk kuis Web Development
        (6, 11), 
        (6, 12), 
        (6, 13), 
        
        # --- Contoh Many-to-Many Murni ---
        # Memasukkan pertanyaan Python ke dalam kuis Web Development juga
        (6, 9),
        # Memasukkan pertanyaan HTML (CSS) ke kuis Python & Django (karena Django butuh frontend)
        (5, 11)
    ]

    # Eksekusi ke database
    cursor.executemany('''INSERT INTO quiz 
                    (name) 
                    VALUES (?)''', tech_quizes)
                    
    cursor.executemany('''INSERT INTO question 
                    (question, answer, wrong1, wrong2, wrong3) 
                    VALUES (?,?,?,?,?)''', tech_questions)
                    
    cursor.executemany('''INSERT INTO quiz_content 
                    (quiz_id, question_id) 
                    VALUES (?,?)''', tech_quiz_content)
                    
    conn.commit()

def show(table):
    query = 'SELECT * FROM ' + table
    open()
    cursor.execute(query)
    data = cursor.fetchall()
    close()
    return data

def show_questions_by_quiz_id(id):
    open()


    cursor.execute('''SELECT * from quiz_content 
                    WHERE quiz_id = (?)''', str(id))
    data = cursor.fetchall()
    questions = list()
    for (id, quiz_id, question_id) in data:
        cursor.execute('''SELECT * FROM question 
                       WHERE id = ''' + str(question_id))
        question =cursor.fetchone()
        questions.append(question)
    conn.commit()

    return questions

def get_questions_by_id(id):
    open()
    cursor.execute('''SELECT * FROM question 
                    WHERE id = (?)''', str(id))
    question = cursor.fetchone()
    return question

def show_tables():
    show('question')
    show('quiz')
    show('quiz_content')


def get_correct_answer(index, jawaban):
    data = get_questions_by_id(index)
    if data[2] == jawaban:
        return 1
    else:
        return 0


def main():
    # clear_db()
    # create_schema()
    # create()
    # show_tables()
    # get_correct_answer(0, "All")
    # show_questions_by_quiz_id('1')
    fill_data_to_tables()

if __name__ == "__main__":
    main()