@echo off
set "maya_bin_path=D:\Program Files\Autodesk\Maya2015\bin"
set "export_path=D:\projects\digitgolf\Raw\Script\output"
set "source_path=D:\projects\digitgolf\Raw\Level\NineDragonsA\MB files-Objects"
set "texture_path1=D:\projects\digitgolf\Raw\Level\NineDragonsA\Objects"
set "texture_path2=D:\projects\digitgolf\Raw\Level\NineDragonsA\QuadTextures"
set "extension=png"


::echo %maya_bin_path%
"%maya_bin_path%\mayapy.exe" fix_texture_path.py "%export_path%" "%source_path%" "%texture_path1%" "%texture_path2%" "%extension%"
pause