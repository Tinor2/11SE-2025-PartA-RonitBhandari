# Orbital Station Escape - Story Progression

## Overview
A text-based adventure game where the player takes on the role of an engineer trying to escape from an orbital space station. The game features multiple locations, items to collect, and obstacles to overcome.

## Game Locations

### 1. Maintenance Tunnels (Starting Point)
- **Initial State**:
  - Flickering lights reveal a sparking droid blocking the east tunnel
  - A diagnostic tool lies on the floor
  - The droid is beeping angrily

### 2. Docking Bay
- **Features**:
  - Zero-gravity environment
  - Floating debris
  - Shattered window
  - Energy Crystal lodged in the wall
  - Escape pod with jammed hatch due to broken gravity generators

### 3. Launch Pad (Final Area)
- **Features**:
  - Escape pod ready for launch
  - Control panel with various dials and measures

## Game Progression

### Phase 1: The Blocked Path
1. Player starts in the Maintenance Tunnels
2. Must pick up the Diagnostic Tool (+10 points)
3. Attempting to move east triggers the droid encounter

### Phase 2: The Malfunctioning Droid
1. First attempt to pass results in being shoved back (+1 Hazard)
2. Player must use the Diagnostic Tool on the droid
3. Successful repair makes the droid move aside (+20 points)

### Phase 3: The Docking Bay Puzzle
1. Player enters the zero-gravity Docking Bay
2. Must collect the Energy Crystal
3. Crystal resets the gravity when picked up (+50 points)

### Phase 4: Escape
1. Player reaches the Launch Pad
2. Types "win" to launch the escape pod
3. Game completes with final score calculation

## Scoring System
- Picking up Diagnostic Tool: +10 points
- Fixing the droid: +20 points
- Collecting Energy Crystal: +50 points
- Hazard points are tracked but don't reduce score
- Bonus points: +30 for completing the game

## Commands
- `pick up [item]`: Collect items
- `use [item]`: Use an item from inventory
- `move [direction]`: Move in specified direction
- `look`: Examine current location
- `inventory`: View carried items
- `win`: Final command to escape (only available at launch pad)

## Victory Conditions
- Successfully reach the launch pad
- Type "win" to initiate escape sequence
- Final score is calculated based on points earned and hazards encountered
