import streamlit as st
import json


from prompts import build_resume_prompt
from ai_client import generate_resume_advice,DEFAULT_MODEL
from utils import (
    build_download_text, 
    validate_result_data,
    build_file_name,
    create_word_file
    )



if "result_data" not in st.session_state:
    st.session_state.result_data = None

if "full_result_text" not in st.session_state:
    st.session_state.full_result_text = ""

if "cover_letter_text" not in st.session_state:
    st.session_state.cover_letter_text = ""

if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = ""

if "result_data" not in st.session_state:
    st.session_state.result_data = None




st.title("AI 简历与求职信助手")

st.write("根据目标岗位 JD，帮助你优化简历内容并生成求职信草稿。")

st.sidebar.header("输出设置")

st.sidebar.caption(f"当前模型：{DEFAULT_MODEL}")

output_language = st.sidebar.selectbox(
    "输出语言",
    ["中文", "英文"]
)

cover_letter_length = st.sidebar.selectbox(
    "求职信长度",
    ["简短", "中等", "详细"]
)

writing_tone = st.sidebar.selectbox(
    "表达风格",
    ["专业", "自信", "简洁"]
)


sample_col, clear_col = st.columns(2)

with sample_col:
    if st.button("填入示例数据"):
        st.session_state.target_job_title_input = "Software QA Engineer"

        st.session_state.job_description_input = """
We are looking for a Software QA Engineer to design and execute test cases, perform API testing, support automation testing, track defects, and collaborate with developers and product managers to ensure high-quality software delivery.

Requirements:
- Experience in software testing
- Familiar with test case design and defect tracking
- Knowledge of API testing tools such as Postman
- Experience with automation testing tools such as Selenium
- Good communication and problem-solving skills
"""

        st.session_state.work_experience_input = """
I have experience in software testing, including test case design, manual testing, regression testing, bug tracking, and working with developers to verify fixes. I have participated in testing web applications and supported product release cycles.
"""

        st.session_state.skills_input = """
Selenium, Postman, JIRA, Python, API Testing, Regression Testing, Test Case Design, Bug Tracking
"""

        st.session_state.education_input = """
Bachelor's degree in Engineering. Completed software testing and automation testing related training.
"""

        st.rerun()


with clear_col:
    if st.button("清空输入"):
        st.session_state.target_job_title_input = ""
        st.session_state.job_description_input = ""
        st.session_state.work_experience_input = ""
        st.session_state.skills_input = ""
        st.session_state.education_input = ""

        st.session_state.result_data = None
        st.session_state.full_result_text = ""
        st.session_state.cover_letter_text = ""
        st.session_state.last_prompt = ""

        st.rerun()



target_job_title = st.text_input(
    "目标岗位",
    placeholder="例如：Software QA Engineer / Data Analyst / AI Product Assistant",
    key="target_job_title_input"
)

job_description = st.text_area(
    "岗位描述 JD",
    placeholder="请粘贴目标岗位的 Job Description，例如岗位职责、技能要求、任职资格等。",
    height=180,
    key="job_description_input"
)

work_experience = st.text_area(
    "工作经历",
    placeholder="请描述你的工作经历，例如：公司、职位、主要职责、项目经验、使用过的工具、取得的成果等。",
    height=180,
    key="work_experience_input"
)

skills = st.text_area(
    "技能",
    placeholder="例如：Python, Selenium, Postman, JIRA, API Testing, SQL, Communication Skills",
    height=120,
    key="skills_input"
)

education = st.text_area(
    "教育背景 / 其他背景（可选）",
    placeholder="例如：本科专业、硕士专业、证书、培训经历、转行背景等。",
    height=120,
    key="education_input"
)

if st.button("生成简历建议"):
    if not target_job_title.strip() or not job_description.strip() or not work_experience.strip() or not skills.strip():
        st.warning("请先填写目标岗位、岗位描述 JD、工作经历和技能。")
    else:
        prompt = build_resume_prompt(
            target_job_title,
            job_description,
            work_experience,
            skills,
            education,
            output_language,
            cover_letter_length,
            writing_tone
        )

        st.session_state.last_prompt = prompt

        try:
            with st.spinner("AI 正在分析简历与岗位匹配度，请稍等..."):
                result = generate_resume_advice(prompt)

            result_data = json.loads(result)

            is_valid, error_message = validate_result_data(result_data)

            if not is_valid:
                st.error(error_message)
                st.text_area("AI 原始返回内容", result, height=600)
                st.stop()

            resume_bullets_text = ""
            for bullet in result_data["resume_bullets"]:
                resume_bullets_text += f"- {bullet}\n"

            full_result_text = (
                f"【岗位匹配分析】\n"
                f"{result_data['match_analysis']}\n\n"
                f"【优化后的简历 Bullet Points】\n"
                f"{resume_bullets_text}\n"
                f"【求职信草稿】\n"
                f"{result_data['cover_letter']}\n\n"
                f"【改进建议】\n"
                f"{chr(10).join(['- ' + s for s in result_data['improvement_suggestions']])}"
            )

            st.session_state.result_data = result_data
            st.session_state.full_result_text = full_result_text
            st.session_state.cover_letter_text = result_data["cover_letter"]

        except json.JSONDecodeError:
            st.error("AI 返回的内容不是标准 JSON，暂时无法拆分展示。")
            st.text_area("AI 原始返回内容", result, height=600)

        except Exception as e:
            st.error("AI 生成失败，请检查 API Key、网络连接或账户额度。")
            st.write(e)
 


if st.session_state.result_data:
    result_data = st.session_state.result_data

    title_col, button_col = st.columns([4, 1])

    with title_col:
        st.subheader("AI 生成结果")

    with button_col:
        if st.button("清空结果"):
            st.session_state.result_data = None
            st.session_state.full_result_text = ""
            st.session_state.cover_letter_text = ""
            st.rerun()

    tab1, tab2, tab3, tab4 = st.tabs([
        "岗位匹配分析",
        "简历 Bullet Points",
        "求职信草稿",
        "改进建议"
    ])

    with tab1:
        st.write(result_data["match_analysis"])

    with tab2:
        for bullet in result_data["resume_bullets"]:
            st.write(f"- {bullet}")

    with tab3:
        edited_cover_letter = st.text_area(
            "求职信",
            height=300,
            key="cover_letter_text"
        )

    with tab4:
        for suggestion in result_data["improvement_suggestions"]:
            st.write(f"- {suggestion}")



    file_type_col, download_button_col = st.columns([2,1])

    with file_type_col:
        file_type = st.selectbox(
        "下载类型",
        ["txt", "docx"]
        )
    

    with download_button_col:
        st.markdown("<div style='height: 28px'></div>", unsafe_allow_html=True)


        current_full_result_text = build_download_text(result_data, edited_cover_letter)

        download_file_name = build_file_name(target_job_title,file_type)



        if file_type == "docx":
            data = create_word_file(current_full_result_text)
            mime= "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            
        else:
            data = current_full_result_text
            mime="text/plain"



        st.download_button(
            label="下载完整简历建议",
            data=data,
            file_name=download_file_name,
            mime=mime
        )

  