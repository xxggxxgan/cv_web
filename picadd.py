from PIL import Image, ImageDraw, ImageFont
import os
import random


COLOR_PATH = './static/color'
COVER_PATH = './static/cover'
IMAGES_PATH = './static/img'  # 图片集地址
IMAGES_FORMAT = ['.jpg', '.JPG']  # 图片格式
IMAGE_SIZE = 1669  # 每张小图片的大小
IMAGE_ROW = 4  # 图片间隔，也就是合并成一张图后，一共有几行
IMAGE_COLUMN =3   # 图片间隔，也就是合并成一张图后，一共有几列
IMAGE_SAVE_PATH = './static/images/final.jpg'  # 图片转换后的地址
#1669

#women case
Image_Path_test_w = './static/gender/woman.jpg'
imgw = Image.open(Image_Path_test_w)  
  

#man case
Image_Path_test_m = './static/gender/man.jpg'
imgm = Image.open(Image_Path_test_m)  

#cover case
# Image_Path_test_cover = './static/layer.png'
# imgcover = Image.open(Image_Path_test_cover)  




# 获取图片集地址下的所有图片名称
kk = [os.path.splitext(name)[0] for name in os.listdir(IMAGES_PATH) for item in IMAGES_FORMAT if
               os.path.splitext(name)[1] == item]
vv = [name + ".jpg" for name in kk]
print(kk)
#print(vv)
image_names = [name for name in os.listdir(IMAGES_PATH) for item in IMAGES_FORMAT if
               os.path.splitext(name)[1] == item]
image_names = image_names[0:9]
#print(image_names)

#random.shuffle(image_names)

to_image = Image.new('RGB', (5007, 6676),(255,255,255))
coverlist = ['layer1.png','layer2.png','layer3.png','layer4.png','layer5.png','layer6.png','layer7.png','layer8.png','layer9.png']

colorlist = ['color1.png','color2.png','color3.png','color4.png','color5.png','color6.png','color7.png','color8.png','color9.png']

def image_final(gender,commonlist,text,date):
    if(gender == 'male'):
        imgm.resize((3338,3338),Image.ANTIALIAS)
        to_image.paste(imgm,(0,3338))
    else:
        imgw.resize((3338,3338),Image.ANTIALIAS)
        to_image.paste(imgw,(0,3338))
    count = 0
    random.shuffle(coverlist)
    random.shuffle(colorlist)
    print('cover we use is ',coverlist[0])
    print('color we use is ',colorlist[0])
    tocover = Image.open(COVER_PATH + "/" +coverlist[0]).resize(
                                to_image.size,Image.ANTIALIAS)

    tocolor = Image.open(COLOR_PATH + "/" +colorlist[0]).resize(
                                to_image.size,Image.ANTIALIAS)                         

    for y in range(0, IMAGE_ROW ):
        for x in range(0, IMAGE_COLUMN ):
            if(x != 0 or y!= 2 ):
                if(x != 0 or y!= 3):
                    if(x != 1 or y!= 3):
                        if(count < 9):
                            #print("x + y " , x ," ",y)
                            from_image = Image.open(IMAGES_PATH + "/" +commonlist[count]).resize(
                                (IMAGE_SIZE, IMAGE_SIZE),Image.ANTIALIAS)
                            from_image.convert('1')
                            to_image.paste(from_image, (x  * IMAGE_SIZE, y * IMAGE_SIZE))
                            count += 1
    #to_image.resize((900,1200),Image.ANTIALIAS)
    font = ImageFont.truetype('./static/Carneys Gallery.ttf',280)
    font2 = ImageFont.truetype('./static/Carneys Gallery.ttf',120)
    draw = ImageDraw.Draw(to_image)
    
    draw.text((160,6020),date, fill=(0,0,0),font=font)
    draw.text((160,6350),text, fill=(0,0,0),font=font2)

    #imgcover.resize(to_image.size,Image.ANTIALIAS)
    #to_image.paste(imgcover,mask = imgcover)
    to_image.paste(tocover,mask = tocover)
    to_image.paste(tocolor,mask = tocolor)
    return to_image.save(IMAGE_SAVE_PATH) 
    #return sd.save(IMAGE_SAVE_PATH)

#image_final('male',image_names,'sdsad','safsa')

#image_final('male')
