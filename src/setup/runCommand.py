import subprocess
from src.entities.jobStatus import JobStatus

"""
    Runs a specific command from this app
    command: The command to run
    workingDir: The working directory to run the command from
    showErrors: A boolean as to whether error messages should be shown
    timeoutSeconds: The time in seconds before a command should be timed out
    returns: A tuple of the job status and any errors that occurred
"""
def runCommand(command:str, workingDir: str, showErrors: bool, timeoutSeconds: int):
    try:
        # Run the command
        process = subprocess.run(command,
                            cwd=workingDir,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            timeout=timeoutSeconds)
        
    except subprocess.TimeoutExpired:
        return (JobStatus.TIMEOUT, "")
    
    if (process.returncode == 0):
        return (JobStatus.SUCCESS, process.stdout.decode("UTF-8"))
    else:
        return (JobStatus.FAILURE, process.stdout.decode("UTF-8") + "\n" + process.stderr.decode("UTF-8"))

# python3 main.py -d "C:\Users\tomst\Git\Simple-Local-CI" -c testci.yaml -e t