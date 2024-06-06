import pymysql
import pymysql.cursors

class Database:
    def __init__(self, host, user, password, database, port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.connection = None

    def create_database(self, db_name):
        """创建数据库
        :param db_name:数据库名字"""
        try:
            connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            with connection.cursor() as cursor:
                cursor.execute(
                    f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
                )
                print(f"数据库 {db_name} 创建成功")
                connection.close()
        except pymysql.Error as e:
            print(f"Error during database creation: {e}")



    def connect_database(self):
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except pymysql.Error as e:
            print(f"Error during database connection: {e}")

    def close_connection(self):
        if self.connection:
            self.connection.close()

    def create_table(self, table_name, columns:list):
        """创建表
        :param table_name:表名字
        :param columns:属性的列表：columns = ['id INT AUTO_INCREMENT PRIMARY KEY', 'title VARCHAR(255)', 'url VARCHAR(255)',
               'dept VARCHAR(255)', 'timestamp TIMESTAMP', 'txt TEXT', 'table_list TEXT']"""
        with self.connection.cursor() as cursor:
            columns = ', '.join(columns)
            sql = f'CREATE TABLE IF NOT EXISTS {table_name} ({columns})'
            try:
                cursor.execute(sql)
                print(f"数据表 {table_name} 创建成功")
            except pymysql.Error as e:
                print(f"Error during table creation: {e}")
        self.connection.commit()

    def select_table(self, attributes, table_name, conditions):
        """
        从数据表中查询数据
        :param attributes: 要查询的字段列表
        :param table_name: 要查询的数据表的名称
        :param conditions: 查询条件
        :return: 查询结果
        """
        if attributes == '*':
            attribute_str = '*'
        else:
            attribute_str = ','.join(attributes)

        with self.connection.cursor() as cursor:
            if conditions == '':
                # 如果没有条件，则将条件字符串设为空字符串
                condition_str = ''
                # 构建SQL语句
                sql = f'SELECT {attribute_str} FROM {table_name}'
            else:
                condition_str = conditions
                # 构建SQL语句
                sql = f'SELECT {attribute_str} FROM {table_name} {condition_str}'

            cursor.execute(sql)
            result = cursor.fetchall()

        return result

    def insert_table(self, table_name, columns, data):
        """插入数据
        :param table_name:表名
        :param columns:属性列表
        :param data:要插入的数据：data = [
    [1, 'Alice', 30],
    [2, 'Bob', 25],
    [3, 'Charlie', 35]
]"""

        with self.connection.cursor() as cursor:
            columns_str = ', '.join(columns)
            placeholders = ', '.join(['%s'] * len(columns))
            insert_query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
            try:
                cursor.executemany(insert_query, data)
            except pymysql.Error as e:
                print(f"Error during data insertion: {e}")
        self.connection.commit()

    def delete_rows(self, table_name, condition):
        with self.connection.cursor() as cursor:
            if condition:
                delete_query = f"DELETE FROM {table_name} WHERE {condition}"
            try:
                cursor.execute(delete_query)
            except pymysql.Error as e:
                print(f"Error during row deletion: {e}")
        self.connection.commit()


def main():
    db_host = 'localhost'
    db_user = 'root'
    db_password = 'Y1j1i1123'
    db_name = 'python_database'
    db_port = 3306

    db = Database(db_host, db_user, db_password, db_name, db_port)


    db.connect_database()

    table_name = 'example_table'

    result = db.select_table('*', table_name, 'WHERE id=4 And title="Title 1"')
    # db.delete_rows(table_name,'id=3')

    print("查询结果:")
    for row in result:
        print(row)

    db.close_connection()

if __name__ == "__main__":
    main()
