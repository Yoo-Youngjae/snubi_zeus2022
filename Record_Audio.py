import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 3 #마이크 입력 시간
#WAVE_OUTPUT_FILENAME = "output.wav"
#MP3_OUTPUT_FILENAME = "ouput.mp3"


def start(WAVE_OUTPUT_FILENAME):
    p = pyaudio.PyAudio()

    # 클래스화
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Start to record the audio.")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)): #설정된 시간만큼 녹음
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording is finished.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    #wf = wave.open("D:\python files\Rbiz\STT/audio_data/"+WAVE_OUTPUT_FILENAME, 'wb')
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb') #녹음 데이터 wav로 저장
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()