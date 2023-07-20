import asyncio
import bisect
import time
from datetime import datetime, timedelta
from collections import deque
from dataclasses import dataclass
from typing import List, Dict
from contextlib import suppress
from .config import config
from .models import Proposal
from .story_generator import StoryGenerator
from .trideque import TriDeque

@dataclass
class CharacterProfile:
    name: str
    age: int
    occupation: str
    skills: List[str]
    relationships: Dict[str, str]

class Memory:
    def __init__(self, content, priority=0):
        self.content = content
        self.priority = priority
        self.timestamp = time.time()

class TriDeque:
    def __init__(self, maxlen):
        self.data = deque(maxlen=maxlen)

    def push(self, memory):
        # Insert memory in order of priority
        index = bisect.bisect([m.priority for m in self.data], memory.priority)
        self.data.insert(index, memory)

    def remove(self, memory):
        # Remove a specific memory item
        self.data.remove(memory)

    def update_priority(self, memory, new_priority):
        # Remove the memory item
        self.remove(memory)
        # Update its priority
        memory.priority = new_priority
        # Re-insert it with the new priority
        self.push(memory)

    def __iter__(self):
        # Make the TriDeque iterable
        return iter(self.data)

class CharacterMemory:
    MAX_PAST_ACTIONS = 100  # maximum number of past actions to store in memory

    def __init__(self):
        self.attributes = {}
        self.past_actions = TriDeque(self.MAX_PAST_ACTIONS)  # Initialize a TriDeque with a size of MAX_PAST_ACTIONS
        self.color_code = "white"  # default color
        self.profile = CharacterProfile("John Doe", 40, "Detective", ["Investigation", "Hand-to-hand combat"], {"Sarah": "Wife", "Tom": "Partner"})

    def update_attribute(self, attribute, value):
        self.attributes[attribute] = value
        if attribute == "mood":
            self.update_color_code(value)

    def update_color_code(self, mood):
        if mood == "happy":
            self.color_code = "yellow"
        elif mood == "sad":
            self.color_code = "blue"
        elif mood == "angry":
            self.color_code = "red"
        else:
            self.color_code = "white"

    def add_past_action(self, action, priority=0):
        memory = Memory(action, priority)
        self.past_actions.push(memory)


class LlmGameHooks:
    """
    Hooks that get called for various events within the game.
    """

    async def on_get_narration_result(
        self, narration_result: str, proposal: Proposal, proposal_id: int
    ):
        """
        Triggered after choosing a proposal and generating a narration result.

        Args:
            narration_result: The generated story narration.
            proposal: The proposal object that led to the narration result.
            proposal_id: The unique id of the proposal.
        """
        pass


class LlmGame:
    """
    Main game logic, handling story generation, proposal management and voting.

    Args:
        hooks: Handlers
    """
    def __init__(self, hooks: LlmGameHooks = LlmGameHooks()):
        # other initializations...
        self.character_memory = CharacterMemory()  # Create a CharacterMemory object
        self.generator = StoryGenerator(self.character_memory)  # Pass it to the StoryGenerator
        self.background_task = None
        self.hooks = hooks
        self.proposals = []

    @property
    def initial_story_message(self) -> str:
        """
        Returns the initial story message.

        Returns:
            The initial story message.
        """
        assert self.generator.past_story_entries
        return self.generator.past_story_entries[-1].narration_result

    def add_proposal(self, story_action: str, author: str) -> int:
        """
        Adds a proposal for an action for the main character to take

        Args:
            story_action: The proposed story action by a user.
            author: The username of the person submitting the proposal.

        Returns:
            The id of the newly created proposal.
        """
        proposal = Proposal(user=author, message=story_action, vote=0)
        print(proposal)
        self.proposals.append(proposal)
        proposal_id = len(self.proposals)
        if self.background_task is None:
            self.background_task = asyncio.create_task(self._background_thread_run())
        return proposal_id

    async def _background_thread_run(self):
        """
        A private asynchronous method which handles the collection of
        the votes after the time limit has elapsed
        """

        proposal = max(self.proposals, key=lambda x: x.vote)
        proposal_id = self.proposals.index(proposal)
        narration_result = await self.generator.generate_next_story_narration(
            proposal.message
        )
        await self.hooks.on_get_narration_result(
            narration_result, proposal, proposal_id
        )
        self._new_turn()

    def _new_turn(self):
        """Initializes a new turn within the game"""
        self.proposals = []
        self.background_task = None
