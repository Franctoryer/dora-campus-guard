import pymysql

# 建立数据库连接
conn = pymysql.connect(host='localhost', user='root', password='admin123', db='dora')
cursor = conn.cursor()

# 检查 autocommit 状态
autocommit_status = conn.get_autocommit()
print(f"Autocommit enabled: {autocommit_status}")