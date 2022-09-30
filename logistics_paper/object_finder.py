import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import torch
from torch.autograd import Variable
from rembg import remove
from tqdm import tqdm
from evaluation_metric import *
import pandas as pd
import glob
import os
from albumentations import Transpose, HorizontalFlip, VerticalFlip, \
    ShiftScaleRotate, RandomBrightnessContrast, Resize, Normalize, Compose
from albumentations.pytorch.transforms import ToTensorV2
import colorsys


def filter():
    opt = dict()
    opt['img_size1'] = 384
    opt['img_size2'] = 384
    opt['mean'] = [0.485, 0.456, 0.406]
    opt['std'] = [0.229, 0.224, 0.225]

    return Compose([Transpose(p=0.5),
                    HorizontalFlip(p=0.5),
                    VerticalFlip(p=0.5),
                    ShiftScaleRotate(p=0.5),
                    RandomBrightnessContrast(brightness_limit=(-0.1,0.1), contrast_limit=(-0.1, 0.1), p=0.5),
                    Resize(opt['img_size1'], opt['img_size2']),
                    Normalize(mean=opt['mean'], std=opt['std'], max_pixel_value=255.0, p=1.0),
                    ToTensorV2(p=1.0),
                    ], p=1.)


import time
def preprprocess_image(image_name):
    # 1. Load the image with Pillow library
    img = Image.open(image_name)

    img = img.resize((600, 600))

    img = remove(img, alpha_matting=True)
    im2 = img.crop(img.getbbox())
    background = Image.new("RGB", im2.size, (255, 255, 255))
    background.paste(im2, mask=im2.split()[3])  # 3 is the alpha channel
    im2 = background

    im2.save(image_name)


#
# def HSVColor(img):
#     if isinstance(img, Image.Image):
#         r, g, b = img.split()
#     Hdat = []
#     Sdat = []
#     Vdat = []
#     for rd, gn, bl in zip(r.getdata(), g.getdata(), b.getdata()):
#         h, s, v = colorsys.rgb_to_hsv(rd / 255., gn / 255., bl / 255.)
#     Hdat.append(int(h * 255.))
#     Sdat.append(int(s * 255.))
#     Vdat.append(int(v * 255.))
#     r.putdata(Hdat)
#     g.putdata(Sdat)
#     b.putdata(Vdat)
#     return Image.merge('RGB', (r, g, b))


def get_vector(arg, image_name, im2=None, tensor=False):
    if im2 is None:
        # 1. Load the image with Pillow library
        im2 = Image.open(image_name)

        img = remove(image_name, alpha_matting=True)
        im2 = img.crop(img.getbbox())
        background = Image.new("RGB", im2.size, (255, 255, 255))
        background.paste(im2, mask=im2.split()[3])  # 3 is the alpha channel
        im2 = background
    else:
        image_size = im2.size
        width = image_size[0]
        height = image_size[1]
        bigside = width if width > height else height

        background = Image.new('RGBA', (bigside, bigside), (255, 255, 255, 255))
        offset = (int(round(((bigside - width) / 2), 0)), int(round(((bigside - height) / 2), 0)))
        background.paste(im2, offset)
        im2 = background.convert('RGB')

        #im2 = im2.convert('HSV')
        #im2 = HSVColor(im2)
        #im2.show()
        #im2.save(image_name)
        # 2. Create a PyTorch Variable with the transformed image
    # im2.show()


    t_img = Variable(normalize(to_tensor(scaler(im2))).unsqueeze(0))

    ###########################################
    #transform = filter()
    #t_img = transform(image=np.array(im2))['image'].unsqueeze(0)
    ###########################################
    t_img = t_img.to(device)


    # 3. Create a vector of zeros that will hold our feature vector
    #    The 'avgpool' layer has an output size of 512
    my_embedding = torch.zeros(arg["model_size"])
    #my_embedding2 = torch.zeros(arg["model_size2"])

    # 4. Define a function that will copy the output of a layer
    def copy_data(m, i, o):
        my_embedding.copy_(o.data.reshape(o.data.size(1)))
    # 5. Attach that function to our selected layer
    h = layer.register_forward_hook(copy_data)
    #h2 = layer.

    # 6. Run the model on our transformed image
    model(t_img)
    #model2(t_img)
    # 7. Detach our copy function from the layer
    h.remove()
    #h2.remove()
    # 8. Return the feature vector
    if tensor:
        return my_embedding
    return my_embedding.numpy()

