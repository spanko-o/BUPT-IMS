import pandas as pd
from info.database import Database
import matplotlib.pyplot as plt
import json
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像时负号'-'显示为方块的问题

def ksh_analysis(table_name):
    # 连接到数据库
    db_host = 'localhost'
    db_user = 'root'
    db_password = 'Y1j1i1123'
    db_name = 'python_database'
    db_port = 3306

    db = Database(db_host, db_user, db_password, db_name, db_port)

    db.connect_database()
    db.connect_database()
    print('ok')
    table_name='questions'
    results=db.select_table('*',table_name,'ORDER BY click_count DESC LIMIT 5;')


    # 执行SQL语句

    # 获取查询结果

    title_list=[]
    click_list=[]
    for result in results:
        title_list.append(str(result['title']))
        click_list.append(int(result['click_count']))

    data={'title':title_list,'click_count':click_list,'label':"点击量前五的条目"}

    df = pd.DataFrame(data)
    plt.bar(df['title'], df['click_count'])
    plt.title('点击量前五的条目')
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

