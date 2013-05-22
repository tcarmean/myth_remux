#!/usr/bin/python

import os
import sys
import base64
import uuid
import subprocess
import ConfigParser
import StringIO
import shutil
try:
	import MySQLdb
except ImportError:
	print('You need to install the MySQLdb python module in order to use this script')
	exit(1)

# The hdhomerun is spitting out junk files. We'll use ffmpeg to remux them
# (kind of) in place. We'll then rebuild the cutlist and whatnot.

# We need the dir and filename of the recording passed to us.
# Usage should be: myth_remux.py <dir> <file>

# We need exactly 2 args so fail if we don't have them.

# The first thing we need to do is remux the input file
def remux( filename, temp_file ):
	# Here's what we need to call
	# ffmpeg -i filename -acodec copy -vcodec copy temp_file
	# We will use subprocess.check_call as described here:
	# http://docs.python.org/2/library/subprocess.html
	cmdline = [
		'/usr/bin/avconv',
		'-i',
		filename,
		'-vcodec',
		'copy',
		'-acodec',
		'copy',
		temp_file,
		]
	bn, fn = os.path.split(temp_file)
	# Is os.statvfs really deprecated since version 2.6? Pretty sure I'm able to call it on v2.7...
	st = os.statvfs(bn)
	du = st.f_bavail * st.f_frsize
	fs = os.path.getsize(filename)
	if du <= fs:
		print('I don\'t think you have enough space to do this...')
		print('Original filesize: ' + str(fs) + ' Free disk space: ' + str(du))
		exit(1)
	try:
		print('In remux method: calling subprocess.check_call()')
		print('Remuxing ' + filename + ' to ' + temp_file)
		subprocess.check_call(cmdline)
	except subprocess.CalledProcessError, e:
		print('In remux method: something broke!')
		print (e.cmd)
		print(e.returncode)
#		exit(1)
		os.remove(temp_file)
		exit(1)
	# Right here we should probably replace the file and update the database with the new size.
	print('In remux method: remux completed successfully!')
	print('Results')
	print('File: ' + temp_file + ' Size: ' + str(os.path.getsize(temp_file)))
#	shutil.move(temp_file, filename)
	return

# Rebuild the keyframe index and the like. Not entirely sure what this does but it is suggested here:
# http://www.mythtv.org/wiki/Mythtranscode#Fixing_.22Deadlock_detected._One_buffer_is_full_when_the_other_is_empty.21.22
def reindex ( temp_file ):
	cmdline = [
		'/usr/bin/mythtranscode',
		'--mpeg2',
		'--buildindex',
		'--allkeys',
		'--infile',
		temp_file,
		]
	try:
		print('In reindex method: calling subprocess.check_call()')
		subprocess.check_call(cmdline)
	except subprocess.CalledProcessError, e:
		print('In reindex method: something broke!')
		print(e.cmd)
		print(e.returncode)
		exit(1)
	return

# Here's where we re-run the commflag stuff.
# The commfalg app can't work based off a filename like everything else can so we'll need the following from the userjob stuff:
# %CHANID% %STARTTIME%
# Need to read the wiki page on mythcommflag again. Might not need the extra args here...
def commflag ( channel, starttime ):
	cmdline = [
		'/usr/bin/mythcommflag',
		'--chanid',
		channel,
		'--starttime',
		starttime,
		'--noprogress',
		]
	try:
		print('In commflag method: calling subprocess.check_call()')
		subprocess.check_call(cmdline)
	except subprocess.CalledProcessError, e:
		print('In commflag method: something broke!')
		print(e.cmd)
		print(e.returncode)
		exit(1)
	return

def updatedb ( filename ):
	# ConfigParser requires a [section] header so we have to add one to mysql.txt in order to get it to parse cleanly
	config_path = os.path.expanduser('~') + os.sep + '.mythtv' + os.sep + 'mysql.txt'
	config = StringIO.StringIO()
	config.write('[dummysection]\n')
	config.write(open(config_path, 'r').read())
	config.seek(0, os.SEEK_SET)
	cp = ConfigParser.SafeConfigParser()
	cp.readfp(config)
#	print(cp.items('dummysection'))
#	file_size = os.path.getsize(filename)
	query = 'SELECT VERSION()'
#	query = 'UPDATE recorded SET filesize = \'file_size\' WHERE basename = \'filename\';'
	# we should parse the config file for this info...
	# http://docs.python.org/2/library/configparser.html
	# http://stackoverflow.com/questions/9161439/parse-key-value-pairs-in-a-text-file
	try:
		db = MySQLdb.connect(host=cp.get('dummysection','dbhostname'),
			user=cp.get('dummysection','dbusername'),
			passwd=cp.get('dummysection','dbpassword'),
			db=cp.get('dummysection','dbname'),
			port=cp.get('dummysection','dbport'))
		cur = db.cursor()
		cur.execute(query)
		# only for example purposes won't need this in the real, final script...
		ver = cur.fetchone()
		print('Database Version: ' + ver)
	except MySQLdb.Error, e:
		# error handling
		print('Error: ' + e.args[0] + e.args[1])
		exit(1)
	finally:
		# THIS ALWAYS GETS EXECUTED NO MATTER WHAT HAPPENS ABOVE
		cur.close()
		db.close()
	return

# Main method. This is the entry point of the application
# TODO: See notes on commflag. Need to add 2 more args and store them to variables
if __name__ == "__main__":
	if (len(sys.argv) != 3):
		exit(1)

	filename = os.path.join(sys.argv[1], sys.argv[2])
	# Example: we can ue os.path.split to break stuff up into the base dir and the end filename
#	bn, fn = os.path.split(filename)
#	print('Base: ' + bn)
#	print('File: ' + fn)
	temp_path = '/tmp'
	temp_file = base64.urlsafe_b64encode(uuid.uuid4().bytes) + '.mpg'
	temp_fn = os.path.join(temp_path, temp_file)
	#print('Remuxing ' + filename + ' as ' + temp_file)
	updatedb(filename)
#	remux(filename,temp_fn)

