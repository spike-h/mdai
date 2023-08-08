from PIL import Image, ImageDraw, ImageFont
from urllib.request import urlopen
import requests
import mdai
import re
import random

# Get gpt inforgaphics script. Requires instantiated mdai client using mdai.Client
def gpt_script(report, mdai_client, num_sections):
  prompt = f'Generate text for an infographic explaining the given report in a patient friendly way. Give it in {num_sections} sections.'

  messages = [{"role": "user", "content": report + '/n' + prompt}]
  reply = mdai_client.chat_completion.create(messages, model='gpt-4', temperature=0)

  text = reply['choices'][0]['message']['content']
  text = re.sub('[\n]+', '\n', text) # removes double new line breaks
  text = text.split('\n')

  headers = text[::2]
  texts = text[1::2]

  return headers, texts

def place_text(draw, location, rect, font_url, text, color, title=False):
  # find font size for text `"Hello World, "` to fit in rectangle 200x100
  selected_size = 1
  selected_text = text
  for size in range(5, 150):
    fit = True
    arial = ImageFont.FreeTypeFont(urlopen(font_url), size=size)
    left, top, right, bottom = draw.multiline_textbbox((0,0), text, font=arial)
    w = right - left
    h = bottom - top

    words = text.split()
    new_text = ""

    if w > rect[0]:
      for word in words:
        left, top, right, bottom = draw.multiline_textbbox((0,0), new_text + word + " ", font=arial)
        w = right - left
        h = bottom - top

        if w > rect[0]:
          new_text += '\n' + word + ' '
        else:
          new_text += word + ' '

        if h > rect[1]:
          fit = False
          break

    if new_text != "":
        left, top, right, bottom = draw.multiline_textbbox((0,0), new_text, font=arial)
        w = right - left
        h = bottom - top

    if w > rect[0] or h > rect[1]:
      fit = False
      break

    if fit:
      selected_size = size
      selected_text = new_text

  if selected_text == "":
    selected_text = text

  selected_font = ImageFont.FreeTypeFont(urlopen(font_url), size=selected_size)

  offset = [left, top]
  true_loc =  (location[0] - offset[0], location[1] - offset[1])



  if title:
    draw.text(true_loc, selected_text, fill=color, font=selected_font, anchor='mm')
  else:
    draw.text(true_loc, selected_text, fill=color, font=selected_font, anchor='la')

def draw_all_text(*, template, report, header_positions, header_rects, header_colors, 
                  text_positions, text_rects, text_colors, 
                  img_positions, img_bboxes, num_sections, api_key, mdai_client):
  headers, texts = gpt_script(report, mdai_client, num_sections)

  font_url = 'https://github.com/googlefonts/roboto/blob/main/src/hinted/Roboto-Regular.ttf?raw=true' # not gpt

  # Load image
  image = Image.open(template)
  draw = ImageDraw.Draw(image)

  # Draw headers and texts
  for i in range(len(header_positions)):
    place_text(draw, header_positions[i], header_rects[i], font_url, headers[i], header_colors[i])
    place_text(draw, text_positions[i], text_rects[i], font_url, texts[i], text_colors[i])

  if api_key:
    place_images(image, img_positions, img_bboxes, api_key)

def place_images(original, img_positions, img_bboxes, api_key):
  current = original
  for pos, bbox in zip(img_positions, img_bboxes):
    img = download_random_image(api_key)
    img = img.resize((bbox[0], bbox[1]), Image.ANTIALIAS)

    watermark_layer = Image.new("RGBA", original.size)
    watermark_layer.paste(img, pos)

    watermarked = Image.alpha_composite(current.convert('RGBA'), watermark_layer)
    current = watermarked

  watermarked_rgb = watermarked.convert('RGB')
  watermarked_rgb.save('infographic.jpg', 'JPEG')

def download_random_image(api_key):
  url = "https://pixabay.com/api/"

  params = {
      'key': api_key,
      'q': 'medical',
      'image_type': 'vector',
      'per_page': 200
  }

  response = requests.get(url, params=params)

  if response.status_code == 200:
      data = response.json()
      images = data['hits']
      random_image = random.choice(images)
      image_url = random_image['webformatURL']
      print(image_url)
      response = requests.get(image_url)

      if response.status_code == 200:
          image = Image.open(io.BytesIO(response.content))
          return image
      else:
          print('Unable to download image')
  else:
      print('Unable to fetch images')
