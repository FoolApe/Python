### Hebe演唱會 , 帶入cookie登入後開啟座位表
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep
import easyocr
import json

# 設定 Chrome 選項
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# 呼叫 Chrome 的套件並設定選項
PATH = "chromedriver.exe"
driver = webdriver.Chrome(PATH, options=chrome_options)

# 開啟指定網頁
driver.get('https://tixcraft.com/activity/detail/23_hebe')

# 最大化視窗
driver.maximize_window()

# 設定cookie參數
with open('cookie/hebe.json') as f:
    cookies = json.load(f)
for cookie in cookies:
    driver.add_cookie(cookie)
driver.refresh() ### 完成後會發現已成功登入

# 等待元素導入
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, f'/html/body/div[2]/div[1]/section[1]/div[3]/div/div/div/div[1]/img'))
)

# show 出資訊
i = 13
while i <= 20:
    raw = driver.find_element(By.XPATH, f'//*[@id="intro"]/p[{i}]/span/span')
    info = raw.text
    print(info)
    i += 1

# 開一個新分頁 , 切換到分頁
driver.execute_script("window.open();")
driver.switch_to.window(driver.window_handles[1])

# 打開座位表
image_url = "https://static.tixcraft.com/images/activity/field/23_hebe_f75ed57befb94d8114731b511c6f5e2b.png"
driver.get(image_url)