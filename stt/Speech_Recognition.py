import json
import requests


def stt(audio_file):
    Lang = "Kor" # Kor / Jpn / Chn / Eng
    URL = "https://naveropenapi.apigw.ntruss.com/recog/v1/stt?lang=" + Lang
        
    ID = "25rj9cxxg9" # 인증 정보의 Client ID
    Secret = "cRelYN0orvwQIjYbRct1AiLqZqffiNonv0n2Cv5V" # 인증 정보의 Client Secret
        
    headers = {
        "Content-Type": "application/octet-stream", # Fix
        "X-NCP-APIGW-API-KEY-ID": ID,
        "X-NCP-APIGW-API-KEY": Secret,
    }

    data = open(audio_file, "rb") # STT를 진행하고자 하는 음성 파일

    print("Request STT")
    response = requests.post(URL,  data=data, headers=headers) #CRS 요청(speech to text)
    print("STT Complete")
    rescode = response.status_code

    # if(rescode == 200): # 정상 작동이라면 출력
    #     print (response.text)
    # else:
    #     print("Error : " + response.text)

    data.close()

    return response.json() #json 파일로 전달