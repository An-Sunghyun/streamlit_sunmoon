import streamlit as st
import pymysql
import datetime

# MySQL 데이터베이스에 접속하는 함수
def fetch_data():
    # MySQL 서버 연결 설정
    db_config = {
        'host': '13.124.130.141',
        'port': 50314,
        'user': 'swanm13',  # 여기에 사용자 이름 입력
        'password': 'darkdaki23',  # 여기에 비밀번호 입력
        'database': 'sunmoon'
    }

    # MySQL 서버에 연결
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    # 오늘 날짜를 가져와서 문자열 형태로 변환
    today = datetime.datetime.now().strftime('%Y-%m-%d')

    # 데이터 조회 쿼리
    query = """
    SELECT restaurant_name, food_category, menu, date
    FROM sunmoon_today_menu
    WHERE date = %s
    """
    
    cursor.execute(query, (today,))
    
    rows = cursor.fetchall()

    # 연결 종료
    cursor.close()
    conn.close()

    return rows

# Streamlit 앱 구성
st.title("오늘의 식단")

# 데이터 가져오기
rows = fetch_data()

# 데이터 파싱
data = {}
for row in rows:
    restaurant_name, food_category, menu, date = row
    if restaurant_name not in data:
        data[restaurant_name] = {}
    if food_category not in data[restaurant_name]:
        data[restaurant_name][food_category] = []
    menu_items = menu.split('|')
    data[restaurant_name][food_category].append((menu_items, date))

# 탭 구성
tab1, tab2, tab3 = st.tabs(["학생회관식당", "오렌지식당", "교직원식당"])

# 탭 내용 출력 함수
def display_data(restaurant_name):
    if restaurant_name in data:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.header("한식")
            if "한식" in data[restaurant_name]:
                for menus, date in data[restaurant_name]["한식"]:
                    st.subheader(f"Date: {date}")
                    for item in menus:
                        st.write(f"- {item}")
            else:
                st.write("No data")

        with col2:
            st.header("양식")
            if "양식" in data[restaurant_name]:
                for menus, date in data[restaurant_name]["양식"]:
                    st.subheader(f"Date: {date}")
                    for item in menus:
                        st.write(f"- {item}")
            else:
                st.write("No data")

        with col3:
            st.header("분식")
            if "분식" in data[restaurant_name]:
                for menus, date in data[restaurant_name]["분식"]:
                    st.subheader(f"Date: {date}")
                    for item in menus:
                        st.write(f"- {item}")
            else:
                st.write("No data")
    else:
        st.write("No data found for today.")

# 각 탭에 데이터 출력
with tab1:
    display_data("학생회관식당")

with tab2:
    display_data("오렌지식당")

with tab3:
    display_data("교직원식당")

# 스타일링 추가
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    h1, h2, h3 {
        color: #4CAF50;
        text-align: center;
    }
    .stHeader {
        background-color: #f0f0f0;
        padding: 10px;
        border-radius: 5px;
    }
    .stSubheader {
        color: #3a3a3a;
        font-weight: bold;
    }
    .stText {
        color: #555555;
    }
    @media (max-width: 768px) {
        .stColumn {
            display: block;
            width: 100%;
            margin-bottom: 10px;
        }
    }
    </style>
""", unsafe_allow_html=True)
