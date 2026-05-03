# Supabase 配置指南

## 1. 创建Supabase项目

1. 访问 https://supabase.com 并注册/登录
2. 点击 "New Project"
3. 填写项目名称（如：polish-word-checkin）
4. 设置数据库密码
5. 选择地区（建议选择离你最近的）
6. 点击 "Create new project"

## 2. 创建数据库表

进入项目后，点击左侧菜单的 "SQL Editor"，运行以下SQL：

```sql
-- 创建words表（存储所有添加的单词）
CREATE TABLE words (
    id SERIAL PRIMARY KEY,
    polish TEXT NOT NULL,
    chinese TEXT NOT NULL,
    date TEXT NOT NULL
);

-- 创建checkin_history表（存储打卡记录）
CREATE TABLE checkin_history (
    id SERIAL PRIMARY KEY,
    date TEXT NOT NULL,
    polish TEXT NOT NULL,
    chinese TEXT NOT NULL
);

-- 启用行级安全（可选，如果需要多用户隔离）
-- ALTER TABLE words ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE checkin_history ENABLE ROW LEVEL SECURITY;
```

点击 "Run" 执行SQL。

## 3. 获取API凭据

1. 点击左侧菜单的 "Project Settings" (齿轮图标)
2. 点击 "API"
3. 复制以下信息：
   - **Project URL** (在 "URL" 部分)
   - **anon public** key (在 "Project API keys" 部分)

## 4. 配置Streamlit Cloud

1. 在Streamlit Cloud中打开你的应用
2. 点击右上角的 "..." > "Settings"
3. 点击 "Secrets"
4. 添加以下配置（替换为你的实际值）：

```toml
SUPABASE_URL = "https://xxxxx.supabase.co"
SUPABASE_KEY = "eyJhbGc..."
```

5. 点击 "Save"

## 5. 本地测试（可选）

在项目根目录创建 `.streamlit/secrets.toml` 文件：

```toml
SUPABASE_URL = "你的URL"
SUPABASE_KEY = "你的KEY"
```

或直接在代码中临时填写（不推荐提交到GitHub）。

## 完成！

现在你的应用已经连接到Supabase云数据库，数据会永久保存，即使Streamlit Cloud重启也不会丢失。
