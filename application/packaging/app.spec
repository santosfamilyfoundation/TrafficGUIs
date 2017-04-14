# -*- mode: python -*-

import os

path = os.getcwd()

block_cipher = None



a = Analysis([path+'/app.py'],
             pathex=[path],
             binaries=[],
             datas=[(path+ '/datas/fonts/*', '/qtawesome/fonts'),(path+ '/datas/fonts/*', './datas/fonts')],
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
          name='SantosTrafficAnalysis',
          debug=False,
          strip=False,
          upx=True,
          console=True,
          icon = path+'/packaging/santos_app_logo.ico')
