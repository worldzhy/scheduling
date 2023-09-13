from typing import List
from entities.Program import Program


class Coach:
    # Initializes coach
    def __init__(self, id: str, name: str):
        # Returns coach ID
        self.id = id
        # Returns coach name
        self.name = name
        # List of programs qualified
        self.programs: List[Program] = []

    def add_program(self, program: Program):
        self.programs.append(program)

    def is_qualified(self, program: Program):
        for p in self.programs:
            if (program.id == p.id):
                return True
        return False