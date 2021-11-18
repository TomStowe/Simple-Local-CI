import subprocess, platform
from time import sleep
from src.entities.job import Job
from src.logging.logger import Logger
from src.setup.runCommand import runCommand

"""
    Defines the job runner
"""
class TestRunner:
    """
        The constructor for the test runner
        showErrors: Whether the errors should be shown
        timeoutSeconds: How long before the test should timeout
    """
    def __init__(self, showErrors = False, timeoutSeconds = 30):
        self.showErrors = showErrors
        self.timeoutSeconds = timeoutSeconds
        
        # Init the logprinter
        self.logPrinter = Logger()
        
    """
        Test all of the jobs in the jobs list
        jobs: A list of Jobs
        returns: True if all jobs were successful, false otherwise
    """
    def startTest(self, jobs):
        allJobsSuccessful = True
        
        self.logPrinter.setupLogPrinter(jobs)
        self.logPrinter.printMainTestingMessage("Tests Started")
        
        try:
            for job in jobs:
                sucessfulJob = self.__runJob(job)
                
                if (allJobsSuccessful):
                    allJobsSuccessful = sucessfulJob
        
        except KeyboardInterrupt:
            # Friendly exit if the tests are interrupted
            self.logPrinter.printInterruptedMessage(job.name)
            self.logPrinter.printMainTestingMessage("Tests Interrupted")
            quit()
            
        self.logPrinter.printMainTestingMessage("Tests Completed")
        return allJobsSuccessful
       
    """
        Run a specific job
        job: The job to run
        returns: True if the job was successful, false otherwise
    """ 
    def __runJob(self, job: Job):
        self.logPrinter.printRunningMessage(job.name)
        
        # Run all of the commands from the job
        result = self.__runCommand(job.getStringJobSteps(), job.path)
        
        # Timeout check
        if (result.returncode == None):
            self.logPrinter.printTimeoutMessage(job.name)
                
        # Success Check
        elif (result.returncode == 0):
            self.logPrinter.printSuccessMessage(job.name)
            return True
        
        # If the test errored
        else:
            self.logPrinter.printErrorMessage(job.name)
            
        return False
        
    """
        Run a command
        command: The command to run
        workingDir: The directory to run the command for
    """
    def __runCommand(self, command: str, workingDir: str):
        return runCommand(command, workingDir, self.showErrors, self.timeoutSeconds)
        

if __name__ == "__main__":
    jobs = [
        Job("Backend Build", ["dotnet clean", "dotnet build -warnAsError"], "C:/Users/tstowe/Git/net-zero-platform"),
        Job("Backend Test", ["dotnet test"], "C:/Users/tstowe/Git/net-zero-platform"),
        Job("Frontend Install", ["npm install"], "C:/Users/tstowe/Git/net-zero-platform/web-app"),
        Job("Frontend Build", ["npm run build"], "C:/Users/tstowe/Git/net-zero-platform/web-app"),
        Job("Frontend Lint", ["npm run build"], "C:/Users/tstowe/Git/net-zero-platform/web-app"),
        Job("Frontend Test", ["set CI=true", "npm run test"], "C:/Users/tstowe/Git/net-zero-platform/web-app")
    ]
    try:
        TestRunner().startTest(jobs)
    except KeyboardInterrupt:
        print("\nTests Interrupted")
