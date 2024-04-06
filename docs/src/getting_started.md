## Installation
0. Prerequisites: [Blender 3.6](https://www.blender.org/download/) and Windows or GNU/Linux (tested on Ubuntu 22.04 LTS). (Transmogrifier may work on MacOS, but this has not been tested.)
1. [Download the latest version](https://github.com/SapwoodStudio/Transmogrifier/releases/latest). Select the .zip file with the version number at the end (e.g. "Transmogrifier-**v1.x.x.zip**"), not the ones named "Source Code".

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/551e98a3-15e4-4cd2-be31-8ae30c729f24" width="250">


2. Install the addon, [like this](https://www.youtube.com/watch?v=vYh1qh9y1MI).
3. Choose where to display the addon menu in Blender.

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/6d30d803-9290-4b96-95c0-f130d1565291" height="350">


4. (_Optional_) Copy example workflow/import/export presets to local Blender preferences directory.

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/fef58e7c-4f17-4d6c-b299-6b589618a558" height="350">


## Quickstart Demo 🧪
1. Download "PolyHaven_Demo_Files.zip" from the [latest release page](https://github.com/SapwoodStudio/Transmogrifier/releases/latest).
2. Unzip the directory.
3. Select the unzipped "PolyHaven_Demo_Files" as the "Import Directory".

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/d9cb4665-ad16-4757-ae3b-881cf2c2a542" width="350">

4. Click "Batch Convert".

## User Interface

## General Usage 🏭

1. **Select a directory** containing 3D files of the chosen **import format**, or a parent directory of arbitrary organization and/or depth as long as there exists at least one 3D file of the specified import format somewhere inside.  Try out the [Demo](#demo-) 🧪 below to get started.

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/9e977a7f-57d7-4659-a5eb-df903e837e79" width="250">

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/e3dc4110-ff04-4297-8698-18a1ce5a358f" width="600">


2. **Select an output directory** to which 3D files of the chosen **export format(s)** should be exported. "Adjacents" means that converted models will be saved to the same directories from which they were imported. "Custom" means that converted models will be saved to a chosen custom directory.

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/116d5ace-0772-48ac-9f2e-c68195019591" width="250">

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/cb6dbc9e-1eee-4b79-a3f5-bd3866f4b2ad" width="250">

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/f5c54398-b248-4cae-9ddd-e57511750e00" width="250">


3. **Set additional export settings** as described in the [Features](#features-) section below. (_Optional: to save current settings for later use, save the current .blend file_)

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/248c5c34-1100-4822-a285-6e11571ebdd2" width="250">


4. **Click "Batch Convert"**. This will spawn another instance of Blender. The new Blender window will remain grey while the conversion process gets output to the console window. The original Blender window will remain frozen/unresponsive until the batch conversion is complete. This is normal operation. After the conversion finishes, the greyed-out Blender window will disappear and the original Blender instance will report how many files were converted.  If you wish to see the conversion process get logged in real-time, you must start Blender from your terminal/Command Line first before Transmogrifying.

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/02bf64ab-3675-4175-bcba-0af212ec97f3" width="250">

(Ubuntu Example)

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/1ebf7242-368f-4199-aaef-8ce7fe1ca05a" width="600">

(Windows Example)

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/053903c1-5167-488e-86e4-a5c65a7aa6ad" width="600">

<img src="https://github.com/SapwoodStudio/Transmogrifier/assets/87623407/90cc4699-137c-4c69-bf8d-dd887d2cae61" width="350">
