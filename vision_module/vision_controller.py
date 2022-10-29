import cv2
import os

# import some common detectron2 utilities
from detectron2.utils.logger import setup_logger
setup_logger()
from detectron2.engine import DefaultPredictor
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog
from detectron2.config import get_cfg
import math

#zeus_cfg = '/home/snubi/PycharmProjects/snubi_zeus2022/vision_module/weight_cfg/zeus_real_final_3.yaml'
zeus_cfg = '/home/snubi/PycharmProjects/snubi_zeus2022/vision_module/weight_cfg/zeus_1022_delete.yaml'

class DetectronController:
    def __init__(self):
        cfg = get_cfg()
        cfg.merge_from_file(zeus_cfg) # cfg file change
        os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
        self.cfg = cfg
        self.predictor = DefaultPredictor(cfg)

    def get_object_center_coordnates(self, image, show_debug):
        # inference
        outputs = self.predictor(image)
        v = Visualizer(image[:, :, ::-1], MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]), scale=1.2)
        v = v.draw_instance_predictions(outputs["instances"].to("cpu"))
        bboxes = outputs["instances"].to("cpu").pred_boxes.tensor.numpy()
        masks = outputs["instances"].to("cpu").pred_masks.numpy()
        img = v.get_image()[:, :, ::-1] # masked image
        if show_debug:
            img = cv2.resize(img, dsize=(1280, 720), interpolation=cv2.INTER_CUBIC)

        # get center coord of each objects
        center_coordinate_list = []
        dist_scale = 3
        for bbox, mask, obj_class in zip(bboxes, masks, outputs["instances"].to("cpu").pred_classes.numpy()):
            # get center coordinate
            x0, y0, x1, y1 = bbox
            center_x, center_y = int(x0 + x1) // 2, int(y0 + y1) // 2

            # get min width angle
            min_dist_list_of_each_degree = []
            min_dist_list_of_each_degree_180 = []

            for i in range(18):
                cnt = 0
                cnt_for_180 = 0
                # print('start ',i)
                for j in range(50):
                    x     = int(center_x + math.cos(math.pi / 18 * i) * j * dist_scale)
                    y     = int(center_y + math.sin(math.pi / 18 * i) * j * dist_scale)
                    x_180 = int(center_x + math.cos(math.pi + math.pi / 18 * i) * j * dist_scale)
                    y_180 = int(center_y + math.sin(math.pi + math.pi / 18 * i) * j * dist_scale)

                    x     = min(x, 1279)
                    x_180 = min(x_180, 1279)
                    y     = min(y, 719)
                    y_180 = min(y_180, 719)
                    # print('x, x_180, y, y_180', x, x_180, y, y_180)
                    if mask[y][x]:
                        cnt += 1
                    if mask[y_180][x_180]:
                        cnt_for_180 += 1
                    if not mask[y][x] and not mask[y_180][x_180]:
                        break

                min_dist_list_of_each_degree.append(cnt)
                min_dist_list_of_each_degree_180.append(cnt_for_180)

            # find min_width
            min_dist = [i+j for i,j in zip(min_dist_list_of_each_degree, min_dist_list_of_each_degree_180)]

            min_width = min(min_dist_list_of_each_degree)
            min_width_angle = min(range(len(min_dist)), key=lambda i: min_dist[i])
            min_width_angle *= 10

            if show_debug:
                min_angle_x_s = int(center_x + math.cos(math.pi + math.pi / 180 * min_width_angle) * min_width * dist_scale)
                min_angle_y_s = int(center_y + math.sin(math.pi + math.pi / 180 * min_width_angle) * min_width * dist_scale)
                min_angle_x_e = int(center_x + math.cos(math.pi / 180 * min_width_angle) * min_width * dist_scale)
                min_angle_y_e = int(center_y + math.sin(math.pi / 180 * min_width_angle) * min_width * dist_scale)
                img = cv2.line(img, (min_angle_x_s, min_angle_y_s), (min_angle_x_e, min_angle_y_e), (0, 255, 0), thickness=5)
                img = cv2.circle(img, (center_x, center_y), 10, (0, 0, 255), -1)
            center_coordinate_list.append((center_x, center_y, min_width_angle, obj_class))
        object_label_np = outputs["instances"].to("cpu").pred_classes.numpy()
        return sorted(center_coordinate_list, key=lambda tup: tup[0], reverse=True), img, list(object_label_np)
