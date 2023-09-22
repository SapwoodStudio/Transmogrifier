# Transmogrifier
A Blender addon for batch converting 3D files and associated textures into other formats - with an emphasis on visualization for the web and AR.  Supports conversions between FBX, OBJ, glTF/GLB, STL, PLY, X3D, DAE, ABC, and USD/USDA/USDC/USDZ.

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/3166c6a1-5a56-44f0-8cbe-3471d1f3faa6" width="600">

[Installation](#installation-) 📥 **·** [Usage](#usage-) 🏭 **·** [How it Works](#how-it-works-) ⚙ **·** [Benefits](#benefits-) 🎁 **·** [Features](#features-) ✨ **·** [Credits](#credits-) 🙏


<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/7332a89c-13d8-4d3f-916a-9b3214a9186d" height="1000"> <img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/1bd4fe67-5703-4524-8ab9-0cc1900d074f" height="1000">



## INSTALLATION 📥
0. Prerequisites: [Blender 3.6](https://www.blender.org/download/) and Windows. (Transmogrifier may work on GNU/Linux and MacOS, but this has not been tested. Support for GNU/Linux is on our roadmap.)
1. [Download the latest version](https://github.com/SapwoodStudio/Transmogrifier/releases/latest). Select the .zip file with the version number at the end (e.g. "Transmogrifier-**v1.0.0**), not the ones named "Source Code".
- <img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/48dec91c-8ca4-42d0-83c8-db54ee7d473a" width="250">

2. Install the addon, [like this](https://www.youtube.com/watch?v=vYh1qh9y1MI).
3. Choose where to display the addon menu in Blender.
- <img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/ef4212ea-9ad7-455f-97e4-26de81a6070f" height="350">


4. (_Optional_) Copy example workflow/import/export presets and a studiolight, "[neutral.hdr](https://github.com/google/model-viewer/blob/master/packages/shared-assets/environments/neutral.hdr)", to local Blender preferences directory. The studiolight is used for rendering preview image thumbnails of converted models.
- <img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/08b3569f-4f0d-4524-82fe-4c80ac902c72" height="350">


## USAGE 🏭
1. **Select a directory** containing 3D files of the chosen **import format**, or a parent directory of arbitrary organization and/or depth as long as there exists at least one 3D file of the specified import format somewhere inside.
- <img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/dd380972-3559-497d-bb2c-e8f49ce34563" width="250">
- <img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/46975114-4e36-4cdc-be0a-8d4559aafc11" width="600">
- <img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/b69a7fd1-6de5-4924-ab92-87f0a16a3248" width="250">

2. **Select an output directory** to which 3D files of the chosen **export format(s)** should be exported. "Adjacents" means that converted models will be saved to the same directories from which they were imported. "Custom" means that converted models will be saved to a chosen custom directory.
- <img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/e182bf04-8866-4dfe-b0ef-0d2f58c3f527" width="250">
- <img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/68257c02-6b05-4977-9f5b-1db2f9020a9a" width="250">

3. **Set additional export settings** as described in the [Features](#features-) section below. (_Optional: to save current settings for later use, save the current .blend file_)
- <img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/0c6c6582-23da-4753-b8a5-1317cad164aa" width="250">

4. **Click "Batch Convert"**. This will spawn a console window and another instance of Blender. The new Blender window will remain grey while the conversion process gets output to the console window. The original Blender window will remain frozen/unresponsive until the batch conversion is complete. This is normal operation. After the conversion finishes, the greyed-out Blender window and console will disappear and the original Blender instance will report how many files were converted.
- <img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/9f1f804e-e0d2-4963-9a19-935a413bac41" width="600">
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

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/95f406bd-d5cc-4a52-970a-55bd69f2b5b7" width="350">
<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/fa8cd957-c372-452d-8f13-8843cc1e3484" width="350">


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

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/e95a8322-d5be-463d-8a2f-81f46103c37c" width="350">


### Import/Export Presets
Set user-defined import and export presets.

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/1ecfc99e-46c0-4a22-a42d-fcc2e93c419f" width="350">


### Import Location
Select a directory containing 3D files of the chosen import format, or a parent directory of arbitrary organization and/or depth as long as there exists at least one 3D file of the specified import format somewhere inside.

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/dd380972-3559-497d-bb2c-e8f49ce34563" width="250">


### Export Location
Set the export location to either "Adjacent" or "Custom". "Adjacents" means that converted models will be saved to the same directories from which they were imported. "Custom" means that converted models will be saved to a chosen custom directory. Choose whether to place converted models in subdirectories of their same names. If so, choose whether to copy original files from import directories to respective subdirectories.

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/f83015fa-f751-43ef-b34f-26ab4db2581d" width="350">


### Name
Set a custom prefix and/or suffix for every exported file. Synchronize object names and object data names according to the former. Rename UV channels of all objects to "UVMap" (and "UVMap_1", etc. for objects with more than 1 UV channel).

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/cfdf71c6-ca26-4758-b007-1642bf360165" width="350">


### Textures

Transmogrifier can detect the presence of multiple image texture sets and non-destructively modify them during the conversion process. Select whether to use textures, regex the PBR tags in the textures' names, and keep the otherwise temporary textures folders with their modifications.

#### Source:
- **External**: image textures nearby the imported model. 
  - in a "textures" subfolder
  - in "[texture set]" subfolders inside a "textures" subfolder
  - in the same directory as the imported 3D file
- **Packed**: image textures packed into the imported file (e.g. GLB or USDZ)
- **Custom**: image textures from a custom directory, which will be applied to all models converted.

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/101e287b-11b9-4728-b347-9b4434003a6e" width="350">

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
- Decimate mesh objects (Uses edge collapse at 50% ratio each time. Set a maximum decimate iteration.)

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/abedd1bb-bf82-4766-a3a6-648eeb9bc4c6" width="350">


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
