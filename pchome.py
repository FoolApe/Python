from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

# 設定 Chrome 選項
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# 設定使用者代理，使程式更像真人
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
chrome_options.add_argument(f"user-agent={user_agent}")

# 呼叫 Chrome 的套件並設定選項
PATH = "chromedriver.exe"
driver = webdriver.Chrome(PATH, options=chrome_options)

# 網頁函式
def load_browser(url):
    # 開啟指定網頁
    driver.get(url)

    # 最大化視窗
    driver.maximize_window()

    # 帶入 cookie 登入 > Only with name/value/domain
    with open('cookie/pchome.json') as f:
        cookies = json.load(f)
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()

    # 等待暢銷排行導入
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, 'bestSellers'))
    )

    # 秀出所有暢銷商品
    best_items = driver.find_elements(By.CSS_SELECTOR, '.c-listInfo__list .c-listInfo__item.c-listInfo__item--bg')

    # 逐一印出每個元素的 title
    for item in best_items:
        title = item.find_element(By.CSS_SELECTOR, '.c-prodInfo__title').text
        print(title)

    # 關閉瀏覽器
    driver.quit()

# 呼叫函式(網址/價錢/張數)
load_browser('https://24h.pchome.com.tw/')
