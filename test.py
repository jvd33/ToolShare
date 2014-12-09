import shutil

shutil.copy2("testfactory.py","messageBoard/testfactory.py")
shutil.copy2("testfactory.py","userManagement/testfactory.py")
shutil.copy2("testfactory.py","toolshareapp/testfactory.py")
shutil.copy2("testfactory.py","userMessaging/testfactory.py")

# Any file that starts with "test" and ends with .py will be included automatically.
"""
from messageBoard.tests import *
from userManagement.tests import *
from toolshareapp.tests import *
from userMessaging.tests import *
"""
