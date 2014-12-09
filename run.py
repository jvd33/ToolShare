import os
import os.path

if os.path.exists("db.sqlite3"):
	print("db found")
	#runs program in background
	os.system("Start /b python tasks.py")
	#runs the server on top of the other process
	os.system("Start /b python manage.py runserver --insecure")
else:
	#syncthe db
	os.system("python manage.py syncdb")
	#seed the db
	os.system("python seed.py")
	#runs program in background
	os.system("Start /b python tasks.py")
	#runs the server on top of the other process
	os.system("Start /b python manage.py runserver --insecure")
