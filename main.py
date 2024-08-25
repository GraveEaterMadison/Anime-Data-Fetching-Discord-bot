import discord
from discord.ext import commands
import aiohttp
import html2text
import random

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)  # Disable the default help command

TOKEN='Your_discord_bot_token'

ANILIST_URL = 'https://graphql.anilist.co'

FUNNY_ANIME_LINES = [
    "Believe it! - Naruto Uzumaki",
    "I'm not a pervert, I'm a super pervert! - Jiraiya",
    "I am gonna be King of the Pirates! - Monkey D. Luffy",
    "You can't spell slaughter without laughter. - Rintarou Okabe",
    "I am not a cat, I am a nekomimi. - Azusa Nakano",
    "In the name of the moon, I will punish you! - Usagi Tsukino",
    "Just because you’re correct doesn’t mean you’re right. - Shirou Emiya",
    "I am Justice! - Light Yagami",
    "Bang! - Spike Spiegel",
    "I love the kind of woman that can kick my ass. - Spike Spiegel",
    "The world isn’t perfect. But it’s there for us, doing the best it can. That’s what makes it so damn beautiful. - Roy Mustang"
]


async def fetch_anilist_info(query, variables):
    async with aiohttp.ClientSession() as session:
        async with session.post(ANILIST_URL, json={'query': query, 'variables': variables}) as response:
            if response.status != 200:
                print(f"Failed to fetch data from AniList: {response.status}")
                return None
            return await response.json()


async def fetch_image(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                print(f"Failed to fetch image: {response.status}")
                return None
            return await response.read()


@bot.command(description="Fetches information about an anime.")
async def anime(ctx, *, title=None):
    if title is None:
        await ctx.send("Please provide the title of the anime. Usage: `!anime <title>`")
        return

    query = '''
        query ($search: String) {
            Media(search: $search, type: ANIME) {
                title {
                    romaji
                    english
                    native
                }
                description
                episodes
                status
                averageScore
                coverImage {
                    large
                }
            }
        }
    '''
    variables = {'search': title}
    data = await fetch_anilist_info(query, variables)
    anime_info = data.get('data', {}).get('Media', None)

    if anime_info:
        description = html2text.html2text(anime_info['description'])

        # Fetch image from URL
        image_data = await fetch_image(anime_info['coverImage']['large'])
        
        if image_data:
            embed = discord.Embed(
                title=f"Anime Info: {anime_info['title']['romaji']}",
                description=description,
                color=discord.Color.blue()
            )
            embed.add_field(name="English Title", value=anime_info['title']['english'], inline=True)
            embed.add_field(name="Native Title", value=anime_info['title']['native'], inline=True)
            embed.add_field(name="Episodes", value=anime_info['episodes'], inline=True)
            embed.add_field(name="Status", value=anime_info['status'], inline=True)
            embed.add_field(name="Average Score", value=anime_info['averageScore'], inline=True)
            embed.set_image(url=anime_info['coverImage']['large'])

            # Add a funny anime line
            funny_line = random.choice(FUNNY_ANIME_LINES)
            embed.set_footer(text=funny_line)

            try:
                await ctx.send(embed=embed)
            except Exception as e:
                print(f"An error occurred while sending the anime image: {e}")
                await ctx.send("An error occurred while fetching or sending the anime image.")
        else:
            await ctx.send("An error occurred while fetching the anime image.")
    else:
        await ctx.send("Anime not found or an error occurred.")


@bot.command(description="Fetches information about a manga.")
async def manga(ctx, *, title=None):
    if title is None:
        await ctx.send("Please provide the title of the manga. Usage: `!manga <title>`")
        return

    query = '''
        query ($search: String) {
            Media(search: $search, type: MANGA) {
                title {
                    romaji
                    english
                    native
                }
                description
                chapters
                status
                averageScore
                coverImage {
                    large
                }
            }
        }
    '''
    variables = {'search': title}
    data = await fetch_anilist_info(query, variables)
    manga_info = data.get('data', {}).get('Media', None)

    if manga_info:
        description = html2text.html2text(manga_info['description'])

        image_data = await fetch_image(manga_info['coverImage']['large'])
        
        if image_data:
            embed = discord.Embed(
                title=f"Manga Info: {manga_info['title']['romaji']}",
                description=description,
                color=discord.Color.green()
            )
            embed.add_field(name="English Title", value=manga_info['title']['english'], inline=True)
            embed.add_field(name="Native Title", value=manga_info['title']['native'], inline=True)
            embed.add_field(name="Chapters", value=manga_info['chapters'], inline=True)
            embed.add_field(name="Status", value=manga_info['status'], inline=True)
            embed.add_field(name="Average Score", value=manga_info['averageScore'], inline=True)
            embed.set_image(url=manga_info['coverImage']['large'])

            funny_line = random.choice(FUNNY_ANIME_LINES)
            embed.set_footer(text=funny_line)

            try:
                await ctx.send(embed=embed)
            except Exception as e:
                print(f"An error occurred while sending the manga image: {e}")
                await ctx.send("An error occurred while fetching or sending the manga image.")
        else:
            await ctx.send("An error occurred while fetching the manga image.")
    else:
        await ctx.send("Manga not found or an error occurred.")

@bot.command(description="Fetches information about a character.")
async def character(ctx, *, name=None):
    if name is None:
        await ctx.send("Please provide the name of the character. Usage: `!character <name>`")
        return

    query = '''
        query ($search: String) {
            Character(search: $search) {
                name {
                    full
                    native
                }
                description
                image {
                    large
                }
            }
        }
    '''
    variables = {'search': name}
    data = await fetch_anilist_info(query, variables)
    character_info = data.get('data', {}).get('Character', None)

    if character_info:
        description = html2text.html2text(character_info['description'])

        image_data = await fetch_image(character_info['image']['large'])
        
        if image_data:
            embed = discord.Embed(
                title=f"Character Info: {character_info['name']['full']}",
                description=description,
                color=discord.Color.purple()
            )
            embed.add_field(name="Native Name", value=character_info['name']['native'], inline=True)
            embed.set_image(url=character_info['image']['large'])

            funny_line = random.choice(FUNNY_ANIME_LINES)
            embed.set_footer(text=funny_line)

            try:
                await ctx.send(embed=embed)
            except Exception as e:
                print(f"An error occurred while sending the character image: {e}")
                await ctx.send("An error occurred while fetching or sending the character image.")
        else:
            await ctx.send("An error occurred while fetching the character image.")
    else:
        await ctx.send("Character not found or an error occurred.")


@bot.command(name='help', description="Displays a list of available commands and their descriptions.")
async def custom_help(ctx):
    embed = discord.Embed(
        title="Help",
        description="List of available commands:",
        color=discord.Color.gold()
    )
    for command in bot.commands:
        embed.add_field(name=f'!{command.name}', value=command.description, inline=False)
    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

bot.run(TOKEN)
