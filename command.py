import subprocess
from logging import error
from subprocess import CompletedProcess
from typing import Self


class Command:
    def __init__(self, cmd: str, capture_output: bool=False) -> None:
        self.cmd: list[str] = cmd.split()
        self.capture_output: bool = capture_output

    def expand_by(self, other_cmd: list[str]) -> Self:
        for arg in other_cmd:
            self.cmd.append(arg)
        return self 
    
    def execute(self) -> None:
        self.unwrap(self.execute_output())

    def execute_output(self) -> CompletedProcess[bytes]:
        return subprocess.run(self.cmd, capture_output=self.capture_output)

    def unwrap(self, proc: CompletedProcess[bytes]) -> None:
        if proc.returncode == 1:
            error(f"Process breaked down: {proc}")
        else:
            return


