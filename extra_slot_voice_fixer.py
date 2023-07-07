import sys
import json
from os import path, listdir
from getpass import getpass

def safe_listdir(d):
    if path.isdir(d):
        return listdir(d)
    return []

def file_is_audio(filename):
	return path.splitext(filename)[1] == ".nus3audio"

def file_is_bank(filename):
	return path.splitext(filename)[1] == ".nus3bank"

def file_is_cheer(filename):
	return "_cheer" in path.basename(filename)

def pluralize(base, num, singularSuffix="", pluralSuffix="s"):
    return base+singularSuffix if num == 1 else base+pluralSuffix

def yes_or_no(question):
    while True:
        reply = str(input(question+' (y/n): ')).lower().strip()
        if reply[:1] == 'y':
            return True
        if reply[:1] == 'n':
            return False

def main():
    # Get the paths to the folders that are provided as command-line arguments
    all_paths = [arg for arg in sys.argv if path.isdir(arg) and path.isfile(path.join(arg, "config.json"))]
    if len(all_paths) == 0:
        print("Valid mod folders not provided. Drag and drop them onto the EXE.")
        getpass("Press Enter to exit.")
        sys.exit()
    print(f"{len(all_paths)} valid mod " + pluralize("folder", len(all_paths)) + " provided.")
    for p in all_paths:
        print(path.basename(p))
    print("")
    response = yes_or_no("Continue?")
    if response == False:
        print("Action cancelled.")
        getpass("Press Enter to exit.")
        sys.exit()

    for mod_folder_path in all_paths:
        print("\n" + path.basename(mod_folder_path))
        config_file_path = path.join(mod_folder_path, "config.json")

        # Get other mod files
        mod_sound_dir = path.join(mod_folder_path, "sound", "bank")
        mod_sound_dir_se = path.join(mod_sound_dir, "fighter")
        mod_sound_dir_voice = path.join(mod_sound_dir, "fighter_voice")
        mod_contains_se_nus3audio = any([file_is_audio(f) for f in safe_listdir(mod_sound_dir_se)])
        mod_contains_se_nus3bank = any([file_is_bank(f) for f in safe_listdir(mod_sound_dir_se)])
        mod_contains_vc_nus3audio = any([(file_is_audio(f) and not file_is_cheer(f)) for f in safe_listdir(mod_sound_dir_voice)])
        mod_contains_vc_nus3bank = any([(file_is_bank(f) and not file_is_cheer(f)) for f in safe_listdir(mod_sound_dir_voice)])
        mod_contains_cheer_nus3audio = any([(file_is_audio(f) and file_is_cheer(f)) for f in safe_listdir(mod_sound_dir_voice)])
        mod_contains_cheer_nus3bank = any([(file_is_bank(f) and file_is_cheer(f)) for f in safe_listdir(mod_sound_dir_voice)])

        print(f"Sound Effect nus3audio: {mod_contains_se_nus3audio}")
        print(f"Sound Effect nus3bank:  {mod_contains_se_nus3bank}")
        print(f"Voice nus3audio:        {mod_contains_vc_nus3audio}")
        print(f"Voice nus3bank:         {mod_contains_vc_nus3bank}")
        print(f"Cheer nus3audio:        {mod_contains_cheer_nus3audio}")
        print(f"Cheer nus3bank:         {mod_contains_cheer_nus3bank}")

        # Read the config JSON file
        with open(config_file_path, 'r') as file:
            data = json.load(file)

        # Check if the "share-to-vanilla" key exists in the config
        if 'share-to-vanilla' in data:
            # Get the value associated with the "share-to-vanilla" key
            share_to_vanilla = data['share-to-vanilla']

            # Check if the value is a dictionary
            if isinstance(share_to_vanilla, dict):
                # Remove entries ending with "nus3audio"
                print(f"Old share_to_vanilla size: {len(share_to_vanilla.keys())}")
                share_to_vanilla = {
                    key: value for key, value in share_to_vanilla.items()
                    if not (
                        (mod_contains_se_nus3audio and file_is_audio(key) and "/fighter/se_" in key)
                        or (mod_contains_se_nus3bank and file_is_bank(key) and "/fighter/se_" in key)
                        or (mod_contains_vc_nus3audio and file_is_audio(key) and not file_is_cheer(key) and "/fighter_voice/vc_" in key)
                        or (mod_contains_vc_nus3bank and file_is_bank(key) and not file_is_cheer(key) and "/fighter_voice/vc_" in key)
                        or (mod_contains_cheer_nus3audio and file_is_audio(key) and file_is_cheer(key) and "/fighter_voice/vc_" in key)
                        or (mod_contains_cheer_nus3bank and file_is_bank(key) and file_is_cheer(key) and "/fighter_voice/vc_" in key)
                    )
                }
                print(f"New share_to_vanilla size: {len(share_to_vanilla.keys())}")

                # Update the JSON data with the modified "share-to-vanilla" value
                data['share-to-vanilla'] = share_to_vanilla

                # Save the updated JSON back to the file
                with open(config_file_path, 'w') as file:
                    json.dump(data, file, indent=4)
                    print(f'Updated JSON saved to {config_file_path}')
            else:
                print('The value associated with "share-to-vanilla" is not a dictionary.')
        else:
            print('"share-to-vanilla" key not found in the JSON.')

    print("\nDone.")
    getpass("Press Enter to exit.")

if __name__ == '__main__':
    main()