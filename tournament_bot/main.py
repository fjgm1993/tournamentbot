
from discord.ext import commands
import discord
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

players = []
matches = []
current_round = []
bracket_started = False

@bot.event
async def on_ready():
    print(f"Bot activo como {bot.user}")

@bot.command()
async def registrar(ctx):
    if bracket_started:
        await ctx.send("🚫 El torneo ya comenzó, no puedes registrarte.")
        return
    if ctx.author not in players:
        players.append(ctx.author)
        await ctx.send(f"✅ {ctx.author.display_name} ha sido registrado.")
    else:
        await ctx.send("⚠️ Ya estás registrado.")

@bot.command()
async def lista(ctx):
    if not players:
        await ctx.send("No hay jugadores registrados todavía.")
        return
    message = "📋 Jugadores registrados:
"
    for p in players:
        message += f"- {p.display_name}
"
    await ctx.send(message)

@bot.command()
async def iniciar(ctx):
    global matches, current_round, bracket_started
    if bracket_started:
        await ctx.send("🚫 El torneo ya está en curso.")
        return
    if len(players) < 2:
        await ctx.send("❗ Se necesitan al menos 2 jugadores.")
        return
    bracket_started = True
    current_round = list(players)
    matches = list(zip(current_round[::2], current_round[1::2]))
    await ctx.send("🏁 ¡Torneo iniciado!")
    for p1, p2 in matches:
        await ctx.send(f"🆚 {p1.display_name} vs {p2.display_name}")

@bot.command()
async def reportar(ctx, opponent: discord.Member, resultado: str):
    global current_round, matches
    if not bracket_started:
        await ctx.send("🚫 No hay torneo en curso.")
        return
    match = next(((p1, p2) for p1, p2 in matches if ctx.author in (p1, p2) and opponent in (p1, p2)), None)
    if not match:
        await ctx.send("❌ No estás en un emparejamiento activo con ese jugador.")
        return
    winner = ctx.author if resultado.lower() == "victoria" else opponent
    await ctx.send(f"🏆 {winner.display_name} gana el enfrentamiento.")
    current_round = [p for p in current_round if p not in match]
    current_round.append(winner)
    matches = list(zip(current_round[::2], current_round[1::2]))
    if len(current_round) == 1:
        await ctx.send(f"🎉 ¡{winner.display_name} es el campeón del torneo!")
        reset_tournament()
    else:
        await ctx.send("🔁 Nueva ronda:")
        for p1, p2 in matches:
            await ctx.send(f"🆚 {p1.display_name} vs {p2.display_name}")

def reset_tournament():
    global players, matches, current_round, bracket_started
    players = []
    matches = []
    current_round = []
    bracket_started = False

bot.run(os.getenv("TOKEN"))
