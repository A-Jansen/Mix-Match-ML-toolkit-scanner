import streamlit as st
from PIL import Image
import numpy as np
import easyocr
from oocsi_source import OOCSI

if 'oocsi' not in st.session_state:
    st.session_state.oocsi = OOCSI('', 'oocsi.id.tue.nl')

labeled_data_tokens = {
    'Audio': {'Char': 'a', 'ASCII code': 97},
    'Image': {'Char': 'b', 'ASCII code': 98},
    'table': {'Char': 'c', 'ASCII code': 99},
    'text': {'Char': 'd', 'ASCII code': 100},
    'series': {'Char': 'e', 'ASCII code': 101},
    'video': {'Char': 'f', 'ASCII code': 102}
}

unlabeled_data_tokens = {
    'Audio*': {'Char': 'g', 'ASCII code': 103},
    'Image*': {'Char': 'h', 'ASCII code': 104},
    'table*': {'Char': 'i', 'ASCII code': 105},
    'text*': {'Char': 'j', 'ASCII code': 106},
    'series*': {'Char': 'k', 'ASCII code': 107},
    'video*': {'Char': 'l', 'ASCII code': 108}
}

supervised_learning_tokens = {
    'Categorize': {'Char': 'm', 'ASCII code': 109},
    'Foresee': {'Char': 'n', 'ASCII code': 110},
    'Identify': {'Char': 'o', 'ASCII code': 111},
    'Communicate': {'Char': 'q', 'ASCII code': 113},
    'Translate': {'Char': 'u', 'ASCII code': 117},
    'Understand': {'Char': 'z', 'ASCII code': 122}
}

unsupervised_learning_tokens = {
    'Cluster': {'Char': 'p', 'ASCII code': 112},
    'Distinguish': {'Char': 'r', 'ASCII code': 114},
    'Generate': {'Char': 's', 'ASCII code': 115},
    'Recommend': {'Char': 't', 'ASCII code': 116}
}

reinforcement_learning_tokens = {
    'Navigate': {'Char': 'B', 'ASCII code': 66},
    'Optimize': {'Char': 'x', 'ASCII code': 120}
}


token_dicts = {
    'labeled': labeled_data_tokens,
    'unlabeled': unlabeled_data_tokens,
    'supervised_learning_tokens': supervised_learning_tokens,
    'unsupervised_learning_tokens': unsupervised_learning_tokens,
    'reinforcement_learning_tokens': reinforcement_learning_tokens
}


def photoTaken():
    print("Yeahhh!")


reader = easyocr.Reader(['tr', 'en'], gpu=False)


def detect_tokens(ocr_output, token_dicts):
    detected_tokens = set()
    token_set = set()

    for bbox, text, confidence in ocr_output:
        # Extracting the text and bounding box coordinates
        text = text.lower()
        print(text)
        x_values = [point[0] for point in bbox]
        y_values = [point[1] for point in bbox]
        min_x, max_x = min(x_values), max(x_values)
        min_y, max_y = min(y_values), max(y_values)
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2
        # print(text)
        # Checking proximity to each type in the dictionary
        for token_type, token_dict in token_dicts.items():
            for token, info in token_dict.items():
                ascii_code = info['ASCII code']
                if token.lower() == text:
                    # print(text)
                    if 'unlabeled' in text.lower():
                        detected_tokens.add(
                            (token, 'labeled_data_tokens', ascii_code))
                    elif 'labeled' in text.lower():
                        detected_tokens.add(
                            (token, 'unlabeled_data_tokens', ascii_code))
                    else:
                        print("else")
                        detected_tokens.add(
                            (token))
                        token_set.add(ascii_code)

    return detected_tokens, token_set


oocsi_channel = st.text_input(
    'OOCSI channel (enter from the website)', 'MMMLtoolkit_')

img_file_buffer = st.camera_input(
    "Take a picture of your tokens", on_change=photoTaken)
# rand_nium = np.random.rand(1)
# print(img_file_buffer)
print(",,,,")

if img_file_buffer is not None:

    # To read image file buffer as a PIL Image:
    img = Image.open(img_file_buffer)

    # To convert PIL Image to numpy array:
    img_array = np.array(img)
    result = reader.readtext(img_array)  # turn image to numpy array
    # print(result)
    with st.spinner('Wait for it...'):

        detected_tokens, token_set = detect_tokens(result, token_dicts)
        token_array = list(token_set)
        print(detected_tokens)
        print(token_array)
    st.success(detected_tokens)
    # print(result)
    st.session_state.oocsi.send(oocsi_channel, {
        "tokens": token_array
    })
