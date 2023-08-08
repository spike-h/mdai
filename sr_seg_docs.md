# SR_SEG_Export Documentation

This class is used to export you're MD.ai annotations into DICOM SR or SEG format.

______
### SR Exports
If your output format is SR, all annotations will be converted, capturing the label's and their parent's name in SR format (The specific Code Value of each annotation will be arbitrary). An SR file will be created for each annotator in each annotated **study**. The SR's DICOM data will be consistent with the study it references. The study and annotation information comes from the inputted "Annotation Json" and "Metadata Json" (These jsons have to be referencing the same dataset(s) for it to work).

The labels will be ordered from exam level to series to image. Each image level label will have a "Referenced Image" section preceding the label to indicate it's source. Series labels will have "Series UID: xxx" under them for better referencing as well.
______
### Segmentation Exports
If your output format is SEG, only local annotations will be exported. This export process converts the annotation data into a binary mask, and creates the relevant segmentation DICOM data to export a DICOM Segmentation file. A Segmentation file will be created for each annotator in each annotated **series**. Additionally, if `combine_label_groups` is `False`, a different file will be created for each label group. The file's DICOM headers will be consistent with the original DICOM's. The study and annotation information comes from the inputted "Annotation Json" and "Metadata Json" (These jsons have to be referencing the same dataset(s) for it to work).

The segmentation frames are grouped together by their labels and within those groups, they are ordered by their source's frame number.
______

  Inputs:

    `output_format` - determines if the output should be in DICOM SR/SEG
                      (accepted inputs are "SR" or "SEG")
    `annotation_json` & `metadata_json` - are the exported annotation and metadata json paths from the md.ai project
                                          MAKE SURE THE DATASETS MATCH UP
    `combine_label_groups` - If `True` then each SEG file includes the annotations from every label group for that series
                             If `False` then a different SEG file will be created for each different label group annotation
                            (only applies to SEG output. Will be ignored for SR)
    `output_dir` - Specifies where the files should be downloaded
                   If None then files will be placed in a "SR(or SEG)_OUTPUT" folder in your cwd.
Outputs:

`
  There will be a folder in your cwd, specified by the output_dir parameter, containing your SR/SEG exports.
`

## Example Usage:


```python
# Generated from Clarence's GPT documentation project

import mdai
from glob import glob

# Define your personal token and project id
personal_token = '8b80c4ca0f05'
project_id = 'LFdpnJGv'

# Create an mdai client
mdai_client = mdai.Client(domain='public.md.ai', access_token=personal_token)

# Download the annotation data only (all label groups)
p = mdai_client.project(project_id, path='.',  annotations_only=True)

# Download only the DICOM metadata
p = mdai_client.download_dicom_metadata(project_id, format ='json', path='.')

# Use glob to find the downloaded json files (or get them manually)
annotation_file = glob('*annotations*.json')[0]
metadata_file = glob('*dicom_metadata*.json')[0]

# Use the SR_SEG_Export class to export the annotations to DICOM SR/SEG format

# Should replace to mdai.SR_SEG_Export once integrated with library
exporter = SR_SEG_Export(
    output_format = 'SEG',
    annotation_json = annotation_file,
    metadata_json = metadata_file,
    output_dir = 'out_folder'
)
```
