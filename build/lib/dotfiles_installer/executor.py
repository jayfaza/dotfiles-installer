import subprocess
import time

from config import Config
from printer import prLightGray, prRed


class Executor:
    def __init__(self, config: Config):
        self.quite: bool = config.quiet

    def execute(self, command: str, manual_quiet=False, kill_after=0):
        command: list[str] = command.split()
        if not manual_quiet:
            if kill_after == 0:
                process = subprocess.run(command, capture_output=True, shell=True)
                if not self.quite:
                    if process.returncode == 0:
                        prLightGray(process.stdout.decode().strip())
                        return process.stdout.decode().strip()
                    if process.returncode == 1:
                        prRed(f"Error while executing process: {process.args}.")
                        prRed(f"Stderr: {process.stderr.decode().strip()}")
                        exit(1)
                if self.quite:
                    if process.returncode == 0:
                        return process.stdout.decode().strip()
                    if process.returncode == 1:
                        prRed(f"Error while executing process: {process.args}.")
                        prRed(f"Stderr: {process.stderr.decode().strip()}")
                        exit(1)
            else:
                process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
                time.sleep(kill_after)
                out, err = process.communicate()
                if not self.quite:
                    if process.returncode == 0:
                        prLightGray(out.decode().strip())
                        return out.decode().strip()
                    if process.returncode == 1:
                        prRed(f"Error while executing process: {process.args}.")
                        prRed(f"Stderr: {err.decode().strip()}")
                        exit(1)
                if self.quite:
                    if process.returncode == 0:
                        return out.decode().strip()
                    
                    if process.returncode == 1:
                        prRed(f"Error while executing process: {process.args}")
                        prRed(f"Stderr: {err.decode().strip()}")
                        exit(1)
        if manual_quiet:
            return self.execute_manual_quite(command, kill_after)

    def execute_manual_quite(self, command: list[str], kill_after: int):
        if kill_after == 0:
            process = subprocess.run(command, capture_output=True, shell=True)
            if process.returncode == 0:
                return process.stdout.decode().strip()
            if process.returncode == 1:
                prRed(f"Error while executing process: {process.args}.")
                prRed(f"Stderr: {process.stderr.decode()}")
                exit(1)
        else:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
            time.sleep(kill_after)
            out, err = process.communicate()
            if process.returncode == 0:
                return out.decode().strip()
                
            if process.returncode == 1:
                prRed(f"Error while executing process: {process.args}")
                prRed(f"Stderr: {err.decode()}")
                exit(1)
            



