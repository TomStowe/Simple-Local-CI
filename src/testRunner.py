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
        requireSuccessToProgress: Whether the previous job must be a success to trigger the next job
    """
    def __init__(self, showErrors = False, timeoutSeconds = 30, noColour = False, requireSuccessToProgress = False):
        self.showErrors = showErrors
        self.timeoutSeconds = timeoutSeconds
        self.requireSuccessToProgress = requireSuccessToProgress
        
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
                
                jobStatus, errors = self.__runJob(jobs[jobIndex])
                jobs[jobIndex].status = jobStatus
                
                
                if (allJobsSuccessful):
                    allJobsSuccessful = jobStatus == JobStatus.SUCCESS
                    
                # Stop here if a job has failed, but we require that all jobs are successful
                if (self.requireSuccessToProgress and not allJobsSuccessful):
                    # Set the rest of the jobs as cancelled
                    for toInterruptJobIndex in range(jobIndex+1, len(jobs)):
                        jobs[toInterruptJobIndex].status = JobStatus.CANCELLED
                    
                    self.logPrinter.printAllJobs(jobs, errors if self.showErrors else None)
                    
                    return allJobsSuccessful
                else:
                    # If all is going well, print the jobs
                    self.logPrinter.printAllJobs(jobs)
        
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
        returns: A tuple of the job status and any errors that occurred
    """ 
    def __runJob(self, job: Job):        
        # Run all of the commands from the job
        return self.__runCommand(job.getStringJobSteps(), job.path)
        
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
