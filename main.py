import nextcord
import string
import sqlite3
import random
import secrets
import os
import requests
import aiohttp
from nextcord.ext import commands, tasks

intents = nextcord.Intents.default()
intents.guilds = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    learning = nextcord.Game("BTDS BOT")
    await bot.change_presence(status=nextcord.Status.idle, activity=learning)

    for guild in bot.guilds:
        welcome_message = f"Hey there! I'm {bot.user.name}! I'm ready to work in {guild.name}!"

        channel = nextcord.utils.get(guild.channels, name="bdts-bot-testing")

        if channel:
            await channel.send(welcome_message)

# Duck generator
def get_duck_image_url():
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']

@bot.slash_command(name='duck', description="Sends a duck picture")
async def duck(ctx):
    image_url = get_duck_image_url()
    await ctx.send(image_url)

# Dog generator
def get_dog_image_url():
    url = 'https://random.dog/woof.json'
    try:
        res = requests.get(url)
        res.raise_for_status()  # Raise an HTTPError for bad requests
        data = res.json()
        return data['url']
    except requests.RequestException as e:
        print(f"Error getting dog image: {e}")
        return None

@bot.slash_command(name='dog', description="Sends a dog picture")
async def dog(ctx):
    image_url = get_dog_image_url()
    try:
        await ctx.send(image_url)
    except nextcord.errors.NotFound as e:
        print(f"Error sending dog image: {e}")

# CAT GENERATOR
def get_cat_image_url():
    url = 'https://api.thecatapi.com/v1/images/search'
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        return data[0]['url']  # Assuming the response is a list
    except requests.RequestException as e:
        print(f"Error getting cat image: {e}")
        return None

@bot.slash_command(name='cat', description="Sends a cat picture")
async def cat(ctx):
    image_url = get_cat_image_url()
    if image_url:
        await ctx.send(image_url)
    else:
        await ctx.send("Failed to fetch cat image.")


# Animal command
@bot.slash_command(name='animals', description="Sends you a random animal.")
async def animals(ctx):
    animals_folder = "image"
    animals = [f for f in os.listdir(animals_folder) if os.path.isfile(os.path.join(animals_folder, f))]

    if animals:
        random_animals = os.path.join(animals_folder, random.choice(animals))
        with open(random_animals, 'rb') as f:
            picture = nextcord.File(f)
        await ctx.send(file=picture)
    else:
        await ctx.send("No animal found.")

# Math commands
@bot.slash_command(name="calculator", description="Perform arithmetic operations")
async def calculator(ctx, operation: str, num1: float, num2: float):
    try:
        if operation.lower() == "add":
            result = num1 + num2
            operator = "+"
        elif operation.lower() == "multiply":
            result = num1 * num2
            operator = "*"
        elif operation.lower() == "subtract":
            result = num1 - num2
            operator = "-"
        elif operation.lower() == "divide":
            if num2 == 0:
                raise ValueError("Cannot divide by zero")
            result = num1 / num2
            operator = "/"
        else:
            raise ValueError("Invalid operation. Please choose 'add', 'multiply', 'subtract', or 'divide'.")

        embed = nextcord.Embed(
            title=f"Arithmetic Operation",
            description=f"Performing {num1} {operator} {num2}",
            color=0x3498db
        )
        embed.add_field(name="Result", value=str(result), inline=False)
        embed.set_footer(text=f"Requested by {ctx.user.display_name}", icon_url=ctx.user.avatar.url)

        await ctx.send(embed=embed)
    except ValueError as ve:
        await ctx.send(f'Error: {str(ve)}')
    except Exception as e:
        await ctx.send(f'Error: {str(e)}')

# Random commands
# Adding roles
@bot.slash_command(name="add_roles", description="Add a role to yourself")
async def add_roles(ctx, role: nextcord.Role = None):
    if role is None:
        await ctx.send("You need to choose your role")
        return
    await ctx.user.add_roles(role)
    await ctx.send(f'Role {role.name} has been successfully assigned!')

