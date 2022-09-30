import cv2
import numpy as np
import scipy.fftpack  # For FFT2
from PIL import Image

image_name = '/home/snubi/PycharmProjects/snubi_zeus2022/logistics_paper/test_image/3.png'
# img = Image.open(image_name)
img = cv2.imread(image_name)
img_YUV = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
# cv2.imshow('img_YUV', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

print(img_YUV.shape)
y = img_YUV[:, :, 0]

rows = y.shape[0]
cols = y.shape[1]

imgLog = np.log1p(np.array(y, dtype='float') / 255)  # y���� 0~1���̷� ������ �� log(x+1)

M = 2 * rows + 1
N = 2 * cols + 1

### gaussian mask ���� sigma = 10
sigma = 10
(X, Y) = np.meshgrid(np.linspace(0, N - 1, N), np.linspace(0, M - 1, M))  # 0~N-1(and M-1) ���� 1������ space�� ����
Xc = np.ceil(N / 2)
Yc = np.ceil(M / 2)
gaussianNumerator = (X - Xc) ** 2 + (Y - Yc) ** 2

LPF = np.exp(-gaussianNumerator / (2 * sigma * sigma))
HPF = 1 - LPF

LPF_shift = np.fft.ifftshift(LPF.copy())
HPF_shift = np.fft.ifftshift(HPF.copy())

img_FFT = np.fft.fft2(imgLog.copy(), (M, N))
img_LF = np.real(np.fft.ifft2(img_FFT.copy() * LPF_shift, (M, N)))  # low frequency ����
img_HF = np.real(np.fft.ifft2(img_FFT.copy() * HPF_shift, (M, N)))  # high frequency ����

gamma1 = 0.3
gamma2 = 1.5
img_adjusting = gamma1 * img_LF[0:rows, 0:cols] + gamma2 * img_HF[0:rows, 0:cols]

img_exp = np.expm1(img_adjusting)  # exp(x) + 1
img_exp = (img_exp - np.min(img_exp)) / (np.max(img_exp) - np.min(img_exp))  # 0~1���̷� ����ȭ
img_out = np.array(255 * img_exp, dtype='uint8')

img_YUV[:, :, 0] = img_out
result = cv2.cvtColor(img_YUV, cv2.COLOR_YUV2BGR)
cv2.imshow('result', result)
cv2.waitKey(0)