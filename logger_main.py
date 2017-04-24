#!/usr/bin/env python

# Load the libraries
import serial       # Serial communications
import time         # Timing utilities
import subprocess   # Shell utilities ... compressing data files
import requests     # Send data to Thingspeak


# Set the time constants
rec_time = time.gmtime()
start_time = int(time.time())
timestamp = time.strftime("%Y/%m/%d %H:%M:%S GMT", rec_time)
prev_minute = rec_time[4]
# Set the minute averaging variables
min_no2 = 0
min_temp = 0
n_samples = 0
# Read the settings from the settings file
settings_file = open("./settings.txt")
# e.g. "/dev/ttyUSB0"
port = settings_file.readline().rstrip('\n')
print(port)
# path for data files
# e.g. "/home/logger/datacpc3010/"
datapath = settings_file.readline().rstrip('\n')
print(datapath)
prev_file_name = datapath + time.strftime("%Y%m%d.txt", rec_time)
flags = settings_file.readline().rstrip().split(',')
print(flags[0])

# Thingspeak address
thingspk = settings_file.readline().rstrip('\n').split(',')
# Thingspeak channel
channel = settings_file.readline().rstrip('\n').split(',')
# Thinkgspeak readkey
readkey = settings_file.readline().rstrip('\n').split(',')
# Thinkgspeak writekey
writekey = settings_file.readline().rstrip('\n').split(',')

# Close the settings file
settings_file.close()

# Hacks to work with custom end of line
eol = b'\n'
leneol = len(eol)
bline = bytearray()
# Open the serial port and clean the I/O buffer
ser = serial.Serial(port, 9600, parity=serial.PARITY_NONE,
                    bytesize=serial.EIGHTBITS)
ser.flushInput()
ser.flushOutput()
# If the sensor was working in a continuous mode, stop
ser.write('r\r')
# Wait 5 seconds to stabilize the sensor
time.sleep(5)
# Start the logging
while True:
    # Request a reading (send any character through the serial port)
    ser.write('g\r')
    # Get the line of data from the instrument
    while True:
        c = ser.read(1)
        bline += c
        if bline[-leneol:] == eol:
            break
    # Parse the data line
    line = bline.decode("utf-8")
    # Set the time for the record
    rec_time_s = int(time.time())
    rec_time = time.gmtime()
    timestamp = time.strftime("%Y/%m/%d %H:%M:%S GMT", rec_time)
    # SAMPLE LINE ONLY
    # line = '111416020452, -160, 20, 60, 32852, 24996, 34986, 00, 00, 02, 48'
    line = line.rstrip()
    # Make the line pretty for the file
    # If it has been within 1 hour of the start, flag the data by adding X to
    # serialn
    if ((rec_time_s - start_time) < 3600):
        file_line = timestamp + ', X' + line
    else:
        if (flags[0] == 'clean'):
            ser.write('g')
            ser.write('Z')
            ser.write('12345\r')
            # Wait 2 seconds for the setting to be active
            time.sleep(2)
            # clear the serial buffer
            ser.flushInput()
        file_line = timestamp + ',' + line
    print(file_line)
    sep_line = line.split(',')
    if flags[0]=='online':
        min_no2 = min_no2 + eval(sep_line[1])
        min_temp = min_temp + eval(sep_line[2])
        n_samples = n_samples + 1
    # Save it to the appropriate file
    current_file_name = datapath + time.strftime("%Y%m%d.txt", rec_time)
    current_file = open(current_file_name, "a")
    current_file.write(file_line + "\n")
    current_file.flush()
    current_file.close()
    line = ""
    bline = bytearray()
    ## Push data to thingspeak if required
	if flags[0] == 'online':
		# Is it the top of the minute?
		if rec_time[4] != prev_minute:
			prev_minute = rec_time[4]
			# YES! --> Update the Thinkgspeak channel
			# Average for the minute with what we have
			min_no2 = min_no2 / n_samples
            min_temp = min_temp / n_samples
            # Update thingspeak channel
            options = {'api_key':writekey,'field1':no2,'field2':temp}
            req = requests.post(thingspk,data=options)
            min_no2 = 0
            min_temp = 0
            n_samples = 0
    # Compress data if required
    # Is it the last minute of the day?
    if flags[1] == 1:
        if current_file_name != prev_file_name:
            subprocess.call(["gzip", prev_file_name])
            prev_file_name = current_file_name
    # Wait 10s for the next measurement --- OPTIONAL
    while int(time.time()) < (rec_time_s + 10):
        # wait a few miliseconds
        time.sleep(0.05)
print('I\'m done')
