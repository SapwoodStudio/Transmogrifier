# Transmogrifier
A Blender addon for batch converting 3D files and associated textures into other formats. 

[Installation](#installation) **·** [Usage](#usage) **·** [Features](#features)

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/bddff411-a246-429d-8c39-cba946c59a71" height="800">


## INSTALLATION
1. [Download the latest version](https://github.com/SapwoodStudio/Transmogrifier/releases/latest).
2. Install the addon, [like this](https://www.youtube.com/watch?v=vYh1qh9y1MI).
3. Choose where to display the addon menu in Blender.

![Install_Step_3_350px](https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/baec8b30-a4aa-4e86-8ed7-913b5ebacba8)


4. (_Optional_) Copy example export presets and a studiolight, "[neutral.hdr](https://github.com/google/model-viewer/blob/master/packages/shared-assets/environments/neutral.hdr)", to local Blender preferences directory. The studiolight is used for rendering preview image thumbnails of converted models.

![Install_Step_4_350px](https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/628274f6-fc0a-45c7-9809-3715b90c32e9)



## USAGE
1. **Set the 3D file format** to be imported and converted.
2. **Select a directory** containing 3D files of the chosen format or a parent directory containing an arbitrary organization and/or depth as long as there exists at least one 3D file of the specified import format somewhere inside.
3. **Set up export settings** as described in the [Features](#features) section below. (_Optional: to save current settings for later use, save the current .blend file_)
4. **Click "Batch Convert"**. This will spawn a console window and another instance of Blender. The new Blender window will remain grey while the conversion process gets output to the console window. The original Blender window will remain frozen/unresponsive until the batch conversion is complete. This is normal operation.


## FEATURES
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

### Import/Export Presets
Set user-defined import and export presets.

### Name
Set a custom prefix and/or suffix for every exported file. Syncrhonize object names and object data names according to the former.

### Textures

Transmogrifier can detect the presence of multiple image texture sets and non-destructively modify them during the conversion process.

#### Source:
- **External**: image textures nearby the imported model
  - inside a "textures" subfolder
  - beside the imported model
- **Packed**: image textures packed into the imported file (e.g. GLB or USDZ)
- **Custom**: image textures from a custom directory, which will be applied to all models converted.

#### Resolution:
Resize textures and filter what to include by PBR type. Images will not be upscaled.

- 8192
- 4096
- 2048
- 1024
- 512
- 256
- 128

#### Format: 
Reformat textures and filter what to include by PBR type.

- PNG
- JPEG (.jpg)
- TARGA
- TIFF
- WEBP
- BMP

### Transformations
Perform custom transformations and/or apply transformations to every model before export.

### Animations
Delete animations of every imported object before export. 

### Scene
Set a custom unit system and length unit for export.

### File
Perform dynamic file-resizing methods to every model in order reduce the exported file size below a target maximum. If all methods are exhausted and the file size is still above the target maximum, Transmogrifier will report this in the log and move on.

Auto-File-Resize Methods:
- Draco compression (only works for GLB/glTF)
- Resize textures (won't go below 512px resolution)
- Reformat textures
- Decimate mesh objects (edge collapse)

### Archive
Save a .blend and/or render an image preivew thumbnail with Material Preview viewport shading for every imported file. Save a log of the conversion process to troubleshoot errors or simply to get a list of the output files and their file sizes.
