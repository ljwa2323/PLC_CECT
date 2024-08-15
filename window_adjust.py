import os
import nibabel as nib
import numpy as np

# 指定源文件夹路径
folder = "E:/HCC-TACE-Seg_1/"

# 指定目标文件夹路径
target_folder = "E:/wb1/"  # 请替换为您的目标文件夹路径

# 定义目标强度范围的最小值和最大值
target_min_intensity = -200  # 替换为所需的最小值
target_max_intensity = 200  # 替换为所需的最大值

# 遍历源文件夹中的所有子文件夹
for subdir in os.listdir(folder):
    subdir_path = os.path.join(folder, subdir)
    
    # 如果这不是一个子文件夹，就跳过
    if not os.path.isdir(subdir_path):
        continue

    # 在目标文件夹中创建相应的子文件夹
    target_subdir = os.path.join(target_folder, subdir)
    if not os.path.exists(target_subdir):
        os.makedirs(target_subdir)

    # 获取子文件夹内的所有 .nii.gz 文件路径
    file_paths = [os.path.join(subdir_path, filename) for filename in os.listdir(subdir_path) if filename.endswith('.nii.gz')]

    # 遍历每个NIfTI文件
    for nii_file_path in file_paths:
        # 读取NIfTI文件
        nii_img = nib.load(nii_file_path)
        header = nii_img.header
        data = nii_img.get_fdata(dtype=np.float64)

        # 限制像素值在目标范围内
        data_clipped = np.clip(data, target_min_intensity, target_max_intensity)

        # 创建新的NIfTI图像
        new_nii_img = nib.Nifti1Image(data_clipped, nii_img.affine, header)

        # 保存修改后的NIfTI文件到目标文件夹
        output_path = os.path.join(target_subdir, "adjusted_" + os.path.basename(nii_file_path))
        new_nii_img.to_filename(output_path)

        print(f"已调整 {nii_file_path} 的强度范围为 ({target_min_intensity}, {target_max_intensity})")
        print(f"调整后的文件已保存为 {output_path}")

print("所有文件处理完成")