## Patch 1.4 notes:
- made error messages less shit for !beat and !confirm commands
- made table rendering more robust since someone kept adding characters to his chess profile and breaking the discord character limit
- fixed previous error where a boss of 2 ladders would lose his role upon losing position on one of the ladders
- ladder boss role is automatic now
- wintracking now included for ladder boss

## Patch 1.3 notes:
- automanages ladder boss role

## Patch 1.2 notes:
- new ladder display shortcuts: !l for basic display, !ld for ladderDetailed, !ls for ladderStats (just doing my job to save yall's hands :D)
- added w/l stats, so you guys will need to start entering scores in the !beat and !confirm commands. It's basically !beat @opponent score game, where score is in the format 'x-y'. E.g. "!beat @seen 3-0 melee". You'll also have to confirm the score in the same way. See !help for more details.
- melee stats were getting over the 2k character limit, so I split up long tables.
Devnote: now gitignoring .pkl files to reduce the chance of accidentally wiping all the data
- spreadsheet updating should be fixed... i hope...

## Patch 1.1 notes:
- new admin commands (for illuminati, not ladder managers):
    - 'addLadder': pretty self explanatory
        - you'll need to manually create a tab and format it in the google spreadsheet. Make sure to
        use the same format as the previous 
    - 'removeLadder': also self explanatory
    - 'changeLadderName: changes name of a ladder
- new general commands:
    - 'ladderDetailed': provides detailed ladder info on players
    - 'ladderStats': provides ladder statistics (only one stat for now, more coming)
Note: smush is now to be known as ssbu, please use this keyword exclusively in the future
