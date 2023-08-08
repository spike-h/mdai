# Report to SR
This function  inputs a report as a string/text file/directory of text files and outputs an SR document containing the information as text values.

**WARNING**: this just creates a bare bones SR document where the observations are just stored as text. There are no specified codes
         associated with any of the observations/fields on the outputted SR document.
         This is mainly for ease of viewing/transporting reports within a PACS/healthcare system.
         
**TODO**:
      
      - Add Patient and Observer/institution demographics (fields highlighted below)
      
      - Change Name of outputted document
      
      - Change title from "SR Report"

# Example Usage


```python
input_report = """
Procedure: [CT of the Abdomen without contrast]

Comparison: [None.]

Indications: [Patient diagnosed with stage 2 Hepatocellular carcinoma (HCC).]

Technique: [CT images were created without intravenous contrast.]

Findings

Liver: [A single, well-defined lesion measuring approximately 3 cm in diameter is noted in the right lobe of the liver, consistent with the known diagnosis of HCC. No other focal lesions are identified.]

Impression

[Findings are consistent with the known diagnosis of stage 2 Hepatocellular carcinoma. The lesion appears to be localized to the liver with no evidence of metastasis or vascular invasion. Recommend follow-up with oncology for further management.]
"""

report_to_SR(input_report)
```

OR

```python
report_to_SR('/content/report.txt')
```

OR

```python
report_to_SR('/content/Untitled Folder')
```
