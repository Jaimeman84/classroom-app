import random
import time

class NamePicker:
    def __init__(self):
        self.names = []

    def add_names(self, names):
        """Add names to the picker"""
        self.names.extend(names)

    def pick_random_name(self):
        """Pick a random name from the list"""
        if not self.names:
            return None
        return random.choice(self.names)

    def remove_name(self, name):
        """Remove a name from the list"""
        if name in self.names:
            self.names.remove(name)