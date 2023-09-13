class Qualification:
    # Initializes qualification
    def __init__(self, programId: str, coachId: str, is_qualified: bool):
        self.programId = programId
        self.coachId = coachId
        self.is_qualified = is_qualified