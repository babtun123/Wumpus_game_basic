"""Game file"""

import sys
from character import Pit, Wumpus, Person

class Room:
    """
        Room class:
        Each individual room in the cave
        Each room will have 3 adjacent room
        Each room will also have an option of whether 
        there is a character in the room or none.
    """
    def __init__(self, index_pos):
        self.type_character = None
        self.position = index_pos
        self.adjacent_rooms = []
        self.name = "Room " + str(self.position)

class WumpusGame:
    """
        The cave has 20 rooms total
        each cave has three adjacent rooms
    """
    def __init__(self):
        self.cave = [Room(x) for x in range(0, 21)]

    def set_adj_rooms(self):
        """
            Used to set each room post in the cave
            I ignore index 0
        """
        self.cave[1].adjacent_rooms = [self.cave[2], self.cave[5], self.cave[8]]
        self.cave[2].adjacent_rooms = [self.cave[1], self.cave[3], self.cave[10]]
        self.cave[3].adjacent_rooms = [self.cave[2], self.cave[4], self.cave[12]]
        self.cave[4].adjacent_rooms = [self.cave[3], self.cave[5], self.cave[14]]
        self.cave[5].adjacent_rooms = [self.cave[1], self.cave[4], self.cave[6]]
        self.cave[6].adjacent_rooms = [self.cave[5], self.cave[7], self.cave[15]]
        self.cave[7].adjacent_rooms = [self.cave[6], self.cave[8], self.cave[17]]
        self.cave[8].adjacent_rooms = [self.cave[1], self.cave[7], self.cave[9]]
        self.cave[9].adjacent_rooms = [self.cave[8], self.cave[10], self.cave[18]]
        self.cave[10].adjacent_rooms = [self.cave[2], self.cave[9], self.cave[11]]
        self.cave[11].adjacent_rooms = [self.cave[10], self.cave[12], self.cave[19]]
        self.cave[12].adjacent_rooms = [self.cave[3], self.cave[11], self.cave[13]]
        self.cave[13].adjacent_rooms = [self.cave[12], self.cave[14], self.cave[20]]
        self.cave[14].adjacent_rooms = [self.cave[4], self.cave[13], self.cave[15]]
        self.cave[15].adjacent_rooms = [self.cave[6], self.cave[14], self.cave[16]]
        self.cave[16].adjacent_rooms = [self.cave[15], self.cave[17], self.cave[20]]
        self.cave[17].adjacent_rooms = [self.cave[7], self.cave[16], self.cave[18]]
        self.cave[18].adjacent_rooms = [self.cave[9], self.cave[17], self.cave[19]]
        self.cave[19].adjacent_rooms = [self.cave[11], self.cave[18], self.cave[20]]
        self.cave[20].adjacent_rooms = [self.cave[13], self.cave[16], self.cave[19]]

    def print_cave_room_details(self):
        """Print out each room in the cave properties"""
        for room in self.cave[1: ]:
            adj_ids = [adj.position for adj in room.adjacent_rooms if adj is not None]
            print(
                f"Room: {room.position} | "
                f"Character: {room.type_character} | "
                f"Neighbors: {adj_ids}"
            )

    def available_positions(self):
        """Used to get positions that are empty"""
        empty_pos = []
        for i, n in enumerate(self.cave):
            if i != 0 and n.type_character is None:
                empty_pos.append(i)
        return empty_pos

    def update_available_positions(self, object_to_add, position):
        """Used to set an object to a room"""
        self.cave[position].type_character = object_to_add

    def is_adj_move_valid(self, player_curr_pos, room_to_move_to):
        """Used to check if the player move is valid"""
        curr_cave = self.cave[player_curr_pos]
        next_cave = self.cave[room_to_move_to]
        if next_cave in curr_cave.adjacent_rooms:
            return True
        return False

