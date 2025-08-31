from konlpy.tag import Okt
import numpy as np
import speech_recognition as sr
import pyttsx3 as tts
import webbrowser
import time
import threading
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
                                webbrowser.open(f"https://geota.co.kr/gersang/satongpaldal?keyword={keywords}")
                                flag = False
                            else:
                                speak(f"거타 사통팔달 {key} 서버를 {keywords} 실행합니다.")
                                time.sleep(0.3)
                                webbrowser.open(f"https://geota.co.kr/gersang/satongpaldal?serverId={serverId}&keyword={keywords}")
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
                                webbrowser.open(f"https://geota.co.kr/gersang/yukeuijeon&itemName={keywords}&orderDirection=asc&page=1")
                                flag = False
                            else:
                                speak(f"거타 육의전 {key} 서버 {keywords}를 실행합니다.")
                                time.sleep(0.3)
                                webbrowser.open(f"https://geota.co.kr/gersang/yukeuijeon?serverId={serverId}&itemName={keywords}&orderDirection=asc&page=1")
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