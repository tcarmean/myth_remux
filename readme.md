myth_remux
==========

UserJob for MythTV that attempts to get around broken pipe errors in mythtranscode when cutting commercials.

This app is written to work with MythBuntu 12.04.1 tracking the MythTV 0.25-fixes branch, but it should be fairly portable.

Dependencies (Version reflects what is presently installed on my system, not a hard and fast requirement):
libav-tools Version: 4:0.8.6-0ubuntu0.12.04.1
mythtv-backend Version: 2:0.25.0+fixes.20120410.1f5962a-0ubuntu1
mythtv-transcode-utils Version: 2:0.25.2+fixes.20120802.46cab93-0ubuntu

The problem:

My HDHomerun is dumping out files that mythtranscode can't cut commercials from. It is continually failing with the, "Deadlock detected. One buffer is full when the other is empty," error mesage (http://www.mythtv.org/wiki/Mythtranscode#Fixing_.22Deadlock_detected._One_buffer_is_full_when_the_other_is_empty.21.22). This app is meant to be a wrapper that can be run in a User Job to fix the file, reflag all the commercials, and (lossless) transcode the file without commercials.

I'm very much a python newb so please make suggestions on how to improve the code. I'm mostly doing this to learn!

