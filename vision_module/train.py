from detectron2.engine import DefaultTrainer
from detectron2.config import get_cfg
import os
# 라이브러리 import
import torch, torchvision
import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()

# import some common libraries
import matplotlib.pyplot as plt
import numpy as np
import cv2
import register
# import some common detectron2 utilities
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog

from detectron2.data.datasets import register_coco_instances

def start_train(name, class_num, path, iteration):
    register_coco_instances(name, {}, "data/trainval.json", "data/images")
    zeus_snu_metadata = MetadataCatalog.get(name)
    dataset_dicts = DatasetCatalog.get(name)

    cfg = get_cfg()
    cfg.merge_from_file(path)
    cfg.DATASETS.TRAIN = (name,)
    cfg.DATASETS.TEST = ()   # no metrics implemented for this dataset
    cfg.DATALOADER.NUM_WORKERS = 2
    cfg.MODEL.WEIGHTS = "detectron2://COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x/137849600/model_final_f10217.pkl"  # initialize from model zoo
    cfg.SOLVER.IMS_PER_BATCH = 2
    cfg.SOLVER.BASE_LR = 0.00025
    cfg.SOLVER.MAX_ITER = iteration    # 300 iterations seems good enough, but you can certainly train longer
    cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 128   # faster, and good enough for this toy dataset
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = class_num  # 18 classes

    os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
    trainer = DefaultTrainer(cfg)
    trainer.resume_or_load(resume=False)
    trainer.train()


if __name__ == '__main__':
    iteration = 8000
    merge_file_path = '/home/snubi/PycharmProjects/snubi_zeus2022/vision_module/detectron2/configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml'
    start_train('zeus_real_final_4', 16, merge_file_path, iteration) #name, class_num, merge_file_yaml
    register.register_zeus_snu('zeus_real_final_4', 16, merge_file_path, iteration)