### 列出首頁的焦點活動 , 並顯示標題與售票狀態
from bs4 import BeautifulSoup
import requests

# 發送 HTTP GET 請求取得網頁內容
url = "https://kktix.com/"
response = requests.get(url)
html_content = response.text

# 使用 BeautifulSoup 解析 HTML 內容
soup = BeautifulSoup(html_content, "html.parser")

# 尋找名稱為 "tab-pane active" 的元素
tab_pane = soup.find(class_="tab-pane active")

if tab_pane is not None:
    # 尋找該元素底下的所有 class
    class_elements = tab_pane.find_all(class_=True)
    
    # 逐一處理每個 class 元素
    for class_element in class_elements:
        class_name = class_element["class"][0]
        
        # 檢查 class 是否為 "type-counter", "type-selling" 或 "type-view"
        if class_name in ["type-counter", "type-selling", "type-view"]:
            # 檢查 class 元素底下是否有 "event-title" 和 "fake-btn pull-right"
            if class_element.find(class_="event-title") is not None and class_element.find(class_="fake-btn pull-right") is not None:
                event_title = class_element.find(class_="event-title").text.strip()
                event_date = class_element.find(class_="date").text.strip()
                status = class_element.find(class_="fake-btn pull-right").text.strip()
                
                # 輸出標題/日期/售票狀況
                print("Event:", event_title)
                print("Date:", event_date)
                print("Status:", status) ### 開賣時間會騙人 , 需要另外處理
                print()

else:
    print("No element with class 'tab-pane active' found.")