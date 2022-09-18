import cv2
import os

# import some common detectron2 utilities
from detectron2.utils.logger import setup_logger
setup_logger()
from detectron2.engine import DefaultPredictor
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog
from detectron2.config import get_cfg


class VisionController:
    def __init__(self):
        ##### for connect detectron
        cfg = get_cfg()
        cfg.merge_from_file("/home/snubi/PycharmProjects/snubi_zeus2022/vision_module/detectron2/configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
        cfg.DATASETS.TRAIN = ("zeus_snu",)
        cfg.DATASETS.TEST = ()  # no metrics implemented for this dataset
        cfg.DATALOADER.NUM_WORKERS = 2
        cfg.MODEL.WEIGHTS = "detectron2://COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x/137849600/model_final_f10217.pkl"  # initialize from model zoo
        cfg.SOLVER.IMS_PER_BATCH = 2
        cfg.SOLVER.BASE_LR = 0.02
        cfg.SOLVER.MAX_ITER = 300  # 300 iterations seems good enough, but you can certainly train longer
        cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 128  # faster, and good enough for this toy dataset
        cfg.MODEL.ROI_HEADS.NUM_CLASSES = 13  # 13 classes
        os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
        cfg.MODEL.WEIGHTS = "/home/snubi/PycharmProjects/snubi_zeus2022/vision_module/output/model_final.pth"
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set the testing threshold for this model
        cfg.DATASETS.TEST = ("zeus_snu",)
        self.cfg = cfg
        self.predictor = DefaultPredictor(cfg)

        # for connect opencv camera
        index = 0
        arr = []
        for i in range(20):
            cap = cv2.VideoCapture(index)
            if cap.read()[0]:
                arr.append(index)
                cap.release()
            index += 1
        print('camera id lists', arr)

        capture = cv2.VideoCapture(0)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.capture = capture
    def read_camera(self, idx):
        while True:
            cap = cv2.VideoCapture(idx)
            (grabbed, frame) = cap.read()
            if grabbed == True:
                yield frame
    def get_object_center_coordnates(self):
        # ret = self.capture.grab()
        # ret, frame = self.capture.retrieve()
        # ret = self.capture.grab()
        # ret, image = self.capture.retrieve()
        ret, image = self.capture.read()
        outputs = self.predictor(image)
        v = Visualizer(image[:, :, ::-1], MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]), scale=1.2)
        v = v.draw_instance_predictions(outputs["instances"].to("cpu"))
        bboxes = outputs["instances"].to("cpu").pred_boxes.tensor.numpy()
        img = v.get_image()[:, :, ::-1]

        center_coordinate_list = []
        for bbox in bboxes:
            x0, y0, x1, y1 = bbox
            center_x, center_y = int(x0 + x1) // 2, int(y0 + y1) // 2
            center_coordinate_list.append((center_x, center_y))

        cv2.imshow("Image", img)
        cv2.waitKey(1)
        cv2.destroyAllWindows()
        print('show image')

        return sorted(center_coordinate_list, key=lambda tup: tup[0]), img