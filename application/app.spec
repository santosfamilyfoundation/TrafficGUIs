# -*- mode: python -*-

block_cipher = None

a = Analysis(['app.py'],
             pathex=['/Users/user/Documents/SantosGUI/application'],
             binaries=[],
             datas=[],
             hiddenimports = [
             'packaging.qt',
             'sklearn.neighbors.typedefs'
             ],
             hookspath=['packaging'],
             runtime_hooks=['packaging/rthook_pyqt4.py',
                            'packaging/rthook_qtapi.py'], 
             excludes=['Tkinter', 'FixTk',
                       'IPython', 'PyQt4.QtAssistant',
                       'PyQt4.QtNetwork', 'PyQt4.QtWebKit',
                       'PyQt4.QtSql', 'PyQt4.QtXml', 'PyQt4.QtTest', 
                       'PyQt4.QtOpenGL'],
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
