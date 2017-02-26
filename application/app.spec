# -*- mode: python -*-

import os

print os.getcwd()
path = os.getcwd()

block_cipher = None

            

a = Analysis(['app.py'],
             pathex=[path],
             binaries=[],
             datas=[(path+ '/datas/fonts/*', '/qtawesome/fonts')],
             hiddenimports = ['qtawesome','sklearn.neighbors.typedefs'],
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
          name='app',
          debug=False,
          strip=False,
          upx=True,
          console=True )
