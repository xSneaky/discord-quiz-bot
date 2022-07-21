import discord
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
import os 
import random
import sqlite3

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix=".")

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
        #a = self.conn.execute('SELECT id FROM Questions WHERE id = ?', ("",))
        get_last_question = self.conn.execute("SELECT id FROM Questions ORDER BY id DESC LIMIT 1")
        pull_random_question = self.conn.execute('SELECT * FROM Questions WHERE id = ?', (random.randint(1, get_last_question.fetchall()[0][0]),))
        return pull_random_question.fetchall()
            
aa = DataBaseConnection("discord-quiz-bot/questions.db") #.add_to_database("What layer is Application?", "Layer 4", "Layer 2", "Layer 8", "Layer 7")

@bot.command()
async def give_question(ctx):
    quesion_bank = {}
    random_question_bank = {}

    user_discord_user = ctx.message.author.id
    random_number = random.randint(1, 2)
    question = DataBaseConnection("discord-quiz-bot/questions.db").get_quesstion()

    await ctx.send(question[0][1])
    
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
        await ctx.send(bb[1])



    def check(m):
        global user_answer
        user_answer = m.content
        global user_id
        user_id = m.author.id
        return m.content
    
    msg = await bot.wait_for("message", check=check)
    if user_id == user_discord_user:
        if random_question_bank[int(user_answer)] == str(question[0][5]):
            await ctx.send("Correct")
        else:
            await ctx.send("Wrong")
    else:
        await ctx.send("You can't answer sorry")

    print(random_question_bank[int(user_answer)])
    print(question[0][5])
    


bot.run(token)
