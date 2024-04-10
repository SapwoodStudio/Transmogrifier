# Auto-Optimize File Size

Perform automatic file-optmization methods adaptive to every model in order reduce the exported file size below a custom target threshold. Filter which methods are used. 

!!! tip 
    This feature adapts to each model, meaning that Transmogrifier iteratively reduces an export's file size only inasmuch as required to "sneak" below the target threshold.  This allows you to always have each individual export exist at its maximum allowable quality within the limit you set.


![Optimize File Size.gif](assets/images/Optimize File Size.gif)


## Target
Set a target threshold below which Transmogrifier should attempt to adaptively reduce each export files' size (in `Megabytes`).  


## Overwrite Files
If you elected to `Overwrite Exports` above in the `Exports` box, then you have the option to overwrite `All` existing export files or overwrite export files `Only Above Target`.  

!!! question "How is this helpful?"
    Sometimes a batch conversion with auto-optimize can still yield some exports with file sizes above the target threshold.  This allows you to focus on re-batch-converting only the few outliers that need extra optimization.
    
    !!! example 
        
        - Let's say that out of `100` models converted, `5` models are still above a target of `15MB`.  
            - Let's also say that batch took `7min.` to process. 
            - But you absolutely have to have all `100` models below `15MB`.

        - You have two options:

            | Overwrite `All` 🐢 | Overwrite `Only Above Target` 🐇 |
            | ---- | ---- |
            | Adjust your auto-optimize settings, re-batch-converting, and waiting another `7min.` for the `100` models to convert all over again when `95` didn't need to. | Adjust your auto-optimize settings, then `Only Above Target` will only re-batch-convert those `5` files in, say, `20sec.`.  You just saved about `6.5min.`! |
    

## Methods

| Method | Description | Adjustment | 
| ---- | ---- | ---- |
| Draco | Try activating Draco compression for exported models. (Only works for `glTF`/`GLB` files) | Draco compression level |
| Resize textures | Set minimum image texture resolution for auto file size not to go below. Images will not be upscaled | Resolution |
| Reformat textures | Try reformatting all textures except the normal map to JPEG's to lower the exported file size | Include Normal Maps (usually avoided because JPG compression causes artifacts in norma maps) |
| Decimate |  Try decimating objects to lower the exported file size (Uses edge collapse at 50% ratio each time. Set a maximum decimate iteration). | Decimate iteration limit |

!!! warning "Decimate Warning"
    [Decimation](https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/decimate.html) is a destructive form of mesh optimization.  When batch converting models with textures, it's important to note that while Blender does its best to preserve UV's when decimating, texture distortion can occur.


!!! example
    For example, let's say you're exporting a `USDZ` with a target threshold set to `15MB` and with default `Methods` settings.  Your import file is a `10MB` `FBX` + (4) 4K, `PNG` external textures at `10MB` each = `50MB` total.  
    
    Transmogrifier will run through the following steps in order to optimize the file:
    
    0. Export the model
        1. Export the model with no adjustments
        2. Get the export file's size (`50MB`)
    1. First iteration    
        1. `Resize Textures` by halving their resolution
            1. `4096px` / `2` = `2048px`
            3. Export the model again
            2. Get the export file's size (`30MB`)
        2. `Reformat Textures` by converting them to a `JPEG` format
            1. Export the model again
            2. Get the export file's size (`22MB`)
                - Since `22MB` is still greater than your target of `15MB`, Transmogrifier will begin again with another optimize iteration 🔁
    2. Second iteration
        1. `Resize Textures` by halving their resolution
            1. `2048px` / `2` = `1024px`
            2. Export the model again
            3. Get the export file's size (`14MB`) 
                - Since `14MB` < `15MB`, Transmogrifier will exit the auto-optimize loop and move on the converting the next model. ✅


!!! question "What if Transmogrifier Runs out of options?"
    If all methods are exhausted and the file size is still above the target maximum, Transmogrifier will report this in the log and move on to converting the next file.


!!! question "Missing Something?"
    Do you think we're missing a feature?  Submit a request on Github!

    [Request Feature](https://github.com/SapwoodStudio/Transmogrifier/issues){ .md-button .md-button--primary }