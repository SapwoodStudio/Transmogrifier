# Transmogrifier
A Blender addon for batch converting 3D files and associated textures into other formats. 

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/8b9ad32e-51cd-4009-8908-4597bb2fa5f1" width="450">

[Installation](#installation-) **·** [Usage](#usage-) **·** [Benefits](#benefits-) **·** [Features](#features-) **·** [Credits](#credits-)


<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/5592793d-f7d9-4c1a-bad1-86da4d4657ba" height="1000">


## INSTALLATION 📥
0. Prerequisites: [Blender 3.6](https://www.blender.org/download/) and Windows. (Transmogrifier may work on GNU/Linux and MacOS, but this has not been tested).
1. [Download the latest version](https://github.com/SapwoodStudio/Transmogrifier/releases/latest). Select the .zip file with the version number at the end (e.g. "Transmogrifier-**v1.0.0**), not the ones named "Source Code".
- <img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/48dec91c-8ca4-42d0-83c8-db54ee7d473a" width="250">

2. Install the addon, [like this](https://www.youtube.com/watch?v=vYh1qh9y1MI).
3. Choose where to display the addon menu in Blender.
- <img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/ef4212ea-9ad7-455f-97e4-26de81a6070f" height="350">


4. (_Optional_) Copy example export presets and a studiolight, "[neutral.hdr](https://github.com/google/model-viewer/blob/master/packages/shared-assets/environments/neutral.hdr)", to local Blender preferences directory. The studiolight is used for rendering preview image thumbnails of converted models.
- <img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/08b3569f-4f0d-4524-82fe-4c80ac902c72" height="350">


## USAGE 🏭
1. **Select the 3D file format** to be imported and converted.
- <img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/5e7af679-1536-41cc-87d7-a8b2c4885985" width="250">

3. **Select a directory** containing 3D files of the chosen format inside, or a parent directory of arbitrary organization and/or depth as long as there exists at least one 3D file of the specified import format somewhere inside.
- <img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/8690027d-fcbc-42c9-af9f-be0d11b53a12" width="250">
- <img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/46975114-4e36-4cdc-be0a-8d4559aafc11" width="600">


4. **Set up export settings** as described in the [Features](#features-) section below. (_Optional: to save current settings for later use, save the current .blend file_)
- <img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/4f788690-44fe-4f88-9b43-756728f08087" width="250">

5. **Click "Batch Convert"**. This will spawn a console window and another instance of Blender. The new Blender window will remain grey while the conversion process gets output to the console window. The original Blender window will remain frozen/unresponsive until the batch conversion is complete. This is normal operation. After the conversion finishes, the greyed-out Blender window and console will disappear and the original Blender instance will report how many files were converted.
- <img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/9f1f804e-e0d2-4963-9a19-935a413bac41" width="600">
- <img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/90cc4699-137c-4c69-bf8d-dd887d2cae61" width="350">


## HOW IT WORKS ⚙

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/6429a930-903f-426b-a8d1-7bc662f4794c" height="700">

_Models from [Polyhaven](https://polyhaven.com/models) ([CC0](https://creativecommons.org/share-your-work/public-domain/cc0/)). The scenarios shown depend on whether the selected import or export formats support textures._

## BENEFITS 🎁

- ⏳ **Saves Time**. Automates the boring stuff so you can focus on creating instead of converting. 
- 🛡️ **Private and Secure**. Runs offline/locally. No account needed.
- ⚓ **Non-Destructive**. Original files are preserved (unless converting between the same formats).
- 🔓 **Open Source**. View, modify, and share the code freely. 
- 🆓 **Free**. No paywall, no trial, no strings attached.

## FEATURES ✨
Transmogrifier includes a robust set of tools for non-destructively converting 3D files and associated textures into other formats.

### 3D Formats
- FBX
- OBJ
- glTF/GLB
- STL
- PLY
- DAE
- X3D
- DAE
- ABC
- USD/USDA/USDC/USDZ

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/292d28b3-405d-4ecc-ba74-e07cd75856ed" width="350">


### Import/Export Presets
Set user-defined import and export presets.

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/9c9c9d84-c103-40fd-9498-4ad7d6535670" width="350">


### Name
Set a custom prefix and/or suffix for every exported file. Synchronize object names and object data names according to the former.

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/d635f947-e2bd-4747-a695-b3b8dd2ee1c9" width="350">


### Textures

Transmogrifier can detect the presence of multiple image texture sets and non-destructively modify them during the conversion process.

#### Source:
- **External**: image textures nearby the imported model
  - in a "textures" subfolder
  - in "[texture set]" subfolders inside a "textures" subfolder
  - in the same directory as the imported 3D file
- **Packed**: image textures packed into the imported file (e.g. GLB or USDZ)
- **Custom**: image textures from a custom directory, which will be applied to all models converted.

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/101e287b-11b9-4728-b347-9b4434003a6e" width="350">


<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/c261ea84-65ba-4c2c-89b2-02e7ca65629b" width="700">

_Models from [Polyhaven](https://polyhaven.com/models) ([CC0](https://creativecommons.org/share-your-work/public-domain/cc0/)). The scenarios shown depend on whether the selected import or export formats support textures._


#### Resolution:
Resize textures and filter what to include by PBR type. Images will not be upscaled.

- 8192
- 4096
- 2048
- 1024
- 512
- 256
- 128

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/a5fe3bb7-8fd1-47d7-9766-443927e7c201" width="350">


#### Format: 
Reformat textures and filter what to include by PBR type.

- PNG
- JPEG (.jpg)
- TARGA
- TIFF
- WEBP
- BMP

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/6399d39a-8220-4a59-8182-8455ec4b1ba3" width="350">


### Transformations
Perform custom transformations and/or apply transformations to every model before export. Filter what transformations to set/apply.

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/39ab41d8-b6d7-4fce-bc16-30ff5c949ece" width="350">


### Animations
Delete animations of every imported object before export. 

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/4b72b4c1-4a37-4698-8d1d-e8cdd765b494" width="350">


### Scene
Set a custom unit system and length unit for export.

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/977e734f-ac85-4e17-8505-942272ec4f16" width="350">


### File
Perform automatic file-resizing methods to every model in order reduce the exported file size below a custom target maximum. Filter which methods are used. If all methods are exhausted and the file size is still above the target maximum, Transmogrifier will report this in the log and move on.

Approaches:
- All (Always export despite any pre-existing file that is already below the target file size.)
- Only Above Max (Only export and resize files that are above the target file sizes. Pre-existing files already below the target are ignored.)
- None (Don't auto-resize at all.)

Methods:
- Draco compression (Only works for GLB/glTF.)
- Resize textures (Set a minimum resolution limit.)
- Reformat textures (Convert all textures to JPG except normal maps.)
- Decimate mesh objects (Uses edge collapse. Set a maximum decimate iteration.)

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/ccb26492-78eb-4dbe-bc6c-aff84308fb84" width="350">


### Archive
Save a .blend and/or render an image preivew thumbnail with Material Preview viewport shading for every imported file. Save a log of the conversion process to troubleshoot errors or simply to get a list of the output files and their file sizes.

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/46035d1d-8f2b-4e88-824f-713184da04d1" width="350">


## CREDITS 🙏
Many thanks to the [people](https://www.blender.org/about/people/) who develop Blender, without whom this addon would have no foundation to exist!

Transmogrifier used code from the following repositories in the following ways. If you give a star to this repository, please also do the same for theirs!
- Transmogrifier's GUI is based on [MrTriPie](https://github.com/mrtripie)'s excellent Blender addon, [Blender Super Batch Export](https://github.com/mrtripie/Blender-Super-Batch-Export) ([GPL-v3](https://www.blender.org/support/faq/#using-blender-8)). 
- Some additional code snippets have been adapted into Transmogrifier from the following repositories (search for their names in [Converter.py](https://github.com/SapwoodStudio/Transmogrifier/blob/main/Converter.py) to view the specific adaptations):
  - [Simple Renaming Panel](https://github.com/Weisl/simple_renaming_panel/)
  - [Node Wrangler](https://docs.blender.org/manual/en/latest/addons/node/node_wrangler.html)
