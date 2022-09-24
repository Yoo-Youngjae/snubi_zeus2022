from rembg import remove
import cv2


for i in range(0,1):
    input_path = '/home/snubi/PycharmProjects/snubi_zeus2022/test/thumbnail/'+str(i)+'.png'
    input = cv2.imread(input_path)
    output = remove(input, alpha_matting=True)
    output_path = '../thumb_output/'+str(i+10)+'.png'
    cv2.imwrite(output_path, output)