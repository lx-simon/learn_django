from PIL import Image, ImageDraw, ImageFont

img = Image.new(mode='RGB', size=(120, 30), color=(255, 255, 255))
 
# 在图片查看器中打开
# img.show() 
font = ImageFont.truetype("验证码字体文件/Monaco.ttf", 28)
draw = ImageDraw.Draw(img, mode='RGB')
# 第一个参数：表示起始坐标
# 第二个参数：表示写入内容
# 第三个参数：表示颜色
draw.text([0,0],'xxx',"black",font=font)
# 保存在本地
with open('code.png','wb') as f:
    img.save(f,format='png')