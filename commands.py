from random import randint


def coin_flip() -> str:
    if randint(0, 1) == 0:
        return 'heads'
    return 'tails'


def roll_dice() -> int:
    return randint(1, 6)


def commands() -> str:
    command_list = ['Use \'!\' to initiate the use of any command\n'
                    '-------------------------------------------\n'
                    'coinflip ----------------- Flip a coin\n'
                    'roll --------------------- Roll a 6-sided die']

    for row in command_list:
        return row