def get_all_database_tensor(df):
    full_tensor = None
    for idx in tqdm(df['id']):
        image_name = 'image/' + str(idx) + '.jpg'
        im2 = Image.open(image_name)
        target_feature = get_vector(arg, None, im2=im2, tensor=True)
        target_feature = torch.reshape(target_feature, (1, -1))
        if full_tensor is None:
            full_tensor = target_feature
            continue
        full_tensor = torch.cat([full_tensor, target_feature], dim=0)
    return full_tensor

def get_target_image(idx):
    image_name = 'image/' + str(idx) + '.jpg'

    im2 = Image.open(image_name)
    target_image = np.array([get_vector(arg, image_name, im2)])

    return target_image[0]

def get_test_image(arg, idx):
    image_name = glob.glob(arg['test_image_dir']+str(idx)+'.*')[0]
    #image_name = '/home/snubi/PycharmProjects/snubi_zeus2022/test/data/' + str(idx) + '.png'
    img = Image.open(image_name)

    output = remove(img, alpha_matting=True)
    output = np.array(output)
    alphas = output[:,:,3]

    first_idx = 0
    last_idx = 0
    object_finding = False
    object_vector_list = []
    im_list = []
    for i in range(alphas.shape[1]):
        if i <= last_idx + 20:
            continue
        if np.any(alphas[:,i] >= 240):
            if object_finding is False:
                object_finding = True
                first_idx = i
        elif object_finding is True:
            object_finding = False
            last_idx = i
            if last_idx - first_idx <= 10:
                continue
            img = Image.fromarray(output[:,first_idx:i])
            im2 = img.crop(img.getbbox())


            rembg_img = Image.new("RGB", im2.size, (255, 255, 255))
            rembg_img.paste(im2, mask=im2.split()[3])  # 3 is the alpha channel

            image_size = rembg_img.size
            width = image_size[0]
            height = image_size[1]
            bigside = width if width > height else height

            background = Image.new('RGBA', (bigside, bigside), (255, 255, 255, 255))
            offset = (int(round(((bigside - width) / 2), 0)), int(round(((bigside - height) / 2), 0)))

            background.paste(rembg_img, offset)
            im2 = background.convert('RGB')

            im_list.append(im2)
            object_vector_list.append(get_vector(arg, None, im2=im2))

    return object_vector_list, im_list

def make_result_dir(save_dir):
    for i in range(7):
        if os.path.isdir(save_dir+str(i)):
            print("exists: ", save_dir+str(i))
        else:
            os.makedirs(save_dir+str(i))
            print("dir made: "+save_dir+str(i))


def save_result(arg, arg_save_dir, test_idx, inference_idxes, obj_img):
    test_img = Image.open(arg['test_image_dir']+str(test_idx)+'.png')
    test_img = test_img.resize((360, 640))
    test_img = np.asarray(test_img)

    obj_img = obj_img.resize((360, 640))
    obj_img = np.asarray(obj_img)

    images = np.hstack((test_img, obj_img))

    for inference_idx in inference_idxes:
        infer_img = Image.open('image/' + str(inference_idx) + '.jpg')
        infer_img = infer_img.resize((360, 640))
        infer_img = np.asarray(infer_img)

        images = np.hstack((images, infer_img))

    img = Image.fromarray(images)
    img.save(arg_save_dir+str(test_idx)+'.png')

# def save_result(test_idx, inference_idx, obj_img):
#     test_img = Image.open('test_image_800/'+str(test_idx)+'.png')
#     test_img = test_img.resize((360, 640))
#     test_img = np.asarray(test_img)
#
#     obj_img = obj_img.resize((360, 640))
#     obj_img = np.asarray(obj_img)
#
#     infer_img = Image.open('image/' + str(inference_idx) + '.jpg')
#     infer_img = infer_img.resize((360, 640))
#     infer_img = np.asarray(infer_img)
#
#     images = np.hstack((test_img, obj_img))
#     images = np.hstack((images, infer_img))
#     img = Image.fromarray(images)
#     img.save('result_800_filtered/'+str(test_idx)+'.png')

scaler = transforms.Resize((320, 320))
normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
to_tensor = transforms.ToTensor()


