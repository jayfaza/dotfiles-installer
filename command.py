import subprocess
from logging import error
from subprocess import CompletedProcess
from typing import Self

from printer import prRed


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
        return subprocess.run(self.cmd, capture_output=self.capture_output, shell=True)

    def unwrap(self, proc: CompletedProcess[bytes]) -> None:
        if proc.returncode == 0:
            return
        else:
            prRed(f"Error while executing: {proc.args}")
            prRed(f"Error: {proc.stderr.decode()}")
            exit(1)


