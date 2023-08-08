# SR to Annotations/JSON Documentation

This function is used to convert an SR file into an MD.ai Annotation note or JSON format. It is meant to convert the entirety of the SR's **content sequence** into text while keeping note of the referenced studies.

The JSON format will have two fields: "Referenced DICOM" and "SR Content". Referenced DICOM is a list of dictionaries containing a "Study UID" field which points to the referenced studies (indicated by the content sequence's ReferencedSOPSequence tag). SR Content will be a list of lines of text, each containing a field from the SR document.

The annotation note format will import an annotation into the given project and dataset based on the studies that the SR references. The annotation will have a note containing the SR's content. You must initiate an mdai_client for this to work. Additionally, you must go into the UI and create a label, then input the label_id into the function.
______

  Inputs:

    `file_path` - File path to the SR (required)
    `json_out` - Boolean flag to determine if should output to JSON (optional)
    `project_id` & `dataset_id` & `label_id` - Project information necessary to output SR to annotation note. All must be present if any are present. (optional)
    `mdai_client` - mdai client object instantiated by calling `mdai.Client`. Must be present to export SR to annotation note.
Outputs:


  If `json_out` is `True` then there will be a json file in your cwd called "SR_content". If all the project and client information is filled out, then there will be an annotation with the SR content as an annotation note, for each study in the project that is referenced by the SR.


## Example Usage:


```python
import mdai

# Get variables from project info tab and user settings
DOMAIN = 'public.md.ai'
YOUR_PERSONAL_TOKEN = '8b80c4ca0f'
mdai_client = mdai.Client(domain=DOMAIN, access_token=YOUR_PERSONAL_TOKEN)

dataset_id = 'D_0Z4qeN'
project_id = 'L1NpnQBv'
label_id = 'L_QnlPAg'

file_path = 'path_to_SR.dcm'
```

    Successfully authenticated to staging.md.ai.



```python
SR_to_Annot(file_path,
            dataset_id=dataset_id,
            project_id=project_id,
            label_id=label_id,
            mdai_client=mdai_client)
```

    Importing 1 annotations into project L1NpnQBv, dataset D_0Z4qeN...                                  
    Successfully imported 1 / 1 annotations into project L1NpnQBv, dataset D_0Z4qeN.



```python
import mdai

# Get variables from project info tab and user settings
DOMAIN = 'public.md.ai'
YOUR_PERSONAL_TOKEN = '8b80c4ca0f'
mdai_client = mdai.Client(domain=DOMAIN, access_token=YOUR_PERSONAL_TOKEN)

dataset_id = 'D_0Z4qeN'
project_id = 'L1NpnQBv'
label_id = 'L_QnlPAg'

file_path = 'path_to_SR.dcm'
```

    Successfully authenticated to staging.md.ai.



```python
SR_to_Annot(file_path,
            dataset_id=dataset_id,
            project_id=project_id,
            label_id=label_id,
            mdai_client=mdai_client)
```

    Importing 1 annotations into project L1NpnQBv, dataset D_0Z4qeN...                                  
    Successfully imported 1 / 1 annotations into project L1NpnQBv, dataset D_0Z4qeN.

