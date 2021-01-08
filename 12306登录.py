import asyncio
import os
import sys
import time
import random

from PIL import Image
from pyppeteer import launch

from Chaojiying_Python import chaojiying

width, height = 1915, 750
sys.path.append(os.getcwd() + "/Chaojiying_Python")

from chaojiying import Chaojiying_Client


async def main():
    browser = await launch({"headless": False}, args=['--disable-infobars', f'--window-size={width},{height}'])
    page = await browser.newPage()
    await page.setViewport({'width': width, 'height': height})
    await page.goto('https://kyfw.12306.cn/otn/resources/login.html')

    await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
    a = await page.xpath("//li[@class='login-hd-account']/a")
    await asyncio.sleep(2)
    await a[0].click()
    await asyncio.sleep(2)
    await page.screenshot({'path': '12306.png'})
    # await page.xpath("//input[@id='J-userName']")
    await page.type("#J-userName", '15340851022')
    await page.type("#J-password", 'lr060018')

    locations = await page.xpath("//img[@id='J-loginImg']")
    location = await locations[0].boundingBox()
    left = int(location['x'])
    top = int(location['y'])
    right = left + 300
    bottom = top + 188

    # 通过Image处理图像
    im = Image.open('12306.png')
    im = im.crop((left, top, right, bottom))
    # 保存得到的验证码图片
    im.save('code.png')

    chaojiying = Chaojiying_Client('lemon1106', 'lr060018', '96001')  # 用户中心>>软件ID 生成一个替换 96001
    im = open('code.png', 'rb').read()  # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
    ret = chaojiying.PostPic(im, 9004)  # 1902 验证码类型  官方网站>>价格体系 3.4+版 print 后要加()
    print(ret)
    pic_list = []
    pic_str = ret['pic_str']
    if pic_str.find('|') != -1:
        pic = pic_str.split('|')
        for p in pic:
            pic_2 = p.split(',')
            pic_list.append(pic_2)
            print(pic_2)

    else:
        pic_2 = pic_str.split(',')
        pic_list.append(pic_2)

    for pic in pic_list:
        left = left + int(pic[0]) + 5
        top = top + int(pic[1]) + 2.5
        print(left, top)
        # await page.mouse.move(left, top)
        await page.mouse.click(left, top)
        await page.waitFor(random.randint(567, 3456))
        # await page.mouse.click(left,top)
        print('111')
    login = await page.xpath("//div[@class='login-btn']")
    await login[0].click()

    time.sleep(100)


asyncio.get_event_loop().run_until_complete(main())
