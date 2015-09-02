@echo off
set "maya_bin_path=C:\Program Files\Autodesk\Maya2015\bin"
set "export_path=D:\Kenshin\digitgolf\Raw\Level\Common"
set "source_path=D:\Kenshin\digitgolf\Raw\Level\Common\MB files-Objects"


::echo %maya_bin_path%
"%maya_bin_path%\mayapy.exe" find_multi_texture.py "%export_path%" "%source_path%"
pause