def play(wumpus_game, pit_one, pit_two, wumpus_arg, person_arg):
    """game workflow"""

    # First, set all adjacent rooms
    wumpus_game.set_adj_rooms()

    # set initial postions for all characters
    set_postion_helper(wumpus_game, pit_one, pit_two, wumpus_arg, person_arg)

    print("You are in room 16.")

    player_input = input("Enter your move (or 'D' for directions): ")

    if player_input.upper() == 'C':
        cheating(pit_one, pit_two, wumpus_arg, person_arg)
    elif player_input.upper() == 'D':
        directions()
    elif player_input.upper() == 'R':
        cheating(pit_one, pit_two, wumpus_arg, person_arg)
        reset_input = input("Enter the room locations (1..20) for player, wumpus, pit1, and pit2: ")
        int_list = [int(x) for x in reset_input.split()]
        reset(wumpus_game, pit_one, pit_two, wumpus_arg, person_arg, int_list)
        cheating(pit_one, pit_two, wumpus_arg, person_arg)
        print(wumpus_game.available_positions())
    elif player_input.upper() == 'G':
        guess_wumpus_input = input("Enter room (1..20) you think Wumpus is in: ")
        if guess_wumpus_input == wumpus_arg.get_position():
            print("You won!")
            print("\nExiting Program ...")
        else:
            print("You lost!")
            print("\nExiting Program ...")
        sys.exit()
    elif player_input.upper() == 'M':
        player_move_input = input("Enter the room number you wish to move to: ")
        if wumpus_game.is_adj_move_valid(person_arg.get_position(), player_move_input):
            print(f"You are in room {player_move_input}")
        else:
            print("Invalid move")
    elif player_input.upper() == 'X':
        sys.exit()
    else:
        print("Invalid move. Try again")


def reset(g, p1, p2, w, p, list_positions):
    """Used to reset the current pos of each character"""

    # first, get the current pos for later
    curr_p1_pos = p1.get_position()
    new_p1 = p1.set_reset_position(g, list_positions[0])
    if new_p1 is not None:
        g.update_available_positions(p1, new_p1)
        g.cave[curr_p1_pos].type_character = None
    else:
        return

    curr_p2_pos = p2.get_position()
    new_p2 = p2.set_reset_position(g, list_positions[1])
    if new_p2 is not None:
        g.update_available_positions(p2, new_p2)
        g.cave[curr_p2_pos].type_character = None
    else:
        return

    curr_w_pos = w.get_position()
    new_w = w.set_reset_position(g, list_positions[2])
    if new_w is not None:
        g.update_available_positions(w, new_w)
        g.cave[curr_w_pos].type_character = None
    else:
        return

    curr_p_pos = p.get_position()
    new_p = p.set_reset_position(g, list_positions[3])
    if new_p is not None:
        g.update_available_positions(p, new_p)
        g.cave[curr_p_pos].type_character = None
    else:
        return


def cheating(p1, p2, w, p):
    """Print this when the player cheats"""
    print("Cheating! Game elements are in the following rooms:")
    print(
        f"Player: {p.get_position()} | "
        f"Wumpus: {w.get_position()} | "
        f"Pit one: {p1.get_position()} | "
        f"Pit two: {p2.get_position()} | "
    )

def directions():
    """directions for Wumpus Game"""
    instructions = """
    Hunt the Wumpus:                                             
    The Wumpus lives in a completely dark cave of 20 rooms. Each 
    room has 3 tunnels leading to other rooms.                   

    Hazards:                                                     
    1. Two rooms have bottomless pits in them.  If you go there you fall and die.   
    2. The Wumpus is not bothered by the pits, as he has sucker feet. Usually he is 
    asleep. He will wake up if you enter his room. When you move into the Wumpus'
    room, then he wakes and moves if he is in an odd-numbered room, but stays    
    still otherwise.  After that, if he is in your room, he snaps your neck and  
    you die!                                                                     

    Moves:                                                                          
    On each move you can do the following, where input can be upper or lower-case:  
    1. Move into an adjacent room.  To move enter 'M' followed by a space and       
    then a room number.                                                          
    2. Enter 'R' to reset the person and hazard locations, useful for testing.      
    3. Enter 'C' to cheat and display current board positions.                      
    4. Enter 'D' to display this set of instructions.                               
    5. Enter 'P' to print the maze room layout.                                     
    6. Enter 'G' to guess which room Wumpus is in, to win or lose the game!         
    7. Enter 'X' to exit the game.                                                  

    Good luck!
    """
    print(instructions)

def set_postion_helper(game, p1, p2, w, p):
    """Helper function to set positions and update cave"""
    pit1_initial_pos = p1.set_random_position(game)
    game.update_available_positions(p1, pit1_initial_pos)

    pit2_initial_pos = p2.set_random_position(game)
    game.update_available_positions(p2, pit2_initial_pos)

    wumpus_initial_pos = w.set_random_position(game)
    game.update_available_positions(w, wumpus_initial_pos)

    person_initial_pos = p.set_random_position(game)
    game.update_available_positions(p, person_initial_pos)



if __name__ == '__main__':
    new_game = WumpusGame()
    pit1 = Pit("Pit 1")
    pit2 = Pit("Pit 2")
    wumpus = Wumpus("Wumpus")
    person = Person("Person")

    play(new_game, pit1, pit2, wumpus, person)
