from list import p_list
import random

class Dungeon:
    def __init__(self):
        self.dungeon = random.choice(p_list)
        self.rows = self.dungeon.splitlines()
        self.player_pos = self.find_player()
        self.exit_pos = self.find_exit()
        self.key_pos = self.find_key()
        self.door_pos = self.find_door()
        self.treasure_pos = self.find_treasure()
        self.moves = 0
        self.health = 100
        
        # History stack to store previous game states for the undo feature
        self.history = []

    def find_player(self):
        for i, row in enumerate(self.rows):
            if 'P' in row:
                return (i, row.index('P'))
        return None

    def find_exit(self):
        for i, row in enumerate(self.rows):
            if 'E' in row:
                return (i, row.index('E'))
        return None

    def find_key(self):
        for i, row in enumerate(self.rows):
            if 'K' in row:
                return (i, row.index('K'))
        return None

    def find_door(self):
        for i, row in enumerate(self.rows):
            if 'D' in row:
                return (i, row.index('D'))
        return None

    def find_treasure(self):
        for i, row in enumerate(self.rows):
            if 'T' in row:
                return (i, row.index('T'))
        return None

    def display(self):
        for row in self.rows:
            print(row)

    def health_status(self):
        if self.player_pos == self.exit_pos:
            self.health -= 10
        if self.player_pos == self.key_pos:
            self.health -= 5
        if self.player_pos == self.door_pos and self.key_pos is None:
            self.health -= 5
        if self.player_pos == self.treasure_pos:
            self.health -= 20
        print(f" health: {self.health}")

    def key_status(self):
        score = 0
        if self.player_pos == self.exit_pos:
            score += 10
        if self.player_pos == self.key_pos:
            score += 5
        if self.player_pos == self.door_pos and self.key_pos is None:
            score += 5
        if self.player_pos == self.treasure_pos:
            score += 20
        print(f" keyscore: {score}")

    def score_status(self):
        if self.player_pos == self.exit_pos:
            score = 100 - self.moves + (20 * self.health)
            if score < 0:
                score = 0
        else:
            score = 0
        print(f"score: {score}")

    def status(self):
        if self.player_pos == self.exit_pos:
            print("WON")
        elif self.player_pos == self.key_pos:
            print("KEY")
        elif self.player_pos == self.door_pos and self.key_pos is None:
            print("DOOR")
        elif self.player_pos == self.treasure_pos:
            print("TREASURE")
        else:
            print("IN PROGRESS")

    def move_score(self):
        score = 0
        if self.player_pos == self.exit_pos:
            score += 10
        if self.player_pos == self.key_pos:
            score += 5
        if self.player_pos == self.door_pos and self.key_pos is None:
            score += 5
        if self.player_pos == self.treasure_pos:
            score += 20
        print(f" movescore: {score}")

    def save_state(self):
        # Save a deep copy of the full game state before a move alters it
        state = {
            'rows': list(self.rows),
            'player_pos': self.player_pos,
            'key_pos': self.key_pos,
            'door_pos': self.door_pos,
            'treasure_pos': self.treasure_pos,
            'moves': self.moves,
            'health': self.health
        }
        self.history.append(state)

    def undo_move(self):
        if not self.history:
            print("No moves to undo!")
            return False
        
        # Pop the last state and restore game values completely
        previous_state = self.history.pop()
        self.rows = previous_state['rows']
        self.player_pos = previous_state['player_pos']
        self.key_pos = previous_state['key_pos']
        self.door_pos = previous_state['door_pos']
        self.treasure_pos = previous_state['treasure_pos']
        self.moves = previous_state['moves']
        self.health = previous_state['health']
        print("Undo successful!")
        return True

    def move_player(self, direction):
        direction = direction.upper()
        
        if direction == 'U':
            self.undo_move()
            return

        if direction == 'W':
            new_pos = (self.player_pos[0] - 1, self.player_pos[1])
        elif direction == 'S':
            new_pos = (self.player_pos[0] + 1, self.player_pos[1])
        elif direction == 'A':
            new_pos = (self.player_pos[0], self.player_pos[1] - 1)
        elif direction == 'D':
            new_pos = (self.player_pos[0], self.player_pos[1] + 1)
        else:
            print("Invalid direction! Use 'w', 's', 'a', 'd', or 'u' to undo.")
            return

        if self.is_valid_move(new_pos):
            # Save state only if the move is valid and about to change things
            self.save_state()
            self.moves += 1
            self.update_player_position(new_pos)
        else:
            print("You can't move there!")

    def is_valid_move(self, pos):
        if pos[0] < 0 or pos[0] >= len(self.rows) or pos[1] < 0 or pos[1] >= len(self.rows[0]):
            return False
        if self.rows[pos[0]][pos[1]] == '#':
            return False
        return True

    def update_player_position(self, new_pos):
        row_list = list(self.rows[self.player_pos[0]])
        row_list[self.player_pos[1]] = '.'
        self.rows[self.player_pos[0]] = ''.join(row_list)
        
        row_list = list(self.rows[new_pos[0]])
        row_list[new_pos[1]] = 'P'
        self.rows[new_pos[0]] = ''.join(row_list)
        self.player_pos = new_pos

    def check_game_status(self):
        if self.player_pos == self.exit_pos:
            print("Congratulations! You've reached the exit!")
            return True
        if self.player_pos == self.key_pos:
            print("key!")
            self.key_pos = None
        if self.player_pos == self.door_pos and self.key_pos is None:
            print("door!")
            self.door_pos = None
        if self.player_pos == self.treasure_pos:
            print("You've found the treasure!")
            self.treasure_pos = None
        return False

    def play(self):
        while True:
            self.display()
            direction = input("Enter direction (w/s/a/d or u to undo): ")
            self.move_player(direction)
            self.health_status()
            self.key_status()
            self.score_status()
            self.move_score()
            if self.check_game_status():
                break

    def get_player_position(self):
        return self.player_pos

if __name__ == "__main__":
    dungeon = Dungeon()
    dungeon.play()
