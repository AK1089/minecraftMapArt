// stores the colours in a dictionary
const colours = {
    "grass_block": [127, 178, 56],
    "sand": [247, 233, 163],
    "diorite": [255, 252, 245],
    "redstone_block": [255, 0, 0],
    "cobweb": [199, 199, 199],
    "big_dripleaf": [0, 124, 0],
    "packed_ice": [160, 160, 255],
    "iron_block": [167, 167, 167],
    "white_concrete": [255, 255, 255],
    "clay": [164, 168, 184],
    "dirt": [151, 109, 77],
    "stone": [112, 112, 112],
    "water": [64, 64, 225],
    "oak_planks": [143, 119, 72],
    "acacia_planks": [216, 127, 51],
    "magenta_wool": [178, 76, 216],
    "light_blue_wool": [102, 153, 216],
    "yellow_wool": [229, 229, 51],
    "lime_wool": [127, 204, 25],
    "pink_wool": [242, 127, 165],
    "light_gray_wool": [153, 153, 153],
    "cyan_wool": [76, 127, 153],
    "blue_wool": [51, 76, 178],
    "dark_oak_planks": [102, 76, 51],
    "green_wool": [102, 127, 51],
    "red_wool": [153, 51, 51],
    "black_wool": [25, 25, 25],
    "gold_block": [250, 238, 77],
    "diamond_block": [92, 219, 213],
    "lapis_block": [74, 128, 255],
    "emerald_block": [0, 217, 58],
    "podzol": [129, 86, 49],
    "netherrack": [112, 2, 0],
    "white_terracotta": [209, 177, 161],
    "orange_terracotta": [159, 82, 36],
    "magenta_terracotta": [149, 87, 108],
    "light_blue_terracotta": [112, 108, 138],
    "yellow_terracotta": [186, 133, 36],
    "lime_terracotta": [103, 117, 53],
    "pink_terracotta": [160, 77, 78],
    "gray_terracotta": [57, 41, 35],
    "light_gray_terracotta": [135, 107, 98],
    "cyan_terracotta": [87, 92, 92],
    "purple_terracotta": [122, 73, 88],
    "blue_terracotta": [76, 62, 92],
    "brown_terracotta": [76, 50, 35],
    "green_terracotta": [76, 82, 42],
    "red_terracotta": [142, 60, 46],
    "black_terracotta": [37, 22, 16],
    "crimson_nylium": [189, 48, 49],
    "warped_nylium": [22, 126, 134],
    "deepslate": [100, 100, 100],
    "raw_iron_block": [216, 175, 14]
};
const blocks = Object.keys(colours);

// copies the RGB values into the new list
let colours_rgb = {};
for (const [key, value] of Object.entries(colours)) {
    colours_rgb[key] = [...value]; // Create a copy of the array
}

// start coordinates of the map
const startX = -3392;
const startY = 140;
const startZ = -1600;

// functions to handle some of the respacing from RGB -> XYZ then XYZ -> CIE-L*ab
// documentation for this conversion / mathematical source can be found at http://www.easyrgb.com/en/math.php
function respaceToXYZ(x) {
    return x.map(val => (val > 0.04045 ? 100 * Math.pow((val + 0.055) / 1.055, 2.4) : val / 0.1292));
}

function respaceFromXYZ(x) {
    return x.map(val => (val > 0.008856 ? Math.pow(val, 1 / 3) : (7.787 * val) + (16 / 116)));
}

// function taking in an array of 3 integers (a color in RGB) and returning a 3-long array (the same color in CIE-L*ab).
// this is because (Euclidean) distance in CIE-L*ab is more closely correlates to human color perception than in RGB.
function convertToCIELAB(rgb) {

    // conversion matrices to be used from respaced RGB to XYZ (M_1), then respaced XYZ to CIE-L*ab (M_2)
    const M_1 = [
        [0.4124, 0.3576, 0.1805],
        [0.2126, 0.7152, 0.0722],
        [0.0193, 0.1192, 0.9505]
    ];

    const M_2 = [
        [0, 116, 0],
        [500, -500, 0],
        [0, 200, -200]
    ];

    // we're converting through XYZ color space, so this is our halfway point.
    // normalizes the RGB values, respaces that, and uses the first matrix to give us XYZ.
    // then, divide it by the other normalization values (D65 illuminant, 2Â° observer)
    // to get the right values in XYZ space.
    const normalizedRGB = rgb.map(val => val / 255);
    const respacedRGB = respaceToXYZ(normalizedRGB);
    const XYZ = multiplyMatrixVector(M_1, respacedRGB).map((val, i) => val / [95.047, 100.000, 108.883][i]);

    // then, respace this set of values, and multiply it by the second conversion matrix
    // to get our CIE-L*ab values. note that technically, the L value should be 16 lower,
    // however as we only ever need the relative values, we can safely omit this.
    const respacedXYZ = respaceFromXYZ(XYZ);
    return multiplyMatrixVector(M_2, respacedXYZ);
}

