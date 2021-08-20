import ar
from ar import  video_src
# from nokia import Dicts,Dictz
import os 

if ar.close.startflag == True:
    video = ar.App()
    video.run()
    ###dictionary creation
    # print('dicts',Dicts)
    #         # Dicts.sort(key=lambda x:x['Timestamp'])
    # print('dictz',Dictz)
    # f = open("Dictz.txt","a+")
    # f.truncate(0)
    # f.write( str(Dictz) )

    #######crop folder creation
    # path = "crop"

    # try:  
    #     os.mkdir(path)
    # except OSError:  
    #     print ("crop folder creation %s failed" % path)
    # else:  
    #     print ("Successfully created the crop folder %s " % path)

        
else:
    print("Application closed!!!!!!")
    
# else:
#     print("chasis not placed properly ")
