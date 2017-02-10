"""
Test file for the different methods that represent events that occur
"""
from setup import *
from search import *
from methods import *
from story import StoryNode

class TestMove:
    """
    Test class for the move method
    """
    def test_move_works_to_different_location(self):
        """
        Tests if actor's place changes to specified location
        """
        ACTORS = {
            "ALICE": {
                "name": "Alice",
                "home": PLACES["ALICES_HOUSE"],
                "place": PLACES["ALICES_HOUSE"],
                "health": 10,
                "items": [ITEMS["GUN"]],
                "anger": {},
            },
        }

        current_state = StoryNode(ACTORS,PLACES,ITEMS,"",1)
        new_state = move(current_state, "ALICE", "BOBS_HOUSE")

        assert new_state.actors["ALICE"]["place"]["name"] == PLACES["BOBS_HOUSE"]["name"]

    def test_move_to_same_place(self):
        """
        Tests if believability is 0 when moving to same location
        """
        ACTORS = {
            "ALICE": {
                "name": "Alice",
                "home": PLACES["ALICES_HOUSE"],
                "place": PLACES["ALICES_HOUSE"],
                "health": 10,
                "items": [ITEMS["GUN"]],
                "anger": {},  # dictionary of other actors to their anger value
            },
        }

        current_state = StoryNode(ACTORS,PLACES,ITEMS,"",1)
        new_state = move(current_state, "ALICE", "ALICES_HOUSE")

        assert new_state.believability == 0

    def test_move_when_dead(self):
        """
        Tests if believability is 0 when moving while dead
        """
        ACTORS = {
            "ALICE": {
                "name": "Alice",
                "home": PLACES["ALICES_HOUSE"],
                "place": PLACES["ALICES_HOUSE"],
                "health": 0,
                "items": [ITEMS["GUN"]],
                "anger": {},  # dictionary of other actors to their anger value
            },
        }

        current_state = StoryNode(ACTORS,PLACES,ITEMS,"",1)
        new_state = move(current_state, "ALICE", "BOBS_HOUSE")

        assert new_state.believability == 0


