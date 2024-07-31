from random import randint
from TicTacToe import TicTacToeView
from discord import Intents, Client, app_commands
from Trivia import retrieve_questions, pick_question, check_answer

# Bot Setup
intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)
tree = app_commands.CommandTree(client)

# Trivia Game Variables
questions_list = retrieve_questions('questions.json')
questions = []
current_question = 0
total_questions = 0
num_correct = 0
game_active = False


# Commands
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


@tree.command(name="trivia", description="Play Trivia")
@app_commands.describe(num_questions="Enter the number of questions you would like to answer")
async def trivia(interaction, num_questions: int = 5):
    global questions, current_question, total_questions, game_active
    total_questions = num_questions
    questions = [pick_question(questions_list) for _ in range(total_questions)]
    current_question = 0
    game_active = True
    await interaction.response.send_message('Welcome to Trivia! Type !a <your answer> to answer the question.')
    await interaction.followup.send(questions[current_question]['question'])


@client.event
async def on_message(message) -> None:
    global current_question, questions, game_active, num_correct
    if message.author == client.user:
        return

    if message.content.startswith('!a') and game_active:
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
            game_active = False
