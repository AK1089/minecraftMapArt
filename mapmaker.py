# Image sequencing library used to get RGB data from input pictures
from PIL import Image

# blocks and their respective RGB values on a map
data = '''127 178 56 grass_block
247 233 163 sand
255 252 245 diorite
255 0 0 redstone_block
199 199 199 cobweb
0 124 0 oak_sapling
160 160 255 packed_ice
167 167 167 block_of_iron
255 255 255 white_concrete
164 168 184 clay
151 109 77 dirt
112 112 112 stone
64 64 225 water
143 119 72 oak_planks
216 127 51 acacia_planks
178 76 216 magenta_wool
102 153 216 light_blue_wool
229 229 51 yellow_wool
127 204 25 lime_wool
242 127 165 pink_wool
153 153 153 light_gray_wool
76 127 153 cyan_wool
51 76 178 blue_wool
102 76 51 dark_oak_planks
102 127 51 green_wool
153 51 51 red_wool
25 25 25 black_wool
250 238 77 block_of_gold
92 219 213 block_of_diamond
74 128 255 lapis_block
0 217 58 block_of_emerald
129 86 49 podzol
112 2 0 netherrack
209 177 161 white_terracotta
159 82 36 orange_terracotta
149 87 108 magenta_terracotta
112 108 138 light_blue_terracotta
186 133 36 yellow_terracotta
103 117 53 lime_terracotta
160 77 78 pink_terracotta
57 41 35 gray_terracotta
135 107 98 light_gray_terracotta
87 92 92 cyan_terracotta
122 73 88 purple_terracotta
76 62 92 blue_terracotta
76 50 35 brown_terracotta
76 82 42 green_terracotta
142 60 46 red_terracotta
37 22 16 black_terracotta
189 48 49 crimson_nylium
22 126 134 warped_nylium
100 100 100 deepslate
216 175 147 raw_iron_block'''

# a place for the colour data to be stored in a dictionary
colours = {}

# converts the raw text in data to a dictionary with namespaced block IDs as keys
for line in data.split('\n'):
    r,g,b, block = line.split(' ')
    colours[block] = (int(r), int(g), int(b))


# a function which gets the squared distance between two points in 3D space
# defined by RGB vectors, as a pretty good proxy for colour similarity
def calculateDistance(rgb1, rgb2):
    return ((rgb1[0] - rgb2[0]) ** 2 + (rgb1[1] - rgb2[1]) ** 2 + (rgb1[2] - rgb2[2]) ** 2)

# for an RGB vector, returns the block ID which most closely matches it
def closestMatch(rgb):

    # currentClosest stores the best match so far and its squared distance
    currentClosest = ('null', 90000)

    # for every colour, evaluate its distance function
    for c in colours:
        dist = calculateDistance(colours[c],rgb)

        # if it is a better match than the current closest, replace current closest
        if dist < currentClosest[1]:
            currentClosest = (c, dist)

    # return final best match having checked all possible colours
    return currentClosest

# starting coordinates for generating setblock commands
startX = -3392
startY = 140
startZ = -1600 


# takes in the name of a 128x128 PNG file and makes a text file with the commands
# to generate a map displaying the image
def createCommand(filename, baseBlock='white_concrete'):

    # deals with invalid base blocks
    if f' {baseBlock}\n' not in data:
        baseBlock = 'white_concrete'

    # parsing filename - only PNGs allowed!
    filename = filename.lower()
    if '.' in filename and '.png' not in filename:
        return 'Invalid file extension. Please use PNG files only.'

    # strips png extensions from filename if applicable
    elif '.png' in filename:
        filename = filename.replace('.png', '')

    # start commands to reset the canvas and remove the script
    command = f'@bypass /fill {startX} {startY-1} {startZ} {startX+127} {startY} {startZ+127} {baseBlock}\n@bypass /s r i -3329 120 -1544'
    
    # loads RGB data from the image
    try:
        im = Image.open(f"{filename}.png")
        pix = im.load()
    except FileNotFoundError:
        return f'Unable to find file {filename}.png - make sure it is in the same directory as this program.'

    return pix

    # iterates through each pixel of the image in natural order (L-R, T-B)
    for zl in range(128):

        # list of commands at this current "line" (one layer on the Z-axis)
        cline = []
        clinetext = ''

        # each x-ordinate within this region
        for xl in range(128):

            # gets the block which most closely matches the pixel's colour
            try:
                match = closestMatch(pix[xl,zl][:3])[0]
            except IndexError:
                return 'Image too small - your image file must be exactly 128x128 pixels in size'

            # add the block to make the colour right to the list
            cline.append(match)

        # wrote this a little while ago without commenting it and don't
        # know exactly how it works any more, but it gets the job done
        cline.append('null')
        currentStreak = -1
        lastBlock = cline[0]
        originalX = startX

        # handles the distinction between /setblock and /fill
        for block in cline:

            # if the same block appears as before, expand the streak for /fill
            if block == lastBlock:
                currentStreak += 1

            # otherwise, add an additional command
            else:

                # small optimisation: doesn't bother adding superfluous commands
                # to place down white concrete, as the background exists already
                if lastBlock != baseBlock:

                    # /setblock vs /fill
                    if currentStreak == 0:
                        clinetext += f'@bypass /setblock {originalX} {startY} {startZ+zl} {lastBlock}\n'
                    else:
                        clinetext += f'@bypass /fill {originalX} {startY} {startZ+zl} {originalX+currentStreak} {startY} {startZ+zl} {lastBlock}\n'
                    
                # resets for the next streak
                originalX = originalX + currentStreak + 1
                currentStreak = 0
                lastBlock = block

        # adds the last command of the line
        command = command + clinetext
    
    # write the command text to a text file named after the image
    with open(f'{filename}.txt', 'w+') as f:
        f.write(command)
    
    return f'Successfully saved script for map art at {filename}.txt'
