import time
from selenium import webdriver
from PIL import Image
from aip import AipOcr
import os

driver = webdriver.Chrome()

##打开浏览器
driver.get('http://pt.cdzj.chengdu.gov.cn:8202/Login.aspx?')

#窗口最大化
driver.maximize_window()

# (1)登录页面截图
driver.save_screenshot("D:\TestFile\Testshuju\pic.png")#可以修改保存地址

# (2)输入用户名和密码
driver.find_element_by_id("txtUserId").send_keys("ywzy")
driver.find_element_by_id("txtPassword").send_keys("Zy123321")

# (3)获取图片验证码坐标
code_ele = driver.find_element_by_id("imgVerfyCode")
# print("验证码的坐标为：", code_ele.location)#控制台查看{'x': 1032, 'y': 458}
# print("验证码的大小为：", code_ele.size)# 图片大小{'height': 30, 'width': 120}

# (4)图片4个点的坐标位置
left = code_ele.location['x']+2#x点的坐标
top = code_ele.location['y']+2#y点的坐标
right = code_ele.size['width']-3+left#上面右边点的坐标
down = code_ele.size['height']-3+top#下面右边点的坐标
image = Image.open('D:\TestFile\Testshuju\pic.png')

# (5)将图片验证码截取
code_image = image.crop((left, top, right,down))
code_image.save('D:\TestFile\Testshuju\pic1.png')#截取的验证码图片保存为新的文件

# (6)调用百度API识别验证码
""" 你的 APPID AK SK """
APP_ID = '24744093'
API_KEY = 'qwQ0NkPg9phe6QeejvBT4ung'
SECRET_KEY = 'YGrztkNlbKX8ZfXkS1Xh0BDTqGqttDTu'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


""" 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

image = get_file_content('D:/TestFile/Testshuju/pic1.png')

""" 调用通用文字识别, 图片参数为本地图片 """
code_ocr_original_result=client.basicAccurate(image);
for text in code_ocr_original_result.get('words_result'):
    code_ocr_final_result=text.get('words')

"""去掉识别验证码中的空格"""
nospace_result=code_ocr_final_result.replace(" ","")
# print(nospace_result)

# (7)输入验证码
driver.find_element_by_id("txtYzm").send_keys(nospace_result)
time.sleep(2)

# (8)点击登录
driver.find_element_by_css_selector("[value='登录']").click()

# #关闭打开的窗口
# driver.quit()