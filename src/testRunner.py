from src.entities.job import Job
from src.entities.jobStatus import JobStatus
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
        noColour: Whether no colour should be used in logging
    """
    def __init__(self, showErrors = False, timeoutSeconds = 30, noColour = False):
        self.showErrors = showErrors
        self.timeoutSeconds = timeoutSeconds
        
        # Init the logprinter
        self.logPrinter = Logger(noColour)
        
    """
        Test all of the jobs in the jobs list
        jobs: A list of Jobs
        returns: True if all jobs were successful, false otherwise
    """
    def startTest(self, jobs):
        allJobsSuccessful = True
        
        self.logPrinter.setupLogPrinter(jobs)
        self.logPrinter.printAllJobs(jobs)
        
        try:
            for jobIndex in range(len(jobs)):
                jobs[jobIndex].status = JobStatus.RUNNING
                self.logPrinter.printAllJobs(jobs)
                
                jobStatus = self.__runJob(jobs[jobIndex])
                jobs[jobIndex].status = jobStatus
                
                self.logPrinter.printAllJobs(jobs)
                
                if (allJobsSuccessful):
                    allJobsSuccessful = jobStatus == JobStatus.SUCCESS
        
        except KeyboardInterrupt:
            # Friendly exit if the tests are interrupted
            for toInterruptJobIndex in range(jobIndex, len(jobs)):
                jobs[toInterruptJobIndex].status = JobStatus.INTERRUPTED
            self.logPrinter.printAllJobs(jobs)
            quit()
            
        return allJobsSuccessful
       
    """
        Run a specific job
        job: The job to run
        returns: True if the job was successful, false otherwise
    """ 
    def __runJob(self, job: Job):        
        # Run all of the commands from the job
        result = self.__runCommand(job.getStringJobSteps(), job.path)
        
        # Timeout check
        if (result.returncode == None):
            return JobStatus.TIMEOUT
                
        # Success Check
        elif (result.returncode == 0):
            return JobStatus.SUCCESS
        
        # If the test errored
        else:
            return JobStatus.FAILURE
        
    """
        Run a command
        command: The command to run
        workingDir: The directory to run the command for
    """
    def __runCommand(self, command: str, workingDir: str):
        return runCommand(command, workingDir, self.showErrors, self.timeoutSeconds)
        

if __name__ == "__main__":
    jobs = [
        Job("Backend Build", ["dotnet clean", "dotnet build -warnAsError"], "C:/Users/tstowe/Git/net-zero-platform", "PENDING"),
        Job("Backend Test", ["dotnet test"], "C:/Users/tstowe/Git/net-zero-platform", "PENDING"),
        Job("Frontend Install", ["npm install"], "C:/Users/tstowe/Git/net-zero-platform/web-app", "PENDING"),
        Job("Frontend Build", ["npm run build"], "C:/Users/tstowe/Git/net-zero-platform/web-app", "PENDING"),
        Job("Frontend Lint", ["npm run build"], "C:/Users/tstowe/Git/net-zero-platform/web-app", "PENDING"),
        Job("Frontend Test", ["set CI=true", "npm run test"], "C:/Users/tstowe/Git/net-zero-platform/web-app", "PENDING")
    ]
    try:
        TestRunner().startTest(jobs)
    except KeyboardInterrupt:
        print("\nTests Interrupted")
