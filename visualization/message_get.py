from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver import ChromeOptions
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import re
import pandas as pd
import io

def clean_filename(filename):
    # 使用正则表达式替换不允许的字符
    cleaned_filename = re.sub(r'[\\/*?:"<>|]', ' ', filename)
    return cleaned_filename
def trans_text(text):
    lines = text.split('\n')
    indented_lines = []
    for line in lines:
        # 在每段的首行加入制表符
        indented_lines.append('&emsp;&emsp;' + line)
    return '\n'.join(indented_lines)

def write_markdown(filename, text):
    # 将换行符替换为Markdown换行符并进行缩进处理
    # text = trans_text(text)
    text = text.replace('\n', '  \n')

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)

# 创建 CSV 文件并写入标题行
csv_name = f'本科{datetime.now().strftime("%Y%m%d")}.csv'
with open(csv_name, mode='a', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['title', 'url', 'dept', 'timestamp', 'txt','table_list'])
    """txt是文本内容，timestamp时间戳，dept为发布部门，table_list是一个列表，代表着当前网页中所有表的集合"""

    # 导航到登录页面
    session_request = requests.session()
    from selenium.webdriver.edge.options import Options

    options = ChromeOptions()

    # 禁用自动化控制特性
    options.add_experimental_option('excludeSwitches', ['enable-automation'])

    # 禁用 Blink 特性
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_path="D:\\chromeDriver\\chromedriver-win64\\chromedriver.exe"
    # 启动 Edge 浏览器
    web = webdriver.Chrome(chrome_path,options=options)
    login_url = 'https://auth.bupt.edu.cn/authserver/login?service=http%3A%2F%2Fmy.bupt.edu.cn%2Fsystem%2Fresource%2Fcode%2Fauth%2Fclogin.jsp%3Fowner%3D1664271694'
    web.get(login_url)
    web.switch_to.frame("loginIframe")
    web.maximize_window()
    # 点击密码登录按钮
    WebDriverWait(web, 20).until(EC.presence_of_element_located((By.XPATH, "//body")))
    password_login_button = WebDriverWait(web, 10).until(
        EC.presence_of_element_located((By.XPATH, '//a[@i18n="login.type.password"]'))
    )
    password_login_button.click()

    # 等待用户名和密码字段出现
    username_field = WebDriverWait(web, 10).until(
        EC.presence_of_element_located((By.ID, 'username'))
    )
    password_field = WebDriverWait(web, 10).until(
        EC.presence_of_element_located((By.ID, 'password'))
    )

    # 输入用户名和密码
    username_field.send_keys('2022211482')
    password_field.send_keys('Y1j1i1123')

    # 模拟点击登录按钮
    login_button = web.find_element(By.XPATH, '/html/body/div[3]/div/div/div[3]/div[2]/div[7]/input')
    login_button.click()
    for page in range(2, 3):
            main_url = f'http://my.bupt.edu.cn/fz_ssjg.jsp?a218493t=828&a218493p=2&a218493c=10&a218493i=%E6%9C%AC%E7%A7%91&wbtreeid=1154&entrymode=1&researchvalue=false&condition=-1&INTEXT2=5pys56eR&wbtreeids=&news_search_code=&INTEXT=%27web.get%28main_url%29'
            web.get(main_url)

            for i in range(2, 3):
                list = []
                title_path = f'/html/body/div[3]/div/div[2]/form/table[2]/tbody/tr[{i}]/td[1]/a'
                title_element = WebDriverWait(web, 20).until(EC.presence_of_element_located((By.XPATH, title_path)))
                title = clean_filename(title_element.text)

                url_path = f'/html/body/div[3]/div/div[2]/form/table[2]/tbody/tr[{i}]/td[1]/a'
                url_element = web.find_element(By.XPATH, url_path)
                # final_url = url_element.get_attribute('href')
                final_url='http://my.bupt.edu.cn/xntz_content.jsp?urltype=news.NewsContentUrl&wbtreeid=1736&wbnewsid=116499'
                # 等待新页面加载完成
                web.get(final_url)

                # 使用 BeautifulSoup 解析页面
                soup = BeautifulSoup(web.page_source, "html.parser")

                # 查找页面中的表单元素
                form = soup.find("form", attrs={"name": "_newscontent_fromname"})
                if form:
                    print('ok')
                dept = form.find("span", class_='pmeta pdept')
                dept_text = dept.text.strip() if dept else " Unknow"
                dept_name = dept_text.split("：")[1]

                time = form.find("span", class_='pmeta ptime')
                time_text = time.text.strip() if time else "Unknow"
                time_name = time_text.split('：')[1].strip()
                date_time = datetime.strptime(time_name, '%Y-%m-%d').replace(hour=0, minute=0, second=0)
                # 获取时间戳
                timestamp = int(date_time.timestamp())
                print(timestamp)

                for img in soup.find_all("img"):
                    img.decompose()
                abstract_element = soup.find("div", class_="v_news_content")

                tables = abstract_element.find_all("table")
                table_list=[]
                # 如果找到了表格，则遍历每个表格并处理它们
                if tables:
                    for idx, table in enumerate(tables):
                        # 将表格的表示文字替换为 "table1", "table2" 等
                        table.replace_with(f"table{idx + 1}")

                    # 重新获取替换后的 abstract_text
                    abstract_text = abstract_element.text

                    # 打印 abstract_text，它现在可能包含了被替换的表格部分的表示文字
                    print(abstract_text)

                    # 处理每个表格
                    for idx, table in enumerate(tables):
                        table_html = str(table)
                        table_df = pd.read_html(io.StringIO(table_html))[0]

                        # 将表格数据保存为Excel文件，每个表格一个文件
                        table_name = f"{title}_table_{idx + 1}.xlsx"
                        table_df.to_excel(table_name, index=False)
                        table_list.append(table_name)

                else:
                    # 如果没有找到表格，则将 abstract_element 的文本保存为表示文字
                    abstract_text = abstract_element.text
                    print(abstract_text)
                click_element = soup.find("span", class_="dynclicks_wbnews_117635_808")
                click=click_element.text
                print(click)
                # print(table_list)
                #
                # list.append(title)
                # list.append(final_url)
                # list.append(dept_name)
                # list.append(timestamp)
                # list.append(abstract_text)
                # list.append(table_list)
                # writer.writerow(list)
                # filename=f'{title}_{time_name}.md'
                # with open(filename, 'w',encoding="utf-8") as f:
                #     f.write(str(abstract_element))
                #
                # write_markdown(filename,abstract_text)
                web.back()
                web.execute_script('window.scrollBy(0,185)')

# 循环结束后关闭文件
print("爬取完成，关闭文件。")