# Storyteller
*A collaborative twitch-based choose-your-own-adventure game*

Twitch Plays Llm a text-based choose-your-own-adventure game (ie. AI dungeon) set within a specific theme. For the time travel theme, the main character is a timem traveler vising a historic time period with the goal of altering some historic event. The game is played collaboratively through twitch chat. Read more about the vision for this project within [this document](https://docs.google.com/document/d/10TJ-P2iRqNIOWyQ5PRzcVnN7VBCprzPSB9CFGy_-eDo/edit).


Welcome to the Storyteller! The goal of this game is to collaboratively create a story. At each turn, the user says an action and the bot replies with a short continuation of the story outlining the events that happen in the story based on the action the user performed. The user can then vote on the next action to perform. The bot will then continue the story based on the action with the most votes. To perform an action, type "!action <action>". To say something, type "!say <message>". To vote on the next action, type "!vote <number>".'
        )
        
## Development Setup

This project is a standard Python package and can be installed via `pip`. View below for more specific instructions.

### Windows

1. Set up a virtual environment:
   ```
   download and install anaconda then open an anaconda terminal window with anaconda prompt
   ```

2. Install the package in editable mode with development dependencies:
   ```powershell
   pip install -e ".[dev]"  # Install the local folder as a Python package
   ```

3. Run the executable:
   ```powershell
   # Make sure to run beforehand: .venv\Scripts\activate
   twitch-plays-llm -h  # View the available commands
   ```

### Linux / Mac

1. Set up a virtual environment:
   ```bash
   python3 -m venv .venv  # Setup a virtual environment
   source .venv/bin/activate  # Activate virtual environment
   ```

2. Install the package in editable mode with development dependencies:
   ```bash
   pip install -e '.[dev]'  # Install the local folder as a Python package
   ```

3. Run the executable:
   ```bash
   # Make sure to run beforehand: source .venv/bin/activate
   twitch-plays-llm -h  # View the available commands
   ```

### Formatting and linting

To run formatting, run the following:
```bash
# Make sure to activate the virtual environment before running this to access the executables
isort . --profile attrs; black . --line-length 88


```


The codebase for the Twitch Plays LLM Time Traveler game is divided into several Python files, each with its own specific purpose. Here's an overview of each file and its role in the application:

__init__.py: This is an empty file that indicates that the directory should be treated as a Python package. This allows the modules within the directory to be imported elsewhere in the application.

__main__.py: This is the entry point of the application. It sets up the necessary configurations, initializes the OpenAI API key, and starts the application. It uses the uvicorn ASGI server to run the application, which allows for asynchronous handling of requests. This is particularly useful for a chatbot application like this, where multiple users might be interacting with the bot at the same time.

app.py: This file sets up the FastAPI application and defines the API routes. FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints. It's used here to create an API that the Twitch bot can interact with.

character_memory.py: This file defines the CharacterMemory class, which is used to store and manage the character's memory. The character's memory includes attributes like mood and color code, as well as past actions. The memory is used to generate prompts for the OpenAI API, which in turn generates the next part of the story.

config.py: This file is used to manage the configuration of the application. It reads the configuration from environment variables and provides a single point of access for these configuration values throughout the rest of the application.

llm_game.py: This file defines the LlmGame class, which is used to manage the state of the game. It includes methods for adding actions to the game, getting the current game state, and generating the next game state based on the current state and the user's action.

llm_twitch_bot.py: This file defines the LlmTwitchBot class, which is used to interact with the Twitch chat. It uses the twitchio library to connect to the Twitch chat, listen for messages, and send messages to the chat. It also interacts with the LlmGame class to update the game state based on the chat messages.

models.py: This file defines the Pydantic models used in the application. Pydantic is a data validation library that uses Python type annotations to validate the data. It's used here to define the structure of the game state and the chat messages.

story_generator.py: This file defines the StoryGenerator class, which is used to generate the next part of the story based on the user's action and the current game state. It uses the OpenAI API to generate the story.

The application works by running a Twitch bot that listens for messages in the Twitch chat. When a user sends a message, the bot updates the game state based on the message and generates the next part of the story using the OpenAI API. The bot then sends a message to the chat with the next part of the story. This allows the users in the chat to interact with the game and influence the story.




The TriDeque and CharacterMemory classes are key components of the Twitch Plays LLM Time Traveler game. Let's dive into how they work:

TriDeque: This class is a custom data structure that combines the properties of a deque (double-ended queue) and a priority queue. A deque is a type of queue in which elements can be added or removed from either end (front or rear), and a priority queue is a type of queue where elements are served (i.e., removed) based on their priority instead of their order in the queue.

The TriDeque class is initialized with a maximum length, and it stores its data in a Python deque with this maximum length. When a new element (or "memory") is added to the TriDeque using the push method, the element is inserted in the deque at a position determined by its priority. This is done using the bisect module, which allows for efficient insertion into a sorted list. If the deque is full (i.e., it contains maxlen elements), the oldest element is automatically removed.

The TriDeque class does not currently include methods for removing elements or updating their priority, but these could be added if needed.

CharacterMemory: This class represents the memory of the game's character. It stores various attributes of the character, such as their mood and color code, as well as a list of their past actions. The character's profile (name, age, occupation, skills, and relationships) is also stored in a CharacterProfile object.

The CharacterMemory class includes methods for updating the character's attributes and adding new actions to their memory. When a new action is added, if the number of past actions exceeds a certain limit (MAX_PAST_ACTIONS), the oldest action is removed from the memory and written to a file (PAST_ACTIONS_FILE).

The get_memory_prompt method generates a prompt for the OpenAI API based on the character's profile and past actions. This prompt is used to generate the next part of the story.

The CharacterMemory class also includes methods for writing the character's thoughts to a file and reading them back. This could be used to add more depth to the character and make the game more immersive.

In summary, the TriDeque class is a custom data structure used to efficiently store and manage the character's memories based on their priority, and the CharacterMemory class is used to store and manage the character's attributes, past actions, and thoughts.

![image](https://github.com/graylan0/twitch_time/assets/34530588/db694b4a-8322-4070-9c1f-a7b6d71a07f3)



