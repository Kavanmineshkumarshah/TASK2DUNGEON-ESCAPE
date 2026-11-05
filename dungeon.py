import sys
import os
from list import p_list
class Dungeon:
    VALID_CHARS = {'#', '.', 'P', 'E', 'K', 'D', 'T', 'G', 'X'}

    def __init__(self, map_file):
        if not os.path.exists(map_file):
            print(f"ERROR: file not found: {map_file}")
            sys.exit(1)
        try:
            with open(map_file, 'r') as f:
                self.rows = [line.rstrip('\n') for line in f if line.strip()]
        except Exception as e:
            print(f"ERROR: could not read file: {e}")
            sys.exit(1)

        if not self.rows:
            print("ERROR: no jobs or empty map file")
            sys.exit(1)

        self.validate_map()
        self.player_pos = self.find_player()
        self.exit_pos = self.find_exit()
        self.key_pos = self.find_key()
        self.door_pos = self.find_door()
        self.treasure_pos = self.find_treasure()
        self.guard_pos = self.find_guard()
        
        # Guard movement direction tracking (1 for down, -1 for up)
        self.guard_dir = 1
        self.moves = 0
        self.health = 2
        self.has_key = False
        self.game_status = 'IN PROGRESS'
        self.history = []

    def validate_map(self):
        row_length = len(self.rows[0])
        for r_idx, row in enumerate(self.rows):
            if len(row) != row_length:
                print(f"ERROR: row {r_idx + 1} has different length (expected {row_length}, got {len(row)})")
                sys.exit(1)
        
        player_count = 0
        exit_count = 0
        for r_idx, row in enumerate(self.rows):
            for c_idx, char in enumerate(row):
                if char not in self.VALID_CHARS:
                    print(f"ERROR: unknown symbol '{char}' at row {r_idx + 1}, col {c_idx + 1}")
                    sys.exit(1)
                if char == 'P':
                    player_count += 1
                if char == 'E':
                    exit_count += 1

        if player_count != 1:
            print(f"ERROR: invalid player count ({player_count}). Map must have exactly 1 'P'.")
            sys.exit(1)
        if exit_count == 0:
            print("ERROR: no exit ('E') found in map.")
            sys.exit(1)

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

    def find_guard(self):
        for i, row in enumerate(self.rows):
            if 'G' in row:
                return (i, row.index('G'))
        return None

    def display(self):
        for row in self.rows:
            print(row)

    def print_game_metrics(self):
        score = 0
        if self.game_status == 'WON':
            score = 100 - self.moves + 20 * self.health
        print(f"Health: {self.health}\nKeys: {1 if self.has_key else 0}\nMoves: {self.moves}\nStatus: {self.game_status}\nScore: {score}")

    def save_state(self):
        state = {
            'rows': list(self.rows),
            'player_pos': self.player_pos,
            'key_pos': self.key_pos,
            'door_pos': self.door_pos,
            'treasure_pos': self.treasure_pos,
            'guard_pos': self.guard_pos,
            'guard_dir': self.guard_dir,
            'moves': self.moves,
            'health': self.health,
            'has_key': self.has_key,
            'game_status': self.game_status
        }
        self.history.append(state)

    def undo_move(self):
        if not self.history:
            print("No moves to undo!")
            return False
        previous_state = self.history.pop()
        self.rows = previous_state['rows']
        self.player_pos = previous_state['player_pos']
        self.key_pos = previous_state['key_pos']
        self.door_pos = previous_state['door_pos']
        self.treasure_pos = previous_state['treasure_pos']
        self.guard_pos = previous_state['guard_pos']
        self.guard_dir = previous_state['guard_dir']
        self.moves = previous_state['moves']
        self.health = previous_state['health']
        self.has_key = previous_state['has_key']
        self.game_status = previous_state['game_status']
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
            self.save_state()
            self.moves += 1
            self.update_player_position(new_pos)
            
            if self.player_pos == self.guard_pos:
                self.health = 0
                self.game_status = 'LOST'
                print("You walked right into the Guard! GAME OVER.")
                return

            if self.game_status == 'IN PROGRESS':
                self.move_guard()
                self.check_item_interactions()
        else:
            print("You can't move there!")

    def is_valid_move(self, pos):
        if pos[0] < 0 or pos[0] >= len(self.rows) or pos[1] < 0 or pos[1] >= len(self.rows[0]):
            return False
        target_cell = self.rows[pos[0]][pos[1]]
        if target_cell == '#':
            return False
        if target_cell == 'D' and not self.has_key:
            print("The door is locked! You need a key.")
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

    def move_guard(self):
        if not self.guard_pos:
            return
        
        next_row = self.guard_pos[0] + self.guard_dir
        if (next_row < 0 or next_row >= len(self.rows) or self.rows[next_row][self.guard_pos[1]] in ['#', 'D', 'E']):
            # Fixed: Changed `self.guard_dir *= "-1"` (string multiplication error) to integer `-1`
            self.guard_dir *= -1
            next_row = self.guard_pos[0] + self.guard_dir
            
        new_guard_pos = (next_row, self.guard_pos[1])
        under_guard = '.'
        if self.guard_pos == self.key_pos:
            under_guard = 'K'
        elif self.guard_pos == self.door_pos:
            under_guard = 'D'
        elif self.guard_pos == self.treasure_pos:
            under_guard = 'T'

        row_list = list(self.rows[self.guard_pos[0]])
        if row_list[self.guard_pos[1]] == 'G':
            row_list[self.guard_pos[1]] = under_guard
        self.rows[self.guard_pos[0]] = ''.join(row_list)
        
        self.guard_pos = new_guard_pos
        if self.guard_pos == self.player_pos:
            self.health = 0
            self.game_status = 'LOST'
            print("The Guard moved into your space and caught you! GAME OVER.")
            return

        row_list = list(self.rows[self.guard_pos[0]])
        if row_list[self.guard_pos[1]] not in ['P']:
            row_list[self.guard_pos[1]] = 'G'
        self.rows[self.guard_pos[0]] = ''.join(row_list)

    def check_item_interactions(self):
        if self.game_status == 'LOST' and self.health == 0:
            return
            
        if self.player_pos == self.key_pos:
            self.has_key = True
            self.key_pos = None
            print("You picked up the Key!")
        elif self.player_pos == self.door_pos:
            self.door_pos = None
            print("You unlocked and passed through the Door!")
        elif self.player_pos == self.treasure_pos:
            self.treasure_pos = None
            self.health -= 1
            if self.health <= 0:
                self.game_status = 'LOST'
                print("The treasure was cursed! Your health fell to 0. GAME OVER.")
            else:
                print(f"The treasure was cursed! Your health decreased to {self.health}.")
        elif self.rows[self.player_pos[0]][self.player_pos[1]] == 'X':
            self.health = 0
            self.game_status = 'LOST'
            print("You stepped on a trap! GAME OVER.")
        elif self.player_pos == self.exit_pos:
            self.game_status = 'WON'
            print("Congratulations! You've escaped the dungeon!")

    def play(self):
        while self.game_status == 'IN PROGRESS':
            self.display()
            self.print_game_metrics()
            direction = input("Enter direction (w/s/a/d or u to undo): ")
            self.move_player(direction)
            print("-" * 20)
        self.display()
        self.print_game_metrics()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("ERROR: Please provide a map file path.")
        print("Usage: python3 dungeon.py <map_file.txt>")
        sys.exit(1)

    map_filepath = sys.argv[1]
    
    # Ensure the file actually exists before passing it to the Dungeon class
    if not os.path.exists(map_filepath):
        print(f"ERROR: File not found: {map_filepath}")
        sys.exit(1)
        
    dungeon = Dungeon(map_filepath)
    dungeon.play()