// helper function to multiply a matrix and a vector
function multiplyMatrixVector(matrix, vector) {
    return matrix.map(row => row.reduce((sum, val, i) => sum + val * vector[i], 0));
}

// for a given RGB vector, converts to CIELAB and finds the closest colour in the list
function findClosestBlock(rgb) {

    // initialises minimum finding
    const labColor = convertToCIELAB(rgb);
    let minDistance = Infinity;
    let closestBlock = null;

    // for each block, compute the distance
    for (const block of blocks) {
        const blockLabColor = colours[block];
        const distance = squaredDistance(labColor, blockLabColor);

        // if it's a minimum, update the closest block
        if (distance < minDistance) {
            minDistance = distance;
            closestBlock = block;
        }
    }

    // returns the closest block
    return closestBlock;
}

// helper function to get the squared distance between two points
function squaredDistance(color1, color2) {
    const [L1, a1, b1] = color1;
    const [L2, a2, b2] = color2;

    return (L1 - L2) ** 2 + (a1 - a2) ** 2 + (b1 - b2) ** 2;
}

// transforms these colours into CIELAB
for (const c in colours) {
    colours[c] = convertToCIELAB(colours[c]);
}

// makes a script out of the image
async function createCommand(pixels, filename, channels, baseBlock = 'glass') {

    // deals with invalid base blocks
    baseBlock = blocks.includes(baseBlock) ? baseBlock : 'glass';
    let blockList = [];

    try {

        // starting commands - fills the map area with the base block
        let command = `@fast\n@bypass /fill ${startX} ${startY - 1} ${startZ} ${startX + 127} ${startY} ${startZ + 127} ${baseBlock}\n` +
            `@bypass /tellraw {{player}} ["",{"text":"Successfully built map art from ","color":"dark_green"},{"text":"${filename}","color":"blue"},{"text":"!","color":"dark_green"}]\n`;
        let teleportNeeded = false;

        // for each row of the map image (so we can optimise using /fill)
        for (let zl = 0; zl < 128; zl++) {

            // variables for storing the list of blocks/commands
            let commandListText = '';
            const rowBlockList = [];

            // for each column, ie. each pixel
            for (let xl = 0; xl < 128; xl++) {

                // there are `channels` entries per pixel, so find the relevant entries fiven that
                const pixelIndex = (zl * 128 + xl) * channels;
                const rgb = Array.from(pixels.slice(pixelIndex, pixelIndex + 3));

                // if there's no alpha channel then just set alpha to 255
                const alpha = (channels === 4) ? pixels[pixelIndex + 3] : 255;

                // get the closest block, unless it's mostly transparent, then just return glass
                rowBlockList.push(alpha >= 100 ? findClosestBlock(rgb) : 'glass');
            }

            // add an extra element to make iteration easier, then go along the line
            rowBlockList.push('null');
            let currentStreak = -1;
            let originalX = startX;
            let lastBlock = rowBlockList[0];

            // for each block in this row, if it's the same as the last block then optimise with /fill
            for (const block of rowBlockList) {
                if (block === lastBlock) {
                    currentStreak++;
                    continue;
                }

                // if we're moving onto a different block (null will also trigger this) then add a command
                // we can skip commands if the last block is the base block, which saves space
                if (lastBlock !== baseBlock) {
                    if (currentStreak === 0) {
                        commandListText += `@bypass /setblock ${originalX} ${startY} ${startZ + zl} ${lastBlock}\n`;
                    } else {
                        commandListText += `@bypass /fill ${originalX} ${startY} ${startZ + zl} ${originalX + currentStreak} ${startY} ${startZ + zl} ${lastBlock}\n`;
                    }
                }

                // if there's a glass block, then we need to yoink the player over because of the hub
                if (block === 'glass') {
                    teleportNeeded = true;
                }

                // moves the new start point and resets our streak
                originalX = originalX + currentStreak + 1;
                currentStreak = 0;
                lastBlock = block;
            }

            // adds the command to our text
            command += commandListText;
            blockList.push(rowBlockList);
        }

        // if there's transparency, then move the player over, give them a map, and move them back
        if (teleportNeeded) {
            command += '\n' + [
                '@bypass /tellraw {{player}} ["",{"text":"Hold still, this will only take a second...","color":"dark_green"}]',
                '@bypass /teleport {{player}} -3200.5 142.0 -1532.5 180 20',
                '@bypass /clone -3392 139 -1600 -3265 139 -1473 -3264 139 -1600',
                '@bypass /clone -3392 140 -1600 -3265 140 -1473 -3264 140 -1600',
                '@bypass /item replace entity {{player}} weapon.mainhand with minecraft:filled_map{map:12372}',
                '@delay 20\n@bypass /teleport {{player}} -3328.5 119.0 -1532.5 180 20'
            ].join('\n');
        }

        // return the full script and list of blocks we used to render the image
        return {
            command: command,
            blockList: blockList
        };

        // if we can't find the image
    } catch (error) {
        return `Error: Unable to find ${filename} - make sure it is in the same directory as this program.`;
    }
}

