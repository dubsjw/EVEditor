pyinstaller --uac-admin ^
--onefile ^
--windowed ^
--name EVEditor ^
--manifest EVEditor.exe.manifest ^
--icon=resources/icons/icon.ico ^
--paths eveditor_env\Lib\site-packages\PyQt5\Qt\bin ^
--paths EVEditor ^
EVEditor/EVEditor.py 

