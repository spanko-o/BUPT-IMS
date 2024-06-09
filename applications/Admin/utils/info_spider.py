import requests
from bs4 import BeautifulSoup
import re
from fake_useragent import UserAgent
from datetime import datetime


def clean_filename(filename):
    cleaned_filename = re.sub(r'[\\/*?:"<>|]', ' ', filename)
    return cleaned_filename


def trans_text(text):
    lines = text.split('')
    indented_lines = []
    for line in lines:
        indented_lines.append('&emsp;&emsp;' + line)
    return ''.join(indented_lines)


def main():
    session = requests.session()
    login_url = 'https://auth.bupt.edu.cn/authserver/login?service=http%3A%2F%2Fmy.bupt.edu.cn%2Fsystem%2Fresource%2Fcode%2Fauth%2Fclogin.jsp%3Fowner%3D1664271694'
    username = '2022211482'
    password = 'Y1j1i1123'
    login_data = {
        'username': username,
        'password': password
    }
    headers = {
        'User-Agent': UserAgent().random,  # 使用第三方库生成的随机UA
        'Referer': 'https://accounts.douban.com/',  # 添加防盗链，这个因网站而异
    }
    response_ = session.post(login_url, data=login_data)

    if response_.status_code == 200:
        print("登录成功")
        import time
        time.sleep(10)

    else:
        print("登录失败")
        return

    for page in range(2, 3):
        main_url = f'http://my.bupt.edu.cn/list.jsp?totalpage={page}/368&PAGENUM=1&urltype=tree.TreeTempUrl&wbtreeid=1154'
        home = session.post(main_url, data=login_data)
        print(main_url)
        print(home.text)
        if (home is not None):
            print('ok')
        soup = BeautifulSoup(home.content, 'html.parser')

        ul_element = soup.find('ul', class_='newslist list-unstyled')
        li_tags = ul_element.find_all('li')
        for li in li_tags:
            a_tag = li.find('a')
            if a_tag:
                title = a_tag.get('title')
                url = a_tag.get('href')
                print(f'Title: {title}, URL: {url}')
                detail = session.get(url)
                soup = BeautifulSoup(detail.content, 'html.parser')
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
                abstract_element = soup.find("div", class_="v_news_content")
                abstract_text = abstract_element.text.strip() if abstract_element else " Unknow"
                tables = abstract_element.find_all("table")
                if tables:
                    table_list = [table.prettify() for table in tables]
                    # message = Message()
                    #
                    # # 将list中的数据分别赋值给message对象的相应属性
                    # message.title = title
                    # message.url = url
                    # message.dept_name = dept_name
                    # message.timestamp = timestamp
                    # message.abstract_text = abstract_text
                    # message.table_list = table_list
                    # with get_session() as session:
                    #     session.add(message)
                    #     session.commit()

    print("爬取完成，关闭文件。")


if __name__ == '__main__':
    main()