// takes in the image from the input and uses it as the basis for an upload
async function processImage() {

    // gets the username from the input box
    const usernameInput = document.getElementById('usernameInput');
    const username = usernameInput.value.trim();

    // gets the image from the file upload area
    const imageUpload = document.getElementById('imageUpload');
    const file = imageUpload.files[0];

    // if there's no file
    if (!file) {
        alert('Please select an image to upload.');
        return;
    }

    // makes a file reader object
    const reader = new FileReader();

    // when it loads, get the image
    reader.onload = async function(event) {
        const image = new Image();

        // when the image loads, create a 128x128 canvas
        image.onload = async function() {
            const canvas = document.createElement('canvas');
            canvas.width = 128;
            canvas.height = 128;
            const ctx = canvas.getContext('2d');

            // draw the image onto it at the correct scaled resolution, and grab the pixels
            ctx.drawImage(image, 0, 0, 128, 128);
            const imageData = ctx.getImageData(0, 0, 128, 128);
            const pixels = Array.from(imageData.data);
            const filename = file.name;
            const channels = pixels.length / 16384

            // trim the filename to format it correctly 
            filename = filename.split('/').pop().split('.')[0];
            filename = filename.replace(/[^a-zA-Z0-9_]/g, '');
            filename = filename.slice(0, 12);
            if (filename === "") {
                filename = "unknown_img";
            }

            // make a script out of it
            const {
                command,
                blockList
            } = await createCommand(pixels, filename, channels);

            // create a new 256x256canvas for the generated image
            const generatedCanvas = document.createElement('canvas');
            generatedCanvas.width = 256;
            generatedCanvas.height = 256;
            const generatedCtx = generatedCanvas.getContext('2d');

            // Iterate over the blockList and set pixel values based on RGB values from colours_rgb
            for (let y = 0; y < 128; y++) {
                for (let x = 0; x < 128; x++) {
                    const blockKey = blockList[y][x];

                    // if the block in this position isn't transparent, add a small dot of that colour
                    if (blockKey !== 'glass') {
                        const [r, g, b] = colours_rgb[blockKey];
                        generatedCtx.fillStyle = `rgb(${r}, ${g}, ${b})`;
                        generatedCtx.fillRect(2 * x, 2 * y, 2, 2);
                    }
                }
            }

            // convert the generated canvas to a data URL
            const generatedImageURL = generatedCanvas.toDataURL();

            try {

                // post this script using the process-text endpoint
                const response = await axios.post('/process-text', {
                    username: username,
                    text: command
                });

                // get the output div and put the result into it
                const outputDiv = document.getElementById('output');
                outputDiv.innerHTML = `
                    <p class="command-explanation">
                    To import your map on the test server, copy this command and paste it into the chat. On the main server, you'll have to ask an admin.
                    </p>
                    <p class="command-text">
                    /func execute akmap::add("${response.data.key}", "${response.data.uuid}", "${filename}")
                    <span class="copy-icon" onclick="copyToClipboard()">📋</span>
                    </p>
                    <p class="command-explanation">This is what your map will look like in Minecraft:</p>
                    <img src="${generatedImageURL}" alt="Generated Image">
                `;

                // if we encounter an error
            } catch (error) {
                console.error('Error processing text:', error);
            }
        };
        image.src = event.target.result;
    };
    reader.readAsDataURL(file);
}

// copy the text to the clipboard when the copy icon is clicked
function copyToClipboard() {
    const commandText = document.querySelector('.command-text').innerText;
    navigator.clipboard.writeText(commandText.slice(0, -2));
    document.getElementsByClassName("copy-icon")[0].innerText = "✔️";
}
