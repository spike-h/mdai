import re, os
import pydicom
from datetime import datetime
from pydicom.dataset import Dataset, FileMetaDataset
from pydicom.sequence import Sequence

"""
Function which inputs a report as a string/text file/directory of text files and outputs an SR document containing the information as text values

WARNING: this just creates a bare bones SR document where the observations are just stored as text. There are no specified codes
         associated with any of the observations/fields on the outputted SR document.
         This is mainly for ease of viewing/transporting reports within a PACS/healthcare system.
         
TODO: - Add Patient and Observer/institution demographics (fields highlighted below)
      - Change Name of outputted document
      - Change title from "SR Report"

Created by Dyllan (spike) Hofflich (8/8/23)
"""
def report_to_SR(input_report):
  if os.path.exists(input_report):
    if os.path.isdir(input_report):
      reports = []
      directory = os.fsencode(input_report)
      for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".txt"):
          filepath = os.path.join(input_report, filename)
          with open(filepath) as f:
            lines = f.readlines()
          reports.append(''.join(lines))
    else:
      if not input_report.endswith(".txt"):
        raise "Input_report was a file path but not a text file"
      with open(input_report) as f:
        lines = f.readlines()
      reports = [''.join(lines)]
  else:
    reports = [input_report]

  i = 0
  for report in reports:
    i += 1
    # Define headers for the report and SR document
    headings = ['Procedure', 'Technique', 'History', 'Comparison', 'Indications', 'Findings', 'Impression']

    # Separate the report into a list of [header, text, header, text...]
    pattern = "|".join(headings)
    good_list = []
    regex_pattern = r'(' + pattern + r')\n|(' + pattern + r'):' # Separates out headers which are followed by new lines or a new line then followed by a colon
    trash = re.split(regex_pattern, report, flags=re.IGNORECASE)
    for line in trash:
      if not line:
        continue
      text = line.strip()
      # text = re.sub(r'^\[(.*?)\]$', r'\1', text) # Removes square brackets from text lines [Findings: blah.] becomes Findings: blah.
      if text == '':
        continue
      good_list.append(text)

    instance_uid = pydicom.uid.generate_uid(prefix=None)
    series_uid = pydicom.uid.generate_uid(prefix=None)
    study_uid = pydicom.uid.generate_uid(prefix=None)
    date = datetime.now().strftime('%Y%m%d')
    time = datetime.now().strftime('%H%M%S')

    # File meta info data elements
    file_meta = FileMetaDataset()
    file_meta.FileMetaInformationGroupLength = 196
    file_meta.FileMetaInformationVersion = b'\x00\x01'
    file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.88.22'
    file_meta.MediaStorageSOPInstanceUID = instance_uid
    file_meta.TransferSyntaxUID = '1.2.840.10008.1.2.1'
    file_meta.ImplementationClassUID = '1.2.826.0.1.3680043.8.498.1'

    # Main data elements
    ds = Dataset()
    ds.SpecificCharacterSet = 'ISO_IR 192'
    ds.SOPClassUID = '1.2.840.10008.5.1.4.1.1.88.22'
    ds.SOPInstanceUID = instance_uid
    ds.StudyDate = str(date)
    ds.SeriesDate = str(date)
    ds.ContentDate = str(date)
    ds.StudyTime = str(time)
    ds.SeriesTime = str(time)
    ds.ContentTime = str(time)

    ds.StudyInstanceUID = str(study_uid)   # Study Instance UID
    ds.SeriesInstanceUID = str(series_uid)   # Series Instance UID
    ds.SeriesNumber = str(1)           # Series Number

    ds.Modality = 'SR'
    ds.Manufacturer = 'MDAI'

    # Coding Scheme Identification Sequence
    coding_scheme_identification_sequence = Sequence()
    ds.CodingSchemeIdentificationSequence = coding_scheme_identification_sequence

    # Coding Scheme Identification Sequence: Coding Scheme Identification 1
    coding_scheme_identification1 = Dataset()
    coding_scheme_identification_sequence.append(coding_scheme_identification1)
    coding_scheme_identification1.CodingSchemeDesignator = 'DCM'

    ds.StudyDescription = 'SR Report'

    # Procedure Code Sequence
    procedure_code_sequence = Sequence()
    ds.ProcedureCodeSequence = procedure_code_sequence

    ds.SeriesDescription = 'DICOM SR Report'

    # Referenced Performed Procedure Step Sequence
    refd_performed_procedure_step_sequence = Sequence()
    ds.ReferencedPerformedProcedureStepSequence = refd_performed_procedure_step_sequence

