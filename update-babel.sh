#THIS PROBABLY WORKS ONLY ON LINUX SYSTEMS
pybabel extract -F aquaurban/babel.cfg -o aquaurban/messages.pot . 			#register in "aquaurban/messages.pot" all gettext() in python and _() in jinja2
pybabel update -i aquaurban/messages.pot -d aquaurban/translations -l pt 	#update a portuguese (pt) translation text file
pybabel compile -d aquaurban/translations 									#compile all translations into binary files