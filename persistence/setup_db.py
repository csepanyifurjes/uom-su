import sqlite3

con = sqlite3.connect("../data/tutor_db.db")
cur = con.cursor()
cur.executescript("""
    create table questions(
        question_id,
        question_text,
        answer_text
    );
   insert into questions values ( 1, 'How do you greet the customer?', 'Hello! How may I help you?' );
   insert into questions values ( 2, 'What do you say before you finish the conversation with the customer?', 'What else can I help you with?');
""")
cur.execute("SELECT * from questions")
print(cur.fetchall())
con.commit()
con.close()
