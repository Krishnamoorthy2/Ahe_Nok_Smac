# -*- mode: python -*-

block_cipher = None


a = Analysis(['Nokia_Client.py'],
             pathex=['C:\\Users\\SmacAR\\Desktop\\Nokia_PA_local_build\\EXW'],
             binaries=[],
             datas=[],
             hiddenimports=['os','certifi','threading','winsound','tkinter','smtplib','tkinter.messagebox','PIL.Image','PIL.ImageTk','datetime','time',
            'paho.mqtt.subscribe','paho.mqtt.publish','requests','argparse','cv2','numpy','json','pi3d','traceback','glob','pickle',
            'collections','logging','utils.log','math','base64','initial','subprocess','tkinter.font',
            'entry','center','render.py3d','render.overlay','render.ui','render.btn','ar','network.analytics','network.text_handler',
            'camera.camera','core.detector','core.tracker','utils.utils','utils.log','utils.config','nokia','generate_log',
            'db_collector','db_validation','imutils','log_generator','tensorflow','write_xml','xml.etree.cElementTree','xml.dom.minidom','bs4','lxml','logits1','logits2','logits3','logits4','Object_detection_testing_single','re','sys','google','google.protobuf'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Nokia_Client',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          icon='50.ico' )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='Nokia_Client')