# Changelog

## 1.5.0
### New Features
- Blend I/O
- Simple/Advanced UI
- Archive Assets

### Optimizations
- Improved context overrides with new convention.
- Replaced "Save Preview" viewport render with extracted asset preview images.

### Bug Fixes
- Fixed objects not transforming around the 3D Cursor.
- Fixed messy nodes resulting from adaptation of Node Wrangler's "Add Principled Setup".
- Fixed Custom textures source bug that had resulted in not preserving materials/textures when a model imported with materials of the same name.
- A number of bugs resulting from new features.

### Documentation
- Updated screenshots.
- Added documentation for new features.
- Revised texture Rule No. 3.


***
## 1.4.0
### New Features
- GNU/Linux support
- OpenEXR support
- Export UVs
- Rename UVs
- PolyHaven demo files (see attached)

### Optimizations
- Rewrote pathing to use Python's pathlib instead of os.path
- Organized UI into sections

### Bug Fixes
- Fixed auto-texture resize/reformat failing for custom textures
- Fixed a variety of bugs resulting from the pathlib pathing rewrite.

### Documentation
- Added new screenshots
- Added "UVs" and "Demo" sections


***
## 1.3.1-hotfix.1
### New Features
- N/A

### Optimizations
- N/A

### Bug Fixes
- Hotfixed major bug in "Custom" textures scenario. 
    - This bug was missed because save_blend & keep_textures_temp settings were turned on during testing, which had preserved custom textures and materials. However, it was discovered that when these settings were turned off, custom textures & materials were getting deleted after the first item converted. This was due to 1) no fake users getting set, 2) fake users getting removed, and 3) purge orphans happening for every item converted. Custom materials & textures are now preserved throughout the conversion 

### Documentation
- N/A


***
## 1.3.0
### New Features
- Workflow Presets

### Optimizations
- Converted many hard-code to dynamic-code.
- Made "Copy Assets to Preferences" a proper operator button.

### Bug Fixes
- Removed 3-character regex keys, which were too aggressive .
- (e.g. the key "[Ss]ss was turning textures/materials called "StainlessSteel" into "Subsurface")
- Fixed many bugs arising from dynamic-code optimizations (see commits for specifics).
- Fixed other minor bugs (see commits for specifics).

### Documentation
- Improved texture convention documentation.
- Included documentation for Workflows.


***
## 1.2.0
### New Features
- Rename all UV Maps to "UVMap"
- Custom output directory
- Place exports in subdirectories within custom output directory
- Copy original files into each respective subdirectory

### Optimizations
- Improve regex PBR tag keys
- Reorganized UI
- Made UI more compact
- Created functions from some existing code blocks

### Bug Fixes
- A variety of bugs from regex to custom output directory features. See commits for specifics.

### Documentation
- Added many new diagrams and screenshots
- Improved explanations
- Made a logo


***
## 1.1.0
- Updated to Blender 3.6 and remade export presets. 
- Rewrote Auto Resize algorithm.
  - Added menu for choosing what to auto-resize.

  - Added new method options:
    - Resize Textures minimum resolution.
    - Decimate Meshes max number of decimation iterations.


***
## 1.0.0
Initial release of the Transmogrifier addon for Blender.

- Wrote documentation for README.md
- Uploaded initial files.