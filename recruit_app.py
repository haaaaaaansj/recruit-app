import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="채용 지원서", layout="centered")

menu = st.sidebar.radio("📌 메뉴 선택", ["지원서 제출", "지원자 리스트 보기"])

if menu == "지원서 제출":
    st.title("📄 대교 채용 지원서")
    st.markdown("지원서를 작성해 주세요. 제출하시면 자동으로 저장됩니다.")

    with st.form("application_form", clear_on_submit=True):
        name = st.text_input("이름")
        email = st.text_input("이메일")
        phone = st.text_input("연락처")
        job_position = st.selectbox("지원 분야", ["웹기획자", "상담직", "운영관리", "기타"])
        resume = st.file_uploader("이력서 업로드", type=["pdf", "docx"])
        memo = st.text_area("자기소개 및 특이사항")

        submitted = st.form_submit_button("제출하기")

        if submitted:
            if not all([name, email, phone, resume]):
                st.warning("필수 항목을 모두 입력해 주세요.")
            else:
                os.makedirs("지원서", exist_ok=True)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{timestamp}_{name}_{job_position}"

                # 저장
                df = pd.DataFrame([{
                    "이름": name,
                    "이메일": email,
                    "연락처": phone,
                    "지원 분야": job_position,
                    "자기소개": memo,
                    "제출일시": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }])
                df.to_csv(os.path.join("지원서", f"{filename}.csv"), index=False, encoding="utf-8-sig")
                with open(os.path.join("지원서", f"{filename}_{resume.name}"), "wb") as f:
                    f.write(resume.getbuffer())
                st.success("지원이 완료되었습니다. 감사합니다!")

elif menu == "지원자 리스트 보기":
    st.title("📋 지원자 리스트")
    os.makedirs("지원서", exist_ok=True)
    files = [f for f in os.listdir("지원서") if f.endswith(".csv")]

    if not files:
        st.info("아직 제출된 지원서가 없습니다.")
    else:
        dfs = []
        for f in files:
            df = pd.read_csv(os.path.join("지원서", f), encoding="utf-8-sig")
            df["파일명"] = f
            dfs.append(df)

        all_df = pd.concat(dfs, ignore_index=True)
        st.dataframe(all_df)
