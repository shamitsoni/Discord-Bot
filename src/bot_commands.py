import asyncio
import discord
from random import randint
from discord import Intents, Client, app_commands
from command.TicTacToe import TicTacToeView
from command.Trivia import retrieve_questions, pick_question, check_answer
from command.Unscramble import pick_word, scramble


# Bot Setup
intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)
tree = app_commands.CommandTree(client)

# Game Variables
questions_list = retrieve_questions('data/questions.json')
questions = []
words = []
scrambled = []
current_question = 0
total_questions = 0
num_correct = 0
trivia_active = False
scramble_active = False


# Utility
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


# Games
@tree.command(name="tictactoe", description="Play Tic Tac Toe")
@app_commands.describe(mode="Enter 'cpu' to play against the computer")
async def tic_tac_toe(interaction, mode: str = 'player'):
    view = TicTacToeView(playing_computer=(mode.lower() == 'cpu'))
    await interaction.response.send_message("Tic Tac Toe: X starts", view=view)


@tree.command(name="trivia", description="Play Trivia")
@app_commands.describe(num_questions="Enter the number of questions you would like to answer")
async def trivia(interaction, num_questions: int = 5):
    global questions, current_question, total_questions, trivia_active
    total_questions = num_questions
    questions = [pick_question(questions_list) for _ in range(total_questions)]
    current_question = 0
    trivia_active = True
    await interaction.response.send_message('Welcome to Trivia! Type !a <your answer> to answer the question.')
    await interaction.followup.send(questions[current_question]['question'])


@tree.command(name="unscramble", description="Unscramble the Word!")
@app_commands.describe(num_questions="Enter the number of questions you would like to answer")
async def unscramble(interaction, num_questions: int = 5):
    global scramble_active, questions, current_question, total_questions, words, scrambled
    total_questions = num_questions
    words = [pick_word('../data/words.txt') for _ in range(total_questions)]
    for word in words:
        scrambled.append(scramble(word))
    current_question = 0
    scramble_active = True
    await interaction.response.send_message(
        "Welcome to Unscramble the Word! Type !a <your answer> to answer the question or !q to quit.")
    await interaction.followup.send(f'Unscramble: {scrambled[current_question]}')

    
# Used to check user's answer for Trivia and Unscramble
@client.event
async def on_message(message) -> None:
    global current_question, questions, trivia_active, num_correct, scramble_active, words, scrambled
    if message.author == client.user:
        return

    # If the user is playing Trivia
    if message.content.startswith('!a') and trivia_active:
        answer = message.content[len('!a '):]
        if questions and check_answer(questions[current_question], answer):
            num_correct += 1
            await message.channel.send('Correct!')
        else:
            await message.channel.send(f'Incorrect. Correct answer: {questions[current_question]['answer']}')
        current_question += 1

        if current_question < len(questions):
            await message.channel.send(questions[current_question]['question'])
        else:
            await message.channel.send(
                f'All questions answered! Results: {num_correct}/{total_questions} questions correctly answered.')
            questions = []
            current_question = 0
            trivia_active = False

    # If the user is playing Unscramble the Word
    if scramble_active:
        if message.content.startswith('!a'):
            answer = message.content[len('!a '):]
            if answer.lower() == words[current_question]:
                num_correct += 1
                await message.channel.send('Correct!')
            else:
                await message.channel.send(f'Incorrect! The correct answer was: {words[current_question]}')
            current_question += 1

            if current_question < len(scrambled):
                await message.channel.send(f'Unscramble: {scrambled[current_question]}')
            else:
                await message.channel.send(
                    f'All questions answered! Results: {num_correct}/{total_questions} questions correctly answered.')
                words, scrambled = [], []
                current_question = 0
                scramble_active = False

        elif message.content.startswith('!q'):
            await message.channel.send('Game exited.')
            scramble_active = False


# Moderation Tools
@tree.command(name="kick", description="Kick a user from the server")
@app_commands.describe(member="The member to kick", reason="The reason for kicking the member")
async def kick(interaction, member: discord.Member, reason: str = None):
    if interaction.user.guild_permissions.kick_members:
        await member.kick(reason=reason)
        await interaction.response.send_message(f'User {member.mention} has been kicked.')
    else:
        await interaction.response.send_message("You do not have permission to kick members.", ephemeral=True)


@tree.command(name="ban", description="Ban a user from the server")
@app_commands.describe(member="The member to ban", reason="The reason for banning the member")
async def ban(interaction, member: discord.Member, reason: str = None):
    if interaction.user.guild_permissions.ban_members:
        await member.ban(reason=reason)
        await interaction.response.send_message(f'User {member.mention} has been banned.')
    else:
        await interaction.response.send_message("You do not have permission to ban members.", ephemeral=True)


# Mute user for a time in minutes. Will automatically unmute after the duration.
@tree.command(name="mute", description="Mute a user for a selected duration")
@app_commands.describe(member="The member to mute", duration="Time to mute for (minutes).",
                       reason="The reason for banning the member")
async def mute(interaction, member: discord.Member, duration: int = 60, reason: str = None):
    if interaction.user.guild_permissions.manage_roles:
        mute_role = discord.utils.get(interaction.guild.roles, name='Muted')
        if mute_role is None:
            await interaction.response.send_message("Role not found. Please create a role named 'Muted'.",
                                                    ephemeral=True)
            return
        try:
            await member.add_roles(mute_role, reason=reason)
            await interaction.response.send_message(f'User {member.mention} has been muted for {duration} minutes.')
            await asyncio.sleep(duration * 60)
            await member.remove_roles(mute_role)
            await interaction.followup.send(f'User {member.mention} has been unmuted.')
        except discord.Forbidden:
            await interaction.response.send_message(
                'I do not have the necessary permissions. Please update the permissions.', ephemeral=True)
    else:
        await interaction.response.send_message("You do not have permission to mute members.", ephemeral=True)


# Manually unmute a user by command
@tree.command(name="unmute", description="Unmute a user")
@app_commands.describe(member="The member to unmute")
async def unmute(interaction, member: discord.Member):
    if interaction.user.guild_permissions.manage_roles:
        mute_role = discord.utils.get(interaction.guild.roles, name='Muted')
        is_muted = discord.utils.get(member.roles, name='Muted')
        if is_muted:
            await member.remove_roles(mute_role)
            await interaction.response.send_message(f'User {member.mention} has been unmuted.')
        else:
            await interaction.response.send_message(f'Err... User {member.mention} is already unmuted.')
    else:
        await interaction.response.send_message("You do not have permission to unmute members.", ephemeral=True)
