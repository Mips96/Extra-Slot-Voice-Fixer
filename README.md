# Extra Slot Voice Fixer for reslotterGUI
[reslotterGUI](https://github.com/CSharpM7/reslotter) v2.5.1 (the latest version at the time of writing this) has a bug where voice mods will not work properly for extra slots, usually muting them. This is because nus3audio and nus3bank entries for sound effects (`sound/bank/fighter/se_CHAR_cXX`), voice (`sound/bank/fighter_voice/vc_CHAR_cXX`), and audience cheer (`sound/bank/fighter_voice/vc_CHAR_cheer_cXX`) are created in the generated config.json in `share-to-vanilla` regardless of whether or not they’re actually needed.

This utility fixes that bug. Simply **drag and drop one or multiple mod folders onto the executable** and it will fix each mod’s config.json by scanning for and removing unneeded entries. Mods that don’t need to be fixed (either because they don’t have audio or have already been fixed) are unaffected.

This will not fix the current (as of now) ARCropolis bug where multiple slots will share the same voice in a ditto match.

## How To Use
1. Use reslotterGUI to change each mod’s slot as desired.
2. Drag and drop your mod folders onto `Extra Slot Voice Fixer.exe` (you can do them all at once as a batch). It will ask for confirmation before doing anything.
3. Each config file will be edited as needed, replacing the original version. A copy of the original will not be made; you shouldn’t need it, but keep it in mind just in case.
