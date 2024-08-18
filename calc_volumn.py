import numpy as np
import scipy.ndimage as ndimage
import nibabel as nib
from scipy.spatial import ConvexHull
import pandas as pd

# 初始化统计结果列表
stats_results = []

patient_data = pd.read_csv('patient_data.csv', header=0)

# 遍历 patient_data 中的每一行
for index, row in patient_data.iterrows():
    print(f"正在处理第 {index + 1} 行数据...")
    if pd.notna(row['Mask File']):
        mask = nib.load(row['Mask File'])
        mask_data = mask.get_fdata()
        
        # 确保 mask 是二值的
        mask_data = (mask_data > 0).astype(np.int)
        
        # 使用 label 函数找到病灶的连通区域
        labeled_mask, num_features = ndimage.label(mask_data)
        
        if num_features > 0:
            # 选择一个病灶（例如，最大的一个）
            largest_lesion = (labeled_mask == np.argmax(ndimage.sum(mask_data, labeled_mask, index=np.arange(1, num_features + 1)))+1)
            
            # 获取病灶的坐标
            coords = np.argwhere(largest_lesion)
            
            # 检查坐标的维度
            if np.std(coords, axis=0).min() > 0:  # 检查标准差以确定点是否不全在一个平面或直线上
                try:
                    # 计算凸包
                    hull = ConvexHull(coords)
                    # 计算凸包顶点之间的所有距离
                    distances = [np.linalg.norm(coords[hull.vertices[i]] - coords[hull.vertices[j]]) for i in range(len(hull.vertices)) for j in range(i+1, len(hull.vertices))]
                    # 最长直径
                    max_diameter = max(distances)
                except Exception as e:
                    print(f"在处理第 {index + 1} 行时遇到错误: {e}")
                    max_diameter = 0
            else:
                # 如果点集是一维或二维的，计算所有点对的最大距离
                distances = [np.linalg.norm(coords[i] - coords[j]) for i in range(len(coords)) for j in range(i+1, len(coords))]
                max_diameter = max(distances) if distances else 0
        else:
            max_diameter = 0  # 没有病灶时直径为0
        
        # 获取体素的物理尺寸
        voxel_dims = mask.header.get_zooms()[:3]  # 取前三个维度，通常是(x, y, z)
        voxel_volume = np.prod(voxel_dims)  # 计算单个体素的体积
        
        # 计算有病灶的层数
        layers_with_lesions = np.any(mask_data > 0, axis=(0, 1))
        num_layers_with_lesions = np.sum(layers_with_lesions)
        
        # 计算总层数
        total_layers = mask_data.shape[2]
        
        # 计算所有病灶的总体积
        total_lesion_volume = np.sum(mask_data > 0) * voxel_volume
        
        # 添加统计结果到列表
        stats_results.append({
            'Patient ID': row['Patient ID'],
            'Stage': row['Stage'],
            'Cancer Type': row['Cancer Type'],
            'Total Layers': total_layers,
            'Layers with Lesions': num_layers_with_lesions,
            'Total Lesion Volume (mm^3)': total_lesion_volume,
            'Max Lesion Diameter (mm)': max_diameter
        })
    else:
        # 如果没有mask文件，添加基本信息和默认值
        stats_results.append({
            'Patient ID': row['Patient ID'],
            'Stage': row['Stage'],
            'Cancer Type': row['Cancer Type'],
            'Total Layers': 0,
            'Layers with Lesions': 0,
            'Total Lesion Volume (mm^3)': 0,
            'Max Lesion Diameter (mm)': 0
        })