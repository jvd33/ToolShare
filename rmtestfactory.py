"""
If the testfactory.py files within each app (copied from the testfactory.py
from the outer file) accidentally get committed, and if adding them to the
ignore list is too much of a hassle, run this file to get rid of the inner
testfactory.py files before updating or committing code to avoid conflicts.
"""

import os       # Needed for os.remove("file")

exists = True   # Was the file there?

# Inner testfactory.py file locations
inner_file_locs = {
    "messageBoard/testfactory.py",
    "userManagement/testfactory.py",
    "toolshareapp/testfactory.py",
    "userMessaging/testfactory.py"}

# Loop through all existing inner files
for file_loc in inner_file_locs:

    # Represent file location as a readable string
    file_str_tmp = file_loc.split("/")
    file_str = file_str_tmp[1] + " in " + file_str_tmp[0]

    # Will be set to false if the file isn't there. Otherwise, it stays true.
    exists = True

    # Try removing the file. Print error message if the file isn't there.
    try:
        os.remove(file_loc)
    except FileNotFoundError:
        print(file_str + " folder doesn't exist.")
        exists = False

    # If the file was there, print confirmation message.
    if exists:
        print(file_str + " deleted.")
