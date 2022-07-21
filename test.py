import sqlite3
import random

class DataBaseConnection():
    def __init__(self, database_path):
        #sqlite connection
        self.conn = sqlite3.connect(database_path)
        self.cur = self.conn.cursor()

        #creates table if it does not exist yet
        self.conn.execute("CREATE TABLE IF NOT EXISTS Questions(id INTEGER PRIMARY KEY AUTOINCREMENT, main_question TEXT, question_A TEXT, question_B TEXT, question_C TEXT, correct_answer TEXT)")
        self.conn.commit()
    
    #adds questions and answers to database
    def add_to_database(self, question_A, question_B, question_C, question_D, correct_answer):
        entities = question_A, question_B, question_C, question_D, correct_answer
        self.conn.execute("""INSERT INTO Questions(main_question, question_A, question_B, question_C, correct_answer) VALUES(?, ?, ?, ?, ?)""", entities)
        self.conn.commit()

    def get_quesstion(self):
        quesion_bank = {}
        random_question_bank = {}

        #a = self.conn.execute('SELECT id FROM Questions WHERE id = ?', ("",))
        get_last_question = self.conn.execute("SELECT id FROM Questions ORDER BY id DESC LIMIT 1")
        pull_random_question = self.conn.execute('SELECT * FROM Questions WHERE id = ?', (random.randint(1, get_last_question.fetchall()[0][0]),))
        question = pull_random_question.fetchall()
        quesion_bank[1] = question[0][2]
        quesion_bank[2] = question[0][3]
        quesion_bank[3] = question[0][4]
        quesion_bank[4] = question[0][5]
        question[0][1]
        for xx in range(1, 5):
            #print(quesion_bank[xx])
            num, qu = random.choice(list(quesion_bank.items()))
            del quesion_bank[num]
            random_question_bank[xx] = qu

        for bb in random_question_bank.items():
            print(bb[1])

        imp = int(input(": "))

        if random_question_bank[imp] == question[0][5]:
            print("YES")
        else:
            print("NO")
            

#DataBaseConnection("discord-quiz-bot/questions.db").add_to_database("What layer is Application?", "Layer 1", "Layer 4", "Layer 2", "Layer 7")
DataBaseConnection("discord-quiz-bot/questions.db").get_quesstion()