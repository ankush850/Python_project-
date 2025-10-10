import random
import sys
import time

class Token:
    FINISHED_PROGRESS = 57
    def __init__(self, name):
        self.name = name
        self.progress = 0

    def is_home(self):
        return self.progress == 0

    def is_finished(self):
        return self.progress >= Token.FINISHED_PROGRESS

    def __repr__(self):
        if self.progress == 0: return f"{self.name}:HOME"
        if self.is_finished(): return f"{self.name}:FINISHED"
        return f"{self.name}:{self.progress}"

class Player:
    START_INDEX = {'Red': 0, 'Yellow': 13, 'Green': 26, 'Blue': 39}
    def __init__(self, color):
        self.color = color
        self.start_index = Player.START_INDEX[color]
        self.tokens = [Token(f"{color[0]}{i}") for i in range(1, 5)]
        self.finished_count = 0
        self.rank = None
        self.consecutive_sixes = 0

    def all_finished(self):
        return self.finished_count == 4

    def movable_tokens(self, dice):
        movable = []
        for i, t in enumerate(self.tokens):
            if t.is_finished(): continue
            if t.is_home():
                if dice == 6: movable.append(i)
            else:
                if t.progress + dice <= Token.FINISHED_PROGRESS:
                    movable.append(i)
        return movable

class Board:
    MAIN_TRACK_LEN = 52
    def __init__(self):
        self.safe_positions = set([0,8,13,21,26,34,39,47])

    def is_on_main_track(self, p):
        return 1 <= p <= Board.MAIN_TRACK_LEN

    def main_track_index(self, start, prog):
        if not self.is_on_main_track(prog): return None
        return (start + (prog - 1)) % Board.MAIN_TRACK_LEN

    def is_safe(self, idx):
        return idx in self.safe_positions

class LudoGame:
    def __init__(self):
        self.players = [Player(c) for c in ["Red", "Yellow", "Green", "Blue"]]
        self.board = Board()
        self.turn_index = 0
        self.ranking = []
        self.random = random.Random()

    def roll_dice(self):
        return self.random.randint(1,6)

    def try_capture(self, mover, idx):
        token = mover.tokens[idx]
        if not self.board.is_on_main_track(token.progress): return []
        dest = self.board.main_track_index(mover.start_index, token.progress)
        if self.board.is_safe(dest): return []
        captured = []
        for p in self.players:
            if p is mover: continue
            for i, t in enumerate(p.tokens):
                if self.board.is_on_main_track(t.progress):
                    if self.board.main_track_index(p.start_index, t.progress) == dest:
                        t.progress = 0
                        captured.append((p, i))
        return captured

    def move_token(self, player, token_idx, steps):
        t = player.tokens[token_idx]
        info = {'player': player.color, 'token': t.name, 'from': t.progress, 'dice': steps, 'moved': False, 'finished': False, 'captured': []}

        if t.is_home():
            if steps == 6:
                t.progress = 1
                info['moved'] = True
            return info

        if t.progress + steps > Token.FINISHED_PROGRESS:
            return info

        t.progress += steps
        info['moved'] = True

        if t.is_finished():
            player.finished_count += 1
            info['finished'] = True
            if player.all_finished() and player.rank is None:
                player.rank = len(self.ranking) + 1
                self.ranking.append(player.color)

        if self.board.is_on_main_track(t.progress):
            info['captured'] = [(p.color, i+1) for p, i in self.try_capture(player, token_idx)]
        return info

    def display_state(self):
        print("\n--- BOARD STATE ---")
        for p in self.players:
            print(f"{p.color}: " + " | ".join(str(t) for t in p.tokens) + f"  Finished:{p.finished_count}  Rank:{p.rank if p.rank else '-'}")
        print("-------------------\n")

    def choose_token(self, player, dice, movable):
        if not movable: return None
        if len(movable) == 1:
            print(f"Only {player.tokens[movable[0]].name} can move.")
            return movable[0]
        print(f"\n{player.color} tokens:")
        for i, t in enumerate(player.tokens):
            print(f"  {i+1}. {t} {'(movable)' if i in movable else ''}")
        while True:
            c = input(f"Choose token (1-4) for dice {dice}, or 'p' to pass: ").strip().lower()
            if c == 'p': return None
            if c.isdigit():
                n = int(c)
                if 1 <= n <= 4 and (n-1) in movable:
                    return n-1
            print("Invalid choice.")

    def play_turn(self, player):
        while True:
            input(f"\n{player.color}'s turn. Enter to roll.")
            dice = self.roll_dice()
            print(f"{player.color} rolled: {dice}")

            if dice == 6:
                player.consecutive_sixes += 1
            else:
                player.consecutive_sixes = 0

            if player.consecutive_sixes == 3:
                print("3 sixes! Turn lost.")
                player.consecutive_sixes = 0
                return False

            movable = player.movable_tokens(dice)
            if movable:
                choice = self.choose_token(player, dice, movable)
                if choice is not None:
                    info = self.move_token(player, choice, dice)
                    if info['moved']:
                        print(f"Moved {info['token']} from {info['from']} to {player.tokens[choice].progress}")
                        if info['captured']:
                            print(f"Captured: {info['captured']}")
                        if info['finished']:
                            print(f"{player.color} finished a token!")
                            if player.all_finished():
                                player.rank = len(self.ranking) + 1
                                self.ranking.append(player.color)
                                print(f"{player.color} is Rank {player.rank}!")
                    else:
                        print("Illegal move.")
            else:
                print("No moves possible.")

            self.display_state()

            if dice == 6 and not player.all_finished():
                print("Extra turn for rolling 6.")
                continue
            return False

    def is_game_over(self):
        return len(self.ranking) == len(self.players)

    def play(self):
        print("Welcome to Ludo!")
        self.display_state()
        while True:
            p = self.players[self.turn_index]
            if p.all_finished():
                if p.rank is None:
                    p.rank = len(self.ranking) + 1
                    self.ranking.append(p.color)
                self.turn_index = (self.turn_index + 1) % len(self.players)
                if self.is_game_over(): break
                continue

            self.play_turn(p)

            if self.is_game_over(): break
            self.turn_index = (self.turn_index + 1) % len(self.players)

        print("\nGame Over! Rankings:")
        for i, c in enumerate(self.ranking, 1):
            print(f"{i}. {c}")
        for p in self.players:
            if p.color not in self.ranking:
                self.ranking.append(p.color)
                print(f"{len(self.ranking)}. {p.color}")

if __name__ == "__main__":
    try:
        LudoGame().play()
    except KeyboardInterrupt:
        print("\nGame exited.")
        sys.exit(0)
