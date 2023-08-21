# PIL is an image sequencing library used to get RGB data from input pictures
from PIL import Image, PyAccess

# numpy performs some useful operations (eg. allowing us to convert RGB to CIE-L*ab)
# distance from scipy.spatial provides us a way of accessing the vector norm
import numpy as np
from scipy.spatial import distance

# to post to paste.minr.org
from requests import post, Response
import json

# blocks and their respective RGB values as they appear on a map (sourced from the Minecraft wiki)
colours: dict[str, np.array] = {
    "grass_block": (127, 178, 56),
    "sand": (247, 233, 163),
    "diorite": (255, 252, 245),
    "redstone_block": (255, 0, 0),
    "cobweb": (199, 199, 199),
    "big_dripleaf": (0, 124, 0),
    "packed_ice": (160, 160, 255),
    "iron_block": (167, 167, 167),
    "white_concrete": (255, 255, 255),
    "clay": (164, 168, 184),
    "dirt": (151, 109, 77),
    "stone": (112, 112, 112),
    "water": (64, 64, 225),
    "oak_planks": (143, 119, 72),
    "acacia_planks": (216, 127, 51),
    "magenta_wool": (178, 76, 216),
    "light_blue_wool": (102, 153, 216),
    "yellow_wool": (229, 229, 51),
    "lime_wool": (127, 204, 25),
    "pink_wool": (242, 127, 165),
    "light_gray_wool": (153, 153, 153),
    "cyan_wool": (76, 127, 153),
    "blue_wool": (51, 76, 178),
    "dark_oak_planks": (102, 76, 51),
    "green_wool": (102, 127, 51),
    "red_wool": (153, 51, 51),
    "black_wool": (25, 25, 25),
    "gold_block": (250, 238, 77),
    "diamond_block": (92, 219, 213),
    "lapis_block": (74, 128, 255),
    "emerald_block": (0, 217, 58),
    "podzol": (129, 86, 49),
    "netherrack": (112, 2, 0),
    "white_terracotta": (209, 177, 161),
    "orange_terracotta": (159, 82, 36),
    "magenta_terracotta": (149, 87, 108),
    "light_blue_terracotta": (112, 108, 138),
    "yellow_terracotta": (186, 133, 36),
    "lime_terracotta": (103, 117, 53),
    "pink_terracotta": (160, 77, 78),
    "gray_terracotta": (57, 41, 35),
    "light_gray_terracotta": (135, 107, 98),
    "cyan_terracotta": (87, 92, 92),
    "purple_terracotta": (122, 73, 88),
    "blue_terracotta": (76, 62, 92),
    "brown_terracotta": (76, 50, 35),
    "green_terracotta": (76, 82, 42),
    "red_terracotta": (142, 60, 46),
    "black_terracotta": (37, 22, 16),
    "crimson_nylium": (189, 48, 49),
    "warped_nylium": (22, 126, 134),
    "deepslate": (100, 100, 100),
    "raw_iron_block": (216, 175, 147)
}

# list of all blocks
blocks: list[str] = list(colours.keys())


# functions to handle some of the respacing from RGB -> XYZ then XYZ -> CIE-L*ab
# documentation for this conversion / mathematical source can be found at http://www.easyrgb.com/en/math.php
def respace_to_XYZ(x: np.array) -> np.array:
    return np.where(x > 0.04045, 100 * ((x + 0.055) / 1.055) ** 2.4, x / 0.1292)

def respace_from_XYZ(x: np.array) -> np.array:
    return np.where(x > 0.008856, x ** (1/3), (7.787 * x) + (16 / 116))


# function taking in a tuple of 3 integers, (a colour in RGB) and returning a 3-long numpy array (the same colour in CIE-L*ab).
# this is because (Euclidean) distance in CIE-L*ab more closely correlates to human colour perception than in RGB.
def convert_to_CIELAB(rgb: tuple) -> np.array:

    # conversion matrices to be used from respaced RGB to XYZ (M_1), then respaced XYZ to CIE-L*ab (M_2)
    M_1 = np.array([[0.4124, 0.3576, 0.1805],
                    [0.2126, 0.7152, 0.0722],
                    [0.0193, 0.1192, 0.9505]])

    M_2 = np.array([[   0,  116,    0],
                    [ 500, -500,    0],
                    [   0,  200, -200]])
    
    # we're converting through XYZ colour space, so this is our halfway point.
    # normalises the RGB values, respaces that, and uses the first matrix to give us XYZ.
    # then, divide it by the other normalisation values (D65 illuminant, 2° observer)
    # to get the right values in XYZ space.
    XYZ: np.array = np.divide(np.matmul(M_1, respace_to_XYZ(np.array(rgb) / 255)),
                              np.array((95.047, 100.000, 108.883)))
    
    # then, respace this set of values, and multiply it by the second conversion matrix
    # to get our CIE-L*ab values. note that technically, the L value should be 16 lower,
    # however as we only ever need the relative values, we can safely omit this.
    return np.matmul(M_2, respace_from_XYZ(XYZ))


# alters the colours array to use the new colour space, so we don't have to constantly
# recompute the values for every pixel!
for c in colours:
    colours[c] = convert_to_CIELAB(colours[c])


