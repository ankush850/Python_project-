import random

class LudoGame:
    def __init__(self):
        self.players = ["Red", "Yellow", "Green", "Blue"]
        self.tokens = {player: {f"{player[0]}{i}": "HOME" for i in range(1, 5)} for player in self.players}
        self.finish_count = {player: 0 for player in self.players}
        self.winning_score = 4  # tokens to finish

    def roll_dice(self):
        return random.randint(1, 6)

    def move_token(self, player, token, steps):
        pos = self.tokens[player][token]

        # 1. Token is at HOME, can only enter if dice == 6
        if pos == "HOME":
            if steps == 6:
                self.tokens[player][token] = 1  # Enters board at step 1
                print(f"{token} enters the board!")
            else:
                print(f"{token} cannot enter without rolling 6.")
            return

        # 2. Move token normally
        new_pos = pos + steps

        # 3. Check if token reaches or passes finish (assume 51 is finish limit)
        if new_pos >= 51:
            self.tokens[player][token] = "FINISHED"
            self.finish_count[player] += 1
            print(f"{token} reached the finish!")
        else:
            self.tokens[player][token] = new_pos
            print(f"{token} moved to {new_pos}")

    def display(self):
        print("\n--- Game State ---")
        for player in self.players:
            print(f"{player} -> {self.tokens[player]} | Finished: {self.finish_count[player]}")
        print()

    def play(self):
        while all(self.finish_count[p] < self.winning_score for p in self.players):
            for player in self.players:
                input(f"{player}'s turn (Press Enter to roll dice)")
                dice = self.roll_dice()
                print(f"{player} rolled: {dice}")

                # Choose a movable token
                movable_tokens = [t for t, pos in self.tokens[player].items()
                                  if pos != "FINISHED" and (pos != "HOME" or dice == 6)]

                if not movable_tokens:
                    print("No token can move.")
                    self.display()
                    continue

                # Pick a random token (can be improved later)
                token = random.choice(movable_tokens)
                self.move_token(player, token, dice)

                self.display()

                # Check winner
                if self.finish_count[player] == self.winning_score:
                    print(f"🎉 {player} wins the game!")
                    return

if __name__ == "__main__":
    game = LudoGame()
    game.play()
