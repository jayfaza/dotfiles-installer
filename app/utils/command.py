from operator import contains
import subprocess
from subprocess import CompletedProcess
from typing import Self

from app.managers.config import Config

from ..utils.printer import prCyan, prRed


class Command:
    def __init__(self, cmd: str, capture_output: bool=False) -> None:
        self.cmd: str = cmd.strip()
        self.capture_output: bool = capture_output

    def expand_by(self, other_cmd: list[str]) -> Self:
        for arg in other_cmd:
            self.cmd += f" {arg.strip()}"
        return self 
    
    def execute(self) -> None:
        self.unwrap(self.execute_output())

    def execute_output(self) -> CompletedProcess[bytes]:
        if not self.capture_output:
            proc = subprocess.run(self.cmd, stderr=subprocess.PIPE, shell=True)
        else:
            proc = subprocess.run(self.cmd, capture_output=True, shell=True)
        return proc

    def unwrap(self, proc: CompletedProcess[bytes]) -> None:
        if proc.returncode == 0:
            return
        else:
            prRed(f"Error while executing: {proc.args}")
            prRed(f"Error: {proc.stderr.decode()}")
            exit(1)


class Executor:
    def __init__(self, config: Config):
        self.config: Config = config

    def execute(self, cmd: str, capture_output: bool =False):
        if capture_output:
            proc = subprocess.run(cmd, capture_output=True, shell=True, text=True)
        else:
            if not self.config.quiet:
                proc = subprocess.run(cmd, stderr=subprocess.PIPE, shell=True, text=True)
            else:
                proc = subprocess.run(cmd, capture_output=True, shell=True, text=True) 
        if contains(proc.stderr.strip(), "Proceed with installation?"):
            print(proc.stderr.strip())
        self.unwrap(proc)

    def unwrap(self, proc: CompletedProcess[str]):
        if proc.returncode == 0:
            return
        else:
            prRed(f"Error while executing: {proc.args}")
            prRed(f"Error: {proc.stderr}")
            exit(1)

    
