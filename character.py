"""
    Character class to keep track of the different game object like
    pit, wumpus, and person.
"""
import random

class Character:
    """character parent class"""
    def __init__(self, name):
        self.position = 0
        self.name = name

    def set_random_position(self, current_game):
        """Randomly set the initial position of the Pit"""
        options = current_game.available_positions()
        initial_pos = random.choice(options)
        self.position = initial_pos
        return initial_pos

    def get_position(self):
        """Used to get current object position"""
        return self.position

    def set_position(self, postion_val):
        """Used to set position"""
        self.position = postion_val

    def set_reset_position(self, current_game, cave_position):
        """
            Used to set the position to a specific poition
            when user decides to to reset the positions
        """
        options = current_game.available_positions()
        if cave_position not in options:
            print(
                f"You cannot set {self.name} in that position "
                f"because that position contains a character"
            )
            return None
        self.position = cave_position
        return cave_position


class Pit(Character):
    """Pit class"""

class Wumpus(Character):
    """Wumpus class"""

class Person(Character):
    """Person class"""
