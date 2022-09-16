from playsound import playsound

def Speak_Secnario(num):
    if num == '1':
        playsound("/home/snubi/PycharmProjects/snubi_zeus2022/stt/tts_audio/안녕하세요+준오님_+BI+마트에+오신걸+환영합니다_+저는+결제를+도와드릴+누비입니다_.mp3")
    elif num == '4':
        playsound("/home/snubi/PycharmProjects/snubi_zeus2022/stt/tts_audio/셀프+계산대에+상품을+올려놓으시면%2C+결제를+도와드리겠습니다_+.mp3")
    elif num == '5_2':
        playsound("/home/snubi/PycharmProjects/snubi_zeus2022/stt/tts_audio/계산+목록을+확인해주시면+결제를+진행해드리겠습니다_.mp3")
        playsound("/home/snubi/PycharmProjects/snubi_zeus2022/stt/tts_audio/결제를+진행하시겠습니까_.mp3")
    elif num == '5_3':
        playsound("/home/snubi/PycharmProjects/snubi_zeus2022/stt/tts_audio/계산+및+포인트+적립이+완료+되었습니다_.mp3")
    elif num == '6':
        playsound("/home/snubi/PycharmProjects/snubi_zeus2022/stt/tts_audio/장바구니+챙겨+가시기+바랍니다_+.mp3")
        playsound("/home/snubi/PycharmProjects/snubi_zeus2022/stt/tts_audio/좋은+하루+되세요!.mp3")
    elif num == '5_2_n':
        playsound("/home/snubi/PycharmProjects/snubi_zeus2022/stt/tts_audio/장바구니에서+상품을+다시+한번+확인해주시기+바랍니다_.mp3")




