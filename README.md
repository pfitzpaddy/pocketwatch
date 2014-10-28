
## ![](https://dl.dropboxusercontent.com/u/67905790/pocketwatch.png) PocketWatch

- PocketWatch is the command line utility that provides metrics from log files in a timely fashion.

### Requires
 - Python 2.7 or above

### Usage
 - Clone this repo and run from the command line as follows;

		$ python pocketwatch.py -f /path/to/your/logfiles.log

- Or review the help

		$ python pocketwatch.py -h

### Arguments
	
- Required
 
		-f,--file: the path of the log file to analyze

- Optional 
	
		-u,--url: the base URL of the endpoints for analysis (i.e. -u api/users)
		-e,--endpoints: a list of endpoints to perform analysis (i.e. -e ["get_friends_progress", "get_friends_score"])
		-o,--output: output the list in plain text or in json format (i.e. -o json)
	 
 