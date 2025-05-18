# 指定数据库连接
LOCATION = 'redis://127.0.0.1:6379/%d'  # %d表示数据库的编号

# 绑定key模板格式
KEY_TEMPLATE = '%s:verification:%s'

# 过期时间
EXPIRE_TIME = 60
