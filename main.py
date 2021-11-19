import platform
from src.setup.configLoader import ConfigLoader
from src.setup.runCommand import runCommand
from src.testRunner import TestRunner
from src.setup.argsSetup import setupArgs

# Add Args
args = setupArgs()

jobs = ConfigLoader(args.config).loadConfig(args.baseDirectory)

# Run the jobs
testRunner = TestRunner(args.showErrors, args.timeout, args.noColour)
allJobsSuccessful = testRunner.startTest(jobs)

# Run commands on failure or success as defined in the arguments
if (allJobsSuccessful and not args.onSuccess is None):
    runCommand(args.onSuccess, args.baseDirectory, args.showErrors, args.timeout)
elif (not allJobsSuccessful and not args.onFailure is None):
    runCommand(args.onFailure, args.baseDirectory, args.showErrors, args.timeout)