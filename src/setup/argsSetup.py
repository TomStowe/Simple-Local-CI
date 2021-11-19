import argparse

"""
    Setup the arguments for the application
"""
def setupArgs():
    parser = argparse.ArgumentParser(description='A simple python application for running a CI pipeline locally')
    parser.add_argument("-e", "--showErrors", help="Whether the errors should be shown.", type=bool, default=False)
    parser.add_argument("-t", "--timeout", help="The time, in seconds, before a job is timedout.", type=int, default=30)
    parser.add_argument("-d", "--baseDirectory", help="The base directory to run the jobs in.", type=str, required=True)
    parser.add_argument("-c", "--config", help="The configuration file to run the jobs from.", type=str, required=True)
    parser.add_argument("-s", "--onSuccess", help="The command to run on the success of all jobs.", type=str)
    parser.add_argument("-f", "--onFailure", help="The command to run if at least one job fails.", type=str)
    parser.add_argument("-n", "--noColour", help="Whether no colour should be shown in the logging messages.", type=bool, default=False)

    # Return the arguments passed to the system
    return parser.parse_args()
    

if __name__ == "__main__":
    setupArgs()