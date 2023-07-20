import asyncio
import sys
import logging
from typing import Optional
from contextlib import suppress

from twitchio.ext import commands
from twitchio.channel import Channel

from .config import config
from .models import Proposal
from .story_generator import StoryGenerator

# Set up logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class LlmGameHooks:
    def on_get_narration_result(self, narration_result: str, proposal: Proposal, proposal_id: int):
        pass

class LlmGame:
    def __init__(self):
        pass

    def add_proposal(self, story_action: str, author: str):
        pass

    def vote(self, proposal_id: int):
        pass

    def end_vote(self):
        pass

    def restart(self):
        pass

class LlmTwitchBot(commands.Bot, LlmGameHooks):
    max_message_len = 500  # Twitch has a 500 character limit

    def __init__(self, llm_game: LlmGame):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        super().__init__(
            token=config.twitch_bot_client_id,
            prefix='!',
            initial_channels=[config.twitch_channel_name],
        )
        self.game = llm_game
        self.channel: Optional[Channel] = None
        

    async def event_ready(self):
        """Function that runs when bot connects to server"""
        asyncio.get_running_loop().set_debug(True)
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')
        self.channel = self.get_channel(config.twitch_channel_name)
    
        initial_story_message = f'Story: {self.game.initial_story_message}'
        for i in range(0, len(initial_story_message), self.max_message_len):
            chunk = initial_story_message[i:i+self.max_message_len]
            await self.channel.send(chunk)


    @commands.command()
    async def action(self, ctx: commands.Context):
        """Trigger for user to perform an action within the game"""
        story_action = self._extract_message_text(ctx)
        user = ctx.author.name
        await self._propose_story_action(story_action, user)


    @commands.command()
    async def say(self, ctx: commands.Context):
        """Trigger for user to say something within the game"""
        story_action = 'You say "' + self._extract_message_text(ctx) + '"'
        await self._propose_story_action(story_action, ctx.author.name)

    @commands.command()
    async def vote(self, ctx):
        await self._vote(ctx)

    @commands.command()
    async def help(self, ctx: commands.Context):
        """Help command"""
        await self._send(
            'Welcome to the Storyteller! The goal of this game is to collaboratively create a story. At each turn, the user says an action and the bot replies with a short continuation of the story outlining the events that happen in the story based on the action the user performed. The user can then vote on the next action to perform. The bot will then continue the story based on the action with the most votes. To perform an action, type "!action <action>". To say something, type "!say <message>". To vote on the next action, type "!vote <number>".'
        )

    # --- MOD COMMANDS ---

    @commands.command()
    async def reset(self, ctx: commands.Context):
        """Resets the game if the user is a mod"""
        if not ctx.author.is_mod:
            await self._send(ctx.author.name + ', You are not a mod')
            return

        self.game.restart()
        await self._send(f'Game has been reset | {self.game.initial_story_message}')

    @commands.command()
    async def modvote(self, ctx: commands.Context):
        if not ctx.author.is_mod:
            await self._send(ctx.author.name + ', You are not a mod')
            return
        await self._vote(ctx, weight=99)

    @commands.command()
    async def endvote(self, ctx: commands.Context):
        if not ctx.author.is_mod:
            await self._send(ctx.author.name + ', You are not a mod')
            return
        self.game.end_vote()


    # --- Other Methods ---

    async def _vote(self, ctx: commands.Context, weight: int = 1):
        """Trigger for user to vote on the next action"""
        vote_option_str = self._extract_message_text(ctx)

        try:
            proposal = self.game.vote(int(vote_option_str))
            new_count = proposal.vote
        except ValueError:
            await self._send(f'Invalid vote option: {vote_option_str}')
        else:
            await self._send(
                f'Vote added for option {vote_option_str}. Current votes: {new_count}'
            )

    async def on_get_narration_result(
        self, narration_result: str, proposal: Proposal, proposal_id: int
    ):
        await self._send_chunked(
            f'Choose action {proposal_id} ({proposal.vote} votes): {proposal.message} | {narration_result}'
        )

    async def _propose_story_action(self, story_action: str, author: str):
        """Continues the story by performing an action, communicating the result to the channel"""
        proposal_id = self.game.add_proposal(story_action, author)
        await self._send(f'Option {proposal_id} added: {story_action}')

    async def _send_chunked(self, text: str):
        while text:
            suffix = '...' if len(text) >= self.max_message_len else ''
            await self._send(text[: self.max_message_len - 3] + suffix)
            print(text[: self.max_message_len - 3] + suffix)
            await asyncio.sleep(2.0)
            text = text[self.max_message_len - 3 :]

    @staticmethod
    def _extract_message_text(ctx: commands.Context) -> str:
        """
        Extract the text part of a user message after the command
        (ie. "bar baz" from the message "!foo bar baz")
        """
        return ctx.message.content.split(' ', 1)[1]

    async def _send(self, message: str):
        await self.channel.send(message)
