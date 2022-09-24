from rembg import remove
import cv2



for i in range(100,104):
    input_path = '/home/snubi/PycharmProjects/snubi_zeus2022/test/logistics/'+str(i)+'.png'
    input = cv2.imread(input_path)
    output = remove(input, alpha_matting=True)
    output_path = '../output/'+str(i+10)+'.png'
    cv2.imwrite(output_path, output)