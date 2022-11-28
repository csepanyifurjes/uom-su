import sqlite3

con = sqlite3.connect("../data/tutor_db.db")
cur = con.cursor()
cur.executescript("""
    CREATE TABLE questions(
        question_id,
        question_text,
        answer_text
    );
    INSERT INTO questions VALUES ( 1, 'How do you greet the customer?', 'Hello! How may I help you?' );
    INSERT INTO questions VALUES ( 2, 'What do you say before you finish the conversation with the customer?', 'What else can I help you with?');

    CREATE TABLE report(
        report_id INTEGER PRIMARY KEY AUTOINCREMENT,
        report_external_id TEXT,
        question_id INTEGER,        
        created_time DATETIME DEFAULT CURRENT_TIMESTAMP,
        expected_answer TEXT,
        learners_answer TEXT,
        score FLOAT,
        FOREIGN KEY (question_id) REFERENCES questions (question_id)
    );

""")
cur.execute("SELECT * from questions")
print(cur.fetchall())
con.commit()
con.close()