# Removing roles
@bot.slash_command(name="remove_roles", description="Remove a role from yourself")
async def remove_roles(ctx, role: nextcord.Role = None):
    if role is None:
        await ctx.send("You need to choose a role")
        return
    await ctx.user.remove_roles(role)
    await ctx.send(f'Role {role.name} has been successfully removed!')


# Games and entertainment
# Password
@bot.slash_command(name='password', description='Generate a random password')
async def password(ctx):
    password = secrets.token_hex(10)
    await ctx.send(f'Your random password: {password}')
    embed = nextcord.Embed(title = "Password", description = f"Your generated password ", color = "f0000")
    await ctx.send(embed=embed)

# Coin flip
@bot.slash_command(name="coin_flip", description="Flip a coin")
async def coin_flip(ctx):
    result = random.choice(['Heads', 'Tails'])
    embed = nextcord.Embed(title="Coin Flip", color=0x7289da)
    embed.add_field(name="Result:", value=result)
    await ctx.send(embed=embed)

# Ping
@bot.slash_command(name="ping", description="Check your ping")
async def ping(ctx):
    ping = round(bot.latency * 1000)
    embed = nextcord.Embed(title = "Ping", description = f"Your ping is: {ping}", color = 0x7289da)
    await ctx.send(embed=embed)

    
# Avatar
@bot.slash_command(name='avatar', description="Show your or someone else's avatar")
async def avatar(ctx, user: nextcord.Member = None):
    if user is None:
        user = ctx.user
    embed = nextcord.Embed(title=f'{user.name}\'s Avatar', color=0x7289da).set_image(url=user.avatar.url)
    await ctx.send(embed=embed)

# User info
@bot.slash_command(name="userinfo", description="Display user information")
async def userinfo(ctx, user: nextcord.User = None):
    user = user or ctx.user
    created_at = user.created_at.strftime("%Y-%m-%d %H:%M:%S")
    joined_at = user.joined_at.strftime("%Y-%m-%d %H:%M:%S") if user.joined_at else "Not available"

    embed = nextcord.Embed(title=f"{user.name}#{user.discriminator}", description=f"User Information for {user.mention}", color=0x7289da)
    embed.set_thumbnail(url=user.avatar.url)
    embed.add_field(name="User ID", value=user.id, inline=False)
    embed.add_field(name="Account Created", value=created_at, inline=False)
    embed.add_field(name="Joined Server", value=joined_at, inline=False)
    
    await ctx.send(embed=embed)


# 



# Converting text to ASCII code
@bot.slash_command(name='ascii', description="Converts text to ASCII")
async def ascii(ctx, *, text: str):
    ascii_text = ' '.join(str(ord(char)) for char in text)
    embed = nextcord.Embed(title="ASCII code", description=f"Here is your transaltion of {text}: {ascii_text}", color=0x7289da)
    await ctx.send(embed=embed)

# additional commands
# random color 
@bot.slash_command(name="random_color", description="Generate a random color")
async def random_color(ctx):
    color = '%06x' % random.randint(0, 0xFFFFFF)
    embed = nextcord.Embed(title="Random color", description=f"Here is random color balance: {color}", color=0x7289da)
    await ctx.send(embed=embed)

                            #NEW CREATTED COMMANDS
