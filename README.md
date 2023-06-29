Minr Script Minecraft Map Art Maker
===================================

A program to generate scripts in Minr Script Code which automatically builds map art in Minecraft from a reference PNG.


Requirements
------------

- [Python 3.10+](https://www.python.org/downloads/)
- [PIL / Pillow](https://pypi.org/project/Pillow/)
- [NumPy](https://pypi.org/project/numpy/)
- [SciPy](https://pypi.org/project/scipy/)
- [requests](https://pypi.org/project/requests/)


Installation
------------
Download file as ZIP, extract and run **mapmaker.py**.

Make sure the image file you want to convert into a map is in the same directory as the program. You may have to specify a complete file path when inputting an image.


createCommand(filename, baseBlock='glass')
---------------------------------------------------
Takes the name of an image file in PNG form as input. File should ideally be 128x128 pixels in size - if not, it will be scaled down to this size. If you know the primary background block of your map art, specify it as an OPTIONAL second argument, and your script will be slightly more optimised. _For most cases, adding this is entirely unnecessary._

Your script will be uploaded to paste.minr.org, and a function will be generated for you. This function should be sent to the admins to run.


Example Usage - Module
----------------------

```python
createCommand('cat.png')
createCommand('map_logo')
createCommand('blue_ocean')
createCommand('blue_ocean', 'blue_wool') # script is shorter and less laggy
```


Running as Standalone File
--------------------------
You can also simply run the file, and instead of manually calling the function in the console, enter filenames into the input fields.

```python
Enter your image filename here ->  # type an image filename here and press return
```


Feedback
--------
If you encounter any issues while using this program, either while running this code or in-game, please message me on Discord or file an issue here. Also, feel free to suggest improvements, or create a pull request!
