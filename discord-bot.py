import discord
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
import os 
import random

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix=".")


@bot.command()
async def give_question(ctx):
    user_discord_user = ctx.message.author.id
    random_number = random.randint(1, 2)
    questions = {1: {"Question": "What layer is Application?", 1: "Layer 4", 2: "Layer 1", 3: "Layer 7", "Correct": 3}, 2: {"Question": "What is virtualization", 1: "It's a operating system", 2: "Technology that lets you create isolated operating systems on one server", 3: "Technology that lets you create operating systems on one server", "Correct": 2}}
    random_question_bank = []
    counter = 1
    correct_answer = questions[random_number]["Correct"]
    await ctx.send(questions[random_number]["Question"])
    for x in questions[random_number]:
        if x != "Question" and x != "Correct":
            random_question_bank.append(questions[random_number][x])

    for questions in random_question_bank:
        await ctx.send(str(counter) + ") " + questions)
        counter += 1

    def check(m):
        global user_answer
        user_answer = m.content
        global user_id
        user_id = m.author.id
        return m.content
    
    msg = await bot.wait_for("message", check=check)
    if user_id == user_discord_user:
        if str(user_answer) == str(correct_answer):
            await ctx.send("Correct")
        else:
            await ctx.send("Wrong it's " + str(correct_answer))
    else:
        await ctx.send("You can't answer sorry")

bot.run(token)

this is a test
