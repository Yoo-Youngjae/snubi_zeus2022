# Custom 객체 추가
from detectron2.config import get_cfg
from detectron2.data.datasets import register_coco_instances
import shutil
def registet_dataset(name,json_path, image_path):
    register_coco_instances(name, {}, json_path, image_path)

def register_cfg(name, class_num, weight, merge_file, iteration):
    cfg = get_cfg()
    cfg.merge_from_file(merge_file)
    cfg.DATASETS.TRAIN = (name,)
    cfg.DATASETS.TEST = ()  # no metrics implemented for this dataset
    cfg.DATALOADER.NUM_WORKERS = 2
    cfg.SOLVER.IMS_PER_BATCH = 2
    cfg.SOLVER.BASE_LR = 0.00025
    cfg.SOLVER.MAX_ITER = iteration  # 300 iterations seems good enough, but you can certainly train longer
    cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 128  # faster, and good enough for this toy dataset
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = class_num
    cfg.MODEL.WEIGHTS = weight
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set the testing threshold for this model
    cfg.DATASETS.TEST = (name,)

    with open('/home/snubi/PycharmProjects/snubi_zeus2022/vision_module/weight_cfg/'+name+'.yaml', "w") as f:
        f.write(cfg.dump())  # save config to file


def register_zeus_snu(name, class_num, merge_file, iteration):
    json_path = "/home/snubi/PycharmProjects/snubi_zeus2022/vision_module/data/trainval.json"
    image_path = "/home/snubi/PycharmProjects/snubi_zeus2022/vision_module/data/images"
    merge_file ='/home/snubi/PycharmProjects/snubi_zeus2022/vision_module/detectron2/configs/COCO-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_3x.yaml'

    source = "/home/snubi/PycharmProjects/snubi_zeus2022/vision_module/output/model_final.pth"
    destination = '/home/snubi/PycharmProjects/snubi_zeus2022/vision_module/weight_cfg/' + name + '.pth'
    shutil.copyfile(source, destination)
    weight_path = destination
    #weight_path = '/home/snubi/PycharmProjects/snubi_zeus2022/vision_module/weight_cfg/zeus_final.pth'
    #registet_dataset(name, json_path, image_path)
    register_cfg(name, class_num, weight_path, merge_file, iteration)

#merge_file_path = '/home/snubi/PycharmProjects/snubi_zeus2022/vision_module/detectron2/configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml'
#register_zeus_snu('zeus_final_2', 16, merge_file_path, 10000)
