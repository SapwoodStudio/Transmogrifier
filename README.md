# Transmogrifier
A Blender addon for batch converting 3D files and associated textures into other formats. 

[Installation](#installation-) **·** [Usage](#usage-) **·** [Features](#features-) **·** [Credits](#credits-)


<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/bddff411-a246-429d-8c39-cba946c59a71" height="800">


## INSTALLATION 📥
0. Prerequisites: [Blender 3.5.0 or newer](https://www.blender.org/download/). (Transmogrifier may work on older versions, but this has not been tested).
1. [Download the latest version](https://github.com/SapwoodStudio/Transmogrifier/releases/latest).
2. Install the addon, [like this](https://www.youtube.com/watch?v=vYh1qh9y1MI).
3. Choose where to display the addon menu in Blender.

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/e3e1a772-8b1a-4b5e-9bfd-e87b724d9f86" height="350">


4. (_Optional_) Copy example export presets and a studiolight, "[neutral.hdr](https://github.com/google/model-viewer/blob/master/packages/shared-assets/environments/neutral.hdr)", to local Blender preferences directory. The studiolight is used for rendering preview image thumbnails of converted models.

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/0ae23d56-3d03-4109-a14f-b268d2eb1b2e" height="350">


## USAGE 🏭
1. **Set the 3D file format** to be imported and converted.
2. **Select a directory** containing 3D files of the chosen format or a parent directory containing an arbitrary organization and/or depth as long as there exists at least one 3D file of the specified import format somewhere inside.
3. **Set up export settings** as described in the [Features](#features-) section below. (_Optional: to save current settings for later use, save the current .blend file_)
4. **Click "Batch Convert"**. This will spawn a console window and another instance of Blender. The new Blender window will remain grey while the conversion process gets output to the console window. The original Blender window will remain frozen/unresponsive until the batch conversion is complete. This is normal operation.


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

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/5069fcab-6cb8-42bd-a155-59a27c99dcb3" width="350">


### Import/Export Presets
Set user-defined import and export presets.

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/cc9a3528-5f6a-405f-b4cb-3c4e31f18d68" width="350">


### Name
Set a custom prefix and/or suffix for every exported file. Synchronize object names and object data names according to the former.

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/c7a71803-c481-4d8f-a638-1a142ff9c397" width="350">


### Textures

Transmogrifier can detect the presence of multiple image texture sets and non-destructively modify them during the conversion process.

#### Source:
- **External**: image textures nearby the imported model
  - inside a "textures" subfolder
  - beside the imported model
- **Packed**: image textures packed into the imported file (e.g. GLB or USDZ)
- **Custom**: image textures from a custom directory, which will be applied to all models converted.

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/eb0e08d0-cde2-4335-9875-2ee74827a619" width="350">


#### Resolution:
Resize textures and filter what to include by PBR type. Images will not be upscaled.

- 8192
- 4096
- 2048
- 1024
- 512
- 256
- 128

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/9fee57a2-89ab-4fff-9164-49595514338c" width="350">


#### Format: 
Reformat textures and filter what to include by PBR type.

- PNG
- JPEG (.jpg)
- TARGA
- TIFF
- WEBP
- BMP

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/d981fcc1-c396-46cf-9130-40438ceb0526" width="350">


### Transformations
Perform custom transformations and/or apply transformations to every model before export. Filter what transformations to set/apply.

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/9e62a98f-c273-4c27-bfbf-c2f0d12d534d" width="350">


### Animations
Delete animations of every imported object before export. 

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/55840cd5-f9be-4be4-a1bf-36f98c2ff738" width="350">


### Scene
Set a custom unit system and length unit for export.

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/5511ba0d-97b2-4a8d-a0fe-0dc994993d6f" width="350">


### File
Perform dynamic file-resizing methods to every model in order reduce the exported file size below a custom target maximum. Filter which methods are used. If all methods are exhausted and the file size is still above the target maximum, Transmogrifier will report this in the log and move on.

Auto-File-Resize Methods:
- Draco compression (only works for GLB/glTF)
- Resize textures (won't go below 512px resolution)
- Reformat textures
- Decimate mesh objects (edge collapse)

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/592a4e18-d37a-4a1d-b42d-c5bdc0a006f0" width="350">


### Archive
Save a .blend and/or render an image preivew thumbnail with Material Preview viewport shading for every imported file. Save a log of the conversion process to troubleshoot errors or simply to get a list of the output files and their file sizes.

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/45539c4d-401a-4c5e-b975-872d54b6cd2c" width="350">


## CREDITS 🙏
Many thanks to the [people](https://www.blender.org/about/people/) who develop Blender, without whom this addon would have no foundation to exist!

Transmogrifier used code from the following repositories in the following ways. If you give a star to this repository, please also do the same for theirs!
- Transmogrifier's GUI is based on [MrTriPie](https://github.com/mrtripie)'s excellent Blender addon, [Blender Super Batch Export](https://github.com/mrtripie/Blender-Super-Batch-Export) ([GPL-v3](https://www.blender.org/support/faq/#using-blender-8)). 
- Some additional code snippets have been adapted into Transmogrifier from the following repositories (search for their names in Converter.py to view the specific adaptations):
  - [Simple Renaming Panel](https://github.com/Weisl/simple_renaming_panel/)
  - [Node Wrangler](https://docs.blender.org/manual/en/latest/addons/node/node_wrangler.html)
