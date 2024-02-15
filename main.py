import nextcord
import string
import sqlite3
import random
import secrets
import os
import requests
from nextcord.ext import commands

intents = nextcord.Intents.default()
intents.guilds = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

money = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    game = nextcord.Game("BTDS BOT")
    await bot.change_presence(status=nextcord.Status.online, activity=game)

    for guild in bot.guilds:
        welcome_message = f"Hey there! I'm {bot.user.name}! I'm ready to work in {guild.name}!"

        channel = nextcord.utils.get(guild.channels, name="test")

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

        # Create a beautiful embed to display the result
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
    embed = nextcord.Embed(title="Coin Flip", color=0xe74c3c)
    embed.add_field(name="Result:", value=result)
    await ctx.send(embed=embed)

# Ping
@bot.slash_command(name="ping", description="Check your ping")
async def ping(ctx):
    ping = round(bot.latency * 1000)
    embed = nextcord.Embed(title = "Ping", description = f"Your ping is: {ping}")
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


# Caesar cipher
@bot.slash_command(name="caesar_cipher", description="Encrypt text using the Caesar cipher")
async def caesar_cipher(ctx, shift: int, *, text: str):
    if not (1 <= shift <= 25):
        await ctx.send("Please choose a shift between 1 and 25.")
        return

    def caesar(text, shift):
        result = ""
        for char in text:
            if char.isalpha():
                start = ord('A') if char.isupper() else ord('a')
                result += chr((ord(char) - start + shift) % 26 + start)
            else:
                result += char
        return result

    encrypted_text = caesar(text, shift)
    embed = nextcord.Embed(title="Caesar code", description=f"Here is your transaltion of {text}: {encrypted_text}", color=0x7289da)
    await ctx.send(embed=embed)

# Converting text to ASCII code
@bot.slash_command(name='ascii', description="Converts text to ASCII")
async def ascii(ctx, *, text: str):
    ascii_text = ' '.join(str(ord(char)) for char in text)
    embed = nextcord.Embed(title="ASCII code", description=f"Here is your transaltion of {text}: {ascii_text}", color=0x7289da)
    await ctx.send(embed=embed)

# Morse code
morse_code_dict = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
    'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
    'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.', '!': '-.-.--', '/': '-..-.',
    '(': '-.--.', ')': '-.--.-', '&': '.-...', ':': '---...', ';': '-.-.-.', '=': '-...-',
    '+': '.-.-.', '-': '-....-', '_': '..--.-', '"': '.-..-.', '$': '...-..-', '@': '.--.-.'
}
@bot.slash_command(name="morse_code", description="Convert text to Morse code")
async def morse_code(ctx, *, text: str):
    def text_to_morse(text):
        morse_result = ""
        for char in text.upper():
            if char.isalpha() or char.isdigit() or char in morse_code_dict:
                morse_result += morse_code_dict[char] + ' '
            else:
                morse_result += ' '
        return morse_result.strip()

    morse_text = text_to_morse(text)
    embed = nextcord.Embed(title="Morse code", description=f"Here is your translation into Morse code: {morse_text}", color=0x7289da)
    await ctx.send(embed=embed)

            # additional commands
# random color 
@bot.slash_command(name="random_color", description="Generate a random color")
async def random_color(ctx):
    color = '%06x' % random.randint(0, 0xFFFFFF)
    embed = nextcord.Embed(title="Random color", description=f"Here is random color balance: {color}", color=0x7289da)
    await ctx.send(embed=embed)

        #WEATHER (в разработке)
@bot.slash_command(name="weather", description="Get the current weather for a location")
async def weather(ctx, city: str, country_code: str = ""):
    api_key = "YOUR_OPENWEATHERMAP_API_KEY"
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    params = {
        "q": f"{city},{country_code}",
        "appid": api_key,
        "units": "metric"  
    }

    response = requests.get(base_url, params=params)
    weather_data = response.json()

    if response.status_code == 200:
        temperature = weather_data["main"]["temp"]
        description = weather_data["weather"][0]["description"]
        await ctx.send(f"Current weather in {city}, {country_code}:\nTemperature: {temperature}°C\nDescription: {description}")
    else:
        await ctx.send("Unable to fetch weather information.")


            # FINANSE COMMANDS OF BTDS
        
@bot.slash_command(name='balance', description="Check your balance")
async def balance(ctx):
    user_id = str(ctx.user.id)
    balance = money.get(user_id, 0)
    embed = nextcord.Embed(title="Balance", description=f"Here is your balance: {balance}", color=0x7289da)
    await ctx.send(embed=embed)

@bot.slash_command(name='work', description="Earn some money")
async def work(ctx):
    user_id = str(ctx.user.id)
    earnings = random.randint(10, 30)
    
    if user_id in money:
        money[user_id] += earnings
    else:
        money[user_id] = earnings
    embed = nextcord.Embed(title="Income", description=f"Here is your income: {earnings}", color=0x7289da)
    await ctx.send(embed=embed)

#LEVEL OF USER AND MEMBERS OF SERVER
conn = sqlite3.connect('level.db')
c = conn.cursor()

# Создание таблицы, если она не существует
c.execute('''
          CREATE TABLE IF NOT EXISTS users (
              user_id INTEGER PRIMARY KEY,
              level INTEGER DEFAULT 1
          )
          ''')
conn.commit()

@bot.event
async def on_message(message):
    # Обработка сообщений для увеличения опыта и уровня
    if message.user.bot:
        return

    user_id = message.user.id
    c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user_data = c.fetchone()

    if user_data is None:
        c.execute('INSERT INTO users (user_id) VALUES (?)', (user_id,))
        conn.commit()
        user_data = (user_id, 1)

    # Увеличение опыта пользователя
    new_level = user_data[1] + 1
    c.execute('UPDATE users SET level = ? WHERE user_id = ?', (new_level, user_id))
    conn.commit()

    await bot.process_commands(message)

#LEVEL RANG
@bot.slash_command(name='level', description="Shows your level")
async def level(ctx):
    user_id = ctx.user.id
    c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user_data = c.fetchone()

    if user_data is not None:
        level = user_data[1]
        await ctx.send(f"Your level is {level}")
        embed = nextcord.embed(title = "Level", description = f"Your level is {level}!")
        await ctx.send(embed=embed)
    else:
        embed = nextcord.embed(title = "Level", description = "You haven't earned any levels yet")
        await ctx.send(embed=embed)
