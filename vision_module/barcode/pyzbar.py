import cv2
import pyzbar.pyzbar as pyzbar

font = cv2.FONT_ITALIC

def read_frame(frame):
    try:
        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            x, y, w, h = barcode.rect
            barcode_info = barcode.data.decode('utf-8')
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, barcode_info, (x, y-20), font, 0.5, (255, 0, 0), 4)
            
    except Exception as e:
        print(e)
        
    return frame

video_file = "box2.mp4"
cap = cv2.VideoCapture(video_file)
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
out = cv2.VideoWriter('box2-pyzbar.mp4', fourcc, 15.0, (1280, 720))

while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        frame = read_frame(frame)
        cv2.imshow('Barcode', frame)
        out.write(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            out.release()
            cv2.destroyAllWindows()
    else:
        cap.release()
        out.release()
        cv2.destroyAllWindows()       
    