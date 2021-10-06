Minr Script Minecraft Map Art Maker
===================================

A program to generate scripts in Minr Script Code which automatically builds map art in Minecraft from a reference PNG.


Requirements
------------

- [Python >= 3.7](https://www.python.org/downloads/)
- [PIL / Pillow](https://pypi.org/project/Pillow/)


Installation
------------
Download file as ZIP, extract and run **mapmaker.py**
Make sure the image file you want to convert into a map is in the same directory as the program.


createCommand(filename, baseBlock='white_concrete')
---------------------------------------------------
Takes the name of an image file in PNG form as input. File must be 128x128 pixels in size. If you know the primary background block of your map art, specify it as an OPTIONAL second argument, and your script will run slightly faster. For most cases, adding this is entirely unnecessary.

Your script will be uploaded to paste.minr.org and opened in a browser for you.


Example Usage - Module
----------------------

```python
createCommand('cat.png')
createCommand('map_logo')
createCommand('blue_ocean')
createCommand('blue_ocean', 'blue_wool') # script is shorter and runs faster
```


Running as Standalone File
--------------------------
You can also simply run the file, and instead of manually calling the function in the console, enter filenames into the input fields.

```python
Enter your image filename here ->  # type an image filename here and press return
```