class TestSteal:
    """
    Test class for the steal method
    """
    def test_steal_works(self):
        """
        Tests if steal successfully transfers items from actor_b to actor_a
        """
        ACTORS = {
            "ALICE": {
                "name": "Alice",
                "home": PLACES["ALICES_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [ITEMS["GUN"]],
                "anger": {},  # dictionary of other actors to their anger value
            },
            "BOB": {
                "name": "Bob",
                "home": PLACES["BOBS_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [ITEMS["VASE"]],
                "anger": {},
            },
        }
        current_state = StoryNode(ACTORS,PLACES,ITEMS,"",1)
        new_state = steal(current_state, "ALICE", "BOB")
        a_items = new_state.actors["ALICE"]["items"]
        b_items = new_state.actors["BOB"]["items"]
        assert (len(b_items) == 0 and
                len(a_items) == 2 and
                a_items[1] == ITEMS["VASE"])

    def test_steal_believability_works(self):
        """
        Tests if steal outputs proper believability
        """
        ACTORS = {
            "ALICE": {
                "name": "Alice",
                "home": PLACES["ALICES_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [ITEMS["GUN"]],
                "anger": {},  # dictionary of other actors to their anger value
            },
            "BOB": {
                "name": "Bob",
                "home": PLACES["BOBS_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [ITEMS["VASE"]],
                "anger": {},
            },
        }
        current_state = StoryNode(ACTORS,PLACES,ITEMS,"",1)
        new_state = steal(current_state, "ALICE", "BOB")
        a_items = new_state.actors["ALICE"]["items"]
        b_items = new_state.actors["BOB"]["items"]
        assert new_state.believability == ITEMS["VASE"]["value"]

    def test_steal_on_no_items(self):
        """
        Tests if believability is 0 when victim has no items
        """
        ACTORS = {
            "ALICE": {
                "name": "Alice",
                "home": PLACES["ALICES_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [ITEMS["GUN"]],
                "anger": {},  # dictionary of other actors to their anger value
            },
            "BOB": {
                "name": "Bob",
                "home": PLACES["BOBS_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [],
                "anger": {},
            },
        }
        current_state = StoryNode(ACTORS,PLACES,ITEMS,"",1)
        new_state = steal(current_state, "ALICE", "BOB")
        assert new_state.believability == 0

    def test_steal_when_dead(self):
        """
        Tests if believability is 0 when stealer is dead
        """
        ACTORS = {
            "ALICE": {
                "name": "Alice",
                "home": PLACES["ALICES_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 0,
                "items": [ITEMS["GUN"]],
                "anger": {},  # dictionary of other actors to their anger value
            },
            "BOB": {
                "name": "Bob",
                "home": PLACES["BOBS_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [],
                "anger": {},
            },
        }
        current_state = StoryNode(ACTORS,PLACES,ITEMS,"",1)
        new_state = steal(current_state, "ALICE", "BOB")
        assert new_state.believability == 0

    def test_steal_from_dead(self):
        """
        Tests if items can be stolen from dead actor
        """
        ACTORS = {
            "ALICE": {
                "name": "Alice",
                "home": PLACES["ALICES_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [ITEMS["GUN"]],
                "anger": {},  # dictionary of other actors to their anger value
            },
            "BOB": {
                "name": "Bob",
                "home": PLACES["BOBS_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 0,
                "items": [ITEMS["VASE"]],
                "anger": {},
            },
        }
        current_state = StoryNode(ACTORS,PLACES,ITEMS,"",1)
        new_state = steal(current_state, "ALICE", "BOB")
        a_items = new_state.actors["ALICE"]["items"]
        b_items = new_state.actors["BOB"]["items"]
        assert (len(b_items) == 0 and
                len(a_items) == 2 and
                a_items[1] == ITEMS["VASE"])

    def test_steal_when_different_locations(self):
        """
        Tests if believability is 0 when actors are in different locations
        """
        ACTORS = {
            "ALICE": {
                "name": "Alice",
                "home": PLACES["ALICES_HOUSE"],
                "place": PLACES["ALICES_HOUSE"],
                "health": 10,
                "items": [ITEMS["GUN"]],
                "anger": {"BOB": 3},
            },
            "BOB": {
                "name": "Bob",
                "home": PLACES["BOBS_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [ITEMS["VASE"]],
                "anger": {"ALICE": -1},
            },
        }
        current_state = StoryNode(ACTORS,PLACES,ITEMS,"",1)
        new_state = steal(current_state, "ALICE", "BOB")

        assert new_state.believability == 0


class TestPlay:
    """
    Test class for the play method
    """
    def test_play_works_when_empty(self):
        """
        Tests if play creates new entries in the anger dictionary and assigns
        appropriate values
        """
        ACTORS = {
            "ALICE": {
                "name": "Alice",
                "home": PLACES["ALICES_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [ITEMS["GUN"]],
                "anger": {},  # dictionary of other actors to their anger value
            },
            "BOB": {
                "name": "Bob",
                "home": PLACES["BOBS_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [ITEMS["VASE"]],
                "anger": {},
            },
        }
        current_state = StoryNode(ACTORS,PLACES,ITEMS,"",1)
        new_state = play(current_state, "ALICE", "BOB")

        assert (new_state.actors["ALICE"]["anger"]["BOB"] == -1 and
                new_state.actors["BOB"]["anger"]["ALICE"] == -1)

    def test_play_works_with_values(self):
        """
        Tests if play assigns appropriate values when already in place
        """
        ACTORS = {
            "ALICE": {
                "name": "Alice",
                "home": PLACES["ALICES_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [ITEMS["GUN"]],
                "anger": {"BOB": 3},
            },
            "BOB": {
                "name": "Bob",
                "home": PLACES["BOBS_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [ITEMS["VASE"]],
                "anger": {"ALICE": -1},
            },
        }
        current_state = StoryNode(ACTORS,PLACES,ITEMS,"",1)
        new_state = play(current_state, "ALICE", "BOB")

        assert (new_state.actors["ALICE"]["anger"]["BOB"] == 2 and
                new_state.actors["BOB"]["anger"]["ALICE"] == -2)

    def test_play_when_different_locations(self):
        """
        Tests if believability is 0 when actors are in different locations
        """
        ACTORS = {
            "ALICE": {
                "name": "Alice",
                "home": PLACES["ALICES_HOUSE"],
                "place": PLACES["ALICES_HOUSE"],
                "health": 10,
                "items": [ITEMS["GUN"]],
                "anger": {"BOB": 3},
            },
            "BOB": {
                "name": "Bob",
                "home": PLACES["BOBS_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [ITEMS["VASE"]],
                "anger": {"ALICE": -1},
            },
        }
        current_state = StoryNode(ACTORS,PLACES,ITEMS,"",1)
        new_state = play(current_state, "ALICE", "BOB")

        assert new_state.believability == 0


class TestKill:
    """
    Test class for the kill method
    """
    def test_kill_works(self):
        """
        Tests if actor_b gets killed
        """
        ACTORS = {
            "ALICE": {
                "name": "Alice",
                "home": PLACES["ALICES_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [ITEMS["GUN"]],
                "anger": {},  # dictionary of other actors to their anger value
            },
            "BOB": {
                "name": "Bob",
                "home": PLACES["BOBS_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [ITEMS["VASE"]],
                "anger": {},
            },
        }

        current_state = StoryNode(ACTORS,PLACES,ITEMS,"",1)
        new_state = kill(current_state, "ALICE", "BOB")
        assert new_state.actors["BOB"]["health"] == 0

    def test_kill_when_different_locations(self):
        """
        Tests if believability is 0 when actors are in different locations
        """
        ACTORS = {
            "ALICE": {
                "name": "Alice",
                "home": PLACES["ALICES_HOUSE"],
                "place": PLACES["ALICES_HOUSE"],
                "health": 10,
                "items": [ITEMS["GUN"]],
                "anger": {"BOB": 3},
            },
            "BOB": {
                "name": "Bob",
                "home": PLACES["BOBS_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [ITEMS["VASE"]],
                "anger": {"ALICE": -1},
            },
        }
        current_state = StoryNode(ACTORS,PLACES,ITEMS,"",1)
        new_state = kill(current_state, "ALICE", "BOB")

        assert new_state.believability == 0
