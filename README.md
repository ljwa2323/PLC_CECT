# Primary Liver Cancer CECT Imaging Dataset (PLC-CECT)

The PLC-CECT dataset is a comprehensive collection of 3D contrast-enhanced CT (CECT) images focused on primary liver cancer. It includes annotated images from 275 patients diagnosed with Hepatocellular Carcinoma (HCC), Intrahepatic Cholangiocarcinoma (ICC), and Combined Hepatocellular-Cholangiocarcinoma (CHCC), with complete multi-phase coverage (Plain, Arterial, Venous, and Delayed phases). The dataset also features control scans from individuals without liver cancer. With over 50,000 annotated slices labeled by expert clinicians, PLC-CECT is a valuable resource for training deep learning models for liver cancer classification and segmentation tasks. This dataset is publicly available on Physionet, offering a strong foundation for advancing research in the field of liver cancer imaging.

----------------

### How to use the dataset?

### Step 1: Import Necessary Libraries
Start by importing the required Python libraries for data manipulation and visualization:

```{python}
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import nibabel as nib
import random
```

### Step 2: Load the Patient Data
Load the patient data from an Excel file. This dataset includes patient IDs, cancer stages, types, and file paths for CT images and masks.

```{python}
patient_data = pd.read_csv("./patient_data.csv",header=0)
```

### Step 3: Select a Patient Record
Specify a patient ID and a stage to select a particular record from the dataset. This example uses patient ID 'P0059' and stage 'C1'.

```{python}
patient_id = 'P0059'
stage = 'C1'
selected_row = patient_data[(patient_data['Patient ID'] == patient_id) & (patient_data['Stage'] == stage)].iloc[0]
```

### Step 4: Load Imaging Data
Using the paths provided in the dataset, load the CT images and masks using the nibabel library. This includes handling different dimensions of the data.

```{python}
root_folder_path = "D:/liver_db_project/"
liver_image = nib.load(os.path.join(root_folder_path, selected_row['CT File']))
liver_image_data = liver_image.get_fdata()
# Adjust dimensions if necessary
if len(liver_image_data.shape) == 4:
    liver_image_data = liver_image_data[..., 0]
```

### Step 5: Visualize the Data
Create visualizations of the CT images along with the liver and lesion masks. This involves selecting slices with lesions, overlaying masks on the CT images, and adjusting the display settings for better visualization.

```{python}
fig, axes = plt.subplots(3, 5, figsize=(15, 9))
for i, slice_index in enumerate(random_slices):
    axes[0, i].imshow(np.flipud(np.rot90(liver_image_data[:, :, slice_index])), cmap='gray')
    axes[0, i].set_title(f'Slice: {slice_index}')
    axes[0, i].axis('off')
```

### Step 6: Display the Results
Finally, display the plots using plt.show() to visualize the slices of the liver with and without the masks, highlighting areas of interest such as lesions.
This guide provides a structured approach to accessing and visualizing medical imaging data from a specified dataset, focusing on liver CT images and associated masks.

![Demo Figure](assets/demo_fig.png)
<p align="center" style="font-size: 16px;">Sample CECT Image Slice with Segmentations.</p>
<p align="center" style="font-size: 14px;"> This figure presents CECT images from a patient with ID "P0059," diagnosed with HCC. The figure shows five consecutive slices from the arterial phase, all containing the lesion. The first row displays the annotated CECT images: red marks the liver region, and blue highlights the lesion. The second row shows the corresponding CT images of the lesion area, and the third row presents the CT images of the liver area.</p>

For more details, please see the [demo.ipynb](./demo.ipynb) file.
