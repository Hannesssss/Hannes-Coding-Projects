import os

# Function to rename .wav and .mp3 files in a specified folder based on user input
def rename_audio_files_interactively(folder_path, renaming_pattern, original_filenames, revert_dict, append_eng=False):
    # Check if the specified folder exists
    if not os.path.exists(folder_path):
        print(f"The folder '{folder_path}' does not exist.")
        return

    # Get a list of all items in the folder (files and directories)
    items = os.listdir(folder_path)

    # Initialize a dictionary to keep track of renamed files
    renamed_files = {}

    # Define a list of system-related file prefixes to skip
    system_files_to_skip = ['NTUSER.', 'ntuser.', 'Desktop.ini', 'thumbs.db']

    # Store the original filenames and paths before any renaming
    original_to_renamed = {item: os.path.join(folder_path, item) for item in items if item.lower().endswith('.wav') or item.lower().endswith('.mp3')}

    # Reset the current index when a new prefix is specified
    current_index = 1

    # Now that the original filenames are stored, you can proceed with renaming based on the user's input pattern.
    for item, item_path in original_to_renamed.items():
        # Create the new name based on the user's input prefix and whether to append "_ENG"
        new_name = renaming_pattern + str(current_index)

        # Append "_ENG" to filenames if requested
        if append_eng:
            new_name += "_ENG"

        # Ensure the new name has the correct file extension (.wav or .mp3)
        if item.lower().endswith('.wav'):
            new_name += '.wav'
        elif item.lower().endswith('.mp3'):
            new_name += '.mp3'

        # Handle cases where the new name already exists
        while new_name in renamed_files:
            current_index += 1
            new_name = renaming_pattern + str(current_index)
            if append_eng:
                new_name += "_ENG"
            if item.lower().endswith('.wav'):
                new_name += '.wav'
            elif item.lower().endswith('.mp3'):
                new_name += '.mp3'

        # Add the new name to the dictionary of renamed files
        renamed_files[new_name] = 1

        # Construct the old and new paths for renaming
        old_path = item_path  # Use the original filename here
        new_path = os.path.join(folder_path, new_name)

        # Rename the file using os.rename
        os.rename(old_path, new_path)

        # Print a message to show the renaming operation
        print(f"Renamed '{item}' to '{new_name}'")

        # Update the revert dictionary with the renaming information
        revert_dict.update({new_path: item_path})  # Store the new path and the original path

        # Increment the current index for the prefix
        current_index += 1

    # Update the revert dictionary with the renaming information
    revert_dict.update(original_to_renamed)

# Function to display the initial menu and get the user's choice
def initial_menu():
    print("Hannes Audio Renaming Tool")
    print("This tool renames .wav and .mp3 files in a specified folder.")
    print("1. Select folder to rename files.")
    print("2. Exit.")
    return input("Enter your choice (1/2): ")

# Function to display the secondary menu and get the user's choice
def secondary_menu():
    print("\nMenu:")
    print("1. Re-run with a different naming pattern.")
    print("2. Select a new folder and rename files.")
    print("3. Revert to the previous file name.")
    print("4. Revert changes to original filenames.")
    print("5. Exit.")
    return input("Enter your choice (1/2/3/4/5): ")

# Function to prompt for confirmation
def confirm_revert():
    return input("You are about to revert all changes, continue? Yes or No (Y/N): ").strip().lower() == 'y'

# Main program loop
folder_path = ""
renaming_pattern = ""
original_filenames = {}
revert_dict = {}

while True:
    initial_choice = initial_menu()

    if initial_choice == '1':
        # User wants to select a folder to rename files
        folder_path = input("Enter the folder path where your .wav and .mp3 files are located: ")
        
        # Check for eligible audio files before asking for a renaming pattern
        audio_files_present = False

        for item in os.listdir(folder_path):
            if item.lower().endswith('.wav') or item.lower().endswith('.mp3'):
                audio_files_present = True
                break

        if not audio_files_present:
            print("ERROR: No .wav or .mp3 files found in the specified folder. Nothing to rename.")
            continue  # Skip to the next iteration of the initial menu.

        # Check if the user is renaming a large number of files
        num_files = len([item for item in os.listdir(folder_path) if item.lower().endswith('.wav') or item.lower().endswith('.mp3')])
        if num_files >= 100:
            confirmation = input(f"Warning: You are about to rename {num_files} files. Continue? Yes or No? (Y/N): ").strip().lower()
            if confirmation != "y":
                print("Renaming operation canceled.")
                continue

        # Store the original filenames before any renaming
        original_filenames.clear()
        for item in os.listdir(folder_path):
            if item.lower().endswith('.wav') or item.lower().endswith('.mp3'):
                original_filenames[item] = os.path.join(folder_path, item)

        append_eng = input("Append '_ENG' to filenames? (Y/N): ").strip().lower() == 'y'
        renaming_pattern = input("Enter the desired prefix (e.g., 'A'): ")

        # Reset the current index when a new prefix is specified
        current_index = 1

        rename_audio_files_interactively(folder_path, renaming_pattern, original_filenames, revert_dict, append_eng)

        # After renaming is done, display the secondary menu
        while True:
            secondary_choice = secondary_menu()

            if secondary_choice == '1':
                # User wants to re-run with a different naming pattern
                renaming_pattern = input("Enter a new prefix: ")
                append_eng = input("Append '_ENG' to filenames? (Y/N): ").strip().lower()
                current_index = 1  # Reset the current index when a new prefix is specified
                rename_audio_files_interactively(folder_path, renaming_pattern, original_filenames, revert_dict, append_eng)
                continue
            elif secondary_choice == '2':
                # User wants to select a new folder and rename files
                folder_path = input("Enter a new folder path: ")
                renaming_pattern = input("Enter a new prefix: ")
                append_eng = input("Append '_ENG' to filenames? (Y/N): ").strip().lower()
                original_filenames.clear()
                for item in os.listdir(folder_path):
                    if item.lower().endswith('.wav') or item.lower().endswith('.mp3'):
                        original_filenames[item] = os.path.join(folder_path, item)
                current_index = 1  # Reset the current index when a new folder is selected
                rename_audio_files_interactively(folder_path, renaming_pattern, original_filenames, revert_dict, append_eng)
                break
            elif secondary_choice == '3':
                # User wants to revert to the previous filename
                for new_path, original_path in revert_dict.items():
                    if os.path.exists(new_path):
                        os.rename(new_path, original_path)
                        print(f"Reverted '{new_path}' to '{original_path}'")
                    else:
                        print(f"Failed to revert '{new_path}' to '{original_path}' because the original file does not exist.")
                revert_dict.clear()  # Clear the revert dictionary
                print("Reverted to the previous file name.")
                continue
            elif secondary_choice == '4':
                # User wants to revert changes to original filenames
                if confirm_revert():
                    for new_path, original_path in revert_dict.items():
                        if os.path.exists(new_path):
                            os.rename(new_path, original_path)
                            print(f"Reverted '{new_path}' to '{original_path}'")
                        else:
                            print(f"Failed to revert '{new_path}' to '{original_path}' because the original file does not exist.")
                    revert_dict.clear()  # Clear the revert dictionary
                    print("Reverted changes to original filenames.")
                else:
                    print("Revert operation canceled.")
                continue
            elif secondary_choice == '5':
                # User wants to exit
                break
            else:
                print("Invalid choice. Please enter 1, 2, 3, 4, or 5 in the menu.")
        
    elif initial_choice == '2':
        # User wants to exit the program
        break
    else:
        print("Invalid choice. Please enter 1 or 2 in the initial menu.")
