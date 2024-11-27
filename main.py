import sqlite3
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

# 数据库连接函数
def get_db_connection():
    conn = sqlite3.connect('courses.db')
    conn.row_factory = sqlite3.Row  # 使得返回的行可以通过列名访问
    return conn

@app.get("/getAllTable")
async def getAllTable():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 查询 course_schedule 表中的所有数据
    cursor.execute("SELECT * FROM course_schedule;")
    rows = cursor.fetchall()
    
    # 关闭数据库连接
    cursor.close()
    conn.close()
    
    # 将结果转换为字典列表
    result = [dict(row) for row in rows]
    
    # 返回 JSON 格式的响应
    return JSONResponse(content=result)

# 运行应用程序
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
