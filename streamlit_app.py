import streamlit as st
import random
import base64

# 페이지 설정
st.set_page_config(page_title="🦁 몬스터 먹이 주기 게임", layout="wide")

# 몬스터 캐릭터 SVG 생성 함수
def get_monster_svg_html(color="#FF6B9D"):
    return f"""
    <svg width="250" height="280" viewBox="0 0 250 280" xmlns="http://www.w3.org/2000/svg" style="margin: 0 auto; display: block;">
        <ellipse cx="125" cy="150" rx="80" ry="90" fill="{color}" stroke="#333" stroke-width="3"/>
        <circle cx="95" cy="110" r="20" fill="white" stroke="#333" stroke-width="2"/>
        <circle cx="95" cy="115" r="12" fill="#333"/>
        <circle cx="97" cy="112" r="4" fill="white"/>
        <circle cx="155" cy="110" r="20" fill="white" stroke="#333" stroke-width="2"/>
        <circle cx="155" cy="115" r="12" fill="#333"/>
        <circle cx="157" cy="112" r="4" fill="white"/>
        <ellipse cx="125" cy="145" rx="8" ry="12" fill="#333"/>
        <path d="M 110 160 Q 125 175 140 160" stroke="#333" stroke-width="3" fill="none" stroke-linecap="round"/>
        <ellipse cx="125" cy="180" rx="12" ry="10" fill="#FF99CC"/>
        <polygon points="75,60 65,20 85,50" fill="{color}" stroke="#333" stroke-width="2"/>
        <polygon points="175,60 185,20 165,50" fill="{color}" stroke="#333" stroke-width="2"/>
        <ellipse cx="55" cy="150" rx="20" ry="50" fill="{color}" stroke="#333" stroke-width="2" transform="rotate(-25 55 150)"/>
        <circle cx="35" cy="190" r="18" fill="{color}" stroke="#333" stroke-width="2"/>
        <ellipse cx="195" cy="150" rx="20" ry="50" fill="{color}" stroke="#333" stroke-width="2" transform="rotate(25 195 150)"/>
        <circle cx="215" cy="190" r="18" fill="{color}" stroke="#333" stroke-width="2"/>
        <ellipse cx="125" cy="170" rx="35" ry="40" fill="rgba(255,255,255,0.3)" stroke="none"/>
        <ellipse cx="95" cy="235" rx="18" ry="25" fill="{color}" stroke="#333" stroke-width="2"/>
        <ellipse cx="155" cy="235" rx="18" ry="25" fill="{color}" stroke="#333" stroke-width="2"/>
        <path d="M 180 180 Q 220 150 210 100" stroke="{color}" stroke-width="25" fill="none" stroke-linecap="round" stroke-opacity="0.9"/>
    </svg>
    """

