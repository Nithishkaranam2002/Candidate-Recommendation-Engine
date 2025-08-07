class Candidate:
    def __init__(self, name, resume_text, id=None):
        self.id = id
        self.name = name
        self.resume_text = resume_text
        self.embedding = None
        self.score = None
        self.summary = None
