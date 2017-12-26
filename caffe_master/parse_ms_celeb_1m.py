import base64
import struct
import os
import sys
sys.path.append("../test_lfw/")
from fr_wuqianliang import *

clean_list = {}
file_object = open('MS-Celeb-1M_clean_list.txt', 'r')
for line in file_object:
    arr=line.split(' ')
    clean_list[arr[0]]=1


def readline(line):
    MID,ImageSearchRank,ImageURL,PageURL,FaceID,FaceRectangle,FaceData=line.split("\t")
    rect=struct.unpack("ffff",base64.b64decode(FaceRectangle))
    return MID,ImageSearchRank,ImageURL,PageURL,FaceID,rect,base64.b64decode(FaceData)

def writeImage(filename,data):
    with open(filename,"wb") as f:
        f.write(data)

def unpack(filename,target="img"):
    i=0
    with open(filename,"r") as f:
        for line in f:
            MID,ImageSearchRank,ImageURL,PageURL,FaceID,FaceRectangle,FaceData=readline(line)
            img_dir=os.path.join(target,MID)
            if not os.path.exists(img_dir):
                os.mkdir(img_dir)
            img_name="%s-%s"%(ImageSearchRank,FaceID)+".jpg"
            crop_image = crop_align_image(FaceData)
            if clean_list.has_key(img_dir+'/'+img_name) and crop_image is not None:
                writeImage(os.path.join(img_dir,img_name),FaceData)
                print('Processed image:',img_dir+'/'+img_name)
                i+=1
            if i%1000==0:
                print(i,"imgs finished")
    print("all finished")    

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python %s MsCelebV1-Faces-Aligned.tsv MsCelebV1-Faces-Aligned-parsed-dir' % (sys.argv[0]))
        sys.exit()
    tsv_file     = sys.argv[1]
    parsed_dir  = sys.argv[2]

    unpack(tsv_file,target=parsed_dir)
