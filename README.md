# Transmogrifier
A Blender addon for batch converting 3D files and associated textures into other formats - with an emphasis on visualization for the web and AR.  Supports conversions between FBX, OBJ, glTF/GLB, STL, PLY, X3D, DAE, ABC, and USD/USDA/USDC/USDZ.

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/3166c6a1-5a56-44f0-8cbe-3471d1f3faa6" width="600">

[Installation](#installation-) 📥 **·** [Usage](#usage-) 🏭 **·** [How it Works](#how-it-works-) ⚙ **·** [Benefits](#benefits-) 🎁 **·** [Features](#features-) ✨ **·** [Credits](#credits-) 🙏


<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/a8474e89-84bf-44ea-befd-1db00a76354a" height="1000"> <img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/84eb82b8-c46f-47d9-afea-c4a6afb0ccfd" height="1000">



## INSTALLATION 📥
0. Prerequisites: [Blender 3.6](https://www.blender.org/download/) and Windows or GNU/Linux (tested on Ubuntu 22.04 LTS). (Transmogrifier may work on MacOS, but this has not been tested.)
1. [Download the latest version](https://github.com/SapwoodStudio/Transmogrifier/releases/latest). Select the .zip file with the version number at the end (e.g. "Transmogrifier-**v1.x.x.zip**"), not the ones named "Source Code".
- <img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/551e98a3-15e4-4cd2-be31-8ae30c729f24" width="250">


2. Install the addon, [like this](https://www.youtube.com/watch?v=vYh1qh9y1MI).
3. Choose where to display the addon menu in Blender.
- <img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/6d30d803-9290-4b96-95c0-f130d1565291" height="350">


4. (_Optional_) Copy example workflow/import/export presets and a studiolight, "[neutral.hdr](https://github.com/google/model-viewer/blob/master/packages/shared-assets/environments/neutral.hdr)", to local Blender preferences directory. The studiolight is used for rendering preview image thumbnails of converted models.
- <img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/fef58e7c-4f17-4d6c-b299-6b589618a558" height="350">


## USAGE 🏭
1. **Select a directory** containing 3D files of the chosen **import format**, or a parent directory of arbitrary organization and/or depth as long as there exists at least one 3D file of the specified import format somewhere inside.
- <img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/9e977a7f-57d7-4659-a5eb-df903e837e79" width="250">
- <img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/e3dc4110-ff04-4297-8698-18a1ce5a358f" width="600">


2. **Select an output directory** to which 3D files of the chosen **export format(s)** should be exported. "Adjacents" means that converted models will be saved to the same directories from which they were imported. "Custom" means that converted models will be saved to a chosen custom directory.
- <img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/116d5ace-0772-48ac-9f2e-c68195019591" width="250">
- <img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/cb6dbc9e-1eee-4b79-a3f5-bd3866f4b2ad" width="250">
- <img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/f5c54398-b248-4cae-9ddd-e57511750e00" width="250">


3. **Set additional export settings** as described in the [Features](#features-) section below. (_Optional: to save current settings for later use, save the current .blend file_)
- <img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/248c5c34-1100-4822-a285-6e11571ebdd2" width="250">


4. **Click "Batch Convert"**. This will spawn another instance of Blender. The new Blender window will remain grey while the conversion process gets output to the console window. The original Blender window will remain frozen/unresponsive until the batch conversion is complete. This is normal operation. After the conversion finishes, the greyed-out Blender window will disappear and the original Blender instance will report how many files were converted.  If you wish to see the conversion process get logged in real-time, you must start Blender from your terminal/Command Line first before Transmogrifying.
- <img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/02bf64ab-3675-4175-bcba-0af212ec97f3" width="250">
- (Ubuntu Example)
- <img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/1ebf7242-368f-4199-aaef-8ce7fe1ca05a" width="600">
- (Windows Example)
- <img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/053903c1-5167-488e-86e4-a5c65a7aa6ad" width="600">
- <img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/90cc4699-137c-4c69-bf8d-dd887d2cae61" width="350">


## HOW IT WORKS ⚙
Transmogrifier works by searching through a given directory for files ending with the extension of the format selected. When it finds a file, it clears out all the current data blocks in the scene, imports the file, imports the associated textures, creates material(s), assigns that/those material(s) to the object(s) in the scene, and exports the model in the new format specified. If Auto File Resizing is turned on, Transmogrifier will then check the exported file's size and attempt to resize the file. The process then repeats until it has converted all files of the specified import format in the given directory.

The diagram below shows the general process and the variety of ways in which Transmogrifier can convert models with respect to available textures and the chosen import and export formats. Each gray box with rounded corners indicates a directory/folder.

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/8ece50f5-dc28-4c2c-9a6a-0161e01b7abc" height="700">

_Models from [Polyhaven](https://polyhaven.com/models) ([CC0](https://creativecommons.org/share-your-work/public-domain/cc0/))._

## BENEFITS 🎁

- ⏳ **Saves Time**. Automates the boring stuff so you can focus on creating instead of converting. 
- 🛡️ **Private and Secure**. Runs offline/locally. No account needed.
- ⚓ **Non-Destructive**. Original files are preserved (unless converting between the same formats).
- 🔓 **Open Source/Licensed-Free**. View, modify, and share the code freely. 
- 🆓 **Free**. No paywall, no trial, no strings attached.

## FEATURES ✨
Transmogrifier includes a robust set of tools for non-destructively converting 3D files and associated textures into other formats.

### Workflow
Create custom Transmogrifier presets (aka "Workflows) for quickly switching between different conversion scenarios. Click the plus button "+" to create a Workflow from all of the current Transmogrifier settings, giving it a custom name. Workflows are stored as "operator presets" in Blender preferences directory. To remove a workflow, select it from the menu, then click the minus button "-". 

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/4bc129b8-f3e3-42c2-9a0a-e9075614645d" width="350">

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/c4feafda-0e2d-4a39-a828-fc8ad9ed16cf" width="350">


### 3D Formats
- FBX
- OBJ
- glTF/GLB
- STL
- PLY
- X3D
- DAE
- ABC
- USD/USDA/USDC/USDZ

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/b9cd086a-a5d4-47c0-ab5e-ba5a372cc5e3" width="350">


### Import/Export Presets
Set user-defined import and export presets.

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/4b47db1d-2a2c-4ff3-8d6c-dbfcef1ff03a" width="350">


### Import Location
Select a directory containing 3D files of the chosen import format, or a parent directory of arbitrary organization and/or depth as long as there exists at least one 3D file of the specified import format somewhere inside.

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/59cc7cd1-a190-44d3-93c5-14b4be71d011" width="350">


### Export Location
Set the export location to either "Adjacent" or "Custom". "Adjacents" means that converted models will be saved to the same directories from which they were imported. "Custom" means that converted models will be saved to a chosen custom directory. Choose whether to place converted models in subdirectories of their same names. If so, choose whether to copy original files from import directories to respective subdirectories.

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/af484984-c556-4238-875a-6cff2e9fb455" width="350">

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/9d0c3d9d-ab4e-4e84-bdbf-6066c3d24b35" width="350">


### Name
Set a custom prefix and/or suffix for every exported file. Synchronize object names and object data names according to the former.

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/bc0f4688-ee44-4811-81af-6ac891aebd58" width="350">


### Textures

Transmogrifier can detect the presence of multiple image texture sets and non-destructively modify them during the conversion process. Select whether to use textures, regex the PBR tags in the textures' names, and keep the otherwise temporary textures folders with their modifications.

#### Source:
- **External**: image textures nearby the imported model. 
  - in a "textures" subfolder
  - in "[texture set]" subfolders inside a "textures" subfolder
  - in the same directory as the imported 3D file
- **Packed**: image textures packed into the imported file (e.g. GLB or USDZ)
- **Custom**: image textures from a custom directory, which will be applied to all models converted.

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/aba24831-c3fb-459d-990d-846e3870e46b" width="350">
<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/ff6a4355-1888-413b-940e-67d1a06c9aaf" width="350">

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/c261ea84-65ba-4c2c-89b2-02e7ca65629b" width="700">

_Models from [Polyhaven](https://polyhaven.com/models) ([CC0](https://creativecommons.org/share-your-work/public-domain/cc0/)). The scenarios shown depend on whether the selected import or export formats support textures. Each gray box with rounded corners indicates a directory/folder._

#### 3 Texturing Rules

There are three naming conventions that must be followed in order for textures to be properly imported, materials created, and materials assigned to the right objects.
1. **Transparent pieces have "transparent" in name and are separate objects.** Objects that should appear transparent must have the word "transparent" present somewhere in their names. This indicates to Transmogrifier that it should duplicate the material as "[material]_transparent" and turn on "Alpha Blend" blending mode, then assign "[material]" to the opaque objects and "[material]_transparent" to the transparent objects. This convention works for multiple texture sets as well.
- <img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/78ae1583-a459-432b-9779-33ddbf73069e" width="700">

2. **Per item, if only 1 texture set is present, object names don't matter except for Rule 1.** For "External" and "Custom" texture sources and for models with only one texture set present, the first rule doesn't matter because it is assumed that that texture set should be applied to all the objects in the scene. 
- <img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/4393055d-da1f-4787-a704-56ac2827df1e" width="700">

3. **Per item, if >1 texture set is present, object and textures set names do matter: object prefixes must match texture set prefixes.** For "External" and "Custom" texture source and for models with more than one texture set present, a naming convention must be followed for Transmogrifier to correctly import and assign multiple texture sets to the proper objects. Simply ensure that the the **first word** before an underscore or another separator in the textures' and objects' names is 1) **distinct** between texture sets and 2) **consistent** between i.) each PBR image in each texture set and ii.) between the texture sets and the objects to which those textures should be applied (See image below). As such, having multiple materials assigned to different meshes within an object does not work. For "Packed" textures, Transmogrifier automatically synchronizes prefixes by inserting the exising materials' prefixes as prefixes to the names of their corresponding image textures and objects to which those materials are assigned. 
- <img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/5eddbac0-9eb0-4aa9-b28d-f660b681b76f" width="700">


#### Resolution:
Resize textures and filter what to include by PBR type. Images will not be upscaled.

- 8192
- 4096
- 2048
- 1024
- 512
- 256
- 128

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/b6f7aa82-c207-42c6-bda0-0588fcf81e1d" width="350">

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/8e566708-0a43-453f-9a2c-8945c1d52a7e" width="350">


#### Format: 
Reformat textures and filter what to include by PBR type.

- PNG
- JPEG (.jpg)
- TARGA
- TIFF
- WEBP
- BMP
- OPEN_EXR

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/5d2522cb-2b95-43ea-bd86-d713d70a42b1" width="350">
<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/53de71c5-ceaf-4430-8bdd-fc1cb2a5cb70" width="350">


### UVs
#### Rename UV Maps
Rename all UV maps for all objects converted with a custom name.  This is important for USD, where objects sharing the same material evidently need to share the same UV map name as well.  If an object has more than one UV map, a numerical incrementer suffix will be applied to each UV map (e.g. "UVMap_1", "UVMap_2", etc.).

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/02ef204d-02b7-4242-ab41-6f68732bf13e" width="350">


#### Export UV Maps
Export UVs with the same options available via the UV Editor and more.

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/186eed7c-1d03-4d65-988f-3d6aba34357e" width="350">


Set a location for UV's to be exported into:

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/c2df1cfe-4463-4ab1-8371-3933aa37a531" width="350">


Set how UVs should be combined for export:

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/0541a1c9-f0e4-4551-a04c-88f875237321" width="350">



### Transformations
Perform custom transformations and/or apply transformations to every model before export. Filter what transformations to set/apply.

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/f44b1325-5415-45a8-a302-3f668608ef4b" width="350">


### Animations
Delete animations of every imported object before export. 

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/09d58e75-8c56-49c5-b6ee-6e8890e2cf8e" width="350">


### Scene
Set a custom unit system and length unit for export.

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/273edb83-792e-4cef-9a88-b6dec3b6fda1" width="350">


### Optimize
Perform automatic file-optmization methods to every model in order reduce the exported file size below a custom target maximum. Filter which methods are used. If all methods are exhausted and the file size is still above the target maximum, Transmogrifier will report this in the log and move on.

File Included:
- All (Always export despite any pre-existing file that is already below the target file size.)
- Only Above Max (Only export and resize files that are above the target file sizes. Pre-existing files already below the target are ignored.)
- None (Don't auto-resize at all.)

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/1261bf79-2aeb-40a6-b789-9e4e5309c0ba" width="350">


Methods:
- Draco compression (Only works for GLB/glTF.)
- Resize textures (Set a minimum resolution limit.)
- Reformat textures (Convert all textures to JPG except normal maps.)
- Decimate mesh objects (Uses edge collapse at 50% ratio each time. Set a maximum decimate iteration.)

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/052d2b6c-ffa3-4f42-b798-eb6d59e84f82" width="350">


### Archive
Save a .blend and/or render an image preivew thumbnail with Material Preview viewport shading for every imported file. Save a log of the conversion process to troubleshoot errors or simply to get a list of the output files and their file sizes.

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/e59911c7-2835-4072-a16e-2ddabd614d45" width="350">


## CREDITS 🙏
Many thanks to the [people](https://www.blender.org/about/people/) who develop Blender, without whom this addon would have no foundation to exist!

Transmogrifier used code from the following repositories in the following ways. If you give a star to this repository, please also do the same for theirs!
- Transmogrifier's GUI is based on [MrTriPie](https://github.com/mrtripie)'s excellent Blender addon, [Blender Super Batch Export](https://github.com/mrtripie/Blender-Super-Batch-Export) ([GPL-v3](https://www.blender.org/support/faq/#using-blender-8)). 
- Some additional code snippets have been adapted into Transmogrifier from the following repositories (search for their names in [Converter.py](https://github.com/SapwoodStudio/Transmogrifier/blob/main/Converter.py) to view the specific adaptations):
  - [Simple Renaming Panel](https://github.com/Weisl/simple_renaming_panel/)
  - [Node Wrangler](https://docs.blender.org/manual/en/latest/addons/node/node_wrangler.html)