@bot.slash_command(name = "truth_or_dare", description = 'Plays a game Truth or Dare with you.')
async def truth_or_dare(ctx, your_choice: str):
    user = ctx.user.name
    truth1 = [f"{user}'s last lie: When was the last time you lied?", 
             f"{user}'s work misdeed: What is the worst thing you have ever done at work?", 
             f"{user}'s crying game: When was the last time you cried?", 
             f"{user}'s fear factor: What is your biggest fear?", 
             f"{user}'s fantasy world: What is your biggest fantasy?", 
             f"{user}'s discord search: Who is the last person you searched on discord?"
             ]
    dare2 = [f"{user}'s dirty secret: Read out the last dirty text you sent.", 
             f"{user}'s condiment challenge: Eat five spoonfuls of a condiment of your choice", 
             f"{user}'s juggling act: Try to juggle 3 things of the group's choice.", 
             f"{user}'s food item impersonation: Pretend to be a food item of your choice.", 
             f"{user}'s embarrassing moment: Show the most embarrassing photo on your phone.", 
             f"{user}'s text history: Show the last five people you texted and what the messages said."
             ]
    if your_choice.lower() == 'truth':
        choice = random.choice(truth1)
        embed = nextcord.Embed(title="Truth", description=choice, color=0x7289da)
        await ctx.send(embed=embed)

    elif your_choice.lower() == 'dare':
        choice2 = random.choice(dare2)
        embed = nextcord.Embed(title="Dare", description=choice2, color=0x7289da)
        await ctx.send(embed=embed)
    else:
        embed = nextcord.Embed(title="Invalid Choice", description=f'{user} type "truth" or "dare" to play the game', color=0x7289da)
        await ctx.send(embed=embed)


#FAKE PASSPORT 
@bot.slash_command(name="fake_passport", description="Creates you a fake passport")
async def fake_passport(ctx, your_name: str, your_surname: str, your_year: int, your_age: int, your_country: str,):

    embed = nextcord.Embed(title="Fake passport", description=f"User Information for {your_name}", color=0x7289da)
    embed.set_thumbnail(url=ctx.user.avatar.url)
    embed.add_field(name="Name:", value=your_name, inline=False)
    embed.add_field(name="Surname:", value=your_surname, inline=False)
    embed.add_field(name="Year of birth:", value=your_year, inline=False)
    embed.add_field(name="Age:", value=your_age, inline=False)
    embed.add_field(name="Country:", value=your_country, inline=False)
    await ctx.send(embed=embed)
                            
# FAKE DONATE COMMAND
       
#hi
@bot.slash_command(name = "hi", description = "Greets you")
async def hi(ctx, your_mood = str):
    user = ctx.user.name
    if your_mood.lower() == "good" or "хорошое" or "great" or "bien" or "excelent" or "very well":
        embed = nextcord.Embed(title = "Your mood", description=f"It seems like {user} is at {your_mood} mood! Well done!", color = 0x7289da)
        await ctx.send(embed=embed)
    elif your_mood.lower() == "нормальное" or "well" or "normal":
        embed = nextcord.Embed(title = "Your mood", description=f"It seems like you mood is at {your_mood} mood .{user}! make it great", color = 0x7289da)
        await ctx.send(embed=embed)
    else:
        embed = nextcord.Embed(title = "Your mood", description=f"It seems like you mood is at {your_mood} mood .{user}! make it great", color =0x7289da)
        await ctx.send(embed=embed)

#DONATE
@bot.slash_command(name="donate", description="Creates a fake donate and demands you to become a philanthropist")
async def donate(ctx, сумма: float):
    user = ctx.user.name
    if сумма >= 1000:
        embed = nextcord.Embed(title = "Your donate", description=f'Внимание! {user} официально стал филантропом! Спасибо за щедрое пожертвование в размере {сумма}$!', color =0x7289da)
        await ctx.send(embed=embed)
    elif сумма >= 100:
        embed = nextcord.Embed(title = "Your donate", description=f'Спасибо, {user}, за донат в размере {сумма}$! Ты крутой!', color =0x7289da)
        await ctx.send(embed=embed)
    elif сумма <= 100:
        embed = nextcord.Embed(title = "Your donate", description=f'Спасибо за ваше пожертвование, {user}! Ваш вклад в размере {сумма}$ ценится.', color =0x7289da)
        await ctx.send(embed=embed)
    else:
        embed = nextcord.Embed(title = "Your donate", description="Пожалуйста, введите положительную сумму для пожертвования.", color =0x7289da)
        await ctx.send(embed=embed)

