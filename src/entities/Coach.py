from typing import List
from .Program import Program


class Coach:
    def __init__(self, id: str, name: str):
        # returns coach ID
        self.id = id
        # returns coach name
        self.name = name
        # list of programs qualified
        self.programs: List[Program] = []

    def add_program(self, program: Program):
        self.programs.append(program)

    def is_qualified(self, program: Program):
        for p in self.programs:
            if (program.id == p.id):
                return True
        return False