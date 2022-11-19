import sqlite3

con = sqlite3.connect("../data/tutor_db.db")
cur = con.cursor()
cur.executescript("""
    create table questions(
        question_id,
        question_text
    );
   insert into questions values ( '1', 'How do you greet the customer?' );
   insert into questions values ( '2', 'How do you modify the e-mail address of the customer?' );

    """)
cur.execute("SELECT * from questions")
print(cur.fetchall())
con.commit()
con.close()
