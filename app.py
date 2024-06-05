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
        for category, menus in data[restaurant_name].items():
            for menu_items, date in menus:
                st.header(f"Restaurant: {restaurant_name}")
                st.subheader(f"Category: {category}")
                st.write(f"Date: {date}")
                st.write("Menu:")
                for item in menu_items:
                    st.write(f"  - {item}")
    else:
        st.write("No data found for today.")

# 각 탭에 데이터 출력
with tab1:
    display_data("학생회관식당")

with tab2:
    display_data("오렌지식당")

with tab3:
    display_data("교직원식당")
