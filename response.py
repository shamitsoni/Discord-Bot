from commands import *


def get_response(input: str) -> str:
    lowered = input.lower()

    if lowered[0] == '!':
        if '!help' in lowered:
            return commands()
        elif '!coinflip' in lowered:
            return f'Coin Flip: {coin_flip()}'
        elif '!roll' in lowered:
            return f'Rolled: {roll_dice()}'
        else:
            return 'Unknown command. Use !help to view all valid commands'

    if lowered[0:5] == 'hello' or lowered[0:2] == 'hi':
        return 'Hello there!'
