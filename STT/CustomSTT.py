import sounddevice as sd
import numpy as np
from beepy import beep
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import librosa
import pyaudio
import wave


def extract_feature(file_name):
    max_pad_len = 129
    audio, sample_rate = librosa.load(file_name, res_type='kaiser_fast')
    mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
    pad_width = max_pad_len - mfccs.shape[1]
    mfccs = np.pad(mfccs, pad_width=((0, 0), (0, pad_width)), mode='constant')
    return mfccs

class VoiceDataset(Dataset):
    def __init__(self, df):
        self.df = df

    def __len__(self):
        return len(self.df.index)

    def __getitem__(self, idx):
        file_idx = self.df.iloc[idx]['file_idx']
        label = self.df.iloc[idx]['label']
        mfcc_np = extract_feature('voice_wav/'+str(file_idx)+'.wav')
        voice_tensor = torch.from_numpy(mfcc_np).float()
        return voice_tensor, label

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.input_size = 129 * 40
        self.fc1 = nn.Linear(self.input_size, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 2)

    def forward(self, x):
        x = x.view(x.shape[0], -1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


def train(model, train_loader, optimizer):
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        # 학습 데이터를 DEVICE의 메모리로 보냄
        print('target', target)
        data, target = data.to(DEVICE), target.to(DEVICE)
        optimizer.zero_grad()
        output = model(data)
        loss = F.cross_entropy(output, target)
        loss.backward()
        optimizer.step()


# ## 테스트하기

def evaluate(model, test_loader):
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:

            data, target = data.to(DEVICE), target.to(DEVICE)
            output = model(data)

            # 모든 오차 더하기
            test_loss += F.cross_entropy(output, target,
                                         reduction='sum').item()

            # 가장 큰 값을 가진 클래스가 모델의 예측입니다.
            # 예측과 정답을 비교하여 일치할 경우 correct에 1을 더합니다.
            pred = output.max(1, keepdim=True)[1]
            correct += pred.eq(target.view_as(pred)).sum().item()
    test_loss /= len(test_loader.dataset)
    test_accuracy = 100. * correct / len(test_loader.dataset)
    return test_loss, test_accuracy


if __name__ == '__main__':
    USE_CUDA = torch.cuda.is_available()
    DEVICE = torch.device("cuda" if USE_CUDA else "cpu")
    train_df = pd.read_csv('train_df.csv')
    test_df = pd.read_csv('test_df.csv')

    training_data = VoiceDataset(train_df)
    test_data = VoiceDataset(test_df)

    train_loader = DataLoader(training_data, batch_size=5, shuffle=True)
    test_loader = DataLoader(test_data, batch_size=5, shuffle=True)

    model = Net().to(DEVICE)
    optimizer = optim.Adam(model.parameters(), lr=0.0001)


    for epoch in range(1, 10):
        train(model, train_loader, optimizer)
        test_loss, test_accuracy = evaluate(model, test_loader)

        print('[{}] Test Loss: {:.4f}, Accuracy: {:.2f}%'.format(
            epoch, test_loss, test_accuracy))

    idx = 0
    softmax = nn.Softmax(dim=1)
    while True:
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        CHUNK = 1024
        RECORD_SECONDS = 3

        WAVE_OUTPUT_FILENAME = "file.wav"

        audio = pyaudio.PyAudio()

        # start Recording
        stream = audio.open(format=pyaudio.paInt16,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            input_device_index=1,
                            frames_per_buffer=CHUNK)

        print("recording...")
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("finished recording")
        # stop Recording
        stream.stop_stream()
        stream.close()
        audio.terminate()
        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()

        mfcc_np = extract_feature(WAVE_OUTPUT_FILENAME)
        test_tensor = torch.from_numpy(mfcc_np).float()
        test_tensor = test_tensor.unsqueeze(dim=0).to(DEVICE)
        output = model(test_tensor)
        output = softmax(output)
        idx += 1


        print(idx, output, output.argmax().item())
