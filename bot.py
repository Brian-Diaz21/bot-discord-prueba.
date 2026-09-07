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
class MenuView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Saludo", style=discord.ButtonStyle.primary, emoji="👋")
    async def saludo_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"¡Hola {interaction.user.name}! 👋", ephemeral=True)

    @discord.ui.button(label="Tirar dado", style=discord.ButtonStyle.success, emoji="🎲")
    async def dado_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        import random
        numero = random.randint(1, 6)
        await interaction.response.send_message(f"🎲 Salió el número: {numero}", ephemeral=True)

    @discord.ui.button(label="Info del bot", style=discord.ButtonStyle.secondary, emoji="ℹ️")
    async def info_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Soy un bot de prueba armado con Python y discord.py", ephemeral=True)

@bot.command()
async def menu(ctx):
    view = MenuView()
    await ctx.send("Elegí una opción:", view=view)
bot.run(TOKEN)
