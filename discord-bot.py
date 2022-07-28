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
        question_topics = ["computer_fundamentals", "operations", "development", "agile"]
        #sqlite connection
        self.conn = sqlite3.connect(database_path)
        self.cur = self.conn.cursor()
        #creates table if it does not exist yet
        for create_database_tables in question_topics:
            self.conn.execute("CREATE TABLE IF NOT EXISTS " + create_database_tables +"(id INTEGER PRIMARY KEY AUTOINCREMENT, main_question TEXT, question_A TEXT, question_B TEXT, question_C TEXT, correct_answer TEXT)")
            self.conn.commit()
    
    #adds questions and answers to database
    def add_to_database(self, question_A, question_B, question_C, question_D, correct_answer):
        entities = question_A, question_B, question_C, question_D, correct_answer
        self.conn.execute("""INSERT INTO computer_fundamentals(main_question, question_A, question_B, question_C, correct_answer) VALUES(?, ?, ?, ?, ?)""", entities)
        self.conn.commit()

    def get_quesstion(self, topic):
        #a = self.conn.execute('SELECT id FROM Questions WHERE id = ?', ("",))
        get_last_question = self.conn.execute("SELECT id FROM " +topic+" ORDER BY id DESC LIMIT 1")
        pull_random_question = self.conn.execute("SELECT * FROM "+topic+" WHERE id = ?", (random.randint(1, get_last_question.fetchall()[0][0]),))
        return pull_random_question.fetchall()
            
#aa = DataBaseConnection("discord-quiz-bot/questions.db").add_to_database("What does CPU stand for? ", "Control Process Unit", "Control Processing Unit", "Central Price Unit", "Central Processing Unit")
bot.remove_command('help')

@bot.command()
async def help(ctx):
    embed=discord.Embed(title="Quiz bot Help", description='You will have 20 seconds to answer the questions. \nIf you cannot answer the question you can skip by inputting "skip" or you can quit by inputting "quit"', color=0x1a5fb4)
    embed.set_thumbnail(url="https://i.pinimg.com/originals/5c/1a/96/5c1a96decc2a250d2a9079d0ca694179.jpg")    
    embed.add_field(name="Topic", value="Computer Fundamentals \nOperations \nDevelopment \nAgile", inline=True)
    embed.add_field(name="command", value=".give_question computer fundamentals \n.give_question operations \n.give_question development \n.give_question agile", inline=True)
    embed.set_image(url="https://i.imgur.com/yZ03TF2.png")
    await ctx.send(embed=embed)

@bot.command()
async def give_question(ctx, *topic):
    user_discord_user = ctx.message.author.id
    
    def response_proccess(m):
        return m.content

    def generate_questions():
        quesion_bank = {}
        random_question_bank = {}
        counter = 1
        question = DataBaseConnection("discord-quiz-bot/questions.db").get_quesstion("computer_fundamentals")
        correct_answer = question[0][5]
        embed=discord.Embed(title=question[0][1], color=0x1a5fb4, description="")
        for add_to_question_bank in range(1, 5):
            quesion_bank[add_to_question_bank] = question[0][int(add_to_question_bank + 1)]
        
        for add_to_random_question_bank in range(1, 5):
            number, question1 = random.choice(list(quesion_bank.items()))
            del quesion_bank[number]
            random_question_bank[add_to_random_question_bank] = question1
        
        for generate_question_for_discord in random_question_bank.items():
            if counter == 1:
                emoji = ":one:"
            elif counter == 2:
                emoji = ":two:"
            elif counter == 3:
                emoji = ":three:"
            else:
                emoji = ":four:"
            embed.add_field(name=str(emoji) + " " + generate_question_for_discord[1], value="-", inline=False)
            counter += 1
        return embed, correct_answer, random_question_bank

    aaa = generate_questions()
    await ctx.send(embed=aaa[0])
    try:
        while True:
            msg = await bot.wait_for("message", check=response_proccess, timeout=10)
            if user_discord_user == msg.author.id:
                if msg.content == "1" or msg.content == "2" or msg.content == "3" or msg.content == "4":
                    if aaa[2][int(msg.content)] == aaa[1]:
                        await ctx.send("Correct")
                        break
                    else:
                        await ctx.send("WRONG")
                        break
                else:
                    await ctx.send("Incorrect response. Please try again using 1, 2, 3, 4")
            else:
                pass

    except asyncio.TimeoutError:
        await ctx.send("You ran out of time!")

bot.run(token)
