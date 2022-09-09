# -*- encoding=utf-8 -*-

# 导入包
import os

import cv2
from PIL import Image
from math import sqrt
import numpy as np
from tqdm import tqdm
# from skimage.measure import compare_ssim

def similarity_orb(des1, des2):
    # 图片特征
    # 直接传参过来
    # orb = cv2.ORB_create()
    # _, des1 = orb.detectAndCompute(img1, None)
    # _, des2 = orb.detectAndCompute(img2, None)
    # 提取并计算特征点
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    # knn筛选结果
    matches = bf.knnMatch(des1, trainDescriptors=des2, k=2)
    # 查看最大匹配点数目
    good = [m for (m, n) in matches if m.distance < 0.75 * n.distance]
    return len(good) / len(matches)


# 颜色映射
def bgr_mapping(img_val):
    # 将bgr颜色分成8个区间做映射
    if 0 <= img_val <= 31: return 0
    if 32 <= img_val <= 63: return 1
    if 64 <= img_val <= 95: return 2
    if 96 <= img_val <= 127: return 3
    if 128 <= img_val <= 159: return 4
    if 160 <= img_val <= 191: return 5
    if 192 <= img_val <= 223: return 6
    if img_val >= 224: return 7


# 颜色直方图的数值计算
def calc_bgr_hist(image):
    if not image.size: return False
    hist = {}
    # 缩放尺寸减小计算量
    tmp = cv2.resize(image, (32, 32))
    for bgr_list in tmp:
        for bgr in bgr_list:
            # 颜色按照顺序映射
            maped_b = bgr_mapping(bgr[0])
            maped_g = bgr_mapping(bgr[1])
            maped_r = bgr_mapping(bgr[2])
            # 计算像素值
            index = maped_b * 8 * 8 + maped_g * 8 + maped_r
            hist[index] = hist.get(index, 0) + 1
    return hist


# 计算两张图片的相似度
def compare_similar_hist(h1, h2):
    if not h1 or not h2: return False
    sum1, sum2, sum_mixd = 0, 0, 0
    # 像素值key的最大数不超过512，直接循环到512，遍历取出每个像素值
    for i in range(512):
        # 计算出现相同像素值次数的平方和
        sum1 = sum1 + (h1.get(i, 0) * h1.get(i, 0))
        sum2 = sum2 + (h2.get(i, 0) * h2.get(i, 0))
        # 计算两个图片次数乘积的和
        sum_mixd = sum_mixd + (h1.get(i, 0) * h2.get(i, 0))
    # 按照余弦相似性定理计算相似度
    return sum_mixd / (sqrt(sum1) * sqrt(sum2))

# 获取图片的转二进制的值
def hash_img_code(image):
    width, height = image.shape
    avg = image.mean()
    return np.array([1 if image[i, j] > avg else 0 for i in range(width) for j in range(height)])


def run(img_path, merge_img_dir):
    # 用多少张图片去填补原图
    replace_num = 100
    # 获取 原图片的宽度
    image = Image.open(img_path)
    image_origin_w, image_origin_h = image.size
    # 小图宽高比
    mini_image_w, mini_image_h = 20, 30
    # 生成新图片的宽高
    new_image_w = mini_image_w * replace_num
    new_image_h = ((new_image_w / image_origin_w) * image_origin_h // mini_image_h) * mini_image_h

    # 先将图片映射好，方便操作
    np_mapping, calc_bgr_mapping, orb_mapping, a_hash_mapping, avg_rgb_mapping = {}, {}, {}, {}, {}

    for k, file in tqdm(enumerate(os.listdir(merge_img_dir)), desc='mapping映射中'):
        img = Image.open(merge_img_dir + '/' + file).convert('RGB').resize((mini_image_w, mini_image_h),
                                                                           Image.ANTIALIAS)
        np_mapping[file] = np.array(img)

        # 平均色值
        avg_rgb_mapping[file] = np.array([np.mean(np_mapping[file][:, :, 0]), np.mean(np_mapping[file][:, :, 1]), np.mean(np_mapping[file][:, :, 2])])

        # 保存所有图片的hash 值的二进制数值
        a_hash_mapping[file] = hash_img_code(np.array(img.convert('L').resize((8, 8), Image.ANTIALIAS)))

        # 保存所有的图片的直方图数据
        calc_bgr_mapping[file] = calc_bgr_hist(np.array(img))

    # 将图片扩大为新图片的大小
    # 将图片转成jpg格式
    new_image = Image.open(img_path).resize((int(new_image_w), int(new_image_h)), Image.ANTIALIAS)
    new_image = np.array(new_image)

    w, h = int(new_image_w / mini_image_w), int(new_image_h / mini_image_h)

    # 开始替换小图片

    for i in tqdm(range(w), desc='合成图片中'):
        for j in range(h):
            piece = new_image[j * mini_image_h:(j + 1) * mini_image_h, i * mini_image_w:(i + 1) * mini_image_w, :]
            ## ssim 算法
            # selection = {}
            # for k, v in np_mapping.items():
            #     selection[k] = compare_ssim(section, v, multichannel=True)
            # selection = sorted(selection.items(), key=lambda kv: (kv[1], kv[0]))

            # 根据rgb通道均值取
            slice_mean = np.array([np.mean(piece[:, :, 0]), np.mean(piece[:, :, 1]), np.mean(piece[:, :, 2])])
            selection = [(k, np.linalg.norm(slice_mean - v)) for k, v in avg_rgb_mapping.items()]
            selection = sorted(selection, key=lambda kv: kv[1])[:10]

            ## 直方图
            # selection = {}
            # for k, calc_bgr in calc_bgr_mapping.items():
            #     selection[k] = compare_similar_hist(calc_bgr_hist(section), calc_bgr)
            # selection = sorted(selection.items(), key=lambda kv: (kv[1], kv[0]))

            # 图片特征点 orb，调用 similarity_orb 方法

            # 取出最后十个最相同的图片，再去对比找出一张
            item = hash_img_code(np.array(Image.fromarray(piece).convert('L').resize((8, 8), Image.ANTIALIAS)))
            selection = [(key, np.equal(item, a_hash_mapping[key]).mean()) for key, _ in selection[-10:]]

            # 将最同样的那一张图贴到原图里面
            new_image[j * mini_image_h:(j + 1) * mini_image_h, i * mini_image_w:(i + 1) * mini_image_w, :] = np_mapping[
                max(selection, key=lambda kv: kv[1])[0]]
    image = Image.fromarray(new_image)
    image.save('demo/output.jpg')
    print('done')


run('./demo/input.jpg', './bg')
