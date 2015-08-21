@echo off
set "maya_bin_path=C:\Program Files\Autodesk\Maya2015\bin"
set "export_path=D:\Kenshin\digitgolf\Raw\Level\Common\fbx_output"
set "source_path=D:\Kenshin\digitgolf\Raw\Level\Common\MB files-Objects"


::echo %maya_bin_path%
"%maya_bin_path%\mayapy.exe" maya_batch_exporter.py "%export_path%" "%source_path%"
pause