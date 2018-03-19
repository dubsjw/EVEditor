# -*- mode: python -*-

block_cipher = None


a = Analysis(['EVEditor\\EVEditor.py'],
             pathex=['eveditor_env\\Lib\\site-packages\\PyQt5\\Qt\\bin', 'EVEditor', 'C:\\Users\\jacob.dubs\\Desktop\\Development\\Misc\\EVEditor'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='EVEditor',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , uac_admin=True, icon='resources\\icons\\icon.ico', manifest='EVEditor.exe.manifest')
