def build_resume_prompt(
        target_job_title, 
        job_description, 
        work_experience, 
        skills, 
        education,
        output_language,
        cover_letter_length,
        writing_tone
):
    prompt = f"""
你是一名资深招聘经理、职业顾问和简历优化专家，擅长根据目标岗位 JD 优化简历和求职信。

请根据以下用户信息完成任务：

【目标岗位】
{target_job_title}

【岗位描述 JD】
{job_description}

【工作经历】
{work_experience}

【技能】
{skills}

【教育背景 / 其他背景】
{education if education else "用户未提供"}

【输出设置】
输出语言：{output_language}
求职信长度：{cover_letter_length}
表达风格：{writing_tone}

请完成以下任务：
1. 分析用户背景与目标岗位的匹配度。
2. 生成 4–5 条优化后的简历 bullet points。
3. 生成一封简短、专业、有说服力的求职信草稿。
4. 给出提高求职成功率的改进建议。

要求：
语言规则：
- 用户选择的输出语言是：{output_language}
- 如果输出语言是“中文”，所有 JSON value 内容必须全部使用中文。
- 如果输出语言是“英文”，所有 JSON value 内容必须全部使用英文，不要夹杂中文。
- 无论选择哪种语言，JSON key 名必须保持英文，不要翻译 key。
- 表达要专业、清晰、真实。
- 不要编造用户没有提供的经历、技能或成果。
- 如果用户信息不足，请基于已有信息保守表达，并指出需要补充的信息。
- 简历 bullet points 要尽量体现岗位关键词、职责、技能和成果。

请严格按照以下 JSON 格式输出，不要输出 JSON 以外的任何内容：

{{
  "match_analysis": "...",
  "resume_bullets": [
    "...",
    "...",
    "...",
    "..."
  ],
  "cover_letter":  "...",
  "improvement_suggestions": [
    "...",
    "...",
    "..."
  ]
}}
"""
    return prompt