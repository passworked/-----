import sqlite3
import json

# 假设我们有一个函数来获取老师的名字
def get_all_teachers_name(lession):
    teacherAssignmentList = lession.get("teacherAssignmentList")
    teacherNameList = []
    for teacher in teacherAssignmentList:
        teacherNameList.append(teacher.get("name"))
    return ' '.join(teacherNameList)

# 创建或连接到 SQLite 数据库
conn = sqlite3.connect('course.db')
cursor = conn.cursor()

# 创建表的 SQL 语句
create_courses_table_sql = '''
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY,                 -- 课名唯一标识符
    weekIndicesStr TEXT,                    -- 控制起止周，字符串
    startTime INTEGER,                      -- 上课时间，整数
    endTime INTEGER,                        -- 下课时间，整数
    courseName TEXT,                        -- 课程的中文名称，字符串
    Studensname TEXT,                       -- 排课的学生，字符串
    TeachersName TEXT                       -- 老师，字符串
);
'''

create_schedule_table_sql = '''
CREATE TABLE IF NOT EXISTS schedule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lessonId INTEGER,                       -- 关联课程的 ID
    date TEXT,                              -- 上课日期
    roomName TEXT,                          -- 教室名称
    FOREIGN KEY (lessonId) REFERENCES courses(id)
);
'''

# 执行创建表的 SQL 语句
cursor.execute(create_courses_table_sql)
cursor.execute(create_schedule_table_sql)

# 假设 json_data 是从 JSON 文件或 API 获取的数据


# 将 JSON 数据加载为字典
with open('table.json','r',encoding='utf-8') as f:
    data = json.load(f)

# 插入 lessonList 中的数据
for lesson in data['result']['lessonList']:
    id = lesson.get("id")
    weekIndicesStr = lesson.get("scheduleJsonParams")[0].get("weekIndicesStr")
    startTime = lesson.get("startTime")
    endTime = lesson.get("endTime")
    courseName = lesson.get("courseName")
    Studensname = lesson.get("name")
    TeachersName = get_all_teachers_name(lesson)
    
    insert_courses_sql = '''
    INSERT INTO courses (id, weekIndicesStr, startTime, endTime, courseName, Studensname, TeachersName)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(id) DO NOTHING;  -- 如果课程 ID 已存在，则忽略插入
    '''
    cursor.execute(insert_courses_sql, (id, weekIndicesStr, startTime, endTime, courseName, Studensname, TeachersName))

# 插入 scheduleList 中的数据
for schedule in data['result']['scheduleList']:
    lessonId = schedule.get("lessonId")
    date = schedule.get("date")
    roomName = schedule.get("room", {}).get("nameZh")
    
    insert_schedule_sql = '''
    INSERT INTO schedule (lessonId, date, roomName)
    VALUES (?, ?, ?);
    '''
    cursor.execute(insert_schedule_sql, (lessonId, date, roomName))

# 提交事务
conn.commit()

# 查询并打印所有数据以确认插入
cursor.execute("SELECT * FROM courses;")
print("Courses:")
for row in cursor.fetchall():
    print(row)

cursor.execute("SELECT * FROM schedule;")
print("\nSchedule:")
for row in cursor.fetchall():
    print(row)

# 关闭游标和连接
cursor.close()
conn.close()
