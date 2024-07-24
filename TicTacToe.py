from discord.ui import Button, View
import discord


# Class that handles the logic of the game
class TicTacToeGame:
    # Constructor to initialize the game
    # PARAM: playing_computer: Determines whether the player is playing against the computer
    def __init__(self, playing_computer: bool):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.playing_computer = playing_computer
        self.winner = None

    # Method to switch the player
    def switch_player(self):
        if self.current_player == 'X':
            self.current_player = 'O'
        else:
            self.current_player = 'X'

    def computer(self):
        for x in range(3):
            for y in range(3):
                if self.board[x][y] == ' ':
                    self.board[x][y] = self.current_player
                    return x, y

    # Checks all possible win conditions
    def check_winner(self):
        # Horizontal Check - Check if all elements in a row are the same and not empty
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                self.winner = self.board[i][0]
                return True
        # Vertical Check - Check if all elements in a column are the same and not empty
        for i in range(3):
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != ' ':
                self.winner = self.board[0][i]
                return True
        # Diagonal Check - Check if all elements in a diagonal are the same and not empty
        if (self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ') or (
                self.board[0][2] == self.board[1][1] == self.board[2][0] != ' '):
            self.winner = self.board[1][1]
            return True
        # Currently no winner
        return False

    # Checks for a tied game
    def check_tie(self):
        # If the board is full without a winner, it's a tie
        for row in self.board:
            if ' ' in row:
                return False
        return True

    # Resets the game
    def reset(self):
        # Reset all conditions to restart the game
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.winner = None


# Instance of the Tic-Tac-Toe game to be passed to the button, computer is not playing by default
game = TicTacToeGame(playing_computer=False)


# Class that represents a button on the board
class TicTacToeButton(Button):
    # Constructor to initialize the button
    def __init__(self, x, y):
        super().__init__(style=discord.ButtonStyle.secondary, label='\u200b', row=y)
        self.x = x
        self.y = y

    # Method to handle the button clicks
    async def callback(self, interaction):
        # If the space is empty, place the current player's label
        if game.board[self.x][self.y] == ' ':
            game.board[self.x][self.y] = game.current_player
            self.label = game.current_player
            self.disabled = True

            # If there is a winner: Set game board to read only, print the winner, and reset the game
            if game.check_winner():
                for child in self.view.children:
                    child.disabled = True
                await interaction.response.edit_message(content=f'Winner: {game.current_player}!', view=self.view)
                game.reset()
                return
            # If there is a tie: Set game board to read only, print the tie, and reset the game
            elif game.check_tie():
                for child in self.view.children:
                    child.disabled = True
                await interaction.response.edit_message(content='It\'s a tie!', view=self.view)
                game.reset()
                return
            # Otherwise, switch the player and continue the game
            else:
                game.switch_player()

                # If the computer is playing, make a move
                if game.playing_computer and game.current_player == 'O':
                    x, y = game.computer()
                    for child in self.view.children:
                        if child.x == x and child.y == y:
                            child.label = game.current_player
                            child.disabled = True
                    # If the computer won: reset all conditions and print the winner
                    if game.check_winner():
                        for child in self.view.children:
                            child.disabled = True
                        await interaction.response.edit_message(content=f'Winner: {game.current_player}!', view=self.view)
                        game.reset()
                        return
                    # If there is a tie: reset all conditions and print the tie
                    elif game.check_tie():
                        for child in self.view.children:
                            child.disabled = True
                        await interaction.response.edit_message(content='It\'s a tie!', view=self.view)
                        game.reset()
                        return
                    # Otherwise, switch the player and continue the game
                    else:
                        game.switch_player()
                await interaction.response.edit_message(view=self.view)


# Class that represents the board for the game
class TicTacToeView(View):
    # Constructor to initialize the game board
    # PARAM: playing_computer: Passed as a string by the user to determine if the player is playing against the computer
    def __init__(self, playing_computer: bool):
        super().__init__()
        # Access the game instance and modify the playing_computer attribute depending on the user input
        global game
        game = TicTacToeGame(playing_computer=playing_computer)
        self.add_item(TicTacToeButton(0, 0))
        self.add_item(TicTacToeButton(1, 0))
        self.add_item(TicTacToeButton(2, 0))
        self.add_item(TicTacToeButton(0, 1))
        self.add_item(TicTacToeButton(1, 1))
        self.add_item(TicTacToeButton(2, 1))
        self.add_item(TicTacToeButton(0, 2))
        self.add_item(TicTacToeButton(1, 2))
        self.add_item(TicTacToeButton(2, 2))
