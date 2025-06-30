import unittest
from location import Location
from damaged_droid import DamagedMaintenanceDroid

class TestLocation(unittest.TestCase):
    """Test cases for the Location class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.location = Location("Test Location", "A test location.")
        self.other_location = Location("Other Location", "Another test location.")
        self.droid = DamagedMaintenanceDroid()
    
    def test_add_exit(self):
        """Test adding an exit to another location."""
        self.location.add_exit("east", self.other_location)
        self.assertIn("east", self.location.exits)
        self.assertEqual(self.location.exits["east"], self.other_location)
    
    def test_describe_no_items(self):
        """Test location description with no items."""
        description = self.location.describe()
        self.assertIn("Test Location", description)
        self.assertIn("A test location.", description)
    
    def test_describe_with_tool(self):
        """Test location description with a tool."""
        self.location.has_tool = True
        description = self.location.describe()
        self.assertIn("diagnostic tool", description.lower())
    
    def test_describe_with_crystal(self):
        """Test location description with a crystal."""
        self.location.has_crystal = True
        description = self.location.describe()
        self.assertIn("energy crystal", description.lower())
    
    def test_describe_with_droid(self):
        """Test location description with a droid."""
        self.location.set_droid_present(True, self.droid)
        description = self.location.describe()
        self.assertIn("droid", description.lower())
        self.assertIn("malfunctioning", description.lower())
    
    def test_remove_tool(self):
        """Test removing a tool from the location."""
        self.location.has_tool = True
        self.assertTrue(self.location.remove_tool())
        self.assertFalse(self.location.has_tool)
    
    def test_remove_nonexistent_tool(self):
        """Test removing a tool that isn't there."""
        self.assertFalse(self.location.remove_tool())
    
    def test_remove_crystal(self):
        """Test removing a crystal from the location."""
        self.location.has_crystal = True
        self.assertTrue(self.location.remove_crystal())
        self.assertFalse(self.location.has_crystal)
    
    def test_remove_nonexistent_crystal(self):
        """Test removing a crystal that isn't there."""
        self.assertFalse(self.location.remove_crystal())
    
    def test_set_droid_present(self):
        """Test setting a droid in the location."""
        self.location.set_droid_present(True, self.droid)
        self.assertTrue(self.location.droid_present)
        self.assertIsNotNone(self.location.droid)
    
    def test_set_droid_absent(self):
        """Test removing a droid from the location."""
        self.location.set_droid_present(True, self.droid)
        self.location.set_droid_present(False)
        self.assertFalse(self.location.droid_present)
        # Note: We don't set droid to None to maintain reference for other tests


class TestDamagedMaintenanceDroid(unittest.TestCase):
    """Test cases for the DamagedMaintenanceDroid class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.droid = DamagedMaintenanceDroid()
    
    def test_initial_state(self):
        """Test the initial state of the droid."""
        self.assertTrue(self.droid.is_blocking())
    
    def test_repair(self):
        """Test repairing the droid."""
        result = self.droid.repair()
        self.assertFalse(self.droid.is_blocking())
        self.assertIn("moves aside", result)
    
    def test_double_repair(self):
        """Test repairing an already repaired droid."""
        self.droid.repair()
        result = self.droid.repair()
        self.assertIn("already", result.lower())
    
    def test_examine_blocking(self):
        """Test examining a blocking droid."""
        description = self.droid.examine()
        self.assertIn("sparking", description.lower())
    
    def test_examine_repaired(self):
        """Test examining a repaired droid."""
        self.droid.repair()
        description = self.droid.examine()
        self.assertIn("powered down", description.lower())


if __name__ == "__main__":
    unittest.main()
