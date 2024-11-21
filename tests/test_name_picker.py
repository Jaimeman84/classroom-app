import pytest
from src.name_picker import NamePicker

def test_add_names():
    picker = NamePicker()
    names = ["Alice", "Bob", "Charlie"]
    picker.add_names(names)
    assert set(picker.names) == set(names)

def test_pick_random_name():
    picker = NamePicker()
    names = ["Alice", "Bob", "Charlie"]
    picker.add_names(names)
    picked_name = picker.pick_random_name()
    assert picked_name in names

def test_remove_name():
    picker = NamePicker()
    names = ["Alice", "Bob", "Charlie"]
    picker.add_names(names)
    picker.remove_name("Bob")
    assert "Bob" not in picker.names
    assert len(picker.names) == 2