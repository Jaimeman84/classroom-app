import random

class GroupGenerator:
    def __init__(self):
        self.students = []

    def set_students(self, students):
        """Set the list of students"""
        self.students = students.copy()

    def generate_groups(self, num_groups):
        """Generate random groups from the student list"""
        if not self.students or num_groups <= 0 or num_groups > len(self.students):
            return []

        # Create a copy of the student list to shuffle
        students_copy = self.students.copy()
        random.shuffle(students_copy)

        # Calculate the minimum size of each group
        base_size = len(students_copy) // num_groups
        extras = len(students_copy) % num_groups

        # Create groups
        groups = []
        start = 0
        for i in range(num_groups):
            # Add one extra student to some groups if there are extras
            group_size = base_size + (1 if i < extras else 0)
            groups.append(students_copy[start:start + group_size])
            start += group_size

        return groups