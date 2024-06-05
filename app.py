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
st.markdown('<h1 class="title">오늘의 식단</h1>', unsafe_allow_html=True)

# 데이터 가져오기
rows = fetch_data()

# 데이터 파싱
data = {}
categories = set()
for row in rows:
    restaurant_name, food_category, menu, date = row
    if menu:  # 메뉴가 있는 경우만 추가
        categories.add(food_category)
        if restaurant_name not in data:
            data[restaurant_name] = {}
        if food_category not in data[restaurant_name]:
            data[restaurant_name][food_category] = []
        menu_items = menu.split('|')
        data[restaurant_name][food_category].append((menu_items, date))

# 카테고리를 리스트로 변환하여 정렬
categories = sorted(list(categories))

# 카테고리 별 색상 매핑
category_colors = {
    "한식": "#FF6F61",
    "양식": "#4CAF50",
    "분식": "#FFA726",
    "일식": "#A52A2A",
    "중식": "#8A2BE2",
    "기타": "#00CED1",
    "점심" : "#4682B4",
    "저녁" : "#C71585",
}

# 탭 구성
tab1, tab2, tab3 = st.tabs(["학생회관식당", "오렌지식당", "교직원식당"])

# 탭 내용 출력 함수
def display_data(restaurant_name):
    if restaurant_name in data:
        valid_categories = [category for category in categories if category in data[restaurant_name]]
        cols = st.columns(len(valid_categories))

        for i, category in enumerate(valid_categories):
            with cols[i]:
                color = category_colors.get(category, "#FFFFFF")
                st.markdown(f'<div class="category-box" style="background-color: {color}; border: 2px solid {color};"><div class="category-title">{category}</div>', unsafe_allow_html=True)
                for menus, date in data[restaurant_name][category]:
                    st.markdown(f'<p class="date">{date}</p>', unsafe_allow_html=True)
                    for item in menus:
                        st.markdown(f'<li>{item}</li>', unsafe_allow_html=True)  # Using li for styling
                st.markdown('</div>', unsafe_allow_html=True)
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
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@700&display=swap');
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .title {
        font-family: 'Roboto', sans-serif;
        font-size: 2.5em;
        color: #1E90FF;
        text-align: center;
        font-weight: bold;
    }
    .stTabs [role="tablist"] {
        justify-content: center;
    }
    [data-baseweb="tab"] button {
        font-size: 1.5em !important;
    }
    .category-box {
        display: flex;
        flex-direction: column;
        align-items: center;
        background-color: #f9f9f9;
        padding: 5px;
        border-radius: 15px; /* 둥근 박스 설정 */
        margin-top: 2px;
        margin-bottom: 2px;
        text-align: center;
        border: 2px solid; /* 테두리 색상 */
    }
    .category-title {
        color: #ffffff;
        padding: 5px;
        border-radius: 15px; /* 둥근 박스 설정 */
        width: 100%;
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.8em; /* 글자 크기 조정 */
        font-weight: bold; /* bold 처리 추가 */
    }
    .category-box .date {
        color: #666666;
        font-size: 1.8em;
    }
    ul {
        list-style: none;
        padding-left: 0;
    }
    li {
        margin-bottom: 5px; /* 행 간격 조정 */
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
