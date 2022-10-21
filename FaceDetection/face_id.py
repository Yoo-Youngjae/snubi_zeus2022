import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import torch
from torch.autograd import Variable
import pandas as pd
import numpy as np

class FaceId:
    def __init__(self):
        self.scaler = transforms.Resize((320, 320))
        self.normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        self.to_tensor = transforms.ToTensor()

        self.device = torch.device('cuda')

        # feature extract model
        self.model = models.resnet50(pretrained=True)

        self.model.to(self.device)
        self.layer = self.model._modules.get('avgpool')
        self.model.eval()

        self.database_df = pd.read_csv('/home/snubi/PycharmProjects/snubi_zeus2022/FaceDetection/data.csv')
        self.full_database_features = self.get_all_database_tensor(self.database_df)

    def get_vector(self, im2=None, tensor=False):

        image_size = im2.size
        width = image_size[0]
        height = image_size[1]
        bigside = width if width > height else height

        background = Image.new('RGBA', (bigside, bigside), (255, 255, 255, 255))
        offset = (int(round(((bigside - width) / 2), 0)), int(round(((bigside - height) / 2), 0)))
        background.paste(im2, offset)
        im2 = background.convert('RGB')


        t_img = Variable(self.normalize(self.to_tensor(self.scaler(im2))).unsqueeze(0))
        t_img = t_img.to(self.device)


        # 3. Create a vector of zeros that will hold our feature vector
        #    The 'avgpool' layer has an output size of 512
        model_size = 2048
        my_embedding = torch.zeros(model_size)

        # 4. Define a function that will copy the output of a layer
        def copy_data(m, i, o):
            my_embedding.copy_(o.data.reshape(o.data.size(1)))
        # 5. Attach that function to our selected layer
        h = self.layer.register_forward_hook(copy_data)
        #h2 = layer.

        # 6. Run the model on our transformed image
        self.model(t_img)
        # 7. Detach our copy function from the layer
        h.remove()
        # 8. Return the feature vector
        if tensor:
            return my_embedding
        return my_embedding.numpy()

    def get_all_database_tensor(self, df):
        print('user_ids', df['id'])
        full_tensor = None
        for idx in df['id']:
            image_name = '/home/snubi/PycharmProjects/snubi_zeus2022/FaceDetection/user_face_database/' + str(idx) + '.jpg'
            im2 = Image.open(image_name)
            target_feature = self.get_vector(im2=im2, tensor=True)
            target_feature = torch.reshape(target_feature, (1, -1))
            if full_tensor is None:
                full_tensor = target_feature
                continue
            full_tensor = torch.cat([full_tensor, target_feature], dim=0)
        return full_tensor

    def cos_sim(self, A, B):
        return [np.dot(i, B)/(np.linalg.norm(i)*np.linalg.norm(B)) for i in A]

    def check_id(self, img):
        object_vector = self.get_vector(im2=img)
        sim_np = self.cos_sim(self.full_database_features, object_vector)
        checked_id = np.argmax(sim_np)

        return checked_id, self.database_df['name'][checked_id]
