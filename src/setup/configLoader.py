import yaml
from src.entities.job import Job

"""
    Defines the logic for loading the data out of a config file
"""
class ConfigLoader:
    def __init__(self, configFile: str):
        self.configFile = configFile
        
    """
        Loads the config from the file
        baseDirectory: The base directory to add to the jobs
        returns: The list of jobs to be run
    """
    def loadConfig(self, baseDirectory: str):
        try:
            with open(self.configFile, "r") as file:
                configDict = yaml.safe_load(file)
        except:
            print("An error occurred when loading the config file")
            quit()
        
        jobs = []
        
        for key, values in configDict.items():
            # Only look at jobs that have scripts
            if (not(type(values) is dict) or not("script" in values)):
                continue
            
            # Create the job
            jobs.append(Job(name= key, steps= values["script"], path= baseDirectory))
            
        return jobs