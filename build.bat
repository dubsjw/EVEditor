pyuic5 resources/forms/evEditor.ui -o EVEditor/ui_eveditor.py
pyuic5 resources/forms/valueEditor.ui -o EVEditor/ui_valueeditor.py
pyrcc5 resources/resources.qrc -o EVEditor/resources.py


pyinstaller --uac-admin ^
--onefile ^
--windowed ^
--name EVEditor ^
--manifest EVEditor.exe.manifest ^
--icon=resources/icons/icon.ico ^
--paths eveditor_env\Lib\site-packages\PyQt5\Qt\bin ^
--paths EVEditor ^
EVEditor/EVEditor.py 

