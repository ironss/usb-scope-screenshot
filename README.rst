USB Scope Screenshot
####################

Command-line tool to capture a screenshot from an oscilloscope connected via USB.

* Uses PyVISA and SCPI to communicate with the oscilloscope.
* Provide a filename, or let it generate one for you
     <instrument-id>-<date>-<time>.png
* Command-line switch to list connected devices.
* Command-line switch to select a device. Use the first one if not given.
* Command-line switch to select 'inksaver' -- print black-on-white rather than
  white-on-black.
* Command-line switch to crop junk off the edges of the screen.
* Command-line switch to generate a symlink to the most-recent capture.


Testing
=======

* Ubuntu 18.04
* Agilent MSO-X 3032A


TODO
====

* Combine with Rigol screen capture program, using either LAN or USB.
* Add date-time to screenshot.
* Test with Rigol MSO-1000 series scope

