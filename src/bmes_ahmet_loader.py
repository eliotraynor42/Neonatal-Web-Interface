# This file adjusts the python path so you can include Ahmet's shared dropbox folder.
# You may make a copy of only this file and place it in your working directory to help automate find & load bmes.py
# The recommended way of including bmes_ahmet is to keep it in your dropbox folder and
# set up BMESAHMETDIR environment variable to point to that folder. See README.txt for
# instructions for setting up this environment variable. If BMESAHMETDIR environment
# variable is not available, this set up code will try current user's (and then all users')
# dropbox folders for a subfolder called bmes.ahmet. If that cannot be found either, we next
# check for a file called '.BMES_AHMETDIR' in current user's home (and then in all users' homes),
# the content of the file '.BMES_AHMETDIR' should contain the folder name where bmes.ahmet is available.
# by Ahmet Sacan.
######################################################################################################


def io_getsubdirs_(dir):
	import os
	if not os.path.isdir(dir): return [];
	return [f.path for f in os.scandir(dir) if not f.name.startswith('.') and f.is_dir()];

def sys_userhomedir_():
	try:
		import pathlib
		return str(pathlib.Path.home());
	except: #pathlib module may not be installed by default if we are using python2
		import os
		return os.path.expanduser('~');

# locate where bmes.ahmet folder is on this computer.
# Here are the locations checked:
# * BMESAHMETDIR environment variable
# * currentUserHome/.BMESAHMETDIR file
# * AllUsersHomes/.BMESAHMETDIR file
# * currentUserHome/Dropbox/bmes.ahmet folder
# * AllUsersHomes/Dropbox/bmes.ahmet folder
def locatebmesahmetdir():
	import os
	if 'BMESAHMETDIR' in os.environ:
		ret=os.environ['BMESAHMETDIR'];
		if os.path.isdir(ret): return ret;

	file=sys_userhomedir_()+'/.BMES_AHMEDIR';
	if os.path.isfile(file):
		with open(file) as f: return f.read().strip();

	homedirs=io_getsubdirs_('C:/Users')+io_getsubdirs_('/Users')+io_getsubdirs_('/home');
	for h in homedirs:
		file=h+'/.BMES_AHMEDIR';
		if os.path.isfile(file):
			with open(file) as f: return f.read().strip();

	for h in [sys_userhomedir_()] + homedirs:
		ret=h+'/Dropbox/bmes.ahmet';
		if os.path.isdir(ret): return ret;
		ret=h+'/Dropbox/share/bmes.ahmet';
		if os.path.isdir(ret): return ret;
	return '';

import sys
if 'bmes' not in sys.modules:
	d=locatebmesahmetdir()
	if not d:
		raise Exception('Cannot locate bmes.ahmet folder.');
	import pathlib
	sys.path.append(d);
	import bmes
