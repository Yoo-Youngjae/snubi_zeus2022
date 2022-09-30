from rembg import remove
from PIL import Image
import threading
import pandas as pd
from tqdm import tqdm
import os

n = 24

def preprprocess_image(num_id):
    # 1. Load the image with Pillow library
    df = pd.read_csv('data.csv')
    total_items = len(df.index)
    start_id = (total_items//n) * num_id
    end_id = (total_items // n) * (num_id+1)
    n_df = df[start_id: end_id]
    ids = n_df['id']
    for id in tqdm(ids):
        img = Image.open('raw_database_image/'+str(id)+'.jpg')
        img = img.resize((600, 600))
        img = remove(img, alpha_matting=True)
        im2 = img.crop(img.getbbox())
        background = Image.new("RGB", im2.size, (255, 255, 255))
        background.paste(im2, mask=im2.split()[3])  # 3 is the alpha channel
        im2 = background
        im2.save('image/'+str(id)+'.jpg')

def preprprocess_image_by_id(num_id):

    img = Image.open('raw_database_image/'+str(num_id)+'.jpg')
    img = img.resize((600, 600))
    img = remove(img, alpha_matting=True)
    im2 = img.crop(img.getbbox())
    background = Image.new("RGB", im2.size, (255, 255, 255))
    background.paste(im2, mask=im2.split()[3])  # 3 is the alpha channel
    im2 = background
    # im2.show()
    im2.save('image/'+str(num_id)+'.jpg')

if __name__ == "__main__":
    df = pd.read_csv('data.csv')
    # for idx in tqdm(df['id']):
    for idx in tqdm(range(3049, 4875)):
        image_name = 'image/' + str(idx) + '.jpg'
        # if not os.path.exists(image_name):
        preprprocess_image_by_id(idx)
    # for i in range(0, 6):
    #     t = threading.Thread(target=preprprocess_image, args=[i])
    #     t.start()

