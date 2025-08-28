import datetime
import random


def check_cry_laugh_stress_message(msg):
    """감정 표현 체크 - 기존 인터페이스 유지 (메인 진입점)"""
    return check_all_patterns(msg)


def check_all_patterns(msg):
    """모든 패턴 체크 통합 함수"""
    current_hour = datetime.datetime.now().hour

    # 나가라는 말에 대한 반응 (최우선 처리)
    if "나가" in msg:
        return "죄송합니다"

    sleep_result = check_sleep_mention(msg)
    if sleep_result:
        return sleep_result

    # 기본 감정 체크 (기존 로직) - 조건 완화
    basic_emotion = check_basic_emotions(msg)
    if basic_emotion:
        return basic_emotion

    # 음식 관련 체크 추가
    food_result = check_food_mention(msg)
    if food_result:
        return food_result

    # 잠/졸림 관련 체크 추가
    sleep_result = check_sleep_mention(msg)
    if sleep_result:
        return sleep_result

    # 공부 관련 체크 추가
    study_result = check_study_mention(msg)
    if study_result:
        return study_result

    # 추가 감정 체크
    anger_result = check_anger(msg)
    if anger_result:
        return anger_result

    surprise_result = check_surprise(msg)
    if surprise_result:
        return surprise_result

    # 텍스트 패턴 체크
    caps_result = check_caps_lock(msg)
    if caps_result:
        return caps_result

    repeat_result = check_repeat_chars(msg)
    if repeat_result:
        return repeat_result

    question_result = check_question_spam(msg)
    if question_result:
        return question_result

    # 행동 패턴 체크
    aegyo_result = check_aegyo(msg)
    if aegyo_result:
        return aegyo_result

    typo_result = check_typos(msg)
    if typo_result:
        return typo_result

    # 시간/상황 기반 체크
    time_result = check_time_sensitive(msg, current_hour)
    if time_result:
        return time_result

    weather_result = check_weather_mood(msg)
    if weather_result:
        return weather_result

    # 메타 반응 체크
    bot_result = check_bot_mention(msg)
    if bot_result:
        return bot_result

    compliment_result = check_compliment(msg)
    if compliment_result:
        return compliment_result

    return None


def check_basic_emotions(msg):
    """기본 감정 체크 (기존 로직)"""
    if "ㅠ" in msg or "ㅜ" in msg:
        return check_cry(msg)
    elif "ㅋ" in msg or "ㅎ" in msg:
        return check_laugh(msg)
    elif ";" in msg:
        return check_stress(msg)
    return None


def check_cry(msg):
    """울음 체크"""
    messages = ["ㅠㅠㅠㅜㅜㅠ", "왜 우시는 거예요?", "ㅋㅋ얘 운다"]
    if sum(msg.count(char) for char in "ㅠㅜ") >= 2:
        return random.choice(messages)
    return None


def check_laugh(msg):
    """웃음 체크"""
    messages = ["뭘 웃어요;;", "ㅋㄱㅋㄱㅋㄱㅋㄱㅋㄱㅋㄱㅋㅋ", "이게 웃겨요?"]
    if sum(msg.count(char) for char in "ㅋㄱㄲㄴㅌㅎ") >= 5:
        return random.choice(messages)
    return None


def check_stress(msg):
    """스트레스 체크"""
    if sum(msg.count(char) for char in ";:,.") >= 4:
        return "어림도 없지"
    return None


def check_anger(msg):
    """화남 체크"""
    anger_chars = "ㅡㅗㅢㅣ"
    if sum(msg.count(char) for char in anger_chars) >= 3:
        return random.choice(["화내지 마세요", "진정하세요", "왜 화나셨어요"])
    return None


def check_surprise(msg):
    """놀람 체크"""
    if msg.count("!") >= 3 or "헉" in msg or "어머" in msg or "우와" in msg:
        return random.choice(["뭘 그렇게 놀라요", "놀랄 일도 아닌데", "헉 뭐가 놀라워요"])
    return None


def check_question_spam(msg):
    """물음표 도배"""
    if msg.count("?") >= 5 or msg.count("？") >= 5:
        return "물음표가 너무 많아요"
    return None


def check_aegyo(msg):
    """애교 체크"""
    aegyo_words = ["뿌잉", "츄", "헤헤", "히히", "뽀뽀", "야옹", "멍멍", "응애"]
    if any(word in msg for word in aegyo_words):
        return random.choice(["애교 그만;;", "귀여운척 하지 마세요;;", "응애 나 애기"])
    return None


def check_typos(msg):
    """오타 감지"""
    typo_patterns = {
        "ㅁㄴㅇㄹ": "뭔말",
        "ㅇㄱㄹㅇ": "이거레알",
        "ㅂㅂㅂㄱ": "빨리빨리",
        "ㄴㄴ": "노노",
        "ㅇㅇ": "응응",
        "ㅋㅋㄹㅃㅃ": "크크루삥뽕"
    }
    for typo, correction in typo_patterns.items():
        if typo in msg:
            return f"{correction}이라고 하세요"
    return None


