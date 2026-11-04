import random
from list import p_list

class Dungeon:
    def __init__(self):
        self.dungeon = random.choice(p_list)
        self.rows = self.dungeon.splitlines()
        self.player_pos = self.find_player()
        self.exit_pos = self.find_exit()
        self.key_pos = self.find_key()
        self.door_pos = self.find_door()
        self.treasure_pos = self.find_treasure()
        self.guard_pos = self.find_guard()  # Track guard position
        self.moves = 0
        self.health = 2
        self.has_key = False
        self.game_status = "IN PROGRESS"  # Options: IN PROGRESS, WON, LOST
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
        if self.player_pos == self.exit_pos:
            score = 100 - self.moves + 20 * self.health
        print(
            f"Health: {self.health}\n"
            f"Keys: {1 if self.has_key else 0}\n"
            f"Moves: {self.moves}\n"
            f"Status: {self.game_status}\n"
            f"Score: {score}"
        )

    def save_state(self):
        state = {
            'rows': list(self.rows),
            'player_pos': self.player_pos,
            'key_pos': self.key_pos,
            'door_pos': self.door_pos,
            'treasure_pos': self.treasure_pos,
            'guard_pos': self.guard_pos,
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
            self.check_item_interactions()
        else:
            print("You can't move there!")

    def is_valid_move(self, pos):
        # Bound checking
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

    def check_item_interactions(self):
        if self.player_pos == self.key_pos:
            self.has_key = True
            self.key_pos = None
            print("You picked up the Key!")
            
        elif self.player_pos == self.door_pos:
            self.door_pos = None
            print("You unlocked and passed through the Door!")
            
        elif self.player_pos == self.treasure_pos:
            self.treasure_pos = None
            self.health -= 1  # Decrease health by 1
            
            # Check if the player survived the curse or ran out of health
            if self.health <= 0:
                self.game_status = "LOST"
                print("The treasure was cursed! Your health fell to 0. GAME OVER.")
            else:
                self.game_status = "IN PROGRESS"
                print(f"The treasure was cursed! Your health decreased to {self.health}. Status: {self.game_status}")
                
        elif self.player_pos == self.guard_pos:
            self.guard_pos = None
            self.health = 0
            self.game_status = "LOST"
            print("You caught the attention of the Guard! GAME OVER.")
            
        elif self.rows[self.player_pos[0]][self.player_pos[1]] == 'X':
            self.health = 0
            self.game_status = "LOST"
            print("You stepped on a trap! GAME OVER.")
            
        elif self.player_pos == self.exit_pos:
            self.game_status = "WON"
            print("Congratulations! You've escaped the dungeon!")

    def play(self):
        while self.game_status == "IN PROGRESS":
            self.display()
            self.print_game_metrics()
            direction = input("Enter direction (w/s/a/d or u to undo): ")
            self.move_player(direction)
        
        # Display final state summary after game loops terminates
        self.display()
        self.print_game_metrics()

if __name__ == "__main__":
    dungeon = Dungeon()
    dungeon.play()
