import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import re
from db_utils import get_db_connection  # 수정된 db_utils.py의 함수 임포트

# 환경 변수 로드
load_dotenv()

# 알레르기 정보 삽입 함수
def insert_allergy_info(allergen, risk_level):
    with get_db_connection() as supabase:
        data = {'allergen': allergen, 'risk_level': risk_level}
        result = supabase.table('allergy_info').upsert(data).execute()
        return result

# 알레르기 정보 삭제 함수
def delete_allergy_info(allergen):
    with get_db_connection() as supabase:
        result = supabase.table('allergy_info').delete().eq('allergen', allergen).execute()
        return result

# 알레르기 정보 그룹 조회 함수
def get_allergy_info_grouped():
    with get_db_connection() as supabase:
        result = supabase.table('allergy_info').select('allergen, risk_level').order('risk_level').execute()
        df = pd.DataFrame(result.data)
        grouped = {
            "High risk group": df[df['risk_level'] == 'High risk group'],
            "Risk group": df[df['risk_level'] == 'Risk group'],
            "Caution group": df[df['risk_level'] == 'Caution group']
        } if not df.empty else {
            "High risk group": pd.DataFrame(),
            "Risk group": pd.DataFrame(),
            "Caution group": pd.DataFrame()
        }
        return grouped

# 입력값 검증 함수
def validate_allergen(allergen):
    pattern = re.compile(r'^[A-Za-z가-힣\s\-\/]+$')
    return bool(pattern.match(allergen))

# 위험 그룹 이름 매핑 (한국어 <-> 영어)
risk_level_mapping = {
    "고위험": "High risk group",
    "위험": "Risk group",
    "주의": "Caution group"
}

# Streamlit 애플리케이션 시작
st.title("알레르기 정보 관리")

# 알레르기 정보 입력 섹션
st.subheader("알레르기 정보 입력")

# 알레르기 성분 입력
allergen = st.text_input("알레르기 성분을 입력하세요 (예: 땅콩, 우유)", key="allergen_input")

# 위험 그룹 선택 (한국어 이름 사용)
risk_level_korean = st.selectbox("위험 그룹을 선택하세요", list(risk_level_mapping.keys()))

# 알레르기 정보 추가 버튼
if st.button("알레르기 정보 추가"):
    if allergen and risk_level_korean:
        if validate_allergen(allergen):
            risk_level = risk_level_mapping[risk_level_korean]  # 한국어 -> 영어 변환 후 저장
            insert_allergy_info(allergen, risk_level)
            st.success("알레르기 정보가 추가되었습니다!")
        else:
            st.error("알레르기 성분에 유효하지 않은 문자가 포함되어 있습니다.")
    else:
        st.error("알레르기 성분과 위험 그룹을 모두 입력해주세요.")

st.markdown("---")

# 저장된 알레르기 정보 표시 섹션
st.subheader("저장된 알레르기 정보 목록")

# 그룹별 데이터 가져오기
allergy_data_grouped = get_allergy_info_grouped()

# 그룹별로 테이블 및 삭제 버튼 표시
for group, data in allergy_data_grouped.items():
    korean_group_name = {v: k for k, v in risk_level_mapping.items()}[group]  # 영어 -> 한국어 변환

    # 위험도에 따른 색상 및 배경색 지정
    if korean_group_name == "고위험":
        color = "white"
        background_color = "rgba(255, 0, 0, 0.7)"
    elif korean_group_name == "위험":
        color = "black"
        background_color = "rgba(255, 165, 0, 0.7)"
    else:  # "주의" 그룹
        color = "black"
        background_color = "rgba(255, 255, 0, 0.7)"

    if not data.empty:
        allergens_list = " | ".join(data['allergen'])

        st.markdown(
            f"""
            <div style="background-color:{background_color}; padding: 15px; border-radius: 5px; display: flex; justify-content: space-between; align-items: center;">
                <h3 style="color:{color}; font-size: 32px; font-weight: bold; text-align: left; margin: 0;">{korean_group_name}</h3>
                <div style="display: flex; align-items: center;">
                    <p style="font-size: 24px; font-weight: bold; text-align: left; margin: 0; padding-right: 10px; color: {color};">{allergens_list}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # 항목별 삭제 버튼 추가
        for index, row in data.iterrows():
            delete_button = st.button(f"삭제 {row['allergen']}", key=f"delete_{group}_{index}", use_container_width=True)

            if delete_button:
                delete_allergy_info(row['allergen'])  # 해당 항목만 삭제하는 함수 호출
                st.success(f"{row['allergen']} 항목이 삭제되었습니다!")
    else:
        st.write(f"{korean_group_name} 그룹에 저장된 알레르기 정보가 없습니다.")














