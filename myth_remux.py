#!/usr/bin/python

import os
import sys
import base64
import uuid
import subprocess
#import MySQLdb

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
	try:
		# check_call()
		print('In remux method: calling subprocess.check_call()')
		print('Remuxing ' + filename + ' to ' + temp_file)
		subprocess.check_call(cmdline)
	except subprocess.CalledProcessError, e:
		print('In remux method: something broke!')
		print (e.cmd)
		print(e.returncode)
		exit(1)
	# Right here we should probably replace the file and update the database with the new size.
	
	# we should parse the config file for this info...
#	db = MySQLdb.connect(host="localhost",
#		user="foo",
#		passwd="bar",
#		db="mythconverg")
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
	file_size = os.path.getsize(filename)
	query = 'UPDATE recorded SET filesize = \'file_size\' WHERE basename = \'filename\';'
	# we should parse the config file for this info...
	# http://docs.python.org/2/library/configparser.html
	# http://stackoverflow.com/questions/9161439/parse-key-value-pairs-in-a-text-file
#	db = MySQLdb.connect(host="localhost",
#		user="foo",
#		passwd="bar",
#		db="mythconverg")
	return

# Main method. This is the entry point of the application
# TODO: See notes on commflag. Need to add 2 more args and store them to variables
if __name__ == "__main__":
	if (len(sys.argv) != 3):
		exit(1)

#	orig_dir = sys.argv[1]
#	orig_file = sys.argv[2]
	filename = os.path.join(sys.argv[1], sys.argv[2])
	# Example: we can ue os.path.split to break stuff up into the base dir and the end filename
#	bn, fn = os.path.split(filename)
#	print('Base: ' + bn)
#	print('File: ' + fn)
	temp_file = '/tmp/' + base64.urlsafe_b64encode(uuid.uuid4().bytes) + '.mpg'
	print('Remuxing ' + filename + ' as ' + temp_file)
	remux(filename,temp_file)


