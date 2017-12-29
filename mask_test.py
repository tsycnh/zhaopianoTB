from main import Canvas,load_images

CANVAS_WIDTH = 1200
IMAGE_RATIO = 0.9
IMAGE_WIDTH = int(IMAGE_RATIO*CANVAS_WIDTH)
BLOCK_GAP = int((1-IMAGE_RATIO)*CANVAS_WIDTH/2)
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

imgs = load_images(IMAGES_LIST)
c = Canvas(CANVAS_WIDTH)

c.append(imgs[0],round_corner=100)