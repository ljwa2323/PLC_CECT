import os
import shutil  # for copying DICOM files
import sys
# import dicom as pdcm # for pydicom with version < 1.0, use 'import dicom as pdcm'
import pydicom as pdcm  # for pydicom with version >= 1.0, use 'import pydicom as pdcm'

oj = os.path.join  # shorthand to join paths
import warnings
from numpy import sign
import numpy as np
import SimpleITK as sitk
import pandas as pd
import decimal  # decimal.Decimal for very very big int/float arithmatic

def extractDICOM2Image(folder, outputImageFile):
    """convert DICOM files in one folder to one image file.
    Only the first series is extracted"""
    reader = sitk.ImageSeriesReader()
    dcmFileLs = reader.GetGDCMSeriesFileNames(folder)
    reader.SetFileNames(dcmFileLs)
    im = reader.Execute()
    sitk.WriteImage(im, outputImageFile)


src_folder = "E:/HCC-TACE-Seg/1/C1/"
tar_file = "E:/A/nii"
extractDICOM2Image(src_folder, tar_file)
import os

def process_folders(src_root, dst_root):
    # 遍历一级子文件夹
    for folder1 in os.listdir(src_root):
        src_folder1_path = os.path.join(src_root, folder1)
        if os.path.isdir(src_folder1_path):
            # 创建对应的目标一级子文件夹
            dst_folder1_path = os.path.join(dst_root, folder1)
            os.makedirs(dst_folder1_path, exist_ok=True)

            # 遍历二级子文件夹
            for folder2 in os.listdir(src_folder1_path):
                src_folder2_path = os.path.join(src_folder1_path, folder2)
                if os.path.isdir(src_folder2_path):
                    # 生成目标 .nii.gz 文件名
                    dst_file = os.path.join(dst_folder1_path, f"{folder2}.nii.gz")
                    # 调用 extractDICOM2Image 函数进行合并
                    extractDICOM2Image(src_folder2_path, dst_file)


# 指定源文件夹和目标文件夹
src_root = "E:/HCC-TACE-Seg"
dst_root = "E:/A/nii"

# 调用函数处理文件夹
process_folders(src_root, dst_root)
