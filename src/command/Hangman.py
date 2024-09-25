import random


class HangmanGame:
    def __init__(self):
        self.status = False
        self.lives = 0
        self.guessed_letters = []
        self.answer = pick_word('data/hangman-words.txt')

    async def start(self, interaction):
        self.status = True
        self.lives = 5
        await interaction.response.send_message(
            "Welcome to Hangman! Type !g followed by a letter to guess a letter or !a followed by your answer to guess the word. Guess the word before you run out of lives!")
        await interaction.followup.send(f'[{self.lives} Lives Remaining] | Word: {"-" * len(self.answer)}')

    async def handle_guess(self, message):
        guess = message.content[len('!g '):].lower()
        if len(guess) != 1:
            await message.channel.send('Error | Please only guess a singular letter.')
        else:
            self.guessed_letters.append(guess)
            if guess in self.answer:
                await message.channel.send(
                    f'[{self.lives} Lives Remaining] | Word: {"".join([char if char in self.guessed_letters else "-" for char in self.answer])}')
            else:
                self.lives -= 1
                if self.lives > 0:
                    await message.channel.send(
                        f'[{self.lives} Lives Remaining] | Word: {"".join([char if char in self.guessed_letters else "-" for char in self.answer])}')
                else:
                    await self.end(message)

    async def handle_answer(self, message):
        guess = message.content[len('!a '):].lower()
        if guess == self.answer:
            await message.channel.send('You win! You guessed the correct word.')
        else:
            self.lives -= 1
            if self.lives > 0:
                await message.channel.send('Incorrect.')
                await message.channel.send(
                    f'[{self.lives} Lives Remaining] | Word: {"".join([char if char in self.guessed_letters else "-" for char in self.answer])}')
            else:
                await self.end(message)

    async def end(self, message):
        await message.channel.send(f'Game Over! You ran out of lives. Answer: {self.answer}')
        self.status = False
        self.guessed_letters = []
        self.lives = 5


# Picks a random word from the words source file
def pick_word(word_src: str) -> str:
    with open(word_src, 'r') as file:
        words = file.read().splitlines()
    return random.choice(words)
