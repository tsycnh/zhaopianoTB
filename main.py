from PIL import Image

CANVAS_WIDTH = 1200
IMAGE_WIDTH = int(1*CANVAS_WIDTH)
IMAGES_LIST = ['page1.jpg','page2.jpg','page3.jpg']

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
imgs = load_images(IMAGES_LIST)

c = Canvas(CANVAS_WIDTH)

for img in imgs:
    c.append(img)
c.canvas.show()