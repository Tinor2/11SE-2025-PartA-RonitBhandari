Note that the game has a specific UI element; the game information is displayed in steps like 1) or 3), but when the player interacts with the game, prompts like the ones seen in 2) or 4) are displayed.

1) Maintanance tunnels, introduction
╔══════════════════════════════════════════════════╗  
   MAINTENANCE TUNNELS  
   Flickering lights reveal a sparking droid blocking the east tunnel. 
   << ITEMS: Diagnostic Tool glows on the floor  
<< OBSTACLE:   Droid beeps angrily 
 <<  EXITS: [east]  
╚═════════════════════════════════════════════════╝  
    Note that : 
        The title is displayed
        The description is displayed
        Any existing items are displayed
        Any existing obstacles are displayed
        The exits are displayed
2) The next thing the player must do is pickup the diagnostic tool. When this happens, the following prompt should come up
•••
You grab the diagnostic tool. [+10]
(SCORE: 10 | HAZARDS: 0)
•••
    Note that : 
        The action is displayed
        The correspinding score increase/decrease is displayed
        the overall score is displayed
        all the hazards encountered so far is displayed
3) The game reiterates the current game state
╔══════════════════════════════════════════════════╗  
   MAINTENANCE TUNNELS  
   The droid beeps angrily as you approach the exit. 
<< ITEMS: ~No items are available~  
 << OBSTACLE:   Droid beeps angrily 
<< EXITS: [east]  
╚═════════════════════════════════════════════════╝  
    Note that : 
        The same things from before are displayed
        But the items section of the list is updated

4) The next thing the player will try to do is move east. This will actually cause a hazard from arising. Note that the player doesnt technically have to move east, if the player doesnt do this and instead tries to use the tool they picked up, the game will skip the hazard section
>>  Move East
•••
The droid SHOVES you back! (+1 HAZARD)  
   (SCORE: 10 | HAZARDS: 1)  
•••
    Note that : 
        The same structure in Step 2 is displayed, this time, a hazard is displayed. The score is continuos from the last prompt
5) This time the game reiterates the game state, but instead also provides a hint to nudge the player in the right direction
╔═════════════════════════════════════════════════╗  
   MAINTENANCE TUNNELS  
   The droid beeps angrily as you approach the exit.
<< ITEMS: ~No items are available~  
 << OBSTACLE:   Droid beeps angrily   
  << HINT: use tool to fix it.
 << EXITS: [east] 
╚═════════════════════════════════════════════════╝  
    Note that : 
        The same structure in Step 2 is displayed, this time, a hint is displayed to nudge the player in the right direction
6) The next thing the player will try to do is use the tool. This time, the score will increase when the player successfully fixes the droid
>> Use Tool
•••
Droid reboots! It salutes and shuffles aside. [+20]  
(SCORE: 30 | HAZARDS: 1)
•••
    Note that : 
        The same structure as the other player prompts is shown
        The score is updated
        the history from before remains consistent
7) The maintanence tunnels exit is now unblocked, note that means that there are no longer any obstacles in the way of the exit.
╔════════════════════════════════════════════╗
MAINTENANCE TUNNELS
The corridor to the Docking Bay is now clear.
< ITEMS: ~No items are available~  
 << OBSTACLE: ~No obstacles~   
 << EXITS: [east]
╚════════════════════════════════════════════╝
    Note that:
        The structure is maintained
        The obstacle section is updated
8) The player will now move east, this will take them to the docking bay. The location will therefore change, after this prompt is shown
>> Move East
•••
You enter the DOCKING BAY.
(SCORE: 30 | HAZARDS: 1)
•••
    Note that : 
        History stays consistent. The hazard doesnt disappear.
9) The player enters the docking bay. Although the text is different, the structure is identical to the previous location
╔════════════════════════════════════════════╗
DOCKING BAY
Debris floats with no gravity, near a shattered window.
<< ITEMS: A glowing ENERGY CRYSTAL is lodged in the wall...  
 << OBSTACLE: The escape pod's hatch is lodged shut, thank's to the broken gravity generators  
 << EXITS: [west]
╚════════════════════════════════════════════╝
    Note that : 
        The structure is maintained
        The obstacle section is updated
        The items section is updated
        The exits are updated
10) The player will now try to pickup the energy crystal. This will increase the score
•••
The cyrstal vibrates in your palm. You drop to the ground as the gravity resets! [+50]
(SCORE: 80 | HAZARDS: 1)
•••
11) The players environment updates, as the items section is updated. Note that this is different from earlier, where the item needed to be used to clear the obstacle, but this time just picking up the crystal was fine
╔════════════════════════════════════════════╗
DOCKING BAY
The escape pod hatch glows green - Almost there
<< ITEMS: ~No items available~
 << OBSTACLE: ~No obstacles~ 
<< HINT: Your exit is wide open!
 << EXITS: [west]
╚════════════════════════════════════════════╝
12) The player will now, instead of moving, check his status, as shown in the flowchart. Note that this status request can happen at any point in the code, but this is jsut when im mentioning it. When the status is used, the player will read it, then press any key, and then the previous screen (in dot point 11) will be shown again. This should happen no matter whne the status is requested. Also note, that the player can only request for commands when a location menu is being displayed, they cant ask for a command directly after an action description, they need to wait for the location description to be shown
•••
(SCORE: 80 | HAZARDS: 1)
•••
    Note that : 
        this struture should be what is shown whenever the status is requested by the player
13) Now, after checking his status, his next action will be to move west, which will take him to the final location, the launch pad. The following is the default description of the location
╔════════════════════════════════════════════╗
LAUNCH PAD
The escape pod is ready to launch!
<< ITEMS: ~No items available~
 << OBSTACLE: ~No obstacles~ 
<< HINT: Type win to launch!
 << EXITS: [west]
╚════════════════════════════════════════════╝
    Note that: 
        Hints are being used again
14) The player will now try to win, which will end the game. The following is the default description of the location
    🚀 MISSION COMPLETE!  
    FINAL SCORE: 110 
    HAZARDS ENCOUNTERED: 1  
    "Orbital Station saved. Well done, Engineer."  
    
    Note that: 
        This is the final screen, the game ends after this
        The score is the score that we were seeing, plus an extra 30 points that are a bonus
