# db_utils.py
import os
from dotenv import load_dotenv
from contextlib import contextmanager
import streamlit as st
from supabase import create_client, Client

# 환경 변수 로드
load_dotenv()

# Supabase 클라이언트 초기화
def init_supabase():
    url: str = os.getenv('SUPABASE_URL')
    key: str = os.getenv('SUPABASE_KEY')
    return create_client(url, key)

@contextmanager
def get_db_connection():
    supabase = init_supabase()
    try:
        yield supabase
    except Exception as e:
        st.error(f"데이터베이스 오류: {e}")
        raise e

def get_allergen_risk_level(allergen):
    """
    주어진 알레르기 성분의 위험 수준을 반환합니다.
    알레르기 정보가 없으면 None을 반환합니다.
    """
    with get_db_connection() as supabase:
        result = supabase.table('allergy_info')\
            .select('risk_level')\
            .eq('allergen', allergen)\
            .execute()
        
        if result.data and len(result.data) > 0:
            return result.data[0]['risk_level']
        return None

def get_allergens_risk_levels(allergens):
    """
    여러 알레르기 성분의 위험 수준을 반환하는 함수
    allergens: 리스트 형태의 알레르기 성분
    반환: 딕셔너리 {allergen: risk_level}
    """
    if not allergens:
        return {}
    
    with get_db_connection() as supabase:
        result = supabase.table('allergy_info')\
            .select('allergen, risk_level')\
            .in_('allergen', allergens)\
            .execute()
        
        return {row['allergen']: row['risk_level'] for row in result.data}

def insert_allergy_info(allergen, risk_level):
    with get_db_connection() as supabase:
        result = supabase.table('allergy_info')\
            .upsert({'allergen': allergen, 'risk_level': risk_level})\
            .execute()
        return result

def delete_allergy_info(allergen):
    with get_db_connection() as supabase:
        result = supabase.table('allergy_info')\
            .delete()\
            .eq('allergen', allergen)\
            .execute()
        return result