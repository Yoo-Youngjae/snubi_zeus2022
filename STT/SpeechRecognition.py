import requests
import torch
from omegaconf import OmegaConf
from STT.silero_models.src.silero.utils import (init_jit_model,
                                                split_into_batches,
                                                read_audio,
                                                read_batch,
                                                prepare_model_input)
import numpy as np
import sounddevice as sd
from beepy import beep

class STTController:
    def __init__(self):
        self.device = torch.device('cpu')  # gpu also works, but our models are fast enough for CPU
        models = OmegaConf.load('STT/silero_models/models.yml')
        self.model, self.decoder = init_jit_model(models.stt_models.en.v3.jit, device=self.device)

    def stt(self, SEC=3, FS = 16000):
        pos_list = ['n', 'net', 'that', 'yeah']
        neg_list = ['and', 'anyour', 'anio', 'an your', 'honey',
                    'annewyork', 'anual', 'annne', 'i your', 'an',
                    'andne', 'a u', 'annual', 'annneual', 'your',
                    'and you', 'nineion', 'when you', 'a no', 'hor',
                    'anu', 'hano', 'ano', 'ananyion', 'ninee', 'ahnoor',
                    'hio', 'a your', 'hanor', 'hanio', 'anl', 'hanne',
                    'h your', 'anne', 'anuor', 'anor', 'anion', 'an u',
                    'anon', 'andyour', 'hneor', 'anneor', 'mano', 'aneo',
                    'a you', 'annu', 'nineu', 'on your', 'and your', 'a new',
                    'a knew', 'are knew', 'anewor', 'h knew', 'on you',
                    'and no', 'oh you', 'anneo', 'i knew', 'i know',
                    'i you', 'are you', 'when you\'re', 'any', 'annie', 'anie',
                    'on it']
        beep('coin')
        record = sd.rec(FS * SEC, samplerate=FS, channels=1)
        sd.wait()
        record = record * np.iinfo(np.int16).max
        record = record.astype(np.int16).flatten()
        signal = torch.from_numpy(record).to(torch.float32).to(self.device)
        signal = signal.unsqueeze(0)
        output = self.model(signal)
        result = ""
        for example in output:
            result += self.decoder(example.cpu())
        # print('[STT]', result)

        if len(result) >0 and (result[0] == 'a' or result[0] == 'i'):
            print('[STT] negative')
            return 'no'
        elif result in neg_list:
            print('[STT] negative')
            return 'no'
        else:
            print('[STT] positive')
            return 'yes'

def stt_naver(audio_file):
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
    res = response.json()['text']

    pos_list = ["예", "네", "그래", "응", "해줘", "진행해줘"]
    neg_list = ["아니", "아니요", "아니오", "아닌데", "아니야"]
    if res not in neg_list:
        print('[positive]', res)
        return 'yes'
    print('[negative]', res)
    return 'no'