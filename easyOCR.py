from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import time
import easyocr
import PIL
import numpy as np

# 設定 Chrome 選項
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# 呼叫 Chrome 的套件並設定選項
PATH = "chromedriver.exe"
driver = webdriver.Chrome(PATH, options=chrome_options)

# 開啟指定網頁
driver.get('https://www.books.com.tw/')

# 最大化視窗
driver.maximize_window()

# 等待元素生成
element = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, f'//*[@id="header_full_v2"]/nav/div/div[2]/ul/li[1]/a'))
)

# 點選會員登入
driver.find_element(By.XPATH, f'//*[@id="header_full_v2"]/nav/div/div[2]/ul/li[1]/a').click()

# 先截圖
driver.save_screenshot('sceenshit.png')

# 找到驗證碼
element = driver.find_element(By.XPATH, f'//*[@id="captcha_img"]/img')

# 驗證碼定位
left = element.location['x']
right = element.location['x'] + element.size['width']
top = element.location['y']
bottom = element.location['y'] + element.size['height']

# 圖片擷取後轉灰階
img = Image.open('sceenshit.png')
img = img.crop((left, top, right, bottom))
img = img.convert('L')
img.save('capcha.png')
time.sleep(2)

# 呼叫 OCR 函式
reader = easyocr.Reader(['en'], gpu=False)

# 進行文字辨識
result = reader.readtext('capcha.png', detail=0)

### 輸出
print(result[0:])