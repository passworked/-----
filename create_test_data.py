import sqlite3
import random
from datetime import datetime, timedelta
from faker import Faker
def insert_nine_columns(db_name, table_name, data):
    """
    在指定的 SQLite 数据库表中插入一行包含九列的数据。
    
    :param db_name: 数据库文件名
    :param table_name: 表名
    :param data: 要插入的数据，格式为元组，例如 (value1, value2, ..., value9)
    """
    # 检查数据长度是否为 9
    if len(data) != 9:
        raise ValueError("数据长度必须为 9")

    # 连接到 SQLite 数据库
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # 构建 SQL 插入语句
    placeholders = ', '.join('?' * 9)  # 生成 9 个占位符
    sql = f'INSERT INTO {table_name} (course_id, weekIndicesStr, courseName, Studensname, TeachersName, date, roomName, startTime, endTime) VALUES ({placeholders})'
    
    # 执行插入操作
    try:
        cursor.execute(sql, data)
        conn.commit()  # 提交事务
        print("数据插入成功")
    except sqlite3.Error as e:
        print(f"发生错误: {e}")
    finally:
        cursor.close()
        conn.close()

def generate_random_tuple():
    # 1. 生成48195（1-50000）随机数
    random_id = random.randint(1, 50000)

    # 2. 生成7~8周（前比后小，随机数在1-18以内）
    start_week = random.randint(1, 11)  # 1到11周
    end_week = start_week + random.randint(1, 8)  # 7~8周
    weekIndicesStr = f"{start_week}-{end_week}周"

    # 3. 形势与政策5（在课程列表里面随机抽取）
    courses = ['形势与政策', '高等数学', '大学英语', '程序设计', '数据结构',
               '计算机网络', '数据库', '操作系统', '计算机组成原理', '计算机系统结构',
               '计算机科学与技术', '软件工程', '网络工程', '信息安全', '人工智能',
               '大数据技术', '物联网工程', '电子信息工程', '通信工程', '自动化',
               '电气工程', '电子科学与技术', '测绘工程', '遥感科学与技术', '土木工程',
               '机械工程', '材料科学与工程', '化学工程与工艺', '环境科学与工程',
               '生物工程', '食品科学与工程', '药学', '医学', '护理学',
               '法学', '经济学', '管理学', '教育学', '文学', '艺术学',
               '哲学', '历史学', '理学', '工学', '农学', '医学', '管理学', '艺术学',
               ]
    selected_course = random.choice(courses) + '5'

    # 4. 班级生成（在班级列表里面随机抽取）
    classes = [
        '机械', '机械', '机械',
        '测绘', '测绘', '遥感2022',
        '土木', '土木', '土木',
        '计算机', '计算机', '计算机',
        '电气', '电气', '电气',
        '电子', '电子', '电子',
        '通信', '通信', '通信',
        '自动化', '自动化', '自动化',
        '软件', '软件', '软件',
        '物联网', '物联网', '物联网',
        '人工智能', '人工智能', '人工智能',
        '大数据', '大数据', '大数据',
        '网络工程', '网络工程', '网络工程',
    ]
    selected_class = random.choice(classes)

    # 5. 生成姓名
    random_name_list = ['张三', '李四', '王五', '赵六', '孙七', '周八', '吴九', '郑十']
    random_name = random.choice(random_name_list)
    

    # 6. 生成2024年的任意一天（非周末）
    while True:
        random_date = datetime(2024, random.randint(1, 12), random.randint(1, 28))
        if random_date.weekday() < 5:  # 0-4为周一到周五
            break

    # 7. 生成教106（生成教（101-620））
    classroom_number = random.randint(101, 620)
    classroom = f"教{classroom_number}"

    # 8. 1330 在（800 950 1330 1520）挑选
    time_1330_options = [800, 950, 1330, 1520]
    time_1330 = random.choice(time_1330_options)

    # 9. 1700 在（935 1130 1530 1700）挑选，必须比前一项小
    time_1700_options = [935, 1130, 1530, 1700]
    while True:
        time_1700 = random.choice(time_1700_options)
        if time_1700 > time_1330:
            break

    # 生成元组
    result_tuple = (
        random_id,
        weekIndicesStr,
        selected_course,
        selected_class,
        random_name,
        random_date.strftime('%Y-%m-%d'),
        classroom,
        time_1330,
        time_1700
    )

    return result_tuple
for i in range(1000):
    insert_nine_columns('courses.db', 'course_schedule', generate_random_tuple())
