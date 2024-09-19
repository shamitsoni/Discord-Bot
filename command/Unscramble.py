import random


# Picks a random word from the words source file
def pick_word(word_src: str) -> str:
    with open(word_src, 'r') as file:
        words = file.read().splitlines()
    return random.choice(words)


# Scrambles the order of a selected word
def scramble(word: str) -> str:
    chars = list(word)
    random.shuffle(chars)
    return "".join(chars)


