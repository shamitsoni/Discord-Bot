import os
from random import randint
from dotenv import load_dotenv
from discord import Intents, Client, app_commands
from response import get_response

# Load token
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Setup
intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)
tree = app_commands.CommandTree(client)


# Send message to user
async def send_message(message: str, user_message: str) -> None:
    if not user_message:
        print('Empty message')
        return
    try:
        response = get_response(user_message)
        await message.channel.send(response)
    except Exception as e:
        print(e)


# Bot commands
@tree.command(name="coinflip", description="Flip a coin")
async def coin_flip(interaction):
    await interaction.response.send_message('Heads' if randint(0, 1) == 0 else 'Tails')


@tree.command(name="roll", description="Roll a 6-sided die")
async def roll_dice(interaction):
    await interaction.response.send_message(f'Rolled: {randint(1, 6)}')


# Startup
@client.event
async def on_ready() -> None:
    await tree.sync()  # Sync bot commands
    print(f'{client.user} is now running!')


# Retrieve user message
@client.event
async def on_message(message) -> None:
    if message.author == client.user:
        return

    username = str(message.author)
    user_message = message.content
    channel = str(message.channel)

    print(f'{[channel]} {username}: {user_message}')
    await send_message(message, user_message)


def main() -> None:
    client.run(token=TOKEN)


if __name__ == '__main__':
    main()
