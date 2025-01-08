# Piktah

This small python script piktah.py randomly displays images from a google drive folder accessed through API with a credential file. Features a default small window, with some transparency to not obstruct visbility from other windows. The script also makes sure to correct potential orientation issues from missing metadata information, and it doesn't repeat an already displayed image before going through all the pictures in the shared google drive folder.

The script doesn't work out of the box as it needs credentials to function; it's simply a base example. If anybody wants this functional they need to setup and enable interaction with their own google drive API, create some credentials (and download them to be renamed as client_id.json). Enabling read pemissions is also necessary, as well as adding a test user email (when intended for personal use). The files included of client_id.json and token.json are empty and simply place holders.
