from pydantic import BaseModel

class StoryEntry(BaseModel):
    story_action: str
    narration_result: str

class Proposal(BaseModel):
    user: str
    message: str
    vote: int

class CharacterProfile(BaseModel):
    name: str
    age: int
    occupation: str
    skills: list[str]
    relationships: dict[str, str]
