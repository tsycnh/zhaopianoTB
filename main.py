#-*- coding:gbK -*-
#!/usr/bin/env python

from PIL import Image,ImageDraw
from utils import image_stitch,add_text,load_images
import argparse
import os.path
import shutil

CANVAS_WIDTH = 1200
IMAGE_RATIO = 0.9
IMAGE_WIDTH = int(IMAGE_RATIO*CANVAS_WIDTH)
BLOCK_GAP = int((1-IMAGE_RATIO)*CANVAS_WIDTH/2)
IMAGES_LIST = [
'淘宝/信.png',
'淘宝/淘宝图1：放大镜1.jpg',
'淘宝/淘宝图2：打印效果.jpg',
'淘宝/淘宝图3：PDF+JPG.jpg',
'淘宝/淘宝图4：指法标注.jpg',
'淘宝/淘宝图5：教学视频.jpg',
'淘宝/淘宝图6：演奏音频.jpg',
'淘宝/淘宝图7：粉丝群.jpg',
'淘宝/淘宝图8：发货说明.jpg',
'淘宝/淘宝图9：五星好评.jpg'
]
EXPORT_HEIGHT = 1920

class Canvas():
    def __init__(self,width):
        self.bg = self.formatImage(Image.open('bg5.jpg'),new_w=CANVAS_WIDTH)
        self.canvas = self.bg.crop(box=(0,0,width,100))

    def append(self,image,round_corner = -1):
        image, mask = self.formatImage(image,round_corner=round_corner)
        new_height = self.canvas.height + image.height + BLOCK_GAP
        new_canvas = Image.new('RGBA',size=(self.canvas.width,new_height))
        validbg = self.validBg(image.height+BLOCK_GAP)
        new_bg = validbg.crop(box=(0, 0, CANVAS_WIDTH-1, image.height+BLOCK_GAP))
        new_canvas.paste(self.canvas)#粘之前的图
        x = int((self.canvas.width-image.width)/2)
        new_canvas.paste(new_bg,(0,self.canvas.height))
        new_canvas.paste(image,(x,self.canvas.height),mask=mask)
        self.canvas = new_canvas
    def append_png(self,image):
        # 将image2接在image1下面
        image= self.formatImage(image)
        new_height = self.canvas.height + image.height + BLOCK_GAP
        new_canvas = Image.new('RGBA',size=(self.canvas.width,new_height))
        validbg = self.validBg(image.height+BLOCK_GAP)
        new_bg = validbg.crop(box=(0, 0, CANVAS_WIDTH-1, image.height+BLOCK_GAP))
        new_canvas.paste(self.canvas)#粘之前的图
        x = int((self.canvas.width-image.width)/2)
        new_canvas.paste(new_bg,(0,self.canvas.height))
        new_canvas.paste(image,(x,self.canvas.height),mask=image)
        self.canvas = new_canvas
    def formatImage(self,img,new_w = IMAGE_WIDTH,round_corner = -1):
        # new_w = IMAGE_WIDTH
        new_h = int((new_w/img.width)*img.height)
        new_img = img.resize(size=(new_w,new_h))

        if round_corner > 0:
            mask = Image.new(mode='L',size=new_img.size) # 8bit灰度图
            draw = ImageDraw.Draw(mask)
            d = 2*round_corner
            w,h = mask.width,mask.height
            draw.ellipse(xy=[0,0,d,d],fill=(255))
            draw.ellipse(xy=[mask.width-1-d,0,mask.width-1,d],fill=(255))
            draw.ellipse(xy=[0,mask.height-d,d,mask.height],fill=(255))
            draw.ellipse(xy=[mask.width-1-d,mask.height-d,mask.width-1,mask.height],fill=(255))

            draw.rectangle(xy=[d/2,0,w-d/2,h],fill=255)
            draw.rectangle(xy=[0,d/2,w,h-d/2],fill=255)
            # mask.show()
            return new_img,mask
        return new_img

    def validBg(self,asked_height):
        i=2
        bg = self.bg
        while asked_height>bg.height:
            new_bg = Image.new('RGB',size=(self.bg.width,self.bg.height*i))
            new_bg.paste(bg,box=(0,0))
            new_bg.paste(self.bg,box=(0,self.bg.height*(i-1)))
            bg = new_bg
            i+=1
        return bg
    def export(self,save_to_disk = ""):
        current_height = self.canvas.height
        if current_height%EXPORT_HEIGHT == 0:
            total_pages = current_height//EXPORT_HEIGHT
        else:
            total_pages = current_height//EXPORT_HEIGHT + 1
        ex_imgs = []
        for i in range(total_pages):
            left,right = 0,self.canvas.width - 1
            top = i*EXPORT_HEIGHT

            bottom = (i+1)*EXPORT_HEIGHT - 1
            if bottom > self.canvas.height - 1:
                bottom = self.canvas.height - 1
            img = self.canvas.crop(box=(left,top,right,bottom))
            ex_imgs.append(img)
        if save_to_disk != "":
            if os.path.exists(save_to_disk):
                shutil.rmtree(save_to_disk)
            os.mkdir(save_to_disk)
            for key,item in enumerate(ex_imgs):
                item.save(save_to_disk+'/淘宝图'+str(key)+'.jpg')
        return ex_imgs

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('score_file',help='请输入乐谱第一页的文件路径',type=str)
    parser.add_argument('pages',help='请输入全谱页数',type=str)
    parser.add_argument('--nofinger',help='添加此参数表示不输出指法页',action='store_true')
    parser.add_argument('--novideo',help='添加此参数表示不输出教学视频页',action='store_true')
    parser.add_argument('--noaudio',help='添加此参数表示不输出演奏音频页',action='store_true')
    args = parser.parse_args()
    file_name = os.path.basename(args.score_file).split('.')[-2]
    output_dir = os.path.dirname(args.score_file)+'/'+str(file_name)

    score_title     = Image.open('淘宝/淘宝图0：乐谱预览.jpg')
    score_img       = Image.open(args.score_file)
    score_bottom    = Image.open('淘宝/淘宝图10：blank.jpg')



    if args.nofinger:
        IMAGES_LIST.remove('淘宝/淘宝图4：指法标注.jpg')
    if args.novideo:
        IMAGES_LIST.remove('淘宝/淘宝图5：教学视频.jpg')
    if args.noaudio:
        IMAGES_LIST.remove('淘宝/淘宝图6：演奏音频.jpg')
    imgs = load_images(IMAGES_LIST)
    c = Canvas(CANVAS_WIDTH)

    score_bottom = add_text(score_bottom,'全谱共'+args.pages+'页','汉仪小麦体简.ttf')

    score = image_stitch(score_title,score_img)
    score = image_stitch(score,score_bottom)
    imgs.insert(1,score)

    for key,img in enumerate(imgs):
        if key == 0:
            c.append_png(img)
        else:
            c.append(img,round_corner=50)
    ex_imgs = c.export(save_to_disk=output_dir)

