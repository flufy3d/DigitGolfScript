@echo off
set "maya_bin_path=C:\Program Files\Autodesk\Maya2015\bin"
set "export_path=D:\Kenshin\digitgolf\Raw\Level\Common\mb_output"
set "source_path=D:\Kenshin\digitgolf\Raw\Level\Common\MB files-Objects"
set "texture_path1=D:\Kenshin\digitgolf\Raw\Level\Common\Objects"
set "texture_path2=D:\Kenshin\digitgolf\Raw\Level\Common\QuadTextures"
set "extension=png"


::echo %maya_bin_path%
"%maya_bin_path%\mayapy.exe" fix_texture_path.py "%export_path%" "%source_path%" "%texture_path1%" "%texture_path2%" "%extension%"
pause