# starting coordinates for generating setblock commands
startX, startY, startZ = (-3392, 140, -1600)


# takes in the name of a 128x128 PNG file and makes a text file with the commands
# to generate a map displaying the image
def createCommand(filename: str, baseBlock: str = "glass"):

    # deals with invalid base blocks - only the ones in the blocks list are allowed
    baseBlock = baseBlock if baseBlock in blocks else "glass"
        
    # parsing filename - only PNGs are allowed!
    filename = filename.lower()
    if "." in filename and ".png" not in filename:
        return "Error: Invalid file extension. Please use PNG files only."

    # strips png extensions from filename if applicable
    filename = filename.replace(".png", "")

    # loads RGB data from the image
    try:
        im: Image = Image.open(f"{filename}.png")
        im: Image = im.resize((128, 128), resample=Image.Resampling.NEAREST)
        pix: PyAccess = im.load()
        
    except FileNotFoundError: return f"Error: Unable to find {filename}.png - make sure it is in the same directory as this program."

    # strips filename to what should be displayed (ie. without path)
    filename = filename.split("/")[-1]

    # start commands to reset the canvas and tell you you're done
    command: str = f'@fast\n@bypass /fill {startX} {startY-1} {startZ} {startX+127} {startY} {startZ+127} {baseBlock}\n' + \
        '@bypass /tellraw {{player}} ["",{"text":"Successfully built map art from ","color":"dark_green"},{"text":"' + filename + \
            '.png","color":"blue"},{"text":"!","color":"dark_green"}]\n'
    

    # iterates through each pixel of the image in natural order (L-R := z, T-B := x)
    for zl in range(128):

        # list of commands at this current "line" (one slice on the Z-axis)
        clinetext: str = ""

        # gets the block which most closely matches the pixel's colour, provided as an RGB tuple.
        # converts the RGB to CIE-L*ab, gets the distance to all the colours we have access to, finds the block
        # colour which minimises this value, then adds this block to the list of blocks in the line.
        # does this process for each x-ordinate within this slice, ie. each block.
        # however, if the transparency of any pixel is < 100, make it glass (transparent)
        cline: list[str] = [
            blocks[distance.cdist([convert_to_CIELAB(pix[xl, zl][:3])], np.array(list(colours.values()))).argmin()]
            if (len(pix[xl, zl]) == 3 or pix[xl, zl][3]) >= 100 else "glass"
            for xl in range(128)
            ]

        # adds a dummy element at the end, so we can iterate through up to this point.
        # currentStreak gives the number of identical blocks in a row (starting from x = originalX); lastBlock is this block type
        cline.append("null")
        currentStreak: int = -1
        originalX: int = startX
        lastBlock = cline[0]

        # handles the distinction between /setblock and /fill
        for block in cline:

            # if the same block appears as before, expand the "streak" for /fill to use by one
            if block == lastBlock:
                currentStreak += 1
                continue

            # otherwise, we're done with that series of blocks, so need to add our fill or setblock command to the list
            # small optimisation: don't bother adding superfluous commands to place down the background colour, as it exists already
            if lastBlock != baseBlock:

                # /setblock vs /fill - set just that block if there's one, or multiple with /fill if needed 
                if currentStreak == 0:
                    clinetext += f"@bypass /setblock {originalX} {startY} {startZ+zl} {lastBlock}\n"
                else:
                    clinetext += f"@bypass /fill {originalX} {startY} {startZ+zl} {originalX+currentStreak} {startY} {startZ+zl} {lastBlock}\n"

            # resets all our tracking data for the next streak
            originalX = originalX + currentStreak + 1
            currentStreak = 0
            lastBlock = block

        # adds this z-slice's commands to the overall script. note that the last command of the slice would not be included
        # if we had not added our dummy element earlier on.
        command = command + clinetext

    # transparency checking and handling
    if "glass" in command:
         command = command + "\n".join(('\n@bypass /tellraw {{player}} ["",{"text":Hold still, this will only take a second...","color":"dark_green"}',
                                        "@bypass /teleport {{player}} -3200.5 142.0 -1532.5 180 20",
                                        "@bypass /clone -3392 139 -1600 -3265 139 -1473 -3264 139 -1600",
                                        "@bypass /clone -3392 140 -1600 -3265 140 -1473 -3264 140 -1600",
                                        "@bypass /item replace entity {{player}} weapon.mainhand with minecraft:filled_map{map:12372}",
                                        "@delay 20\n@bypass /teleport {{player}} -3328.5 119.0 -1532.5 180 20"))

    # posts to paste.minr.org
    try:
        req: Response = post("https://paste.minr.org/documents", data=command)
        key: str = json.loads(req.content)["key"]
        return f"/func execute akmap::add(\"{key}\", \"YOUR_UUID_GOES_HERE\", \"{filename}\")"

    # we get <KeyError: 'key'> if the script is too long
    except KeyError: return "Error: Script is too long for hastebin to handle. Please try again with a less detailed image."


# easy, convenient main loop
while __name__ == "__main__":
    print(createCommand(input("Enter your image filename here -> ")))