def check_sleep_mention(msg):
    """잠/졸림 관련 체크 강화"""
    sleep_keywords = ["졸려", "졸리", "잠", "자야지", "피곤", "잠와", "잠온", "꿀잠"]

    if any(word in msg for word in sleep_keywords):
        current_hour = datetime.datetime.now().hour

        if current_hour < 6:
            return "늦게까지 뭐해요"
        elif 6 <= current_hour < 10:
            return "일찍 일어나셨네요"
        elif 10 <= current_hour <= 21:
            responses = ["자라;;", "졸리지 마세요", "커피 마셔요", "잠깐 쉬세요"]
            return random.choice(responses)
        elif current_hour >= 22:
            return "너무 힘들면, 자요"

    return None


def check_time_sensitive(msg, current_hour):
    """시간대별 반응"""
    # 기존 점심/공부 관련 로직
    if current_hour >= 22 or current_hour < 6:
        if any(word in msg for word in ["공부", "과제", "숙제", "발표", "프로젝트"]):
            responses = ["늦게까지 고생이 많네요", "잠깐 쉬세요", f"이 시간에 {word}는 너무 힘들죠"]
            return random.choice(responses)

    return None


def check_weather_mood(msg):
    """날씨 관련"""
    weather_words = {
        "비": "우울하네요",
        "눈": "낭만적이네요",
        "더워": "시원한 곳 가세요",
        "추워": "따뜻하게 입으세요",
        "바람": "바람 쐬러 나가세요",
        "햇살": "좋은 날씨네요",
        "구름": "흐린 날이네요"
    }
    tokens = msg.split()
    for word, response in weather_words.items():
        if word in tokens:
            return response
    return None


def check_bot_mention(msg):
    """봇 언급"""
    bot_keywords = ["크하학", "봇", "AI", "인공지능", "챗봇", "로봇", "너", "넌"]
    if any(word in msg for word in bot_keywords):
        return random.choice([
            "저를 부르셨나요?",
            "네 뭐든지 물어보세요",
            "크하학입니다",
            "왜요?"
        ])
    return None


def check_compliment(msg):
    """칭찬 감지"""
    compliments = ["귀여워", "똑똑해", "잘해", "좋아", "멋져", "예뻐", "사랑해", "고마워", "최고"]
    if any(word in msg for word in compliments):
        return random.choice([
            "고마워요 헤헤",
            "저도 좋아해요",
            "칭찬 고마워요",
            "기분 좋네요"
        ])
    return None


def check_food_mention(msg):
    """음식 언급"""
    # 뭐먹을지 물어보는 경우
    if "뭐먹" in msg or "머먹" in msg:
        foods = [
            # 한식
            "돼지갈비!!", "황금볶음밥!!", "미역국!!", "닭갈비!!", "떡볶이!!",
            "김치찌개!!", "된장찌개!!", "비빔밥!!", "냉면!!", "물냉면!!",
            "불고기!!", "삼겹살!!", "갈비탕!!", "설렁탕!!", "순대국!!",
            "김밥!!", "라면!!", "칼국수!!", "짜장면!!", "짬뽕!!",
            "김치볶음밥!!", "제육볶음!!", "bulgogi!!", "치킨!!", "순두부찌개!!",

            # 양식/일식
            "돈까스!!", "스파게티!!", "피자!!", "햄버거!!", "샐러드!!",
            "스테이크!!", "파스타!!", "리조또!!", "우동!!", "카레!!",
            "초밥!!", "라멘!!", "덮밥!!", "규동!!", "오므라이스!!",

            # 중식/기타
            "탕수육!!", "짜장!!", "마파두부!!", "깐풍기!!", "양장피!!",
            "볶음밥!!", "쌀국수!!", "팟타이!!", "분짜!!", "쌀쌀면!!",

            # 간식/디저트
            "치킨!!", "족발!!", "보쌈!!", "마라탕!!", "훠궈!!",
            "타코!!", "부리또!!", "샌드위치!!", "토스트!!", "와플!!",
            "팬케이크!!", "아이스크림!!", "케이크!!", "도넛!!"
        ]
        return random.choice(foods)

    # 일반적인 음식 관련 단어들
    food_words = ["맛있", "맛없", "배고파", "배불러", "먹고싶", "달달"]
    if any(word in msg for word in food_words):
        return random.choice([
            "저도 먹고 싶어요",
            "맛있겠네요",
            "배고프시나봐요",
            "뭘 드실 건가요?"
        ])
    return None


def check_study_mention(msg):
    """공부 관련"""
    study_words = ["시험", "과제", "공부", "숙제", "발표", "프로젝트"]
    if any(word in msg for word in study_words):
        return random.choice([
            "화이팅하세요!",
            "열심히 하시네요",
            "공부 힘들죠",
            "파이팅!"
        ])
    return None