# 커스텀 CSS 스타일
st.markdown("""
    <style>
        /* 배경색 설정 */
        .main {
            background: linear-gradient(135deg, #FFE5B4 0%, #FFB6D9 50%, #C1E4FF 100%);
            padding: 20px;
        }
        
        /* 전체 앱 배경 */
        body {
            background: linear-gradient(135deg, #FFE5B4 0%, #FFB6D9 50%, #C1E4FF 100%) !important;
        }
        
        /* 헤더 스타일 */
        .header-title {
            font-size: 3em;
            font-weight: bold;
            text-align: center;
            background: linear-gradient(90deg, #FF6B9D, #FFC75F, #845EC2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
            margin: 20px 0;
        }
        
        /* 몬스터 표시 영역 */
        .monster-container {
            background: white;
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
            margin: 20px 0;
            border: 4px solid #FFD700;
        }
        
        .monster-emoji {
            font-size: 120px;
            margin: 20px 0;
            animation: bounce 2s infinite;
        }
        
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-20px); }
        }
        
        .monster-text {
            font-size: 1.8em;
            font-weight: bold;
            color: #FF6B6B;
        }
        
        /* 바구니 스타일 */
        .basket-button {
            border-radius: 15px;
            border: 3px solid #FFA500;
            padding: 20px;
            background: linear-gradient(135deg, #FFE5B4, #FFD4A3);
            font-weight: bold;
            font-size: 1.1em;
            transition: all 0.3s ease;
        }
        
        .basket-button:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(255, 165, 0, 0.4);
        }
        
        .basket-selected {
            border: 4px solid #00FF00 !important;
            background: linear-gradient(135deg, #90EE90, #98D98E) !important;
            box-shadow: 0 0 20px rgba(0, 255, 0, 0.5) !important;
        }
        
        /* 시작 버튼 스타일 */
        .start-button {
            background: linear-gradient(90deg, #FF6B9D, #FFC75F) !important;
            border-radius: 20px !important;
            padding: 20px !important;
            font-size: 1.5em !important;
            font-weight: bold !important;
        }
        
        /* 점수 카드 */
        .score-card {
            background: linear-gradient(135deg, #FFE5B4, #FFD4A3);
            border-radius: 15px;
            padding: 15px;
            text-align: center;
            border: 3px solid #FFA500;
            font-weight: bold;
        }
        
        /* 설명 텍스트 */
        .instruction-box {
            background: rgba(255, 255, 255, 0.9);
            border-left: 5px solid #FF6B9D;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            font-size: 1.1em;
        }
        
        /* 정답/오답 메시지 */
        .success-message {
            background: linear-gradient(135deg, #90EE90, #98D98E);
            border-radius: 15px;
            padding: 20px;
            font-size: 1.3em;
            font-weight: bold;
            text-align: center;
            margin: 20px 0;
        }
        
        .error-message {
            background: linear-gradient(135deg, #FFB6B6, #FF9999);
            border-radius: 15px;
            padding: 20px;
            font-size: 1.3em;
            font-weight: bold;
            text-align: center;
            margin: 20px 0;
        }
        
        /* 프로그레스 바 스타일 */
        .progress-bar {
            background: #E0E0E0;
            border-radius: 10px;
            height: 30px;
            margin: 10px 0;
            overflow: hidden;
        }
        
        .progress-fill {
            background: linear-gradient(90deg, #FF6B9D, #FFC75F);
            height: 100%;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            transition: width 0.3s ease;
        }
        
        /* 선택한 바구니 표시 */
        .selection-display {
            background: linear-gradient(135deg, #C1E4FF, #FFE5B4);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            border: 3px dashed #FF6B9D;
            margin: 20px 0;
            font-weight: bold;
        }
        
        /* 버튼들 스타일 */
        div[data-testid="stButton"] > button {
            border-radius: 15px !important;
            font-weight: bold !important;
            font-size: 1.1em !important;
            padding: 12px 20px !important;
            transition: all 0.3s ease !important;
        }
        
        div[data-testid="stButton"] > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2) !important;
        }
    </style>
""", unsafe_allow_html=True)

# 게임 상태 초기화
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.question_count = 0
    st.session_state.selected_baskets = []
    st.session_state.game_started = False
    st.session_state.show_result = False
    st.session_state.is_correct = False

# 새로운 문제 생성
def has_valid_solution(target, basket_counts):
    """
    주어진 target과 basket_counts에서 서로 다른 두 바구니의 합이 target이 되는 조합이 있는지 확인
    
    Args:
        target: 목표 숫자 (몬스터가 원하는 먹이 개수)
        basket_counts: 4개 바구니의 먹이 개수 리스트
    
    Returns:
        정답 조합이 존재하면 True, 없으면 False
    """
    n = len(basket_counts)
    for i in range(n):
        for j in range(i + 1, n):
            if basket_counts[i] + basket_counts[j] == target:
                return True
    return False

def generate_question():
    """
    정답이 존재하는 게임 문제를 생성한다.
    
    반드시 다음 조건을 만족:
    - 서로 다른 두 바구니의 합이 target이 되는 조합이 최소 1개 존재
    - 정답이 없는 문제는 절대 생성되지 않음
    - 모든 문제는 사용자가 풀 수 있음
    
    Returns:
        (monster_want, basket_counts): 몬스터가 원하는 개수, 4개 바구니의 개수
    """
    while True:
        monster_want = random.randint(5, 15)  # 몬스터가 원하는 먹이 개수 (5~15)
        basket_counts = [random.randint(1, 9) for _ in range(4)]  # 4개의 바구니
        
        # 정답이 있는지 검증 - 정답이 있으면 문제 반환
        if has_valid_solution(monster_want, basket_counts):
            return monster_want, basket_counts
        # 정답이 없으면 반복문을 통해 새로운 문제 생성

