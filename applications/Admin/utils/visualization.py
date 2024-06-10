import pandas as pd
from database.models.news import News
import matplotlib.pyplot as plt
import json
from database.db import get_session
from sqlalchemy import select
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像时负号'-'显示为方块的问题
def ksh_analysis(table_name):

    with get_session() as session:
        statement = select(News).order_by(News.click_num)
        results = session.exec(statement).limit(10)

    title_list=[]
    click_list=[]
    for result in results:
        title_list.append(str(result['title']))
        click_list.append(int(result['click_count']))

    data={'title':title_list,'click_count':click_list,'label':"点击量前五的条目"}

    df = pd.DataFrame(data)
    plt.bar(df['title'], df['click_count'])
    plt.title('点击量前10的条目')
    plt.xlabel('题目')
    plt.ylabel('点击数')
    # 绘制条形图
    plt.bar(df['title'], df['click_count'])


    plt.savefig('output.png')
    plt.show()
    return json.dumps(data)


def main():
    data=json.loads(ksh_analysis('questions'))
    print(data)

if __name__ == '__main__':
    main()

