import unittest
from unittest.mock import MagicMock
from player import Player
from location import Location
from damaged_droid import DamagedMaintenanceDroid

class TestPlayer(unittest.TestCase):
    """Test cases for the Player class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create test locations
        self.start = Location("Start", "A starting location.")
        self.other = Location("Docking Bay", "Another location.")
        
        # Connect locations
        self.start.add_exit("east", self.other)
        self.other.add_exit("west", self.start)
        
        # Create a test droid and add to other location
        self.droid = DamagedMaintenanceDroid()
        self.other.droid = self.droid
        self.other.droid_present = True
        
        # Create player
        self.player = Player(self.start)
    
    def test_initial_state(self):
        """Test the player's initial state."""
        self.assertEqual(self.player.current_location, self.start)
        self.assertFalse(self.player.has_tool)
        self.assertFalse(self.player.has_crystal)
        self.assertEqual(self.player.score, 0)
        self.assertEqual(self.player.hazard_count, 0)
    
    def test_move_valid(self):
        """Test moving to a valid location."""
        # Remove droid from the other location for this test
        self.other.droid_present = False
        
        success, message = self.player.move("east")
        self.assertTrue(success)
        self.assertEqual(self.player.current_location, self.other)
        self.assertIn("move east from start to docking bay", message.lower())
    
    def test_move_invalid_direction(self):
        """Test moving in an invalid direction."""
        success, message = self.player.move("north")
        self.assertFalse(success)
        self.assertEqual(self.player.current_location, self.start)
        self.assertIn("no exit", message.lower())
    
    def test_move_blocked_by_droid(self):
        """Test moving when blocked by a droid."""
        # Ensure the droid is blocking
        self.droid.blocking = True
        self.other.droid_present = True
        self.other.droid = self.droid
        
        # Player starts at start location, tries to move to other location with droid
        self.player.current_location = self.start
        
        # Try to move to location with blocking droid
        success, message = self.player.move("east")
        self.assertFalse(success, "Player should not be able to move to a location with a blocking droid")
        self.assertEqual(self.player.hazard_count, 1, "Hazard count should increment when blocked by droid")
        self.assertIn("blocks", message.lower(), "Error message should mention the droid blocking the path")
        self.assertEqual(self.player.current_location, self.start, "Player should still be at the start location")
        
        # Now repair the droid
        self.player.has_tool = True
        # Need to be in the same location as the droid to repair it
        self.player.current_location = self.other
        success, message = self.player.use_tool_on_droid()
        self.assertTrue(success, "Should be able to use tool on droid")
        self.assertFalse(self.droid.is_blocking(), "Droid should no longer be blocking after repair")
        
        # Move back to start location
        self.player.current_location = self.start
        # Now try to move to other location again - should succeed since droid is repaired
        success, message = self.player.move("east")
        self.assertTrue(success, "Player should be able to move to location after droid is repaired")
        self.assertEqual(self.player.current_location, self.other, "Player should have moved to the other location")
    
    def test_pick_up_tool_success(self):
        """Test successfully picking up a tool."""
        self.start.has_tool = True
        success, message = self.player.pick_up_tool()
        self.assertTrue(success)
        self.assertTrue(self.player.has_tool)
        self.assertEqual(self.player.score, 10)
        self.assertIn("pick up", message.lower())
    
    def test_use_tool_on_droid_success(self):
        """Test successfully using the tool on a droid."""
        # Give the player the tool
        self.player.has_tool = True
        
        # Test with explicit droid parameter
        success, message = self.player.use_tool_on_droid(self.droid)
        self.assertTrue(success)
        self.assertEqual(self.player.score, 20)
        self.assertFalse(self.droid.is_blocking())
        self.assertIn("moves aside", message.lower())
        
        # Reset for next test
        self.droid.blocking = True
        self.player.score = 0
        
        # Move to location with droid
        self.player.current_location = self.other
        
        # Test with implicit droid (from current location)
        success, message = self.player.use_tool_on_droid()
        self.assertTrue(success)
        self.assertEqual(self.player.score, 20)
        self.assertFalse(self.droid.is_blocking())
        self.assertIn("moves aside", message.lower())
    
    def test_has_won_conditions(self):
        """Test the winning conditions."""
        # Not in docking bay
        self.assertFalse(self.player.has_won())
        
        # Move to docking bay (without crystal)
        self.player.current_location = self.other  # Docking Bay
        self.player.has_crystal = False
        self.assertFalse(self.player.has_won())
        
        # Has crystal but not in docking bay
        self.player.current_location = self.start  # Not Docking Bay
        self.player.has_crystal = True
        self.assertFalse(self.player.has_won())
        
        # Has crystal and in docking bay with no droid
        self.other.droid_present = False
        self.player.current_location = self.other  # Docking Bay
        self.player.has_crystal = True
        self.assertTrue(self.player.has_won())
        
        # Has crystal and in docking bay with repaired droid
        self.other.droid_present = True
        self.droid.blocking = False
        self.player.current_location = self.other  # Docking Bay
        self.player.has_crystal = True
        self.assertTrue(self.player.has_won())
    
    def test_has_lost_conditions(self):
        """Test the losing conditions."""
        # Not lost yet
        self.player.hazard_count = 5
        self.assertFalse(self.player.has_lost())
        
        # Exactly at max hazards
        self.player.hazard_count = 10
        self.assertTrue(self.player.has_lost())
        
        # Over max hazards
        self.player.hazard_count = 15
        self.assertTrue(self.player.has_lost())


if __name__ == "__main__":
    unittest.main()
