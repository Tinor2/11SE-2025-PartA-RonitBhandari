"""
Damaged Maintenance Droid module for Orbital Station Escape.

This module contains the DamagedMaintenanceDroid class which represents the
malfunctioning droid that blocks the player's path in the game.
"""


class DamagedMaintenanceDroid:
    """Represents a malfunctioning maintenance droid that blocks the player's path.

    Attributes:
        blocking (bool): Whether the droid is currently blocking the path.
    """

    def __init__(self):
        """Initializes the droid in a blocking state."""
        self.blocking = True

    def repair(self) -> None:
        """Repairs the droid, so it no longer blocks the path."""
        self.blocking = False

    def is_blocking(self) -> bool:
        """Checks if the droid is blocking the path.

        Returns:
            True if the droid is blocking, False otherwise.
        """
        return self.blocking
