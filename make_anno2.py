import json
import cv2
import numpy as np
import glob
from multiprocessing import Pool
from tqdm import tqdm
import time
import pickle

NORM_LABEL = ['尾部下沿中间点', '鲸鱼尾巴尖', '尾部入水中间点', '尾部下沿', '尾部侧沿（右侧）', '尾部入水线', '尾部侧沿（左侧）']


def timer(func):
    def wrapper():
        t1 = time.time()
        print(t1)
        func()
        t2 = time.time()
        print('total time is : ', t2 - t1, ' s')

    return wrapper

def make_anno(path):
    hhh = pickle.loads(path)
    for ss in hhh:
        id_name, shape = ss.split(':')
        shape = shape[1:-2].split(', ')
        shape = [int(shape[0]), int(shape[1]), int(shape[2])]
        # Generating corresponding path
        ann_path = f'20190103total/{id_name}.json'

        # Reading
        with open(ann_path, 'r', encoding='utf-8') as f:
            anno = json.load(f)
        # Generating points set
        six_group_points = [[] for _ in NORM_LABEL]
        for key, group in anno['annotation'][0].items():
            idx = NORM_LABEL.index(key)
            for item in group:
                six_group_points[idx].append(int(item['x']))
                six_group_points[idx].append(int(item['y']))
        # Generating heatmap sets
        heatmap = np.zeros([len(NORM_LABEL)] + list(shape[:2]), np.uint8)
        hhh = -1
        sigma = 2
        for point in six_group_points:
            hhh += 1
            if len(point) > 4:
                for i in range(0, len(point) - 2, 2):
                    heatmap[hhh] = cv2.line(heatmap[hhh], (point[i], point[i + 1]), (point[i + 2], point[i + 3]), (1), 3)
            else:
                for i in range(0, len(point), 2):
                    heatmap[hhh] = cv2.circle(heatmap[hhh], (point[i], point[i + 1]), 3, 1, 3)
        # Generating Seg
        flat_points = []
        for point in six_group_points:
            flat_points.extend(point)
        seg_num = len(six_group_points[0]) + len(six_group_points[1]) + len(six_group_points[2])
        seg_heatmap = np.zeros(shape[:2])
        points_np = np.array(flat_points[seg_num:], dtype=np.int32).flatten().reshape(-1, 1, 2)
        cv2.fillPoly(seg_heatmap, [points_np], (1,), cv2.LINE_AA)

        

def sss():
    with open('shape.txt', 'r') as f:
        asf = f.readlines()
    for i in [16, 32, 64]:
        t1 = time.time()
        n = np.int(np.ceil(len(asf) / i))
        _list = [pickle.dumps(asf[i:i+n]) for i in range(0, len(asf), n)]
        with Pool(i) as p:
            with tqdm(p.imap_unordered(make_anno, _list)) as pbar:
                for x in pbar:
                    pass
        t2 = time.time() 
        print(f'The number of process: {i}, its time is {t2-t1} s!')    


sss()

