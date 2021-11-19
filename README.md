# 🏃 Simple Local CI Runner 🏃
A simple python application for running a CI pipeline locally
This app currently supports GitLab CI scripts

## ⚙️ Setup
1. Install the python dependencies in `requirements.txt`
2. Run the CI runner using `python3 main.py -d <directoryToTestIn> -c <configFile>` replacing the fields between `<>`

## ✅ Arguments
When calling the local ci runner, the following arguments can be included
|         Argument        	|                   Description                             	|   Type  	| Required 	| Default 	|
|:-----------------------:	|:----------------------------------------------------------:	|:-------:	|:--------:	|:-------:	|
| `--baseDirectory` (`d`) 	|      The base directory to run the jobs in.               	|  String 	|     Y    	|   N/A   	|
|    `--config` (`-c`)    	|   The configuration file to run the jobs from.            	|  String 	|     Y    	|   N/A   	|
|  `--showErrors` (`-e`)  	|       Whether the errors should be shown.             	    | Boolean 	|     N    	|  False  	|
|    `--timeout` (`-t`)   	| The time, in seconds, before a job is timedout.              	|   Int   	|     N    	|    30   	|
|   `--onSuccess` (`-s`)  	|  The command to run on the success of all jobs.            	|  String 	|     N    	|   N/A   	|
|   `--onFailure` (`-f`)   	|  The command to run if at least one job fails.    	        |  String 	|     N    	|   N/A   	|
|   `--noColour` (`-n`)   	|  Whether no colour should be shown in the logging messages.  	|  Boolean 	|     N    	|  False   	|

## 🎓 Licence
This software is released under the [GNU AGPLv3](LICENSE) licence

## 👨 The Author
[Please click here to see more of my work!](https://tomstowe.co.uk)
