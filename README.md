# 波兰语单词打卡

一个使用Streamlit和SQLite的波兰语单词打卡Web应用。

## 功能

- 添加波兰语单词和中文释义
- 每日打卡记录
- 查看打卡历史
- 数据永久保存在SQLite数据库中

## 本地运行

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 运行应用：
```bash
streamlit run app.py
```

## 部署到Streamlit Cloud

注意：Streamlit Cloud的文件系统是临时的，SQLite数据库会在每次重启时重置。如需在Cloud上永久保存数据，建议使用：
- Google Sheets
- Supabase (PostgreSQL)
- 其他云数据库服务

## 技术栈

- Streamlit
- SQLite
- Python
