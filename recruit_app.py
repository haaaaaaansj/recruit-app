import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="대교 채용 지원서", layout="centered")

st.markdown("""<h1 style='text-align: center; color: navy;'>대교 채용 지원 시스템</h1>""", unsafe_allow_html=True)
st.markdown("#### 📌 아래 탭을 이동하며 지원서를 제출하거나 접수 현황을 확인할 수 있습니다.")

tab1, tab2 = st.tabs(["📝 지원서 작성", "📋 지원자 리스트"])

with tab1:
    st.subheader("📝 지원서 작성")

    with st.form("application_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("이름")
            birth = st.date_input("생년월일")
            email = st.text_input("이메일")
        with col2:
            phone = st.text_input("연락처")
            job_position = st.selectbox("지원 직무", ["웹기획자", "운영관리", "고객상담", "기타"])
            resume = st.file_uploader("이력서 첨부 (PDF, DOCX)", type=["pdf", "docx"])

        memo = st.text_area("자기소개 (선택사항)", height=150)
        submitted = st.form_submit_button("📨 제출하기")

        if submitted:
            if not all([name, birth, email, phone, job_position, resume]):
                st.warning("❗ 필수 항목을 모두 입력해 주세요.")
            else:
                os.makedirs("지원서", exist_ok=True)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{timestamp}_{name}_{job_position}"

                df = pd.DataFrame([{
                    "이름": name,
                    "생년월일": birth.strftime('%Y-%m-%d'),
                    "이메일": email,
                    "연락처": phone,
                    "지원 분야": job_position,
                    "자기소개": memo,
                    "제출일시": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }])
                df.to_csv(os.path.join("지원서", f"{filename}.csv"), index=False, encoding="utf-8-sig")

                with open(os.path.join("지원서", f"{filename}_{resume.name}"), "wb") as f:
                    f.write(resume.getbuffer())

                st.success("✅ 지원서가 제출되었습니다. 감사합니다!")

with tab2:
    st.subheader("📋 지원자 리스트")
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
