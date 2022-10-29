from playsound import playsound
import time
def speak_secnario(num, user_id=0):
    if num == '1':
        playsound("STT/tts_audio/1.mp3")
        #playsound("STT/tts_audio/1-1.mp3") #안녕하세요. 스누비 마트에 오신 것을 환영합니다.
        #playsound("STT/tts_audio/1-2.mp3") #저는 스누비 마트의 마스코트. 누비,입니다.
        #playsound("STT/tts_audio/1-3.mp3") #얼굴이 드러나게, 가까이 와 주세요.
    elif num == '2':
        if user_id == 1:
            playsound("STT/tts_audio/2-1-1.mp3") #반갑습니다 준오님 오늘도 방문해주셔서 감사합니다_
        elif user_id == 2:
            playsound("STT/tts_audio/2-1-2.mp3") #반갑습니다 예솔님 오늘도 방문해주셔서 감사합니다_
        elif user_id == 3:
            playsound("STT/tts_audio/2-1-3.mp3")  # 반갑습니다 예솔님 오늘도 방문해주셔서 감사합니다_
        else: # user_id == 0:
            playsound("STT/tts_audio/2-1-0.mp3") #반갑습니다 회원님 오늘도 방문해주셔서 감사합니다_
        playsound("STT/tts_audio/2-2.mp3") #상품 계산을 시작하겠습니다.
    elif num == '3-1':
        playsound("STT/tts_audio/3-1.mp3") #벨트 위에 물건을 차례차례 올려주세요!
    elif num == '3-2':
        playsound("STT/tts_audio/3-2.mp3") #손상되기 쉬운 물건은, 나중에 넣을게요!
    elif num == '3-3':
        playsound("STT/tts_audio/3-3.mp3") #죄송합니다. 유통기한이 지난 상품이네요. 이건 제가 수거하도록 하겠습니다!
    elif num == '3-4':
        playsound("STT/tts_audio/3-4.mp3") #더 이상 구매하실 물건이 없으신가요?
    elif num == '3-5':
        playsound("STT/tts_audio/3-5.mp3") #빼 두었던 상품을 넣겠습니다.
    elif num == '4':
        playsound("STT/tts_audio/4.mp3")
        #time.sleep(1)
        #playsound("STT/tts_audio/4-1.mp3") #오늘 구매하시는 물건의 총액은 다음과 같네요!
        #playsound("STT/tts_audio/4-2.mp3") #등록된 결제 정보를 화면에서 확인해 주세요!
        #time.sleep(1.5)
        #playsound("STT/tts_audio/4-3.mp3") #해당 결제 정보로, 결제를 진행하겠습니다.
        #time.sleep(3)
        #playsound("STT/tts_audio/4-4.mp3") #계산이 모두 완료되었습니다! 장바구니를 받아주세요!
    elif num == '5':
        playsound("STT/tts_audio/5.mp3")
        #playsound("STT/tts_audio/mute_0_5sec.mp3")
        #playsound("STT/tts_audio/5-1.mp3") #오늘도 스누비 마트를 이용해 주셔서 감사합니다.
        #playsound("STT/tts_audio/5-2.mp3") #행복한 하루 보내세요!


