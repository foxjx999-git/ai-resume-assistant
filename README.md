# AI 简历与求职信助手

这是一个基于 `Streamlit` 和 `OpenAI API` 开发的小型 AI 应用。用户可以输入目标岗位、岗位描述 JD、工作经历、技能和教育背景，系统会根据这些信息生成简历优化建议、求职信草稿、岗位匹配分析和改进建议。

## 功能

- 输入目标岗位和 Job Description
- 输入个人工作经历、技能和教育背景
- 根据 JD 分析岗位匹配度
- 生成 4–5 条简历 Bullet Points
- 生成求职信草稿
- 给出改进建议
- 支持中文或英文输出
- 支持 txt / docx 下载
- 支持查看 Prompt
- 支持示例数据填充和清空输入

## 技术栈

- `Python`
- `Streamlit`
- `OpenAI API`
- `python-dotenv`
- `python-docx`

## 项目结构

```text
ai-resume-assistant/
├── app.py
├── prompts.py
├── ai_client.py
├── utils.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置 API Key

在项目根目录创建 `.env` 文件，并添加：

```env
OPENAI_API_KEY=你的_API_KEY
```
注意：不要把 `.env`上传到 GitHub。

## 运行项目

```bash
streamlit run app.py
```

## 使用方式

1. 点击“填入示例数据”或手动输入目标岗位、JD、工作经历和技能。
2. 在侧边栏选择输出语言、求职信长度和表达风格。
3. 点击“生成简历建议”。
4. 查看岗位匹配分析、简历 Bullet Points、求职信草稿和改进建议。
5. 选择 txt 或 docx 格式下载结果。

## 当前版本说明


这是第一版 MVP，重点是完成 AI 应用的核心流程：

用户输入 → Prompt 构建 → AI 调用 → JSON 解析 → 页面展示 → 文件下载

后续可以继续优化：

- 保存历史记录
- 支持上传简历文件
- 生成更正式的 Word 简历模板
- 支持中英双语结构化输出
- 支持更多岗位类型
