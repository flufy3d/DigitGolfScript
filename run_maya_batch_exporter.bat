@echo off
set "maya_bin_path=D:\Program Files\Autodesk\Maya2015\bin"
set "export_path=D:\projects\digitgolf\Raw\Script\fbx"
set "source_path=D:\projects\digitgolf\Raw\Script\output"


::echo %maya_bin_path%
"%maya_bin_path%\mayapy.exe" maya_batch_exporter.py "%export_path%" "%source_path%"
pause