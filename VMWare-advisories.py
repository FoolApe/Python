from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import json
import time
import datetime
import requests

# Telegram Bot 相關設定
TELEGRAM_BOT_TOKEN = "YOUR_TOKEN"
TELEGRAM_CHAT_ID = "CAHT_ID"

# 設定 Chrome 選項
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# 設定使用者代理，使程式更像真人
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
chrome_options.add_argument(f"user-agent={user_agent}")

# 呼叫 Chrome 的套件並設定選項
PATH = "chromedriver.exe" ### You have to download this first
driver = webdriver.Chrome(PATH, options=chrome_options)

# 開啟指定網頁
driver.get("https://www.vmware.com/security/advisories.html")

# 最大化視窗
driver.maximize_window()

# 等待結果載入
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.ID, 'table_id'))
)

# 定位主要列表
tab_pane = driver.find_element(By.XPATH, f'/html/body/div[4]/div/div/div[2]/section/div/div/div/div/div[2]/div[5]/table/tbody')

# 點選嚴重度選單,選取"critical"
driver.find_element(By.XPATH, f'/html/body/div[4]/div/div/div[2]/section/div/div/div/div/div[2]/div[2]/div/div[2]/div[2]/div/button').click()
driver.find_element(By.ID, 'chkbox-Critical').click()

tab_pane = driver.find_element(By.XPATH, f'//*[@id="table_id"]/tbody')

# 等待元素載入
time.sleep(3)

advisories = []  # 儲存所有的 Advisory 結果

if tab_pane is not None:
    # 尋找該元素底下的所有具有 "role=row" 屬性的元素
    row_elements = tab_pane.find_elements(By.CSS_SELECTOR, '[role=row]')

    # 逐一處理每個 row 元素
    for row_element in row_elements:
        # 尋找內部的元素
        details_control = row_element.find_element(By.CLASS_NAME, "details-control")
        severity_block = row_element.find_element(By.CLASS_NAME, "severity-block")
        synopsis_block = row_element.find_element(By.CLASS_NAME, "synopsis-block")
        updated_date_block = row_element.find_element(By.CLASS_NAME, "updatedDate-block")

        # 取得內容及網址
        advisory_id = details_control.text.strip()
        level = severity_block.text.strip()
        description = synopsis_block.text.strip()
        update_date = updated_date_block.text.strip()
        link = details_control.find_element(By.TAG_NAME, "a").get_attribute("href")

        # 取得當前年份
        current_year = datetime.datetime.now().year
        date_parts = update_date.split('-')

        # 解析日期並檢查是否為今年
        if len(date_parts) == 3:
            year = int(date_parts[2])
            # 僅印出今年的
            if year == current_year:
                advisory_info = {
                    "Advisory ID": advisory_id,
                    "網址": link,
                    "Level": level,
                    "Description": description,
                    "Updated Date": update_date
                }
                advisories.append(advisory_info)
else:
    print("找不到元素")

# 關閉瀏覽器
driver.quit()

# 格式化訊息
message = "======= VMware Advisories =======\n\n"
for advisory in advisories:
    message += f"Advisory ID: {advisory['Advisory ID']}\n"
    message += f"Updated Date: {advisory['Updated Date']}\n"
    message += f"Level: {advisory['Level']}\n"
    message += f"網址: {advisory['網址']}\n"
    message += f"Description: {advisory['Description']}\n\n"
    

# 透過 Telegram Bot 發送訊息
url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
params = {
    "chat_id": TELEGRAM_CHAT_ID,
    "text": message
}
response = requests.get(url, params=params)
if response.status_code == 200:
    print("訊息已發送至 Telegram")
else:
    print("發送訊息至 Telegram 時發生錯誤")
