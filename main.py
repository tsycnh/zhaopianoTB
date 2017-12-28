from PIL import Image

CANVAS_WIDTH = 1200
IMAGE_WIDTH = int(1*CANVAS_WIDTH)

IMAGES_LIST = [
'淘宝/信.jpg',
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
def load_images(file_list):
    imgs = []
    for path in file_list:
        img =Image.open(path)
        imgs.append(img)
    return imgs
class Canvas():
    def __init__(self,width):
        self.bg = Image.open('background.png')
        self.canvas = Image.new('RGB',size=(width,100),color=(255,0,0))#初始化大小

    def append(self,image):
        image = self.formatImage(image)
        new_height = self.canvas.height + image.height
        new_canvas = Image.new('RGB',size=(self.canvas.width,new_height))
        new_canvas.paste(self.canvas)
        x = int((self.canvas.width-image.width)/2)
        new_canvas.paste(image,(x,self.canvas.height))
        self.canvas = new_canvas

    def formatImage(self,img):
        new_w = IMAGE_WIDTH
        new_h = int((new_w/img.width)*img.height)
        return img.resize(size=(new_w,new_h))

    def export(self,save_to_disk = True):
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
        if save_to_disk:
            for key,item in enumerate(ex_imgs):
                item.save('./淘宝图'+str(key)+'.jpg')
        return ex_imgs

imgs = load_images(IMAGES_LIST)

c = Canvas(CANVAS_WIDTH)

for img in imgs:
    c.append(img)
# c.canvas.show()
ex_imgs = c.export()
# for i in ex_imgs:
#     i.show()
