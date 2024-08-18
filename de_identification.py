import pandas as pd
import nibabel as nib

patient_data = pd.read_csv('patient_data.csv', header=0)

# 遍历 patient_data 中的每一行
for index, row in patient_data.iterrows():
    print(f"正在处理第 {index + 1} 个病人的数据，病人ID: {row['Patient ID']}")
    # 读取 CT 文件路径
    ct_file_path = row['CT File']
    
    # 加载NIFTI文件
    nii = nib.load(ct_file_path)
    
    # 获取并修改头部信息
    header = nii.header
    
    # 清除潜在的PHI信息
    header['db_name'] = ''  # 数据库名
    if 'patient_id' in header:
        header['patient_id'] = ''  # 患者ID
    header['descrip'] = 'Anonymized'  # 描述
    header['aux_file'] = ''  # 辅助文件名
    
    # 保存去识别化后的NIFTI文件
    nib.save(nii, ct_file_path)
