import sqlite3

# 创建或连接到 SQLite 数据库
conn = sqlite3.connect('courses.db')
cursor = conn.cursor()

# 创建 department 表
cursor.execute('''
CREATE TABLE IF NOT EXISTS department (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    majors TEXT
)
''')

# 去重后的专业分类数据
departments = {
    "能源与矿业学院": [],
    "应急管理与安全工程学院": [],
    "地球科学与测绘工程学院": ["测绘", "遥感2022"],
    "化学与环境工程学院": [],
    "机械与电气工程学院": ["机械", "电气", "电子"],
    "人工智能学院": ["人工智能", "大数据"],
    "管理学院": [],
    "力学与土木工程学院": ["土木"],
    "理学院": ["计算机", "自动化", "软件", "物联网", "网络工程"],
    "文法学院": [],
    "马克思主义学院": [],
    "体育教研部": [],
    "继续教育学院": []
}

# 插入数据到 department 表
for department, majors in departments.items():
    majors_str = ', '.join(majors) if majors else None  # 将专业列表转换为字符串
    cursor.execute('''
    INSERT INTO department (name, majors) VALUES (?, ?)
    ''', (department, majors_str))

# 提交更改并关闭连接
conn.commit()
conn.close()
