import discord
from discord.ext import commands
import aiohttp

# Configuration du bot
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

DEVELOPPEUR = "El Fumadero"
MINOTAR_API_URL = 'https://minotar.net/'

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user.name} (Développé par {DEVELOPPEUR})')

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"Pong! (Développé par {DEVELOPPEUR})")

@bot.command(name="credits")
async def credits(ctx):
    await ctx.send(f"Ce bot a été développé par {DEVELOPPEUR}.")

@bot.command(name="aide")
async def aide(ctx):
    embed = discord.Embed(title="Commandes du Bot", description="Voici la liste des commandes disponibles:")
    embed.add_field(name="!ping", value="Vérifie si le bot est en ligne", inline=False)
    embed.add_field(name="!credits", value="Affiche le nom du développeur", inline=False)
    embed.add_field(name="!skin (pseudo Minecraft)", value="Affiche les détails du skin Minecraft d'un joueur", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="skin")
async def skin(ctx, pseudo):
    try:
        async with aiohttp.ClientSession() as session:
            # Récupération de l'image complète du skin
            async with session.get(f'{MINOTAR_API_URL}/skin/{pseudo}') as response:
                if response.status != 200:
                    await ctx.send(f"Erreur lors de la récupération du skin pour {pseudo}. Statut HTTP: {response.status}")
                    return
                skin_data = await response.read()

            # Construction de l'URL de téléchargement
            download_url = f'{MINOTAR_API_URL}/skin/{pseudo}.png'

            # Construction de l'embed Discord avec les données récupérées
            embed = discord.Embed(title=f"Skin de {pseudo}")
            embed.set_image(url=f'{MINOTAR_API_URL}/skin/{pseudo}?scale=4')  # Zoom x4
            embed.set_footer(text=f"Développé par {DEVELOPPEUR}")

            if skin_data:
                embed.add_field(name="Détails du Skin", value=f"Taille: {len(skin_data)} octets")

            # Ajout du lien de téléchargement
            embed.add_field(name="Télécharger", value=f"[Télécharger le skin PNG]({download_url})")

            await ctx.send(embed=embed)

    except aiohttp.ClientError as e:
        print(f'Erreur HTTP lors de la récupération du skin pour {pseudo}: {e}')
        await ctx.send(f'Erreur lors de la récupération du skin pour {pseudo}. Vérifiez votre connexion Internet.')

    except Exception as e:
        print(f'Erreur inattendue lors de la récupération du skin pour {pseudo}: {e}')
        await ctx.send(f'Erreur inattendue lors de la récupération du skin pour {pseudo}.')

# Token du bot
bot.run('TOKEN_DU_BOT')
