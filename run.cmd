@echo off
for %%i in (*.als) do (python AbletonMaExport.py "%%i" --nolog)
@echo processed given project files
@echo on