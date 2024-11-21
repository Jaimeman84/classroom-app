import pytest
from src.group_generator import GroupGenerator

def test_generate_groups():
    generator = GroupGenerator()
    students = ["Alice", "Bob", "Charlie", "David"]
    generator.set_students(students)
    groups = generator.generate_groups(2)
    
    assert len(groups) == 2
    assert sum(len(group) for group in groups) == len(students)
    
    # Check that all students are assigned to a group
    all_students = [student for group in groups for student in group]
    assert set(all_students) == set(students)

def test_generate_groups_invalid_input():
    generator = GroupGenerator()
    students = ["Alice", "Bob", "Charlie"]
    generator.set_students(students)
    
    # Test with invalid number of groups
    assert generator.generate_groups(0) == []
    assert generator.generate_groups(4) == []