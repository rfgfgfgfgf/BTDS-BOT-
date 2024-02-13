import nextcord
import string
import random
import secrets
import os
import requests
from nextcord.ext import commands

intents = nextcord.Intents.default()
intents.guilds = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

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
    res = requests.get(url)
    data = res.json()
    return data['url']

@bot.slash_command(name='dog', description="Sends a dog picture")
async def dog(ctx):
    image_url = get_dog_image_url()
    await ctx.send(image_url)

#CAT GENERATOR
def get_cat_image_url():
    url = 'https://api.thecatapi.com/v1/images/search'
    res = requests.get(url)
    data = res.json()
    return data[0].get('url', '')

@bot.slash_command(name='cat', description="Sends a cat picture")
async def cat(ctx):
    image_url = get_cat_image_url()

    if image_url:
        await ctx.send(image_url)
    else:
        await ctx.send("Unable to fetch cat picture. Please try again later.")


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
# Addition
@bot.slash_command(name="add", description="Add two numbers")
async def add(ctx, a: float, b: float):
    try:
        sum_result = a + b
        await ctx.send(f'The sum of {a} and {b} is: {sum_result}')
    except Exception as e:
        await ctx.send(f'Error: {str(e)}')

# Multiplication
@bot.slash_command(name="multiply", description="Multiply two numbers")
async def multiply(ctx, a: float, b: float):
    try:
        product = a * b
        await ctx.send(f"The product of {a} and {b} is: {product}")
    except Exception as e:
        await ctx.send(f'Error: {str(e)}')

# Difference
@bot.slash_command(name="subtract", description="Subtract two numbers")
async def subtract(ctx, a: float, b: float):
    try:
        difference = a - b
        await ctx.send(f"The difference of {a} and {b} is: {difference}")
    except Exception as e:
        await ctx.send(f'Error: {str(e)}')

# Division
@bot.slash_command(name="divide", description="Divide two numbers")
async def divide(ctx, num1: float, num2: float):
    try:
        if num2 == 0:
            raise ValueError("Cannot divide by zero")
        result = num1 / num2
        await ctx.send(f'The result of dividing {num1} by {num2} is {result}')
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

# Coin flip
@bot.slash_command(name="coin_flip", description="Flip a coin")
async def coin_flip(ctx):
    result = random.choice(['Heads', 'Tails'])
    await ctx.send(f'Coin flip result: {result}')

# Ping
@bot.slash_command(name="ping", description="Check your ping")
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f'Your ping is: {latency} ms')

# Avatar
@bot.slash_command(name='avatar', description="Show your or someone else's avatar")
async def avatar(ctx, user: nextcord.Member = None):
    if user is None:
        user = ctx.author
    embed = nextcord.Embed(title=f'{user.name}\'s Avatar', color=0xe74c3c).set_image(url=user.avatar.url)
    await ctx.send(embed=embed)

# User info
@bot.slash_command(name='user_info', description="Show information about yourself or someone else")
async def user_info(ctx, user: nextcord.Member = None):
    user = user or ctx.author
    created_at = user.created_at.strftime('%Y-%m-%d %H:%M:%S')
    joined_at = user.joined_at.strftime('%Y-%m-%d %H:%M:%S')
    await ctx.send(f'User information {user.name}:\n'
                   f'ID: {user.id}\n'
                   f'Created: {created_at}\n'
                   f'Joined: {joined_at}')

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
    await ctx.send(f"Encrypted text: {encrypted_text}")

# Converting text to ASCII code
@bot.slash_command(name='ascii', description="Converts text to ASCII")
async def ascii(ctx, *, text: str):
    ascii_text = ' '.join(str(ord(char)) for char in text)
    await ctx.send(f"ASCII representation of '{text}': {ascii_text}")

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
    await ctx.send(f"Text in Morse Code: {morse_text}")

            # additional commands
# random color 
@bot.slash_command(name="random_color", description="Generate a random color")
async def random_color(ctx):
    color = '%06x' % random.randint(0, 0xFFFFFF)
    await ctx.send(f"Random color: #{color}")

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
        await ctx.send("Unable to fetch weather information. Please check the location or try again later.")
