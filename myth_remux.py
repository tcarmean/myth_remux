#!/usr/bin/python

import sys
import base64
import uuid
import subprocess

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
		'avconv',
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
		print('weeee!')
	except CalledProcessError:
		print(CalledProcessError.returncode)
		exit(1)
	return

# Rebuild the keyframe index and the like. Not entirely sure what this does but it is suggested here:
# http://www.mythtv.org/wiki/Mythtranscode#Fixing_.22Deadlock_detected._One_buffer_is_full_when_the_other_is_empty.21.22
def reindex ( temp_file ):
	cmdline = [
		'mythtranscode',
		'--mpeg2',
		'--buildindex',
		'--allkeys',
		'--infile',
		temp_file,
		]
	try:
		print('weeeee!')
	except CalledProcessError:
		print(CalledProcessError.returncode)
		exit(1)
	return

# Here's where we re-run the commflag stuff.
# The commfalg app can't work based off a filename like everything else can so we'll need the following from the userjob stuff:
# %CHANID% %STARTTIME%
def commflag ( channel, starttime ):
	cmdline = [
		'mythcommflag',
		'--chanid',
		channel,
		'--starttime',
		starttime,
		'--noprogress',
		]
	try:
		print('weeeeee!')
	except CalledProcessError:
		print(CalledProcessError.returncode)
		exit(1)
	return


# Main method. This is the entry point of the application
# TODO: See notes on commflag. Need to add 2 more args and store them to variables
if __name__ == "__main__":
	if (len(sys.argv) != 3):
		exit(1)

	orig_dir = sys.argv[1]
	orig_file = sys.argv[2]
	filename = sys.argv[1] + sys.argv[2]
	temp_file = '/tmp/' + base64.urlsafe_b64encode(uuid.uuid4().bytes) + '.mpg'
	print('Remuxing ' + filename + ' as ' + temp_file)

