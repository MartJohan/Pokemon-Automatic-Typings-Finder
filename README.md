# Pokemon Automatic Typings Finder

This repository is an idea that was born from playing pokemon games using an emulator on a PC. I'd play different games from pokemon generation 1 - 6 on PC and often struggled to remember the different typings of pokemon and at the same time struggle to remember what kind of attacks against different types that are super effective / normal / not very effective / immune.

Of course, you have the option of going out of your game, open a browser, search for the pokemon you encoutnered and check out it's weaknesses....... but that's boring. Therefore I decided to make a script using Python to do the following for each encoutner:
1. Take an image of the name of the pokemon in which you encountered and store it locally.
2. Then, transform all the pixels in the image of the name that are not pure white. This is done in order to make the image easier to read by OCR later on
3. Insert the image into [PyTesseract](https://pypi.org/project/pytesseract/) and get the name of the pokemon extracted.
4. Use the name of the pokemon and find it's type(s)
5. After finding the pokemons type(s) find out which kind of attacks that are super effective / normal / not very effective / immune to said type.


## Disclaimer
- This program has only been tested for the Pokemon Platinum ROM
- The program will default to take an image of your primary screen
- The program will only calculate the 2x, 1x, 0.5x and 0x damage types. There exists types that will get a 4x damage bonus or a 0.25x damage negation.

## Requirements
Sicne this is a program in which you need to run yourself (as of now at least) there's quite a bit of requirements.
- You need to have Python installed locally on your machine in order to make the program run. I also recommend to include Python in your Environment variables
- You need to have a local version of the [PyTesseract](https://pypi.org/project/pytesseract/) installed. The `.exe` file coming from downloading the Pytesseract should be inside of it's own folder called `tesseract`. Meaning that you should have a folder structure similar to `Pokemon-Typings-Finder/tesseract/<-- your installation of the tesseract .exe file -->`. You should also add the PyTesseract to your Environment variables.
- You need to have an IDE available. I recommend [VS Code](https://code.visualstudio.com/) as it's free and pretty good.


## Running the program
1. Clone this repository to your local machine.
2. Open the folder using your IDE.
3. In the terminal, type `python ./program.py`. After clicking `Enter` the program should now be running smoothly.
4. Press `F7` in order to take a screenshot
5. Hopefully after some OCR magic you should see the effectivess of different attack types.
6. If you want to stop the program from running, press `F8`

Currently it looks like this: 

![image](https://github.com/user-attachments/assets/5c74f75f-058d-477b-a0f0-319a7c9a498f)

