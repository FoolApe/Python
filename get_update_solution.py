from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from telegram import Bot
import asyncio


# 設定 Chrome 選項
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# 載入擴充套件
chrome_options.add_extension("extensions/0.5.5_0.crx")

# 呼叫 Chrome 的套件並設定選項
PATH = "chromedriver.exe"
driver = webdriver.Chrome(PATH, options=chrome_options)

### ====================== VMWare ====================== ###

# 開啟VMware KB
driver.get('https://kb.vmware.com/s/article/91212')

# 最大化視窗
driver.maximize_window()

# 等待元素生成
element = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, f'//*[@id="article_content"]/div[7]/div[2]'))
)

# 抓取更新日期 / Solution
update_date = driver.find_element(By.ID, 'lastModifiedDate').text
solution = driver.find_element(By.XPATH, f'//*[@id="article_content"]/div[7]/div[2]').text

### ====================== NTNX ====================== ###

# 開一個新分頁 , 切換到分頁
driver.execute_script("window.open();")
driver.switch_to.window(driver.window_handles[1])

# 開啟NTNX KB
driver.get('https://portal.nutanix.com/page/documents/kbs/details?targetId=kA07V000000H5fRSAS')

# 等待一下下會被轉導到登入頁
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.NAME, "username"))
)

# 輸入帳密登入
def login(user,passwd):
    driver.find_element(By.NAME, "username").send_keys(user)
    driver.find_element(By.NAME, "password").send_keys(passwd)
    driver.find_element(By.ID, "login-btn").click()
login('YOUR_ACCOUNT','YOUR_PASSWORD')

# 等待元素導入
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, f'//*[@id="app-container"]/div/div[2]/div[2]/div/div/div/div/div/div[2]/div/div[1]/div/div[2]/div'))
)


# 撈取更新日期 / Solution ### 撈取還有問題
update_date_element = driver.find_element(By.XPATH, f'//span[contains(@class, "ntnx-text-label") and contains(@class, "f9c9a531b5")]')
update_date2 = update_date_element.text

solution_element = driver.find_element(By.XPATH, f'//p[contains(@class, "ntnx-paragraph") and @data-type="primary"]')
solution2 = solution_element.text

### ====================== RESULT ====================== ###
"""
print("====================== VMWare ======================")
print("最後更新時間:", update_date)
print("解決方法:", solution)
print("")

print("====================== Nutanix ======================")
print("最後更新時間:", update_date2)
print("解決方法:", solution2)
"""

### ====================== 外拋到telegram ====================== ###

# 設定 Telegram 機器人的token
bot_token = 'YOUR_TOKEN'

# 設定要發送訊息的chat_id
chat_id = 'YPUR_CHAT_ID'

# 建立 Telegram Bot 物件
bot = Bot(token=bot_token)

# 定義發送訊息的函數
async def send_message():
    # 要發送的訊息內容
    message = f"================ KB追蹤 ================\n\nVMWare\n⌚️最後更新時間:  {update_date}\n🔧解決方法:\n{solution}\n\nNTNX\n⌚️最後更新時間:  {update_date2}\n🔧解決方法:\n{solution2}"

    # 使用機器人發送訊息到指定的聊天室
    await bot.send_message(chat_id=chat_id, text=message)

# 建立事件迴圈並執行發送訊息的函數
loop = asyncio.get_event_loop()
loop.run_until_complete(send_message())
loop.close()
