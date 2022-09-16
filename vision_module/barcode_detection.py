from pyzbar import pyzbar
import cv2

i = 20
index = 0
arr = []
while i >0:
    cap = cv2.VideoCapture(index)
    if cap.read()[0]:
        arr.append(index)
        cap.release()
    index +=1
    i -= 1
print(arr)

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)

while True:
    ret, image = capture.read()
    # 이미지에서 바코드를 찾고 각 바코드를 디코드한다.
    barcodes = pyzbar.decode(image)
    print(barcodes)


    for barcode in barcodes:
        (x, y, w, h) = barcode.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        # 바코드 데이터와 타입을 이미지에 그림
        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 0, 255), 2)

    # 바코드타입과 데이터를 터미널에 출력
    try:
        print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
    except Exception as e:
        pass
    cv2.imwrite('example.png', image)
    cv2.imshow("Image", image)
    cv2.waitKey(1)