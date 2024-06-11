import pandas as pd
from database.models.news import News
import matplotlib.pyplot as plt
import io
import base64
from database.db import get_session
from sqlmodel import select

plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像时负号'-'显示为方块的问题


def ksh_analysis():
    with get_session() as session:
        statement = select(News).order_by(News.click_num.desc()).limit(10)
        results = session.exec(statement).all()

    title_list = []
    click_list = []
    for result in results:
        title_list.append(result.title)
        click_list.append(result.click_num)

    data = {'title': title_list, 'click_count': click_list}

    df = pd.DataFrame(data)
    plt.figure(figsize=(10, 6))  # 设置图像大小
    plt.bar(df['title'], df['click_count'], color='skyblue')
    plt.title('点击量前10的条目')
    plt.xlabel('题目')
    plt.ylabel('点击数')
    plt.xticks(rotation=45, ha='right')  # 旋转标题以避免重叠

    # 使用 io.BytesIO 在内存中创建一个字节流
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', bbox_inches='tight')  # 保存图像到字节流
    img_buffer.seek(0)  # 确保缓冲区游标回到起始位置
    plt.close()  # 关闭 plt 避免内存泄漏

    # 将图像数据编码为 Base64
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

    return img_base64