#SET AVATAR COMMAND
@bot.slash_command(name='set_avatar', description='Set an animated avatar for the bot')
async def set_avatar(ctx, avatar_url: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(avatar_url) as resp:
                if resp.status == 200:
                    avatar_image = await resp.read()
                    await bot.user.edit(avatar=avatar_image)
                    await ctx.send("Avatar changed successfully.")
                else:
                    await ctx.send(f"Failed to fetch avatar. Status code: {resp.status}")
    except Exception as e:
        embed = nextcord.Embed(title = "Error with setting avatar", description=f"Error changing avatar: {e}", color =0x7289da)
        await ctx.send(embed=embed)

#ECOLOGY MEME GENERATOR (in prosess of developing)
@bot.slash_command(name='random_memes', description="Sends you a random ecology meme.")
async def random_memes(ctx):
    meme_folder = "images"
    meme = [f for f in os.listdir(meme_folder) if os.path.isfile(os.path.join(meme_folder, f))]

    if meme:
        random_meme = os.path.join(meme_folder, random.choice(meme))
        with open(random_meme, 'rb') as f:
            picture = nextcord.File(f)
        await ctx.send(file=picture)
    else:
        await ctx.send("No meme found.")

# calculations
@bot.slash_command(name = "suggest", description="Gets you a random suggestion!")
async def suggest(ctx):
    user = ctx.user.name  
    suggests = [
        f'{user}, live by the mantra - Reduce, Reuse, and Recycle.',
        f'{user}, keep our surroundings clean.',
        f'{user}, plant more trees.',
        f'{user}, conserve water and water bodies.',
        f'{user}, educate people about the significance of conserving nature.',
        f'{user}, cycle more and drive fewer cars on the road.'
    ]
    suggestion = random.choice(suggests) 
    embed = nextcord.Embed(title = "Random Suggest", description = f"{suggestion}", color = 0x7289da) 
    await ctx.send(embed=embed)

#FAKE BANKCARD GENERATOR
@bot.slash_command(name="bankcard_generator", description="Creates you a fake cart")
async def bankcard_generator(ctx, type_of_cart: str, your_name: str, number_of_cart: int, date: int, pin_code: int):
    if pin_code == 4:
        await ctx.send("Here you are!") 
    else:
        await ctx.send("You need to type 4(****) random digits")
    if number_of_cart == 16:
        await ctx.send("Here you are!")
    else:
        await ctx.send("Write 16 random digits in number of you cart!")

    embed = nextcord.Embed(title="Fake Bankcart", description=f"Bankcard for {your_name}", color=0x7289da)
    embed.set_thumbnail(url=ctx.user.avatar.url)
    embed.add_field(name="Type of card:", value=type_of_cart, inline=False)
    embed.add_field(name="Number of card:", value=number_of_cart, inline=False)
    embed.add_field(name="Date of cart:", value=date, inline=False)
    embed.add_field(name="Owner:", value=your_name, inline=False)
    embed.add_field(name="Pin code:", value=pin_code, inline=False)
    await ctx.send(embed=embed)

#gifhub command 
@bot.slash_command(name = "github", description = 'Provides information about a GitHub user.')
async def github(ctx, user: str):
    user_info_url = f"https://api.github.com/users/{user}"
    response = requests.get(user_info_url)
    user_info = response.json()
    avatar_url = user_info['avatar_url']
    embed = nextcord.Embed(title=f"{user_info['name']}'s GitHub Profile", color=0x7289da, url=user_info['html_url'])
    embed.set_thumbnail(url=avatar_url)
    embed.add_field(name="Bio", value=user_info["bio"], inline=False)
    embed.add_field(name="Public Repositories", value=user_info["public_repos"], inline=True)
    await ctx.send(embed=embed)

bot.run(Write_your_token here)
