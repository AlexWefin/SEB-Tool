![Header Image](https://i.imgur.com/PTtca5T.png)

## Overview

SEB Tool is designed to manage backups on Nintendo Switch emulators, specifically to facilitate the installation and creation of saves. It allows for a much easier process of transferring a save from the Switch via the cloud using [JKSV](https://github.com/J-D-K/JKSV/tree/master), and then installing it on Yuzu without having to open any folders or manually copy files.

## Usage with JKSV and Google Drive

The app works excellently in conjunction with [JKSV](https://github.com/J-D-K/JKSV/tree/master), especially with Google Drive setup. Follow these [steps](https://github.com/J-D-K/JKSV/blob/master/REMOTE_INSTRUCTIONS.MD) to set it up. 

To use this method, you need to have downloaded the Google Drive app for Windows and selected the folder where the JKSV backups are stored. Follow [these steps](https://support.google.com/a/users/answer/13022292?hl) to install Google Drive on your PC.

The folders created within the chosen backup directory will have the exact same name as specified when adding the game in SEB Tool, ensuring consistency with the game name on JKSV in Google Drive.

### Game ID

You need to add the game ID exactly as it appears in the emulator. The app manages everything based on the IDs, ensuring there are no mix-ups or malfunctions.

- **Yuzu**: Right-click on the game and select "Copy Title ID to Clipboard" to avoid errors. 
  ![Yuzu Copy Title ID to Clipboard](https://i.imgur.com/r7s4R3y.png)
  - Example: For Persona 4 Golden, the ID displayed is `0x010062B01525C000`. The correct ID to use in SEB Tool is `010062B01525C000`.
  ![Game ID in Yuzu](https://i.imgur.com/4dl6Iux.png)

- **Ryujinx**: The ID shown is the exact ID to be used in the app, as it does not have the `0x` prefix.
  ![Game ID in Ryujinx](https://i.imgur.com/2W034ux.png)

## Features

- **Auto Backups**: Automatically saves your current save to another folder when installing a new save, preventing loss due to file corruption. This option can be disabled.
- **Custom and Auto-Naming**: Supports both custom file names and automatic naming for convenience.
- **ZIP Compression**: Optionally compress backups into ZIP files for easier management. This feature can also be disabled.

## Personal Note

The app was initially created for personal use, but it turned out so well that I wanted to share it. The icon is inspired by JKSV; I hope this doesn't cause any issues as I genuinely admire the JKSV icon and wanted to create my version. It perfectly illustrates the app's functionality.

I've tested the app extensively, but bugs may still occur. I apologize for any inconvenience this might cause.
