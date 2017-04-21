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
## Only the first lines are processed.
1 <SERIAL PORT ADDRESS>
2 <DATA SAVE PATH>
3 <local/clean selector>,<compress data? 1=='yes'>
local : Ambient exposure and data saved locally (default)
clean : Exposure to CLEAN air (zero). Data saved locally.
```

There is one script to run:
* ```logger_main.py```. This is the main logging script and the one that interacts directly with the sensor. It must be run manually (or started at boot) and it will continue to run until stopped by ```^C```. The outputs from this script are one datafile named ```YYYYMMDD.txt``` with the 1 second data.

For further details contact Gustavo Olivares (gustavo.olivares@niwa.co.nz)
