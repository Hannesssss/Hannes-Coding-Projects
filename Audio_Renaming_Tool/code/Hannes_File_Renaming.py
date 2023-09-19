import os

# Function to rename .wav and .mp3 files in a specified folder based on user input
def rename_audio_files_interactively(folder_path, renaming_pattern, revert_dict=None):
    # Check if the specified folder exists
    if not os.path.exists(folder_path):
        print(f"The folder '{folder_path}' does not exist.")
        return

    # Get a list of all items in the folder (files and directories)
    items = os.listdir(folder_path)

    # Initialize an index for renaming
    index = 1

    # Define a list of system-related file prefixes to skip
    system_files_to_skip = ['NTUSER.', 'ntuser.', 'Desktop.ini', 'thumbs.db']

    # Create a dictionary to store original and renamed filenames
    original_to_renamed = {}

    # Iterate through the items and rename .wav and .mp3 files based on the pattern
    for item in items:
        item_path = os.path.join(folder_path, item)
        
        # Check if the item is a regular file (not a directory), doesn't match any system file prefix,
        # and has a .wav or .mp3 extension
        if (
            os.path.isfile(item_path) and
            not any(item.startswith(prefix) for prefix in system_files_to_skip) and
            (item.lower().endswith('.wav') or item.lower().endswith('.mp3'))
        ):
            # Create the new name by combining the pattern, index, and original file extension
            new_name = f"{renaming_pattern}{index}"

            # Ensure the new name has the correct file extension (.wav or .mp3)
            if item.lower().endswith('.wav'):
                new_name += '.wav'
            elif item.lower().endswith('.mp3'):
                new_name += '.mp3'

            # Construct the old and new paths for renaming
            old_path = item_path
            new_path = os.path.join(folder_path, new_name)

            # Rename the file using os.rename
            os.rename(old_path, new_path)

            # Store the mapping of original to renamed filenames
            original_to_renamed[item] = new_name

            # Print a message to show the renaming operation
            print(f"Renamed '{item}' to '{new_name}'")

            index += 1

    # If a revert dictionary is provided, update it with the renaming information
    if revert_dict is not None:
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
    print("3. Revert changes.")
    print("4. Exit.")
    return input("Enter your choice (1/2/3/4): ")

# Main program loop
folder_path = ""
renaming_pattern = ""

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

        renaming_pattern = input("Enter the renaming pattern: ")

        # Check if the user is renaming a large number of files
        num_files = len([item for item in os.listdir(folder_path) if item.lower().endswith('.wav') or item.lower().endswith('.mp3')])
        if num_files >= 100:
            confirmation = input(f"Warning: You are about to rename {num_files} files. Continue? Yes or No? (Y/N): ").strip().lower()
            if confirmation != "y":
                print("Renaming operation canceled.")
                continue

        rename_audio_files_interactively(folder_path, renaming_pattern)

        # After renaming is done, display the secondary menu
        while True:
            secondary_choice = secondary_menu()

            if secondary_choice == '1':
                # User wants to re-run with a different naming pattern
                renaming_pattern = input("Enter a new renaming pattern: ")
                rename_audio_files_interactively(folder_path, renaming_pattern)  # Call the function again with the new pattern.
                continue
            elif secondary_choice == '2':
                # User wants to select a new folder and rename files
                folder_path = input("Enter a new folder path: ")
                renaming_pattern = input("Enter a new renaming pattern: ")
                rename_audio_files_interactively(folder_path, renaming_pattern)  # Call the function again with the new folder and pattern.
                break
            elif secondary_choice == '3':
                # User wants to revert changes
                revert_dict = {}
                rename_audio_files_interactively(folder_path, renaming_pattern, revert_dict)
                print("Reverted changes.")
                continue
            elif secondary_choice == '4':
                # User wants to exit
                break
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4 in the menu.")
        
    elif initial_choice == '2':
        # User wants to exit the program
        break
    else:
        print("Invalid choice. Please enter 1 or 2 in the initial menu.")
1