import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

@bot.command()
async def hola(ctx):
    await ctx.send(f"!Hola {ctx.author.name}! 👋")

@bot.command()
async def dado(ctx):
    import random
    numero = random.randint(1, 6)
    await ctx.send(f"🎲 Salió el número: {numero}")

@bot.command()
async def info(ctx):
    await ctx.send("Soy un bot de prueba armado con Python y discord.py")

bot.run(TOKEN)
