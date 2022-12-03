import sqlite3

con = sqlite3.connect("../data/tutor_db.db")
cur = con.cursor()
cur.executescript("""
    CREATE TABLE questions(
        question_id INTEGER PRIMARY KEY,
        question_text TEXT NOT NULL ,
        answer_text TEXT NOT NULL
    );
    INSERT INTO questions VALUES ( 1, 'How do you greet the customer?', 'Hello! How may I help you?' );
    INSERT INTO questions VALUES ( 2, 'What do you say before you finish the conversation with the customer?', 
        'What else can I help you with?');

    CREATE TABLE report(
        report_id INTEGER PRIMARY KEY AUTOINCREMENT,
        report_external_id TEXT NOT NULL ,
        question_id INTEGER NOT NULL ,
        created_time DATETIME DEFAULT CURRENT_TIMESTAMP,
        expected_answer TEXT NOT NULL,
        learners_answer TEXT NOT NULL ,
        score FLOAT NOT NULL,
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
