from modules.weather import get_weather_api
from modules.memory import message_memory
from message.friends import check_friends_message
from message.graduate import check_graduate_message
from message.admin import check_admin_message
from message.cry_laugh_stress import check_cry_laugh_stress_message
from message.meme import check_meme_message
from datetime import datetime, timedelta
import re
import random


class MessageHandler:
    def __init__(self):
        self.bot_state = {
            'ailaCount': {},
            'yoshiCount': {},
            'isActive': True,
            'isSilent': False,
            'silentUntil': None
        }

    def process_message(self, msg, sender, room):
        """메시지 처리 메인 함수"""

        # 관리자 명령어 먼저 체크
        admin_response = check_admin_message(msg, sender, self.bot_state)
        if admin_response:
            return admin_response

        # 봇이 비활성화된 경우
        if not self.bot_state['isActive']:
            return None

        # 조용 상태 체크 및 해제
        if self._is_silent():
            # 침묵 해제 명령어만 처리
            if self._is_unsilence_command(msg):
                print(f"🔊 조용 해제 명령어 감지: '{msg}' from {sender}")
                self.bot_state['isSilent'] = False
                self.bot_state['silentUntil'] = None
                return "다시 대답하겠다"
            return None  # 침묵 중이면 아무 응답 안함

        # 조용히 해 명령어 체크 (개선된 버전)
        if self._is_silence_command(msg):
            print(f"🔇 조용 명령어 감지: '{msg}' from {sender}")
            return self._make_silent()

        # 메모리 기능 체크 (우선순위 높음)
        memory_response = message_memory(msg, room, sender)
        if memory_response:
            return memory_response

        # 특별한 상태 관리가 필요한 메시지들 (아일라, 요시)
        special_response = self._handle_special_messages(msg, sender)
        if special_response:
            return special_response

        # 각 message 모듈에서 순차적으로 체크
        # 우선순위: 친구 > 졸업 > 밈 > 감정

        # 친구 이름 체크
        friends_response = check_friends_message(msg)
        if friends_response:
            return friends_response

        # 졸업/전역 관련 체크
        graduate_response = check_graduate_message(msg)
        if graduate_response:
            return graduate_response

        # 밈 응답 체크
        meme_response = check_meme_message(msg)
        if meme_response:
            return meme_response

        # 감정 응답 체크
        emotion_response = check_cry_laugh_stress_message(msg)
        if emotion_response:
            return emotion_response

        # 6. 기본 메시지 체크 (하드코딩된 응답들)
        basic_response = self._handle_basic_messages(msg)
        if basic_response:
            return basic_response

        return None  # 처리할 수 없는 메시지

    def _is_silent(self):
        """조용 상태 확인"""
        if not self.bot_state['isSilent']:
            return False

        if self.bot_state['silentUntil'] is None:
            return False

        # 조용 시간이 지났는지 확인
        if datetime.now() > self.bot_state['silentUntil']:
            self.bot_state['isSilent'] = False
            self.bot_state['silentUntil'] = None
            return False

        return True

    def _is_silence_command(self, msg):
        """조용 명령어인지 확인 (개선된 버전)"""
        # 다양한 조용 명령어 패턴들
        silence_patterns = [
            r'조용.*해',  # 조용해, 조용히해, 조용히 해
            r'조용',      # 조용
            r'닥쳐',      # 닥쳐, 닥쳐라
            r'시끄러',    # 시끄러워, 시끄럽다
            r'입.*닥쳐',  # 입 닥쳐
            r'그만.*말해', # 그만 말해
            r'조용히',    # 조용히
            r'쉿',        # 쉿
            r'조용.*좀',  # 조용 좀
            r'말.*그만',  # 말 그만
            r'shut.*up',  # shut up (영어)
        ]
        
        # 대소문자 구분 없이 체크
        msg_lower = msg.lower()
        
        for pattern in silence_patterns:
            if re.search(pattern, msg_lower):
                return True
        
        return False

    def _is_unsilence_command(self, msg):
        """조용 모드 해제 명령어인지 확인"""
        # 다양한 조용 해제 명령어 패턴들
        unsilence_patterns = [
            r'말해',      # 말해, 말해줘
            r'대답해',    # 대답해, 대답해줘
            r'말하라',    # 말하라
            r'다시.*말',  # 다시 말해
            r'돌아와',    # 돌아와
            r'활동.*시작', # 활동 시작
            r'그만.*조용', # 그만 조용
            r'조용.*그만', # 조용 그만
            r'다시.*활동', # 다시 활동
            r'wake.*up',  # wake up (영어)
            r'come.*back', # come back (영어)
        ]
        
        # 대소문자 구분 없이 체크
        msg_lower = msg.lower()
        
        for pattern in unsilence_patterns:
            if re.search(pattern, msg_lower):
                return True
        
        return False

    def _make_silent(self):
        """조용 모드 설정"""
        self.bot_state['isSilent'] = True
        self.bot_state['silentUntil'] = datetime.now() + timedelta(minutes=10)
        
        # 다양한 조용 응답들
        silence_responses = [
            "10분 동안 조용히 한다",
            "알겠다. 10분 동안 조용히 있겠다",
            "🤐 10분간 침묵 모드",
            "조용히 할게... 10분 후에 다시 말하겠다",
            "😴 10분 동안 조용...",
        ]
        
        return random.choice(silence_responses)

    def _handle_basic_messages(self, msg):
        """기본 메시지 처리 (하드코딩된 응답들)"""

        # 🔥 도움말 기능 추가 (최우선 처리)
        help_keywords = ["help", "Help",
                         "HELP", "도움말", "도움", "사용법", "명령어", "기능"]
        if any(keyword in msg.lower() for keyword in help_keywords):
            return self._get_help_message()

        # 🔥 날씨 관련 처리 - 지역별 지원
        weather_keywords = ["날씨", "기온", "온도", "바람", "습도"]
        if any(keyword in msg for keyword in weather_keywords):
            from modules.weather import get_weather_api
            return get_weather_api(msg)  # 메시지 전체를 전달

        # 또는 더 구체적으로 처리하고 싶다면:
        if "날씨" in msg:
            from modules.weather import get_weather_api
            return get_weather_api(msg)

        if "포항 날씨" in msg:
            from modules.weather import get_pohang_weather
            return get_pohang_weather()

        if "서울 날씨" in msg:
            from modules.weather import get_seoul_weather
            return get_seoul_weather()

        if "부산 날씨" in msg:
            from modules.weather import get_busan_weather
            return get_busan_weather()

        if msg == "KHH":
            return "크하학 크하학"

        # 🔥 학식 관련 - 대학 구분 추가
        if msg == "학식":
            # 기본값은 포항공대
            from modules.postech_meal import get_postech_meal
            return get_postech_meal()

        # 포항공대 학식
        if msg == "포항공대 학식" or msg == "포스텍 학식" or msg == "postech 학식":
            from modules.postech_meal import get_postech_meal
            return get_postech_meal()

        if msg == "포항공대 아침" or msg == "포스텍 아침":
            from modules.postech_meal import get_postech_meal
            return get_postech_meal("아침")

        if msg == "포항공대 점심" or msg == "포스텍 점심":
            from modules.postech_meal import get_postech_meal
            return get_postech_meal("점심")

        if msg == "포항공대 저녁" or msg == "포스텍 저녁":
            from modules.postech_meal import get_postech_meal
            return get_postech_meal("저녁")

        # 중앙대 학식
        # _handle_basic_messages 함수에서 "중학" 부분 수정:

        if msg == "중학":
            from modules.cau_meal import CAUMealAPI
            from datetime import datetime

            api = CAUMealAPI()
            current_hour = datetime.now().hour

            # 시간대별 자동 식사 타입 결정
            if 6 <= current_hour < 10:
                meal_type = '조식'
            elif 10 <= current_hour < 15:
                meal_type = '중식'
            elif 15 <= current_hour < 21:
                meal_type = '석식'
            else:
                meal_type = '중식'  # 기본값

            # 서울캠퍼스
            seoul_result = api.get_meal_data(campus='서울', meal_type=meal_type)
            seoul_formatted = api.format_meal_output(seoul_result)

            return seoul_formatted

        if msg == "다학":
            from modules.cau_meal import CAUMealAPI
            from datetime import datetime

            api = CAUMealAPI()
            current_hour = datetime.now().hour

            # 시간대별 자동 식사 타입 결정
            if 6 <= current_hour < 10:
                meal_type = '조식'
            elif 10 <= current_hour < 15:
                meal_type = '중식'
            elif 15 <= current_hour < 21:
                meal_type = '석식'
            else:
                meal_type = '중식'  # 기본값

            # 안성캠퍼스
            anseong_result = api.get_meal_data(
                campus='안성', meal_type=meal_type)
            anseong_formatted = api.format_meal_output(anseong_result)

            return anseong_formatted

        if msg == "중앙대 학식" or msg == "CAU 학식" or msg == "cau 학식":
            from modules.cau_meal import CAUMealAPI
            api = CAUMealAPI()
            result = api.get_meal_data(campus='서울', meal_type='중식')
            return api.format_meal_output(result)

        if msg == "중앙대 점심" or msg == "중앙대 중식":
            from modules.cau_meal import CAUMealAPI
            api = CAUMealAPI()
            result = api.get_meal_data(campus='서울', meal_type='중식')
            return api.format_meal_output(result)

        if msg == "중앙대 저녁" or msg == "중앙대 석식":
            from modules.cau_meal import CAUMealAPI
            api = CAUMealAPI()
            result = api.get_meal_data(campus='서울', meal_type='석식')
            return api.format_meal_output(result)

        if msg == "중앙대 조식" or msg == "중앙대 아침":
            from modules.cau_meal import CAUMealAPI
            api = CAUMealAPI()
            result = api.get_meal_data(campus='서울', meal_type='조식')
            return api.format_meal_output(result)

        # 안성캠퍼스
        if msg == "다빈치 조식" or msg == "다빈치 아침":
            from modules.cau_meal import CAUMealAPI
            api = CAUMealAPI()
            result = api.get_meal_data(campus='안성', meal_type='조식')
            return api.format_meal_output(result)

        if msg == "다빈치 중식" or msg == "다빈치 점심":
            from modules.cau_meal import CAUMealAPI
            api = CAUMealAPI()
            result = api.get_meal_data(campus='안성', meal_type='중식')
            return api.format_meal_output(result)

        if msg == "다빈치 석식" or msg == "다빈치 저녁":
            from modules.cau_meal import CAUMealAPI
            api = CAUMealAPI()
            result = api.get_meal_data(campus='안성', meal_type='석식')
            return api.format_meal_output(result)

        # 기존 단순 명령어들 (기본값은 포항공대)

        if msg == "아침":
            from modules.postech_meal import get_postech_meal
            return get_postech_meal("아침")
        if msg == "점심":
            from modules.postech_meal import get_postech_meal
            return get_postech_meal("점심")
        if msg == "저녁":
            from modules.postech_meal import get_postech_meal
            return get_postech_meal("저녁")

        return None

    def _get_help_message(self):
        """도움말 메시지 반환"""
        help_text = """    🤖 크하학 봇 사용법

    📱 GitHub: https://github.com/khh-chatbot/khh-chatbot-api

    🍱 학식 정보:
    • 학식 / 중학 / 다학

    🌤️ 날씨 정보:
    • 날씨 / 포항 날씨 / 서울 날씨 / 부산 날씨

    🧠 메모리 기능:
    • !기억 내용 (방별 메모 저장)
    • 뭐였지? (방별 메모 조회)
    • !삭제 방별 / !삭제 개인

    ⏰ 리마인드:
    • !리마인드 내일 14:30 회의
    • !리마인드 오늘 18:00 약속

    🎭 특별 기능:
    • 친구 이름 언급하면 개별 응답

    더 궁금하면 GitHub에서 확인하세요!"""

        return help_text

    def _handle_special_messages(self, msg, sender):
        """상태 관리가 필요한 특별한 메시지들"""

        # 아일라 처리 (카운팅 필요)
        if "아일라" in msg:
            if sender not in self.bot_state['ailaCount']:
                self.bot_state['ailaCount'][sender] = 0

            self.bot_state['ailaCount'][sender] += 1

            if self.bot_state['ailaCount'][sender] == 1:
                return "러닝 하러 가자"
            elif self.bot_state['ailaCount'][sender] == 2:
                weather_info = get_weather_api()
                self.bot_state['ailaCount'][sender] = 0
                return f"러닝을 가기 위한 날씨\n {weather_info}\n"

        # 요시 처리 (카운팅 필요)
        if "요시" in msg:
            if sender not in self.bot_state['yoshiCount']:
                self.bot_state['yoshiCount'][sender] = 0

            self.bot_state['yoshiCount'][sender] += 1

            if self.bot_state['yoshiCount'][sender] >= 3:
                return "요시가 화났다!!!(하하)"
            else:
                return "또 이상한 거 만드셨네.."

        return None
