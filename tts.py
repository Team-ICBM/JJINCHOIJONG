import pyttsx3

engine = pyttsx3.init() # object creation

"""
tts 관련 옵션 변경 
"""

""" RATE"""
rate = engine.getProperty('rate')   # getting details of current speaking rate
# print (rate)                        #printing current voice rate
engine.setProperty('rate', 125)     # setting up new voice rate  default is 125


# """VOLUME"""
# volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
# print (volume)                          #printing current volume level
# engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1


# """VOICE"""
# voices = engine.getProperty('voices')       #getting details of current voice
# #engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
# engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female


def textToSpeak(text: str, *args) -> None:
    """
    주어진 텍스트를 음성으로 변환합니다.
    
    Args:
        text: 기본 텍스트
        *args: tts 함수에 전달할 추가 인자들
    """
    # 모든 인자들을 문자열로 변환하여 결합
    full_text = text

    if args:
        full_text = text + " " + " ".join(str(arg) for arg in args)


    engine.say(full_text)
    engine.runAndWait()
    engine.stop()