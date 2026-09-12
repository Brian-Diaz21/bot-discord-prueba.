import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import os
import random
import asyncio
from google import genai
from google.genai import types

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

client_ia = genai.Client(api_key=GEMINI_KEY)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot conectado como {bot.user}")

@bot.event
async def on_member_join(member):
    canal = discord.utils.get(member.guild.text_channels, name="👋-bienvenida")
    if canal:
        await canal.send(
            f"🎉 ¡Bienvenido/a al servidor, {member.mention}!\n\n"
            f"Te invito a probar mis funciones — escribí **/** en el chat "
            f"y vas a ver todos los comandos disponibles: saludos, un dado, "
            f"info del bot, botones interactivos, ¡y hasta podés charlar con una IA! 🤖\n\n"
            f"Dale un vistazo también a #reglas antes de arrancar 👇"
        )

@bot.tree.command(name="hola", description="El bot te saluda")
async def hola(interaction: discord.Interaction):
    await interaction.response.send_message(f"¡Hola {interaction.user.name}! 👋")

@bot.tree.command(name="dado", description="Tira un dado del 1 al 6")
async def dado(interaction: discord.Interaction):
    numero = random.randint(1, 6)
    await interaction.response.send_message(f"🎲 Salió el número: {numero}")

@bot.tree.command(name="info", description="Información sobre el bot")
async def info(interaction: discord.Interaction):
    await interaction.response.send_message("Soy un bot de prueba armado con Python y discord.py")

@bot.tree.command(name="chat", description="Hacele una pregunta a la IA")
@app_commands.describe(mensaje="Qué le querés preguntar al bot")
async def chat(interaction: discord.Interaction, mensaje: str):
    await interaction.response.defer()
    try:
        respuesta = await asyncio.to_thread(
            client_ia.models.generate_content,
            model="gemini-3.6-flash",
            contents=mensaje,
        )
        texto = respuesta.text
        if len(texto) > 2000:
            texto = texto[:1997] + "..."
        await interaction.followup.send(texto)
    except Exception as e:
        print(f"Error en /chat: {e}")
        await interaction.followup.send("⚠️ Uy, no pude responder eso. Probá de nuevo en un momento.")

class MenuView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Saludo", style=discord.ButtonStyle.primary, emoji="👋")
    async def saludo_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"¡Hola {interaction.user.name}! 👋", ephemeral=True)

    @discord.ui.button(label="Tirar dado", style=discord.ButtonStyle.success, emoji="🎲")
    async def dado_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        numero = random.randint(1, 6)
        await interaction.response.send_message(f"🎲 Salió el número: {numero}", ephemeral=True)

    @discord.ui.button(label="Info del bot", style=discord.ButtonStyle.secondary, emoji="ℹ️")
    async def info_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Soy un bot de prueba armado con Python y discord.py", ephemeral=True)

@bot.tree.command(name="menu", description="Muestra un menú con botones")
async def menu(interaction: discord.Interaction):
    view = MenuView()
    await interaction.response.send_message("Elegí una opción:", view=view)

bot.run(TOKEN)
