from konlpy.tag import Okt
from selenium import webdriver
import numpy as np
import speech_recognition as sr
import pyttsx3 as tts
import webbrowser
import time
import threading
import shutil
# ✅ Recognizer 인식기 초기화
recognizer = sr.Recognizer()
server_list = {
    "백호": 1,
    "주작": 2,
    "현무": 3,
    "청룡": 4,
    "봉황": 5,
    "해태": 6,
    "세종": 7,
    "신구": 8,
    "단군": 9,
    "비호": 10,
    "태극": 11,
    "화랑": 12,
    "태왕": 13
}

okt = Okt()
driver = webdriver.Chrome()

def transcribe_audio(audio, sr_rate=16000):
    try:
        # numpy array  → bytes 변환
        audio_bytes = (audio * 32767).astype(np.int16).tobytes()
        
        # AudioData 객체로 감싸기
        audio_data = sr.AudioData(audio_bytes, sr_rate, 2)
        
        text = recognizer.recognize_google(audio_data, language="ko-KR")
        
        return text
    except sr.UnknownValueError:
        print("Can't not understand audio. 😢")
    except sr.RequestError as e:
        print(f"Faild to request Google Speech Recognition service: {e}")


def searching_title_substring(text):
    keywords = ["사통", "사통팔달", "육전", "육의전", "검색", "해줘", "줘", "서버"]
    
    # 형태소 분석
    tokens = okt.morphs(text)
    filtered_tokens = [word for word in tokens]
    cleaned_text = ''.join(filtered_tokens)
    if any(keyword in cleaned_text for keyword in keywords):
        for keyword in keywords:
            for key in server_list.keys():
                if key in cleaned_text:
                    cleaned_text = cleaned_text.replace(key, "")
            cleaned_text = cleaned_text.replace(keyword, "")
        
    return cleaned_text

def calcul_mercenary(text):
    keywords = ["용병제작", "서버"]
    
    tokens = okt.morphs(text)
    filtered_tokens = [word for word in tokens]
    cleaned_text = ''.join(filtered_tokens)        
    if any(keyword in cleaned_text for keyword in keywords):
        for keyword in keywords:
            for key in server_list.keys():
                if key in cleaned_text:
                    cleaned_text = cleaned_text.replace(key, "")
            cleaned_text = cleaned_text.replace(keyword, "")
    if "각성" in cleaned_text:
        cleaned_text = cleaned_text.replace("각성", "각성+")
    if "바지라오" in cleaned_text:
        cleaned_text = cleaned_text.replace("재상", "재상+바지라오")
    if "화목란" in cleaned_text:
        cleaned_text = cleaned_text.replace("여걸", "여걸+화목란")
    if "초선" in cleaned_text:
        cleaned_text = cleaned_text.replace("무희", "무희+초선")
    if "마조" in cleaned_text:
        cleaned_text = cleaned_text.replace("해신", "해신+마조")
    if "홍길동" in cleaned_text:
        cleaned_text = cleaned_text.replace("도사", "도사+홍길동")
    if "노부츠나" in cleaned_text:
        cleaned_text = cleaned_text.replace("군신", "군신+노부츠나")
    if "주몽" in cleaned_text:
        cleaned_text = cleaned_text.replace("신궁", "신궁+주몽")
    if "맹획" in cleaned_text:
        cleaned_text = cleaned_text.replace("야왕", "야왕+맹획")
    if "최무선" in cleaned_text:
        cleaned_text = cleaned_text.replace("도령", "도령+최무선")
    if "악바르" in cleaned_text:
        cleaned_text = cleaned_text.replace("악바르", "악바르+대제")
    if "여포" in cleaned_text:
        cleaned_text = cleaned_text.replace("봉선", "봉선+여포")
    if "모치츠키" in cleaned_text:
        cleaned_text = cleaned_text.replace("치요메", "모치츠키+치요메")
    if "만선야" in cleaned_text:
        cleaned_text = cleaned_text.replace("선인", "선인+만선야")
    if  "보쿠텐" in cleaned_text:
        cleaned_text = cleaned_text.replace("보쿠텐", "검성+보쿠텐")
    if "레지나" in cleaned_text:
        cleaned_text = cleaned_text.replace("레지나", "레지나+술타나")
    if "기린" in cleaned_text:
        cleaned_text = cleaned_text.replace("기린", "신수+기린")
    if "현무" in cleaned_text:
        cleaned_text = cleaned_text.replace("현무", "신수+현무")
    if "백호" in cleaned_text:
        cleaned_text = cleaned_text.replace("백호", "신수+백호")
    if "주작" in cleaned_text:
        cleaned_text = cleaned_text.replace("주작", "신수+주작")
    if "아이라바타" in cleaned_text:
        cleaned_text = cleaned_text.replace("아이라바타", "신수+아이라바타")
    if "도철" in cleaned_text:
        cleaned_text = cleaned_text.replace("도철", "고용+도철")
    if "도을" in cleaned_text:
        cleaned_text = cleaned_text.replace("도을", "고용+도을")
    if "혼돈" in cleaned_text:
        cleaned_text = cleaned_text.replace("혼돈", "고용+혼돈")
    if "궁기" in cleaned_text:
        cleaned_text = cleaned_text.replace("궁기", "고용+궁기")
    if "각도을" in cleaned_text:
        cleaned_text = cleaned_text.replace("각도을", "각성+도을")
    if "각도철" in cleaned_text:
        cleaned_text = cleaned_text.replace("각도철", "각성+도철")
    if "각혼돈" in cleaned_text:
        cleaned_text = cleaned_text.replace("각혼돈", "각성+혼돈")
    if "각궁기" in cleaned_text:
        cleaned_text = cleaned_text.replace("각궁기", "각성+궁기")
    if "광목" in cleaned_text:
        cleaned_text = cleaned_text.replace("광목", "광목천왕")
    if "다문" in cleaned_text:
        cleaned_text = cleaned_text.replace("다문", "다문천왕")
    if "증장" in cleaned_text:
        cleaned_text = cleaned_text.replace("증장", "증장천왕")
    if "지국" in cleaned_text:
        cleaned_text = cleaned_text.replace("지국", "지국천왕")
    if "각광목" in cleaned_text:
        cleaned_text = cleaned_text.replace("각광목", "각성+광목천왕")
    if "각다문" in cleaned_text:
        cleaned_text = cleaned_text.replace("각다문", "각성+다문천왕")
    if "각증장" in cleaned_text:
        cleaned_text = cleaned_text.replace("각증장", "각성+증장천왕")
    if "각지국" in cleaned_text:
        cleaned_text = cleaned_text.replace("각지국", "각성+지국천왕")
    if "부동" in cleaned_text:
        cleaned_text = cleaned_text.replace("부동", "부동명왕")
    if "대위덕" in cleaned_text:
        cleaned_text = cleaned_text.replace("대위덕", "대위덕명왕")
    if "군다리" in cleaned_text:
        cleaned_text = cleaned_text.replace("군다리", "군다리명왕")
    if "항삼" in cleaned_text:
        cleaned_text = cleaned_text.replace("항삼", "항삼세명왕")
    if "야차" in cleaned_text:
        cleaned_text = cleaned_text.replace("야차", "금강야차명왕")
    return cleaned_text
    
