import sqlite3
import json

# 获取所有老师的名字
def get_all_teachers_name(lesson):
    teacherAssignmentList = lesson.get("teacherAssignmentList", [])
    teacherNameList = []
    for teacher in teacherAssignmentList:
        teacherNameList.append(teacher.get("name"))
    return ' '.join(teacherNameList)

# 创建或连接到 SQLite 数据库
conn = sqlite3.connect('courses.db')
cursor = conn.cursor()

# 创建表的 SQL 语句
create_courses_table_sql = '''
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY,                 -- 课名唯一标识符
    weekIndicesStr TEXT,                    -- 控制起止周，字符串
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
    startTime INTEGER,                      -- 上课时间，整数
    endTime INTEGER,                        -- 下课时间，整数
    FOREIGN KEY (lessonId) REFERENCES courses(id)
);
'''

create_course_schedule_table_sql = '''
CREATE TABLE IF NOT EXISTS course_schedule AS
SELECT 
    c.id AS course_id,
    c.weekIndicesStr,
    c.courseName,
    c.Studensname,
    c.TeachersName,
    s.date,
    s.roomName,
    s.startTime,
    s.endTime
FROM 
    courses c
JOIN 
    schedule s ON c.id = s.lessonId;
'''

# 执行创建表的 SQL 语句
cursor.execute(create_courses_table_sql)
cursor.execute(create_schedule_table_sql)

# 从 JSON 文件导入数据
with open('table.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 插入 lessonList 中的数据
for lesson in data['result']['lessonList']:
    id = lesson.get("id")
    weekIndicesStr = lesson.get("scheduleJsonParams")[0].get("weekIndicesStr")
    courseName = lesson.get("courseName")
    Studensname = lesson.get("name")
    TeachersName = get_all_teachers_name(lesson)
    
    insert_courses_sql = '''
    INSERT INTO courses (id, weekIndicesStr, courseName, Studensname, TeachersName)
    VALUES (?, ?, ?, ?, ?)
    ON CONFLICT(id) DO NOTHING;  -- 如果课程 ID 已存在，则忽略插入
    '''
    cursor.execute(insert_courses_sql, (id, weekIndicesStr, courseName, Studensname, TeachersName))

# 插入 scheduleList 中的数据
for schedule in data['result']['scheduleList']:
    lessonId = schedule.get("lessonId")
    date = schedule.get("date")
    roomName = schedule.get("room", {}).get("nameZh")
    startTime = schedule.get("startTime")  # 从 scheduleList 中获取 startTime
    endTime = schedule.get("endTime")      # 从 scheduleList 中获取 endTime
    
    insert_schedule_sql = '''
    INSERT INTO schedule (lessonId, date, roomName, startTime, endTime)
    VALUES (?, ?, ?, ?, ?);
    '''
    cursor.execute(insert_schedule_sql, (lessonId, date, roomName, startTime, endTime))

# 创建合并后的新表 course_schedule
cursor.execute(create_course_schedule_table_sql)

# 提交事务
conn.commit()

# 查询并打印合并后的新表数据以确认插入
cursor.execute("SELECT * FROM course_schedule;")
print("Course Schedule:")
for row in cursor.fetchall():
    print(row)

# 关闭游标和连接
cursor.close()
conn.close()
