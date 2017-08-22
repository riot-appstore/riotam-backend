import os, errno, sys, time, shutil
import db_config as config
import MySQLdb

# enum-like construct
class ArgumentMode:
	Modules, Device = range(2)

def main(cmd):
	
	cmd = remove_unnecessary_spaces(cmd)
	
	args = cmd.split(" ")
	
	# dictionary as replacement for switch-case
	switcher = {
		"--modules": ArgumentMode.Modules,
		"--device": ArgumentMode.Device,
	}
	
	modules = []
	device = "native"
	
	current_mode  = None
	for arg in args:
		
		new_mode = switcher.get(arg, None)
		
		if current_mode is None and new_mode is None:
			print "error, wrong commands"
			break
			
		elif new_mode is not None:
			current_mode = new_mode
			
		else:
			if current_mode == ArgumentMode.Modules:
				modules.append(arg)
				
			elif current_mode == ArgumentMode.Device:
				device = arg
				
	if len(modules) == 0:
		print "no module selected!"
		
	else:

		parent_path = "RIOT/generated_by_riotam/"
		# unique application directory name, TODO: using locks to be safe
		application_path = "application{!s}/".format(time.time())
		full_path = parent_path + application_path
		
		create_directories(full_path)
		os.chdir(full_path)
		
		write_makefile(device, modules)
		
		execute_makefile()
					
		time.sleep(5)		
		shutil.rmtree("../" + application_path)
	
def remove_unnecessary_spaces(string):
	
	while "  " in string:
		string = string.replace("  ", " ")
		
	return string

def get_module_name(id):
	
	db = MySQLdb.connect(config.db_config["host"], config.db_config["user"], config.db_config["passwd"], config.db_config["db"])

	# cursor object to execute queries
	db_cursor = db.cursor(cursorclass=MySQLdb.cursors.DictCursor)

	db_cursor.execute("SELECT name FROM modules WHERE id=%s", (id,))
	results = db_cursor.fetchall()

	db_cursor.close()
	db.close()
	
	if len(results) != 1:
		"error in database: len(results != 1)"
		return None
	else:
		return results[0]["name"]
	
def create_directories(path):
	
	try:
		os.makedirs(path)

	except OSError as e:

		if e.errno != errno.EEXIST:
			raise
			
def write_makefile(device, modules):
	
	filename = "Makefile"
	with open(filename, "w") as makefile:

		makefile.write("APPLICATION = generated_test_application")
		makefile.write("\n\n")

		# TODO: check, if device is in database!!!
		makefile.write("BOARD ?= {!s}".format(device))
		makefile.write("\n\n")

		makefile.write("RIOTBASE ?= $(CURDIR)/../..")
		makefile.write("\n\n")

		for module in modules:
			module_name = get_module_name(module)

			if module_name is None:
				print "error while reading modules from database"
				break

			else :
				makefile.write("USEMODULE += {!s}\n".format(module_name))

		makefile.write("\n")
		makefile.write("include $(RIOTBASE)/Makefile.include")
		
def execute_makefile():
	
	return

if __name__ == "__main__":
	main(sys.argv[1])