def speak(text):
    def run():
        engine = tts.init()
        engine.say(text)
        engine.runAndWait()

    # 음성 합성은 별도의 스레드에서 실행
    t = threading.Thread(target=run, daemon=True)
    t.start()
    t.join()  # 음성 합성이 끝날 때까지 기다림
     
if __name__ == "__main__":
    mic = sr.Microphone()
    while True:
        with mic as source:
            recognizer.energy_threshold = 200
            recognizer.dynamic_energy_threshold = True
            recognizer.pause_threshold = 1.2
            recognizer.phrase_threshold = 0.2 
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, phrase_time_limit=3)
            
            try:
                
                text = recognizer.recognize_google(audio, language="ko-KR").replace(" ", "")
                print("Recognized Text :", text)
                flag = True
                if "거울" in text:
                    speak("네 거상 관련 도우미 거울이 입니다. 무엇을 도와드릴까요?")
                    while flag:
                        subAudio = recognizer.listen(source, timeout=5, phrase_time_limit=15)
                        subText = recognizer.recognize_google(subAudio, language="ko-KR").replace(" ", "")
                        print("Sub Recognized Text :", subText)
                        if ("사통" in subText or "사통팔달" in subText):
                            serverId = 0
                            for key in server_list.keys():
                                if key in subText:
                                    serverId = server_list[key]
                                    break
                                
                            keywords = searching_title_substring(subText.replace(" ", ""))
                            if serverId == 0:
                                
                                speak(f"거타 사통팔달 메뉴 {keywords}를 실행합니다.")
                                print("")
                                time.sleep(0.3)
                                driver.get(f"https://geota.co.kr/gersang/satongpaldal?keyword={keywords}")
                                flag = False
                            else:
                                speak(f"거타 사통팔달 {key} 서버를 {keywords} 실행합니다.")
                                time.sleep(0.3)
                                driver.get(f"https://geota.co.kr/gersang/satongpaldal?serverId={serverId}&keyword={keywords}")
                                flag = False
                        elif "육전" in subText or "육의전" in subText:
                            serverId = 0
                            for key in server_list.keys():
                                if key in subText:
                                    serverId = server_list[key]
                                    break
                            keywords = searching_title_substring(subText.replace(" ", ""))
                            if serverId == 0:
                                
                                speak(f"거타 육의전 메뉴 {keywords}를 실행합니다.")
                                print("")
                                time.sleep(0.3)
                                driver.get(f"https://geota.co.kr/gersang/yukeuijeon&itemName={keywords}&orderDirection=asc&page=1")
                                flag = False
                            else:
                                speak(f"거타 육의전 {key} 서버 {keywords}를 실행합니다.")
                                time.sleep(0.3)
                                driver.get(f"https://geota.co.kr/gersang/yukeuijeon?serverId={serverId}&itemName={keywords}&orderDirection=asc&page=1")
                                flag = False
                        elif "용병제작" in subText or "용제" in subText:
                            serverId = 0
                            for key in server_list.keys():
                                if key in subText:
                                    serverId = server_list[key]
                                    break
                            keywords = calcul_mercenary(subText)
                            if serverId == 0:
                                
                                speak(f"거타 용병 제작 계산기 메뉴 {keywords}를 실행합니다.")
                                print("")
                                time.sleep(0.3)
                                driver.get(f"https://geota.co.kr/gersang/calculator/mercenary?keyword={keywords}")
                                flag = False
                            else:
                                speak(f"거타 용병 제작 계산기 {key} 서버 {keywords}를 실행합니다.")
                                time.sleep(0.3)
                                driver.get(f"https://geota.co.kr/gersang/calculator/mercenary?serverId={serverId}&keyword={keywords}")
                                flag = False
                        elif "종료" in subText or "그만" in subText or "끝" in subText:
                            speak("도움이 필요하시면 언제든지 불러주세요. 안녕히 계세요!")
                            flag = False
                            exit(0)
                        else:
                            speak("다시 말씀해 주세요.")
                            flag = True
                        
                            
                                 
                                
                        
            except sr.UnknownValueError:
                print("😅 Failed to Recognition (noize or uncertain utterance)")
            except sr.RequestError as e:
                print("Failed to request Error:", e)