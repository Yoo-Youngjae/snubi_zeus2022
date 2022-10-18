from detectron2.utils.logger import setup_logger
setup_logger()

# import some common libraries
import cv2

# import some common detectron2 utilities
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2.engine import DefaultTrainer
from detectron2.config import get_cfg
import os
import math

cfg = get_cfg()
cfg.merge_from_file("./detectron2/configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
cfg.DATASETS.TRAIN = ("zeus_snu",)
cfg.DATASETS.TEST = ()   # no metrics implemented for this dataset
cfg.DATALOADER.NUM_WORKERS = 2
cfg.MODEL.WEIGHTS = "detectron2://COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x/137849600/model_final_f10217.pkl"  # initialize from model zoo
cfg.SOLVER.IMS_PER_BATCH = 2
cfg.SOLVER.BASE_LR = 0.02
cfg.SOLVER.MAX_ITER = 300    # 300 iterations seems good enough, but you can certainly train longer
cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 128   # faster, and good enough for this toy dataset
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 13  # 13 classes
os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
# trainer = DefaultTrainer(cfg)
# trainer.resume_or_load(resume=False)
# trainer.train()
cfg.MODEL.WEIGHTS = "./output/model_final_1011.pth"
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5   # set the testing threshold for this model
cfg.DATASETS.TEST = ("zeus_snu", )
predictor = DefaultPredictor(cfg)

i = 10
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
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    ret, image = capture.read()
    outputs = predictor(image)
    v = Visualizer(image[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=1.2)
    v = v.draw_instance_predictions(outputs["instances"].to("cpu"))
    bboxes = outputs["instances"].to("cpu").pred_boxes.tensor.numpy()
    masks = outputs["instances"].to("cpu").pred_masks.numpy()
    img = v.get_image()[:, :, ::-1]
    img = cv2.resize(img, dsize=(1280, 720), interpolation=cv2.INTER_CUBIC)
    show_custom = True

    center_coordinate_list = []
    dist_scale = 3
    for bbox, mask in zip(bboxes, masks):
        # get center coordinate
        x0, y0, x1, y1 = bbox
        center_x, center_y = int(x0 + x1) //2, int(y0 + y1) //2
        # get min width angle
        min_width = 1000
        min_width_angle = 0
        for i in range(18):
            cnt = 0
            for j in range(50):
                x = int(center_x + math.cos(math.pi / 18 * i) * j * dist_scale)
                y = int(center_y + math.sin(math.pi / 18 * i) * j * dist_scale)
                x_180 = int(center_x + math.cos(math.pi + math.pi / 18 * i) * j * dist_scale)
                y_180 = int(center_y + math.sin(math.pi + math.pi / 18 * i) * j * dist_scale)

                x = min(x, 1279)
                x_180 = min(x_180, 1279)
                y = min(y, 719)
                y_180 = min(y_180, 719)
                if mask[y][x] or mask[y_180][x_180]:
                    cnt += 1
                else:
                    break
            if min_width > cnt:
                min_width = cnt
                min_width_angle = i * 10
        if show_custom:
            min_angle_x_s = int(center_x + math.cos(math.pi + math.pi / 1.8 * min_width_angle) * min_width * dist_scale)
            min_angle_y_s = int(center_y + math.sin(math.pi + math.pi / 1.8 * min_width_angle) * min_width * dist_scale)
            min_angle_x_e = int(center_x + math.cos(math.pi / 1.8 * min_width_angle) * min_width * dist_scale)
            min_angle_y_e = int(center_y + math.sin(math.pi / 1.8 * min_width_angle) * min_width * dist_scale)
            img = cv2.line(img, (min_angle_x_s, min_angle_y_s), (min_angle_x_e, min_angle_y_e), (0, 255, 0), thickness=5)
            img = cv2.circle(img, (center_x, center_y), 10, (0, 0, 255), -1)
        center_coordinate_list.append((center_x, center_y, min_width_angle))
    print(center_coordinate_list)
    cv2.imshow('Custom image', img)
    key = cv2.waitKey(1)
