#!/usr/bin/env python3.6

import visa
import sys
import argparse
import datetime
#import pytz
import csv
import os

try:
    from PIL import Image
except ImportError:
    Image = None
import io

now = datetime.datetime.now()
tstring = now.strftime('%Y-%m-%d_%H.%M.%S%z')

# Parse arguments
parser = argparse.ArgumentParser(description='Agilent/Keysight InfiniiVision screendump tool')
parser.add_argument('filename', nargs='?', help='Optional filename to write the output image to. If not specified, a filename is generated.')
parser.add_argument('-l', '--list', help='Display found devices and exit.', action='store_true')
parser.add_argument('-d', '--device', help='Device ID to connect to, or first device found if not given.')
parser.add_argument('-i', '--inksaver', help='Enable inksaver.', action='store_true')
parser.add_argument('-c', '--crop', help='Crop top and bottom junk', action='store_true')
parser.add_argument('-s', '--symlink', help='Create symlink to file.', action='store_true')
parser.add_argument('-v', '--verbose', help = 'Be verbose.', action='store_true')
args = parser.parse_args()

# Initialise VISA
rm = visa.ResourceManager('@py')
resources = rm.list_resources()

if len(resources) == 0:
    print('no devices found')
    sys.exit(-1)

if args.list:
    for i in resources:
        print(i)
    sys.exit(0)

if args.device == None:
    args.device = resources[0]

scope = rm.open_resource(args.device, encoding = 'iso8859-1')

idn = scope.query("*IDN?").strip()
idnp = list(csv.reader([idn]))[0]
scope.manufacturer = idnp[0]
scope.model = idnp[1]
scope.serialnumber = idnp[2]
scope.version = idnp[3]

if args.filename == None:
    filename = 'screenshot-' + scope.serialnumber + '-' + tstring + '.png'
else:
    filename = args.filename

if args.verbose:
    print('Device %s' % args.device)
    print('Device IDN %s' % idn)
    print('Filename %s' % filename)

# Configure ink saver (black background as seen on screen)
if args.inksaver:
    scope.write(':HARDcopy:INKSaver %u' % args.inksaver)

# Read screen data from scope
# visa.log_to_screen()
scope.query_delay = 1
data = scope.query_binary_values(':DISPlay:DATA? PNG,GRAY', datatype='B', expect_termination=False)
datab = bytearray(data)

if args.crop and Image is not None:
    im = Image.open(io.BytesIO(datab))
    #print(im.width, im.height)
    left = 0
    top = 59
    width = 800
    height = 420
    im = im.crop((left, top, left+width, top+height))
    #print(im.width, im.height)
    im.save(filename)
else:
    with open(filename,'wb') as newfile:
        newfile.write(datab)

if args.symlink:
    os.symlink(filename, 'screenshot-new.png')
    os.rename('screenshot-new.png', 'screenshot.png')

