import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import torch
from torch.autograd import Variable
from sklearn.manifold import TSNE
from numpy import dot
from numpy.linalg import norm
from rembg import remove
from matplotlib import pyplot as plt


def cos_sim(A, B):
  return dot(A, B)/(norm(A)*norm(B))

def get_vector(image_name, im2=None):
    if im2 is None:
        # 1. Load the image with Pillow library
        img = Image.open(image_name)
        im2 = img.crop(img.getbbox())
        background = Image.new("RGB", im2.size, (255, 255, 255))
        background.paste(im2, mask=im2.split()[3])  # 3 is the alpha channel
        im2 = background

        # im2.save('test_rembg'+str(i)+'.png')
        # 2. Create a PyTorch Variable with the transformed image
    # im2.show()
    t_img = Variable(normalize(to_tensor(scaler(im2))).unsqueeze(0))
    # 3. Create a vector of zeros that will hold our feature vector
    #    The 'avgpool' layer has an output size of 512
    my_embedding = torch.zeros(1792)
    # 4. Define a function that will copy the output of a layer
    def copy_data(m, i, o):
        my_embedding.copy_(o.data.reshape(o.data.size(1)))
    # 5. Attach that function to our selected layer
    h = layer.register_forward_hook(copy_data)
    # 6. Run the model on our transformed image
    model(t_img)
    # 7. Detach our copy function from the layer
    h.remove()
    # 8. Return the feature vector
    return my_embedding.numpy()

def get_target_image(idx):
    image_name = 'output/'+str(idx)+'.png'
    target_image = np.array([get_vector(image_name=image_name)])
    return target_image[0]

def get_test_image(idx):
    image_name = '/home/snubi/PycharmProjects/snubi_zeus2022/test/data/' + str(idx) + '.png'
    img = Image.open(image_name)
    output = remove(img, alpha_matting=True)
    output = np.array(output)
    plt.imshow(output)
    plt.show()
    alphas = output[:,:,3]

    first_idx = 0
    last_idx = 0
    object_finding = False
    object_vector_list = []
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
            background = Image.new("RGB", im2.size, (255, 255, 255))
            background.paste(im2, mask=im2.split()[3])  # 3 is the alpha channel
            im2 = background
            im2.show()
            object_vector_list.append(get_vector(None, im2=im2))




    return object_vector_list

scaler = transforms.Resize((320, 320))
normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
to_tensor = transforms.ToTensor()



if __name__ == "__main__":
    # model = models.resnet18(pretrained=True)
    model = models.efficientnet_b4(pretrained=True)
    layer = model._modules.get('avgpool')
    model.eval()

    thres = 0.2
    for j in range(100002, 100007):
        object_vector_list = get_test_image(j)

        for idx, object in enumerate(object_vector_list):
            sim_list = []
            for i in range(115):
                try:
                    target_image = get_target_image(i)
                    sim_list.append(cos_sim(target_image, object))
                    # if thres < cos_sim(target_image, object):
                    # print(idx, i, '유사도 :', cos_sim(target_image, object))
                except:
                    continue
            print(j, idx, np.argmax(np.array(sim_list)), '유사도 :', max(sim_list))

    # for i in range(114):
    #     for j in range(114):
    #         try:
    #             target_image = get_target_image(i)
    #             input_image = get_target_image(j)

    #         except:
    #             continue
