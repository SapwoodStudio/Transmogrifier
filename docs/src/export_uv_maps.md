# Export UV Maps

Export UVs with the same options available via the UV Editor and more.

![Export_UV_Maps.gif](assets/images/Export_UV_Maps.gif)



## Destination 
Set a location for UV's to be exported into.

![Export_UV_Maps_Destination.gif](assets/images/Export_UV_Maps_Destination.gif)

| `Textures` | `UV` | `Model` | `Custom` | 
| ---- | ---- | ---- | ---- |
| Export UVs to a Textures subfolder for each item. If none exists, it creates one. | Export UVs to a 'UV' subfolder for each item. If none exists, it creates one. | Export UVs adjacent to each respective import file. | Export all UVs to a custom directory of choice. |

## Combination
Set how UVs should be combined for export.

![Export_UV_Maps_Combination.gif](assets/images/Export_UV_Maps_Combination.gif)

| `All` | `Object` | `Material` |
| ---- | ---- | ---- |
| Export all UVs together | Export UVs by object | Export UVs by material |
| 1 UV layout per converted model | 1 UV layout per object | 1 UV layout per material |


## Image Settings
Adjust the image `Resolution`, `Format`, and `Fill Opacity`.


## Rename UVs
Synchronize UV map names among every mesh object with a custom name.

Multiple UV maps within the same object will increment, for example, as 'UVMap', 'UVMap_1', 'UVMap_2', and so on. 

!!! example
    Some model files contain mesh objects made in different DCC apps.  Maya, Max, Blender, Modo, etc. use different conventions for naming UV channels.  The difference in channel names can cause errors for certain export formats, which is the reason this feature exists.

!!! bug "USD files and UV Maps"
    `Rename UVs` prevents a bug in USD formats when two or more objects share the same material but have different UV map names, which causes some objects to appear untextured.


***
!!! question "Missing Something?"
    Do you think we're missing a feature?  Submit a request on Github!

    [Request Feature](https://github.com/SapwoodStudio/Transmogrifier/issues){ .md-button .md-button--primary }