# 게임 시작
if not st.session_state.game_started:
    st.markdown('<p class="header-title">🦁 몬스터 먹이 주기 게임 🎮</p>', unsafe_allow_html=True)
    
    # 몬스터 표시
    st.markdown(f"""
    <div class="monster-container">
        {get_monster_svg_html()}
    </div>
    """, unsafe_allow_html=True)
    
    # 설명
    st.markdown("""
    <div class="instruction-box">
        <h2>🎯 게임 방법</h2>
        <p>✨ 몬스터가 원하는 만큼 먹이를 모아줄 수 있니?</p>
        <ul>
            <li>🦁 몬스터가 원하는 먹이의 개수를 확인해요</li>
            <li>🧺 먹이 바구니 2개를 선택해요</li>
            <li>➕ 두 바구니의 먹이를 더했을 때 몬스터가 원하는 개수가 나와야 해요!</li>
            <li>⭐ 정답을 맞추면 점수를 얻어요!</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🎮 게임 시작하기", key="start_button", use_container_width=True):
            st.session_state.game_started = True
            st.session_state.monster_want, st.session_state.basket_counts = generate_question()
            st.session_state.selected_baskets = []
            st.session_state.show_result = False
            st.rerun()

# 게임 진행 중
else:
    st.markdown('<p class="header-title">🦁 몬스터 먹이 주기 게임 🎮</p>', unsafe_allow_html=True)
    
    # 헤더: 점수와 문제 번호
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="score-card">
            ⭐ 점수<br>
            <span style="font-size: 2.5em; color: #FF6B9D;">{st.session_state.score}</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="score-card">
            ❓ 문제 번호<br>
            <span style="font-size: 2.5em; color: #FFC75F;">{st.session_state.question_count + 1}</span>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        success_rate = int(st.session_state.score / (max(st.session_state.question_count, 1) * 10) * 100) if st.session_state.question_count > 0 else 0
        st.markdown(f"""
        <div class="score-card">
            🎯 성공률<br>
            <span style="font-size: 2.5em; color: #845EC2;">{success_rate}%</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 몬스터와 먹이 개수 표시
    st.markdown(f'<div class="monster-container">{get_monster_svg_html()}</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #FFB6D9, #FFE5B4); border-radius: 20px; padding: 30px; text-align: center; border: 4px solid #FF6B9D; box-shadow: 0 5px 15px rgba(255, 107, 157, 0.3);">
            <p style="font-size: 4em; font-weight: bold; color: #FF6B9D; margin: 0;">{st.session_state.monster_want}</p>
            <p style="font-size: 2em; margin: 0;">🍖</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 바구니 선택 영역
    st.markdown("## 🧺 바구니를 선택하세요 (2개)")
    
    basket_cols = st.columns(4)
    for i in range(4):
        with basket_cols[i]:
            is_selected = i in st.session_state.selected_baskets
            basket_num = st.session_state.basket_counts[i]
            
            # 선택 상태에 따른 스타일
            status = '✅ 선택됨' if is_selected else '🧺'
            button_label = f"{status}\n\n바구니 {i+1}\n\n{basket_num}\n🍖"
            button_color = "rainbow" if is_selected else "secondary"
            
            if st.button(
                button_label,
                key=f"basket_{i}",
                use_container_width=True,
                help=f"바구니 {i+1}에는 {basket_num}개의 먹이가 있어요"
            ):
                # 선택 토글
                if i in st.session_state.selected_baskets:
                    st.session_state.selected_baskets.remove(i)
                else:
                    if len(st.session_state.selected_baskets) < 2:
                        st.session_state.selected_baskets.append(i)
                    else:
                        st.session_state.selected_baskets.pop(0)
                        st.session_state.selected_baskets.append(i)
                st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 선택된 바구니 표시
    if len(st.session_state.selected_baskets) > 0:
        selected_counts = [st.session_state.basket_counts[i] for i in st.session_state.selected_baskets]
        
        if len(st.session_state.selected_baskets) == 2:
            total = sum(selected_counts)
            
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.markdown(f"""
                <div style="background: #FFE5B4; border-radius: 15px; padding: 15px; text-align: center; border: 2px solid #FFA500;">
                    <p style="font-size: 0.9em; margin: 0; color: #666;">바구니 {st.session_state.selected_baskets[0]+1}</p>
                    <p style="font-size: 2em; font-weight: bold; color: #FFA500; margin: 5px 0;">{selected_counts[0]}</p>
                    <p style="font-size: 1.2em; margin: 0;">🍖</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="display: flex; align-items: center; justify-content: center; font-size: 2em; font-weight: bold; color: #FF6B9D; height: 100%;">
                    ➕
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div style="background: #FFE5B4; border-radius: 15px; padding: 15px; text-align: center; border: 2px solid #FFA500;">
                    <p style="font-size: 0.9em; margin: 0; color: #666;">바구니 {st.session_state.selected_baskets[1]+1}</p>
                    <p style="font-size: 2em; font-weight: bold; color: #FFA500; margin: 5px 0;">{selected_counts[1]}</p>
                    <p style="font-size: 1.2em; margin: 0;">🍖</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div style="display: flex; align-items: center; justify-content: center; font-size: 2em; font-weight: bold; color: #FF6B9D; height: 100%;">
                    =
                </div>
                """, unsafe_allow_html=True)
            
            with col5:
                color = "#90EE90" if total == st.session_state.monster_want else "#FFB6B6"
                border_color = "#00CC00" if total == st.session_state.monster_want else "#FF6666"
                st.markdown(f"""
                <div style="background: {color}; border-radius: 15px; padding: 15px; text-align: center; border: 3px solid {border_color};">
                    <p style="font-size: 0.9em; margin: 0; color: #333;">합계</p>
                    <p style="font-size: 2em; font-weight: bold; color: #333; margin: 5px 0;">{total}</p>
                    <p style="font-size: 1.2em; margin: 0;">🍖</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # 정답 확인 버튼
            col1, col2, col3 = st.columns(3)
            with col2:
                if st.button("✅ 정답 확인", key="check_answer", use_container_width=True):
                    st.session_state.show_result = True
                    st.session_state.is_correct = total == st.session_state.monster_want
                    if st.session_state.is_correct:
                        st.session_state.score += 10
                    st.session_state.question_count += 1
                    st.rerun()
    
    # 결과 표시
    if st.session_state.show_result:
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.session_state.is_correct:
            st.markdown("""
            <div class="success-message">
                🎉🎉🎉 정답입니다! 🎉🎉🎉<br>
                <span style="font-size: 0.8em;">몬스터가 맛있게 먹었어요! ⭐ +10점 획득!</span>
            </div>
            """, unsafe_allow_html=True)
            st.balloons()
        else:
            total = sum([st.session_state.basket_counts[i] for i in st.session_state.selected_baskets])
            st.markdown(f"""
            <div class="error-message">
                ❌ 틀렸어요! ❌<br>
                <span style="font-size: 0.9em;">정답: {st.session_state.monster_want} 🍖 | 선택: {total} 🍖</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 다음 문제 버튼
        col1, col2, col3 = st.columns(3)
        with col2:
            if st.button("⏭️ 다음 문제", key="next_question", use_container_width=True):
                st.session_state.monster_want, st.session_state.basket_counts = generate_question()
                st.session_state.selected_baskets = []
                st.session_state.show_result = False
                st.rerun()
    
    # 게임 끝내기 버튼
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🏠 게임 끝내기", key="end_game", use_container_width=True):
            st.session_state.game_started = False
            st.session_state.show_result = False
            st.session_state.score = 0
            st.session_state.question_count = 0
            st.session_state.selected_baskets = []
            st.rerun()
    
    with col3:
        if st.session_state.question_count > 0:
            final_percentage = int(st.session_state.score / (st.session_state.question_count * 10) * 100)
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #FFE5B4, #FFD4A3); border-radius: 15px; padding: 15px; text-align: center; border: 3px solid #FFC75F; font-weight: bold;">
                🏆 최종 점수<br>
                <span style="font-size: 1.8em; color: #FF6B9D;">{st.session_state.score}/{st.session_state.question_count * 10}</span><br>
                <span style="color: #FFC75F;">{final_percentage}% 성공!</span>
            </div>
            """, unsafe_allow_html=True)
