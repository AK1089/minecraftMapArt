Minr Script Minecraft Map Art Maker
===================================

A set of programs to generate scripts in Minr Script Code which automatically builds map art in Minecraft from a reference PNG.

The [web version](https://google.com) of this tool is highly recommended unless you have a specialist use case.

## Web Version Usage

1. Click on the "Choose file" button and select an image file to upload.
2. Optionally, enter your Minecraft username in the provided input field.
3. Click the "Upload" button to generate the custom map command.
4. The generated command will be displayed in the output section, along with a preview of the map image.
5. Click on the copy icon next to the command to copy it to the clipboard.
6. Paste the command in your Minecraft chat or command block to generate the custom map in-game.

## Requirements

- [Python 3.10+](https://www.python.org/downloads/)
- [PIL / Pillow](https://pypi.org/project/Pillow/)
- [NumPy](https://pypi.org/project/numpy/)
- [SciPy](https://pypi.org/project/scipy/)
- [requests](https://pypi.org/project/requests/)

**OR**

- [Node.js 20.12.2+](https://nodejs.org/en)
- [Axios](https://www.npmjs.com/package/axios)
- [Cors](https://www.npmjs.com/package/cors)
- [Express](https://www.npmjs.com/package/express)
- [Multer](https://www.npmjs.com/package/multer)


## Installation

Run either `mapmaker.py` or `mapmaker.js` as usual with Python or NPM. Alternatively, use the [web version](https://google.com) (recommended).


## createCommand(filename, baseBlock='glass')

Takes the name of an image file in PNG form as input. File should be 128x128 pixels in size. If you know the primary background block of your map art, specify it as an OPTIONAL second argument, and your script will be slightly more optimised. _For most cases, adding this is entirely unnecessary._

Your script will be uploaded to paste.minr.org, and a function will be generated for you. This function should be sent to the admins to run.

This is identical in either language.


## Python Example Usage - Module

```python
createCommand('cat.png')
createCommand('map_logo')
createCommand('blue_ocean')
createCommand('blue_ocean', 'blue_wool') # script is shorter and less laggy
```


## Python: Running as Standalone File

You can also simply run the file, and instead of manually calling the function in the console, enter filenames into the input fields.

```python
Enter your image filename here ->  # type an image filename here and press return
```

## JavaScript Example Usage - Module

```javascript
createCommand('cat.png')
createCommand('map_logo')
createCommand('blue_ocean')
createCommand('blue_ocean', 'blue_wool') // script is shorter and less laggy
```


## Website File Structure

- `server.js`: Server-side code for handling image processing and API requests
- `public/index.html`: HTML structure of the web application
- `public/script.js`: Client-side JavaScript code for image processing and user interactions
- `public/styles.css`: CSS styles for the web application


## Contributing / Feedback

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue, submit a pull request, or message me on Discord.

