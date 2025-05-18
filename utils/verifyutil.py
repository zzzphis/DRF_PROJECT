import os
import random
import string

from PIL import Image, ImageDraw, ImageFont


class ImageVerify():
    def __init__(self, x=120, y=40, length=4, size=30):
        """
        :param x: width
        :param y: height
        :param length: string length
        :param size: string size
        """
        self.x = x
        self.y = y
        self.length = length
        self.size = size

    def random_str(self):
        """
        随机生产字符串(生成答案)
        :return:
        """
        source = string.ascii_letters + string.digits
        return ''.join(random.sample(source, self.length))

    def random_color(self, start=0, end=255):
        res = [random.randint(start, end) for _ in range(3)]
        return tuple(res)

    def random_lists(self, draw):
        """
        生成随机干扰线
        :param draw:
        :return:
        """
        for i in range(self.length):
            lines = [(random.randint(0, self.x), random.randint(0, self.y)) for i in range(2)]
            draw.line(lines, fill=self.random_color(64, 200), width=2)

    def random_points(self, draw, rate):
        """
        生成随机干扰点
        :param draw:
        :param rate:
        :return:
        """
        for x in range(self.x):
            for y in range(self.y):
                if random.randint(1, 100) <= rate:
                    draw.point(xy=(x, y), fill=self.random_color(64, 200))

    def verify_code(self):
        """
        生成验证码
        :return:
        """
        image = Image.new('RGB', size=(self.x, self.y), color=(255, 255, 255))
        file = os.path.dirname(os.path.abspath(__file__))
        # 设置字体
        font = ImageFont.truetype(f'{file}/fontfamily/Monaco.ttf', self.size)

        draw = ImageDraw.Draw(image)
        self.random_lists(draw)
        self.random_points(draw, 15)
        code = self.random_str()
        for i in range(self.length):
            draw.text(xy=(i * self.size + 5, random.randint(0, 6)), text=code[i], font=font,
                      fill=self.random_color(60, 200))
        return image, code


if __name__ == '__main__':
    image_verify = ImageVerify()
    img, code = image_verify.verify_code()
    print(code)
    with open('./verifycode.png', 'wb') as f:
        img.save(f, 'png')