#-------------------------------------------------------------------------------------------
    # Patient and Institution Demographics
    ds.PatientName = ''
    ds.PatientID = ''
    ds.PatientBirthDate = ''
    ds.PatientSex = ''
    ds.AccessionNumber = ''
    ds.ReferringPhysicianName = ''
    ds.StudyID = ''
    ds.InstanceNumber = 1


    ds.InstitutionName = ''
    ds.InstitutionCodeSequence = Sequence()
    ds.ObservationDateTime = ''
#-------------------------------------------------------------------------------------------

    ds.ValueType = 'CONTAINER'

    # Concept Name Code Sequence
    concept_name_code_sequence = Sequence()
    ds.ConceptNameCodeSequence = concept_name_code_sequence

#-------------------------------------------------------------------------------------------
# Name for Document Header
    # Concept Name Code Sequence: Concept Name Code 1
    concept_name_code1 = Dataset()
    concept_name_code_sequence.append(concept_name_code1)
    concept_name_code1.CodeValue = '270000'
    concept_name_code1.CodingSchemeDesignator = '99MDAI'
    concept_name_code1.CodeMeaning = 'SR Report'
#-------------------------------------------------------------------------------------------

    ds.ContinuityOfContent = 'SEPARATE'

    # Author Observer Sequence
    author_observer_sequence = Sequence()
    author_observer_sequence.PersonIdentificationCodeSequence = Sequence()
    ds.AuthorObserverSequence = author_observer_sequence

    # Author Observer Sequence: Author Observer 1
    author_observer1 = Dataset()
    author_observer_sequence.append(author_observer1)
    author_observer1.ObserverType = 'PSN'
    author_observer1.PersonName = 'Referring Physician'

    # Performed Procedure Code Sequence
    performed_procedure_code_sequence = Sequence()
    ds.PerformedProcedureCodeSequence = performed_procedure_code_sequence

    ds.CompletionFlag = 'COMPLETE'
    ds.VerificationFlag = 'UNVERIFIED'

    # Content Template Sequence
    content_template_sequence = Sequence()
    ds.ContentTemplateSequence = content_template_sequence

    # Content Sequence
    content_sequence = Sequence()
    ds.ContentSequence = content_sequence

    header_dataset = None
    for line in good_list:
      if line in headings:
        # Content Sequence: Content 2
        content2 = Dataset()
        content_sequence.append(content2)
        content2.RelationshipType = 'CONTAINS'
        content2.ValueType = 'CONTAINER'

        # Concept Name Code Sequence
        concept_name_code_sequence = Sequence()
        content2.ConceptNameCodeSequence = concept_name_code_sequence

        # Concept Name Code Sequence: Concept Name Code 1
        concept_name_code1 = Dataset()
        concept_name_code_sequence.append(concept_name_code1)
        concept_name_code1.CodeValue = str(hash(line))[1:6]
        concept_name_code1.CodingSchemeDesignator = '99MDAI'
        concept_name_code1.CodeMeaning = line

        content2.ContinuityOfContent = 'SEPARATE'
        header_dataset = content2
      else:
        # Content Sequence
        content_sequence_1 = Sequence()
        header_dataset.ContentSequence = content_sequence_1

        # Content Sequence: Content 1
        content1 = Dataset()
        content_sequence_1.append(content1)
        content1.RelationshipType = 'CONTAINS'
        content1.ValueType = 'TEXT'

        # Concept Name Code Sequence
        concept_name_code_sequence = Sequence()
        content1.ConceptNameCodeSequence = concept_name_code_sequence

        content1.TextValue = line
        content1.ContinuityOfContent = 'SEPARATE'

        # Content Template Sequence
        content_template_sequence = Sequence()
        content1.ContentTemplateSequence = content_template_sequence

    ds.file_meta = file_meta
    ds.is_implicit_VR = False
    ds.is_little_endian = True
#-------------------------------------------------------------------------------------------
# File Name
    ds.save_as(f'{os.getcwd()}/Report_from_SR_{i}.dcm', write_like_original=False)
#-------------------------------------------------------------------------------------------
