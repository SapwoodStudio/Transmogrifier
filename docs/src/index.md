# Transmogrifier
A Blender addon for batch converting 3D files and associated textures into other formats - with an emphasis on visualization for the web and AR.  Supports conversions between FBX, OBJ, glTF/GLB, STL, PLY, X3D, DAE, ABC, and USD/USDA/USDC/USDZ.

![Transmogrifier_Logo_256.png](https://raw.githubusercontent.com/SapwoodStudio/Transmogrifier/main/docs/assets/images/Transmogrifier_Logo_256.png)


## Benefits 🎁

- ⏳ **Saves Time**. Automates the boring stuff so you can focus on creating instead of converting. 
- 🛡️ **Private and Secure**. Runs offline/locally. No account needed.
- ⚓ **Non-Destructive**. Original files are preserved (unless converting between the same formats).
- 🔓 **Open Source/Licensed-Free**. View, modify, and share the code freely. 
- 🆓 **Free**. No paywall, no trial, no strings attached.


## How it Works ⚙
Transmogrifier works by searching through a given directory for files ending with the extension of the format selected. When it finds a file, it clears out all the current data blocks in the scene, imports the file, imports the associated textures, creates material(s), assigns that/those material(s) to the object(s) in the scene, and exports the model in the new format specified. If Auto File Resizing is turned on, Transmogrifier will then check the exported file's size and attempt to resize the file. The process then repeats until it has converted all files of the specified import format in the given directory.

The diagram below shows the general process and the variety of ways in which Transmogrifier can convert models with respect to available textures and the chosen import and export formats. Each gray box with rounded corners indicates a directory/folder.

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/8ece50f5-dc28-4c2c-9a6a-0161e01b7abc" height="700">

_Models from [Polyhaven](https://polyhaven.com/models) ([CC0](https://creativecommons.org/share-your-work/public-domain/cc0/))._