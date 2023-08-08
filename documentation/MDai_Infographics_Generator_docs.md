# Report to Infographics using templates


Below is a script to generate an infographics script from a medical report, using mdai's GPT4 api, and then place this script onto an infographics template. The locations and color of the texts have to be predefined. Accompanying images will also be generated, and their locations also have to be predefined. The script will maximize the size of the text to fit in the bounding box.

______

  Inputs:

    `template` - either a file path or file-like object that can be opened with Image.open()
    `num_sections` - the number of header, text pairs you want to include in the infographic. The lengths of the following header and text lists must be equal to num_sections.
    `api_key` - Pexels API key for image scraping. Leave this as "" if you don't want to insert images. If this is "" then the following image arguments will be ingored.
    `header_positions` & `text_positions` & `img_positions` - a list of the top left positions of their corresponding bounding boxes. Indicates where the text/image will be placed. Format: [(x,y),...] in pixels
    `header_rects` & `text_rects` & `img_bboxes` - a list of bounding boxes for the texts/images to be placed in. Format: [[width,height],...]
    `header_colors` & `text_colors` - a list of rbg colors for the headers and texts. Format: [(r,b,g,a),...]
    `mdai_client` - MD.aiclient instantiated with mdai.Client()
Outputs:

`
  There will be a file called infographic.jpg in your cwd with the placed text and images.
`

## Example Usage


```python
import mdai
import io

report = """
Age: 42
History: Family history of breast cancer, mother

Examination: Bilateral Digital 2D Screening Mammogram
Technique: Digital 2D CC and MLO views are obtained.

Findings:

Breast Tissue density: A

There is an oval circumscribed mass measuring 8mm in the upper-outer left breast. An oval circumscribed mass of approximate 8mm is also observed in the middle-outer right breast.

Otherwise, there is no suspicious mass, architectural distortion or group microcalcifications.

Impression:
Right and left breast mass for ultrasound imaging recommended.

BI-RADS 0
"""

header_positions = [(430,326), (430,662), (430,1000), (430,1335)]
header_rects = [[688,33] for i in range(4)]
header_colors = [(238,137,153), (255,245,163), (120,190,130), (137,208,226)]
text_positions = [(430,380), (430,721), (430,1046), (430,1386)]
text_rects = [[684,112] for i in range(4)]
text_colors = [(255, 255, 255, 183) for i in range(4)]
img_positions = [(1405, 299), (1400, 629), (1418, 970), (1406,1289)]
img_bboxes = [[209, 206] for i in range(4)]
num_sections = 4

response = requests.get('https://raw.githubusercontent.com/spike-h/mdai/main/misc/temp.png')
template = io.BytesIO(response.content)


# Get variables from project info tab and user settings
# DOMAIN = 'public.md.ai'
# YOUR_PERSONAL_TOKEN = '8b80c4ca0f0587'
# mdai_client = mdai.Client(domain=DOMAIN, access_token=YOUR_PERSONAL_TOKEN)

draw_all_text(template=template, report=report,
              header_positions=header_positions,
              header_rects=header_rects,
              header_colors=header_colors,
              text_positions=text_positions,
              text_rects=text_rects,
              text_colors=text_colors,
              img_positions=img_positions,
              img_bboxes=img_bboxes,
              num_sections=num_sections,
              api_key = 'kjhfkjahiu2o4u5'
              mdai_client=mdai_client)
```
