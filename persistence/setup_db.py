import sqlite3

con = sqlite3.connect("../data/tutor_db.db")
cur = con.cursor()
cur.executescript("""
    CREATE TABLE questions(
        question_id INTEGER PRIMARY KEY,
        question_text TEXT NOT NULL ,
        answer_text TEXT NOT NULL
    );
    INSERT INTO questions VALUES ( 1, 'How do you greet the customer?', 'Hello, how may I help you?' );
    INSERT INTO questions VALUES ( 2, 'What do you say before you finish the conversation with the customer?', 
        'What else can I help you with?');
    INSERT INTO questions VALUES ( 3, 'What do the initials HAL for the HAL 9000 computer mean in "A Space Odyssey" film?', 
        'Heuristically programmed Algorithmic computer');
    INSERT INTO questions VALUES ( 4, 'List the most important elements of a computer!', 'Processor, keyboard, mouse.');
    INSERT INTO questions VALUES ( 5, 'Which components have caused the biggest change in computing in the last 20 years?', 'Processor, graphical processing unit, solid-state drive');
    INSERT INTO questions VALUES ( 6, 'Sum this text up in 1 sentence: A computer is an electronic device designed to process and store data, perform calculations, and execute predefined instructions. It consists of hardware components such as a central processing unit (CPU), memory, storage devices, input devices (like keyboard and mouse), and output devices (such as monitor and printer). Computers operate based on binary code, using combinations of ones and zeros to represent data and instructions. They can run various software programs, allowing users to perform tasks ranging from basic word processing to complex simulations and calculations.', 'A computer is a versatile electronic device that processes data using binary code and executes instructions to perform a wide range of tasks, facilitated by its hardware components and software programs.');
    INSERT INTO questions VALUES ( 7, 'Egy elképzelt szituációban hogyan üdvözli az ügyfelet? Legyen kedves, érdeklődő és segítőkész.', 'üdvözlöm örülök hogy megkeresett minket segíthetek önnek segíthetek jó napot');
    INSERT INTO questions VALUES ( 8, 'Hogyan utasít el udvariasan egy holnapra tervezett találkozót?', 'sajnálom de nem tudok segíteni holnap már van programom');
    INSERT INTO questions VALUES ( 9, 'Definiálja a számítógép fogalmát!', 'elektronikus információfeldolgozó gép amely információk adatok és programok tárolására alkalmas memóriával rendelkezik az adatok feldolgozásához programot használ és saját működését vezérli');
    INSERT INTO questions VALUES ( 10, 'Röviden fogalmazza meg, mit értünk számítógép-programozás alatt!', 'absztrakt algoritmusok megvalósítását jelenti egy bizonyos programozási nyelven'); 

    CREATE TABLE report(
        report_id INTEGER PRIMARY KEY AUTOINCREMENT,
        report_external_id TEXT NOT NULL ,
        question_id INTEGER NOT NULL ,
        created_time DATETIME DEFAULT CURRENT_TIMESTAMP,
        expected_answer TEXT NOT NULL,
        learners_answer TEXT NOT NULL ,
        score FLOAT NOT NULL,
        client_info TEXT,
        grade_group_id INTEGER NOT NULL,
        grade_text TEXT NOT NULL,
        
        FOREIGN KEY (question_id) REFERENCES questions (question_id)
    );

    CREATE TABLE grade(
        grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
        grade_group_id INTEGER NOT NULL,
        range_start FLOAT NOT NULL,
        grade_text TEXT NOT NULL 
    );
    INSERT INTO grade (grade_group_id, range_start, grade_text) VALUES (1, 1, "perfect match");
    INSERT INTO grade (grade_group_id, range_start, grade_text) VALUES (1, 0.8, "very good");
    INSERT INTO grade (grade_group_id, range_start, grade_text) VALUES (1, 0.65, "good");
    INSERT INTO grade (grade_group_id, range_start, grade_text) VALUES (1, 0.55, "try to get even better");
    INSERT INTO grade (grade_group_id, range_start, grade_text) VALUES (1, 0.5, "try to get better");
    INSERT INTO grade (grade_group_id, range_start, grade_text) VALUES (1, 0.0, "unacceptable, try again");
    INSERT INTO grade (grade_group_id, range_start, grade_text) VALUES (2, 0.7, "OK");
    INSERT INTO grade (grade_group_id, range_start, grade_text) VALUES (2, 0.0, "NOT OK");
    INSERT INTO grade (grade_group_id, range_start, grade_text) VALUES (3, 0.8, "A");
    INSERT INTO grade (grade_group_id, range_start, grade_text) VALUES (3, 0.65, "B");
    INSERT INTO grade (grade_group_id, range_start, grade_text) VALUES (3, 0.55, "C");
    INSERT INTO grade (grade_group_id, range_start, grade_text) VALUES (3, 0.5, "D");
    INSERT INTO grade (grade_group_id, range_start, grade_text) VALUES (3, 0.0, "F");
    
    CREATE TABLE config(
        config_id INTEGER PRIMARY KEY AUTOINCREMENT,
        config_key TEXT NOT NULL UNIQUE,
        config_value TEXT NOT NULL
    );
    INSERT INTO config (config_key, config_value) VALUES ("grade_group", "1");
    
""")
cur.execute("SELECT * from questions")
print(cur.fetchall())
con.commit()
con.close()
