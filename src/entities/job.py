from src.entities.jobStatus import JobStatus

"""
    Defines the job that will be used
"""

class Job:
    """
        The constructor for the job
        name: The name of the job
        steps: The steps for the job
        path: The path of the job to run
        status: The status of the job
    """
    def __init__(self, name, steps, path, status: JobStatus):
        self.name = name
        self.steps = steps
        self.path = path
        self.status = status
        
    """
        Gets the steps for the job as a string, strung together with &&
        returns: The steps for the job, strung together with &&
    """
    def getStringJobSteps(self):
        return " && ".join(self.steps)