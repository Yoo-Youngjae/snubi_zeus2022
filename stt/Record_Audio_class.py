import pyaudio
import wave

class Record_Audio:
    def __init__(self):
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.RECORD_SECONDS = 15  # 마이크 입력 시간
        # WAVE_OUTPUT_FILENAME = "output.wav"
        # MP3_OUTPUT_FILENAME = "ouput.mp3"

        self.p = pyaudio.PyAudio()
        #129.19921875
        self.time = self.RATE / self.CHUNK * self.RECORD_SECONDS
        # 클래스화
        self.stream = self.p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)
    def start(self, wave_file):
        print("Start to record the audio.")

        frames = []
        print(self.time)
        for i in range(0, int(self.time)): #설정된 시간만큼 녹음
            data = self.stream.read(self.CHUNK)
            frames.append(data)
            print(i)

        print("Recording is finished.")

        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

        # wf = wave.open("D:\python files\Rbiz\STT/audio_data/"+WAVE_OUTPUT_FILENAME, 'wb')
        wf = wave.open(wave_file, 'wb') # 녹음 데이터 wav로 저장
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(frames))
        wf.close()