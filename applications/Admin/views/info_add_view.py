import csv
from typing import Dict, Any
from applications.base import APIView
from sqlmodel import Session, select
from database.db import get_session
from database.models.news import News
from datetime import datetime
from middleware.responses import ResponseUtils
from middleware.exception_catcher import exception_catcher
from middleware.token_authentication import auth_required


class NewsAddView(APIView):
    @exception_catcher
    @auth_required
    def post(self):
        csv_file_path = 'info/news.csv'
        new_records = []

        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row: Dict[str, Any]
                title: str = row['title']
                url: str = row['url']
                department: str = row['dept']
                time_str: str = row['time'].strip()
                content: str = row['txt']
                chart: str = row.get('chart')

                time_obj = datetime.strptime(time_str, '%Y-%m-%d')

                with get_session() as session:
                    existing_news = session.exec(select(News).where(News.title == title)).first()
                    if existing_news:
                        continue

                    new_news = News(
                        title=title,
                        url=url,
                        department=department,
                        time=time_obj,
                        content=content,
                        chart=chart if chart else None,
                        click_num=0
                    )
                    session.add(new_news)
                    session.commit()
                    new_records.append({
                        'title': new_news.title,
                        'url': new_news.url
                    })

        if not new_records:
            response_data = {
                'message': "No new records added"
            }
            return self.response_utils.ok(self.handler, response_data)

        response_data = {
            'message': f'{len(new_records)} new records added successfully',
            'new_records': new_records
        }
        ResponseUtils.ok(self.handler, response_data)
