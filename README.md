# Multiverse Generator
*A collaborative twitch-based choose-your-own-adventure (In the future or past with 4D Space Coordinates) game*

![image](https://github.com/graylan0/multiverse_generator/assets/34530588/a6d9fbf3-1b36-4905-9488-1e381b6bdcc8)

Multiverse Generator a text-based adventure/simulation game set within a specific theme dynamically generated by an Openai GPT 3.5 Turbo. For the time travel theme, the main character is a time traveler vising a historic time period or future time peroid with no format goals or rules set. The game is played collaboratively through twitch chat. Users can change the storage of information and the output. 

## Demo: 
Simulate accurate 2023 Part Numbers from a 2023 Toyota Tacoma
![image](https://github.com/graylan0/multiverse_generator/assets/34530588/a868b9e0-eb5d-4774-b63e-7d993d00e9eb)

## Setup

This project is a standard Python package and can be installed via `pip`. View below for more specific instructions. We used Python 3.11 for this project as well as an Nvidia A4500

### Windows / Linux
```
required pips

pip install openai
pip install twitchio
pip install uvicorn-loguru-integration
pip install uvicorn
pip install fastapi
```

1. Set up a virtual environment and naviate to the directoy wtih the code after opening an anconda prompt:
   ```
   download and install anaconda then open an anaconda terminal window with anaconda prompt
   ```

2. Install the package in editable mode with development dependencies:
   ```powershell
   pip install -e ".[dev]"  # Install the local folder as a Python package
   ```

3. Run the executable:
   ```powershell
   # 
   twitch-plays-llm run
   ```




