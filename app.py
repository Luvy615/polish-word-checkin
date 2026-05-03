import streamlit as st
from supabase import create_client, Client
from datetime import datetime
import os

# 页面配置
st.set_page_config(
    page_title="波兰语单词打卡",
    page_icon="🇵🇱",
    layout="centered"
)

# 自定义CSS样式 - 简约线条风格
st.markdown("""
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&display=swap">
<style>
    * {
        font-family: "Noto Serif SC", "宋体", SimSun, STSong, serif !important;
    }
    .main {
        font-family: "Noto Serif SC", "宋体", SimSun, STSong, serif;
    }
    .stButton>button {
        background-color: #FFFFFF;
        color: #3498DB;
        font-family: "Noto Serif SC", "宋体", SimSun, STSong, serif !important;
        font-weight: bold;
        border-radius: 3px;
        border: 2px solid #3498DB;
        padding: 10px 24px;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background-color: #3498DB;
        color: #FFFFFF;
    }
    .word-item {
        padding: 12px;
        background: #FFFFFF;
        margin: 8px 0;
        border-radius: 3px;
        border: 1px solid #3498DB;
        border-left: 3px solid #3498DB;
    }
    .polish-word {
        font-weight: bold;
        color: #2C3E50;
        font-size: 18px;
        font-family: "Noto Serif SC", "宋体", SimSun, STSong, serif !important;
    }
    .chinese-meaning {
        color: #7F8C8D;
        margin-left: 15px;
        font-size: 16px;
        font-family: "Noto Serif SC", "宋体", SimSun, STSong, serif !important;
    }
    h1, h2, h3 {
        font-family: "Noto Serif SC", "宋体", SimSun, STSong, serif !important;
        color: #2C3E50;
    }
    h1 {
        text-align: center;
        font-size: 20px;
        font-weight: 300;
    }
    h2 {
        color: #3498DB;
        border-bottom: 2px solid #3498DB;
        padding-bottom: 5px;
    }
    .stTextInput>div>div>input {
        font-family: "Noto Serif SC", "宋体", SimSun, STSong, serif !important;
        border: 2px solid #3498DB;
        border-radius: 3px;
    }
    .stTextInput>div>div>input:focus {
        border-color: #2980B9;
        box-shadow: 0 0 0 1px #2980B9;
    }
</style>
""", unsafe_allow_html=True)

# Supabase配置 - 请在Streamlit Cloud的Secrets中配置
# 本地测试可以在.env文件中配置或直接在下方填写
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "")

# 初始化Supabase客户端
@st.cache_resource
def init_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

# 检查是否配置了Supabase
if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("⚠️ 请配置Supabase凭据！")
    st.info("""
    请按以下步骤配置：
    1. 在 https://supabase.com 注册并创建项目
    2. 在Project Settings > API中获取URL和anon key
    3. 在Streamlit Cloud的App Settings > Secrets中添加：
    ```
    SUPABASE_URL = "你的URL"
    SUPABASE_KEY = "你的KEY"
    ```
    4. 在Supabase SQL Editor中运行以下SQL创建表：
    ```sql
    CREATE TABLE words (
        id SERIAL PRIMARY KEY,
        polish TEXT NOT NULL,
        chinese TEXT NOT NULL,
        date TEXT NOT NULL
    );
    
    CREATE TABLE checkin_history (
        id SERIAL PRIMARY KEY,
        date TEXT NOT NULL,
        polish TEXT NOT NULL,
        chinese TEXT NOT NULL
    );
    ```
    """)
    st.stop()

supabase = init_supabase()

# 删除单词
def delete_word(word_id):
    supabase.table('words').delete().eq('id', word_id).execute()

# 删除打卡历史
def delete_history_word(word_id):
    supabase.table('checkin_history').delete().eq('id', word_id).execute()

# 获取今天日期
today = datetime.now().strftime("%Y-%m-%d")

# 标题
st.title("波兰语单词打卡")

# 添加单词部分
st.header("添加单词")
col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    polish_word = st.text_input("波兰语单词", key="polish_input", placeholder="np. dzień")
with col2:
    chinese_meaning = st.text_input("中文释义", key="chinese_input", placeholder="例如：天")
with col3:
    st.write("")
    st.write("")
    if st.button("添加", key="add_btn"):
        if polish_word and chinese_meaning:
            try:
                supabase.table('words').insert({
                    'polish': polish_word,
                    'chinese': chinese_meaning,
                    'date': today
                }).execute()
                st.success("添加成功！")
                st.rerun()
            except Exception as e:
                st.error(f"添加失败：{str(e)}")
        else:
            st.warning("请填写完整的单词和释义")

# 今日打卡部分
st.header(f"今日打卡 ({today})")

try:
    today_words_response = supabase.table('words').select('*').eq('date', today).execute()
    today_words = [{'id': w['id'], 'polish': w['polish'], 'chinese': w['chinese']} for w in today_words_response.data]
except Exception as e:
    st.error(f"加载今日单词失败：{str(e)}")
    today_words = []

if today_words:
    for word in today_words:
        col1, col2 = st.columns([10, 1])
        with col1:
            st.markdown(f"""
            <div class="word-item">
                <span class="polish-word">{word['polish']}</span>
                <span class="chinese-meaning">{word['chinese']}</span>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("🗑️", key=f"del_today_{word['id']}", help="删除此单词"):
                delete_word(word['id'])
                st.rerun()
    
    if st.button("完成今日打卡", key="checkin_btn"):
        try:
            for word in today_words:
                supabase.table('checkin_history').insert({
                    'date': today,
                    'polish': word['polish'],
                    'chinese': word['chinese']
                }).execute()
            st.success("打卡成功！")
            st.rerun()
        except Exception as e:
            st.error(f"打卡失败：{str(e)}")
else:
    st.info("今天还没有添加单词")

# 打卡历史部分
st.header("打卡历史")

try:
    history_response = supabase.table('checkin_history').select('*').execute()
    history_data = history_response.data
    
    # 按日期分组
    history = {}
    for item in history_data:
        date = item['date']
        if date not in history:
            history[date] = []
        history[date].append({'id': item['id'], 'polish': item['polish'], 'chinese': item['chinese']})
except Exception as e:
    st.error(f"加载历史记录失败：{str(e)}")
    history = {}

if history:
    for date in sorted(history.keys(), reverse=True):
        words_list = history[date]
        with st.expander(f"📅 {date} ({len(words_list)}个单词)"):
            for word in words_list:
                col1, col2 = st.columns([10, 1])
                with col1:
                    st.markdown(f"""
                    <div class="word-item">
                        <span class="polish-word">{word['polish']}</span>
                        <span class="chinese-meaning">{word['chinese']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    if st.button("🗑️", key=f"del_history_{word['id']}", help="删除此单词"):
                        delete_history_word(word['id'])
                        st.rerun()
else:
    st.info("还没有打卡记录")
