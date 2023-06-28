import bpy
op = bpy.context.active_operator

op.filepath = ''
op.selected_objects_only = True
op.visible_objects_only = False
op.export_animation = False
op.export_hair = False
op.export_uvmaps = True
op.export_normals = True
op.export_materials = True
op.use_instancing = False
op.evaluation_mode = 'RENDER'
op.generate_preview_surface = True
op.export_textures = True
op.overwrite_textures = False
op.relative_paths = True
op.root_prim_path = ''
