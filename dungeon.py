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
    def move_player(self, direction):
        if direction == 'up':
            new_pos = (self.player_pos[0] - 1, self.player_pos[1])
        elif direction == 'down':
            new_pos = (self.player_pos[0] + 1, self.player_pos[1])
        elif direction == 'left':
            new_pos = (self.player_pos[0], self.player_pos[1] - 1)
        elif direction == 'right':
            new_pos = (self.player_pos[0], self.player_pos[1] + 1)
        else:
            print("Invalid direction! Use 'up', 'down', 'left', or 'right'.")
            return
        if self.is_valid_move(new_pos):
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
            print("You've found the key!")
            self.key_pos = None
        if self.player_pos == self.door_pos and self.key_pos is None:
            print("You've unlocked the door!")
            self.door_pos = None
        if self.player_pos == self.treasure_pos:
            print("You've found the treasure!")
            self.treasure_pos = None
        return False
    def play(self):
        while True:
            self.display()
            direction = input("Enter direction (up: w, down: s, left: a, right: d): ")
            self.move_player(direction)
            if self.check_game_status():
                break
    def get_player_position(self):
        return self.player_pos
if __name__ == "__main__":
    dungeon = Dungeon()
    dungeon.play()
    
