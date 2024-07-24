import os
import discord
from random import randint
from dotenv import load_dotenv
from discord import Intents, Client, app_commands
from response import get_response
from TicTacToe import *

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


@tree.command(name="randnum", description="Generate a random number")
@app_commands.describe(minimum="Minimum Value", maximum="Maximum Value")
async def random_number(interaction, minimum: int, maximum: int):
    await interaction.response.send_message(f'Number: {randint(minimum, maximum)}')


@tree.command(name="tictactoe", description="Play Tic Tac Toe")
@app_commands.describe(mode="Enter 'cpu' to play against the computer")
async def tic_tac_toe(interaction, mode: str = 'player'):
    view = TicTacToeView(playing_computer=(mode.lower() == 'cpu'))
    await interaction.response.send_message("Tic Tac Toe: X starts", view=view)


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
