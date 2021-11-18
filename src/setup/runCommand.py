import platform, subprocess
from time import sleep

"""
    Runs a specific command from this app
    command: The command to run
    workingDir: The working directory to run the command from
    showErrors: A boolean as to whether error messages should be shown
    timeoutSeconds: The time in seconds before a command should be timed out
"""
def runCommand(command:str, workingDir: str, showErrors: bool, timeoutSeconds: int):
    # Get the platform of the system - this is because windows systems need the command to be run in the background a different way to Unix systems
    isWindowsSystem = platform.system() == "Windows"
    
    # Run the command
    process = subprocess.Popen(command,
                            cwd=workingDir,
                            shell=True,
                            stdout=subprocess.PIPE if not isWindowsSystem and not showErrors else 0,
                            stderr=subprocess.PIPE if not isWindowsSystem and not showErrors else 0,
                            creationflags=subprocess.CREATE_NEW_CONSOLE if isWindowsSystem and not showErrors else 0)
    
    # Timeout the command if it has taken too long
    for t in range(timeoutSeconds):
        sleep(1)
        if (process.poll() is not None):
            return process
        
    process.kill()
    return process