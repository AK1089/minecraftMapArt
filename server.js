// required libraries
const express = require('express');
const cors = require('cors');
const axios = require('axios');

// makes an app using CORS
const app = express();
app.use(cors());
app.use(express.json({ limit: '800kb' }));
app.use(express.static('public'));

// the process-text endpoint to upload to paste.minr.org
app.post('/process-text', async (req, res) => {
    try {

        // get the username and text
        const {
            username,
            text
        } = req.body;

        // upload text to paste.minr.org
        const response = await axios.post('https://paste.minr.org/documents', text, {
            headers: {
                'Content-Type': 'text/plain'
            }
        });

        // get the UUID if the username is provided
        try {

            // if there's no username, then skip the request to save time
            if (!username) {
                throw new TypeError("No username")
            }

            // otherwise, fetch the UUID from the Mojang API
            const mojangResponse = await axios.get(`https://api.mojang.com/users/profiles/minecraft/${username}`);
            const {
                id
            } = mojangResponse.data;
            const uuid = formatUUID(id);

            // respond with the key and UUID as required
            res.json({
                key: response.data.key,
                uuid: uuid
            });

            // if there's no UUID, then just put a placeholder text block here
        } catch (error) {
            res.json({
                key: response.data.key,
                uuid: "YOUR-UUID-GOES-HERE"
            });
        }

        // if there is some other error
    } catch (error) {
        console.error('Error processing text:', error);
        res.status(500).json({
            error: 'An error occurred'
        });
    }
});

// formats a UUID with dashes added
function formatUUID(id) {
    return `${id.slice(0, 8)}-${id.slice(8, 12)}-${id.slice(12, 16)}-${id.slice(16, 20)}-${id.slice(20)}`;
}

// start the server on port 3000
app.listen((process.env.PORT || 3000), () => {
    console.log('Server is running on port 3000');
});
