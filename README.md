Minr Script Minecraft Map Art Maker
===================================

A program to generate scripts in Minr Script Code which automatically builds map art in Minecraft from a reference PNG.


Requirements
------------

- [Python >= 3.7](https://www.python.org/downloads/)
- [PIL](https://pypi.org/project/Pillow/)


Installation
------------
Download file as ZIP, extract and run **mapmaker.py**


createCommand(filename, baseBlock='white_concrete')
---------------------------------------------------
Takes the name of an image file in PNG form as input. File must be 128x128 pixels in size. If you know the primary background block of your map art, specify it as an OPTIONAL second argument, and your script will run slightly faster. For most cases, adding this is entirely unnecessary.

Your script will be saved in the same directory as a text file named after your image.


Usage
-----

```python
createCommand('cat.png') # -> cat.txt
createCommand('map_logo') # -> map_logo.txt
createCommand('blue_ocean') # -> blue_ocean.txt
createCommand('blue_ocean', 'blue_wool') # -> blue_ocean.txt (but the script is more optimised)
```
