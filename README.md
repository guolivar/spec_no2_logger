# CPEC NO2 digital logger
Python utility to read the output from a SPEC DGS-NO2-968-037 digital NO2 sensor.

The script requests data from the sensor every 1 second (see the code to add a delay for less frequent sampling), timestamps it and saves it to a file.

## Modules required
* **pyserial**
* **time**

## Usage
The settings are specified in the ```settings.txt``` file which should look like:

```
/dev/ttyUSB0
./
local,0
http://api.thingspeak.com/update
00000000
RRRRRRRRRRRRRRRR
WWWWWWWWWWWWWWWW
## Only the first lines are processed.
1 <SERIAL PORT ADDRESS>
2 <DATA SAVE PATH>
3 <local/clean selector>,<compress data? 1=='yes'>
4 <Thingspeak update address>
5 <Thingspeak channel id>
6 <Thingspeak readkey>
7 <Thingspeak writekey>
```

There is one script to run:
* ```logger_main.py```. This is the main logging script and the one that interacts directly with the sensor. It must be run manually (or started at boot) and it will continue to run until stopped by ```^C```. The outputs from this script are on a datafile named ```YYYYMMDD.txt```.

You can create a shell script to run this at boot time (through cron or .profile):
```
#!/bin/bash
cd <PATH_TO_logger_main.py>
./logger_main.py
```
The ```settings.txt``` file location is the same folder where the main script is and therefore it is needed to change the working directory to that path before running the script.

For further details contact Gustavo Olivares (gustavo.olivares_AT_niwa.co.nz)

## License
MIT
See ```LICENSE.md``` for the full text.