def start(arg):
    # get data
    database_df = pd.read_csv('data.csv')
    test_label_df = pd.read_csv(f'test_label/{arg["test_label_df"]}.csv')

    if not os.path.exists(f'{arg["full_database_features"]}.pt'):
        full_database_features = get_all_database_tensor(database_df)
        torch.save(full_database_features, f'{arg["full_database_features"]}.pt')
    else:
        full_database_features = torch.load(f'{arg["full_database_features"]}.pt')

    # calculate similarity then print top k accuracy
    thres = 0.2
    top_k_accuracy = [[], []]  # 추가
    all_top_k_accuracy = [[[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]]]

    if arg['save_result']:
        make_result_dir(arg['result_dir'])

    for test_img_idx in tqdm(range(arg["test_len"])):
        object_vector_list, im_list = get_test_image(arg, test_img_idx)
        for inner_test_img_idx, (object, obj_img) in enumerate(zip(object_vector_list, im_list)):
            if arg['similarity_metric_compare_all']:
                all_sim_list = similarity_calculation('all', full_database_features, object)

                for idx, sim_np in enumerate(all_sim_list):
                    if idx < 3:
                        if arg['save_result']:
                            save_result(arg, arg['result_dir']+str(idx)+'/', test_img_idx, poll(sim_np, m='max', top_k=3), obj_img)

                        all_top_k_accuracy[idx][0].append(is_top_k(database_df=database_df,
                                                          test_product_id=test_label_df['product_id'][test_img_idx],
                                                          sim_np=sim_np, m='max', top_k=1))
                        all_top_k_accuracy[idx][1].append(is_top_k(database_df=database_df,
                                                          test_product_id=test_label_df['product_id'][test_img_idx],
                                                          sim_np=sim_np, m='max', top_k=3))
                    else:
                        if arg['save_result']:
                            save_result(arg, arg['result_dir']+str(idx)+'/', test_img_idx, poll(sim_np, m='min', top_k=3), obj_img)

                        all_top_k_accuracy[idx][0].append(is_top_k(database_df=database_df,
                                                          test_product_id=test_label_df['product_id'][test_img_idx],
                                                          sim_np=sim_np, m='min', top_k=1))
                        all_top_k_accuracy[idx][1].append(is_top_k(database_df=database_df,
                                                          test_product_id=test_label_df['product_id'][test_img_idx],
                                                          sim_np=sim_np, m='min', top_k=3))
            else:
                sim_np = similarity_calculation(arg["similarity_metric"], full_database_features, object)  # similarity_func(database_img, test image) comparison
                if arg["save_result"]:
                    save_result(arg, arg['result_dir'], test_img_idx, poll(sim_np, m=arg['min_max'], top_k=3), obj_img)

                # database 통해서 예측값 product_idx 확인, test_label_df['product_idx'][test_img_idx][inner_test_img_idx]
                # print_top_k_values(database_df, test_label_df['product_id'][test_img_idx], sim_list, m='max')
                top_k_accuracy[0].append(is_top_k(database_df=database_df,
                                                  test_product_id=test_label_df['product_id'][test_img_idx],
                                                  sim_np=sim_np, m=arg['min_max'], top_k=1))
                # for top 3
                top_k_accuracy[1].append(is_top_k(database_df=database_df,
                                                  test_product_id=test_label_df['product_id'][test_img_idx],
                                                  sim_np=sim_np, m=arg['min_max'], top_k=3))

                # print_top_k_values(database_df=database_df,
                #                    test_product_id=test_label_df['product_id'][test_img_idx],
                #                    sim_np=sim_np, m='max', top_k=3)

    if arg["similarity_metric_compare_all"]:
        print_all_top_k_metric_result(all_top_k_accuracy)
    else:
        print_top_k_metric_result(top_k_accuracy)

if __name__ == "__main__":
    device = torch.device('cuda')

    eff_model_size = 1792
    # resnet_model_size = 2048

    # feature extract model
    model = models.efficientnet_b4(pretrained=True)
    #model = models.resnet50(pretrained=True)

    model.to(device)
    layer = model._modules.get('avgpool')
    model.eval()

    arg = {"test_label_df": "test_label_final",
           "full_database_features": "full_database_features",
           "test_len": 104,
           "similarity_metric": "fractional_dis",
           "min_max": "min",
           "similarity_metric_compare_all": True,
           "test_image_dir": "test_image/test_image_white_bg/",
           "result_dir": "result/result_white_bg_effnet/",
           "save_result": True,
           "model_size": eff_model_size
           }

    start(arg)

