# -*- mode: python -*-

block_cipher = None


a = Analysis(['d:\\4-Work\\NMHproject\\iterui\\InputDlg.py'],
             pathex=['d:\\4-Work\\NMHproject\\iterui', 'C:\\Python35\\Lib\\site-packages', 'C:\\Python35\\Lib\\site-packages\\PyQt5\\Qt\\bin', 'D:\\4-Work\\项目\\2016年3月ITER活化手册项目\\FDSNMH_GUI'],
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
          name='InputDlg',
          debug=False,
          strip=False,
          upx=True,
          console=True , icon='d:\\4-Work\\NMHproject\\fds.ico')
