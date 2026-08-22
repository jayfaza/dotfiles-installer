import subprocess
from logging import error
from subprocess import CompletedProcess
from typing import Self


class Command:
    def __init__(self, cmd: str) -> None:
        self.cmd: list[str]
        self.init(cmd)

    def init(self, cmd: str) -> None:
        self.cmd = cmd.split()

    def expand_by(self, other_cmd: list[str]) -> Self:
        for arg in other_cmd:
            self.cmd.append(arg)
        return self
    
    def execute(self) -> None:
        self.unwrap(subprocess.run(self.cmd))

    def execute_output(self) -> CompletedProcess[bytes]:
        return subprocess.run(self.cmd)

    def unwrap(self, proc: CompletedProcess[bytes]) -> None:
        if proc.returncode == 1:
            error(f"Error with process run: {proc.stderr}")
        else:
            proc.stdout
            return


