#!/usr/bin/python

import sys
import base64
import uuid

# The hdhomerun is spitting out junk files. We'll use ffmpeg to remux them
# (kind of) in place. We'll then rebuild the cutlist and whatnot.

# We need the dir and filename of the recording passed to us.
# Usage should be: myth_remux.py <dir> <file>

# We need exactly 2 args so fail if we don't have them.
if (len(sys.argv) != 3):
	exit(1)

orig_dir = sys.argv[1]
orig_file = sys.argv[2]
filename = sys.argv[1] + sys.argv[2]
temp_file = '/tmp/' + base64.urlsafe_b64encode(uuid.uuid4().bytes) + '.mpg'
print('Remuxing ' + filename + ' as ' + temp_file)

