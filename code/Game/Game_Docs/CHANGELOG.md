# Changelog

All notable changes to the Orbital Station Escape game will be documented in this file.

## [Unreleased] - 2025-06-30

### Added
- Command pattern implementation for handling player input
- New `commands.py` with command classes for all game actions
- `InputParser` class for processing player input
- Main game loop with command processing
- Support for multiple command aliases (e.g., 'take' and 'pickup')
- Comprehensive help system with command documentation

### Changed
- Refactored Player class to work with new command system
- Updated movement system to properly handle droid blocking
- Improved inventory management system
- Enhanced game messages and feedback
- Restructured game world loading from JSON

### Fixed
- Fixed droid blocking behavior in Maintenance Tunnel
- Resolved issue where player could bypass droid without fixing it
- Fixed item pickup and usage mechanics
- Corrected win condition checking
- Fixed movement between locations
- Addressed potential edge cases in command parsing

### Removed
- Old game loop implementation (replaced with command-based system)
- Redundant code and unused methods
