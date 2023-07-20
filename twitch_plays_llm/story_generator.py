import openai
from asgiref.sync import sync_to_async
from .models import StoryEntry
from .trideque import TriDeque
class StoryGenerator:
    MAX_PAST_ENTRIES = 100  # maximum number of past entries to store in memory

    def __init__(self, character_memory):
        self.character_memory = character_memory
        self.past_story_entries = TriDeque(self.MAX_PAST_ENTRIES)  # Initialize a TriDeque with a size of MAX_PAST_ENTRIES
        initial_prompt = self.construct_initial_prompt()
        self.past_story_entries.push(
            StoryEntry(
                story_action='',
                narration_result=initial_prompt
            )
        )

    def construct_initial_prompt(self):
        rules = """Create a writing prompt to start an Multiverse text adventure game.  Adhere to the following rules:
                    1. The story in a randomly generated location with 4 Dimentional Space Coordnates given to the Prompt.
                    2. You should describe the player's characteristics, where they are, what time period they are in, and what surrounds them, their name, their age, their emotional coloring
                    3. In the Game AI can Simulate SpaceTime and HyperTime.
                    4. Use the 2nd person perspective.
                    5. The prompt should be only 3 - 5 sentences long."""
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=self.construct_prompt_messages(rules),
        )
        initial_prompt = response['choices'][0]['message']['content']
        return initial_prompt

    def construct_prompt_messages(self, story_action: str):
        messages = [
            {
                'role': 'system',
                'content': """Please perform the function of a text adventure game, following the rules listed below:

                            Presentation Rules:

                            1. At each turn, the user says an action and you reply with a multiverse generaiton portal forecasting events in the future based upon the events that happen in the story based on the action the user performed.

                            2. Stay in character as a powerful high throughput multiverse simulator

                            Fundamental Game Mechanics:

                            1. If an action is unsuccessful, respond with a relevant errorlog.


                            Start Simulator.""",
            },
        ]
        for story_entry in self.past_story_entries:
            if story_entry.story_action:
                messages += [{'role': 'user',
                              'content': story_entry.story_action}]
            if story_entry.narration_result:
                messages += [
                    {
                        'role': 'assistant',
                        'content': story_entry.narration_result,
                    }
                ]
        # Add character's past actions to the messages
        for action in self.character_memory.past_actions:
            messages.append({'role': 'user', 'content': action.content})
        messages.append({'role': 'user', 'content': story_action})
        return messages

    @sync_to_async
    def generate_next_story_narration(self, story_action: str):
        """Generates the continuation of the story given a user action"""
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=self.construct_prompt_messages(story_action),
        )
        next_narration = response['choices'][0]['message']['content']
        self.past_story_entries.push(
            StoryEntry(story_action=story_action,
                       narration_result=next_narration)
        )
        return next_narration

    @sync_to_async
    def generate_image_prompt(self):
        """Generates a prompt for DALL-E based on the current scene"""
        # Use the last narration result as the scene description
        scene_description = self.past_story_entries[-1].narration_result
        return scene_description

    def reset(self):
        self.past_story_entries = TriDeque(self.MAX_PAST_ENTRIES)  # Reset it before calling construct_initial_prompt
        initial_prompt = self.construct_initial_prompt()
        self.past_story_entries.push(
            StoryEntry(
                story_action='',
                narration_result=initial_prompt
            )
        )