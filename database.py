import sqlite3
import json
# 连接到 SQLite 数据库（如果数据库不存在，将会自动创建）
conn = sqlite3.connect('courses.db')
with open('table.json','r',encoding='utf-8') as f:
    table = json.load(f)
lessonList = table.get("lessonList")
# 创建一个游标对象
cursor = conn.cursor()

# 创建表的 SQL 语句
create_table_sql = '''
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER,                 -- (课名唯一标识符)用于连接课名 
    weekIndicesStr TEXT,        -- 控制起止周，字符串
    startTime INTEGER,          -- 上课时间，整数
    endTime INTEGER,            -- 下课时间，整数
    courseName TEXT,            -- 课程的中文名称，字符串
    Studensname TEXT,           -- 排课的学生，字符串
    v TEXT            -- 老师，字符串
);
'''

def get_all_teachers_name(lession):
    teacherAssignmentList = lession.get("teacherAssignmentList")
    teacherNameList = []
    for teacher in teacherAssignmentList:
        teacherNameList.append(teacher.get("name"))
    return ' '.join(teacherNameList)
# 执行创建表的 SQL 语句
cursor.execute(create_table_sql)
for lession in lessonList:
    weekIndicesStr = lession.get("scheduleJsonParams")[0].get("weekIndicesStr")
    startTime = lession.get("startTime")
    endTime = lession.get("endTime")
    courseName = lession.get("courseName")
    Studensname =  lession.get("name")
    TeachersName = get_all_teachers_name(lession)
# 关闭游标和连接
cursor.close()
conn.close()
