from playsound import playsound

def speak_secnario(num):
    if num == '1':
        playsound("stt/tts_audio/1.mp3") #01_안녕하세요_스누비마트에_오신_것을_환영합니다____저는_스누비마트의_마스코트_누비입
    elif num == '2':
        playsound("stt/tts_audio/2.mp3") #02_벨트_위에_물건을_차례차례_올려주세요
    elif num == '3':
        playsound("stt/tts_audio/3.mp3") #03_깨지기_쉬운_계란은_나중에_넣을게요.mp3
    elif num == '4':
        playsound("stt/tts_audio/4.mp3") #04_더_이상_구매하실_물건이_없나요_
    elif num == '5':
        playsound("stt/tts_audio/5.mp3") #05_오늘_구매하시는_물건의_총액은_다음과_같네요_미리_등록해두신_결제_정보로_결제를_진행해
    elif num == '6':
        playsound("stt/tts_audio/6.mp3") #07_계산이_모두_완료되었습니다_장바구니를_받아주세요
    elif num == '7':
        playsound("stt/tts_audio/7.mp3") #08_오늘도_스누비마트를_이용해주셔서_감사합니다_행복한_하루_보내세요



