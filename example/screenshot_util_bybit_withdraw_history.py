import textwrap

import cv2
from PIL import Image
from aiogram.utils.markdown import bold
from matplotlib import pyplot as plt

import editor
import editor2
import editor_center
import editor_gradient
import editor_many_color_center_and_font_size
import editor_text_left
import image_crop
import screenshot_writer
import text_center



def reduce_image_size_by_half(input_path, output_path):
    # Open the image
    img = Image.open(input_path)

    # Get original dimensions
    original_width, original_height = img.size

    # Calculate new dimensions
    new_width = original_width // 2
    new_height = original_height // 2

    # Resize with modern resampling filter
    resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Save the result
    resized_img.save(output_path)
    print(f"Image saved to {output_path} with size {new_width}x{new_height}")


def execute(tran_1, tran_2, tran_3, payment, lead_bank, lead_number, persa_number, time_in_description, country_type, input_naming, output_naming):
    fonts_regular = "fonts/ibm-plex-sans-regular.ttf"
    if country_type == "VED":
        country_type = "Bs"

    tran_1 = f"{tran_1} {country_type}"
    tran_2 = f"{tran_2} {country_type}"
    tran_3 = f"{tran_3} {country_type}"
    payment = f"{payment} {country_type}"
    lead_number = f"{lead_number}****"
    persa_number = f"{persa_number}****"

    white = (50, 250, 250)

    fs = 54
    editor_center.execute(fs, input_naming, output_naming, tran_1, (2049, 845 - fs / 2), (2341, 845 - fs / 2), text_color=white, font_family=fonts_regular)
    editor_center.execute(fs, output_naming, output_naming, tran_2, (2049, 1010 - fs / 2), (2341, 1010 - fs / 2), text_color=white, font_family=fonts_regular)
    editor_center.execute(fs, output_naming, output_naming, tran_1, (2049, 1177 - fs / 2), (2341, 1177 - fs / 2), text_color=white, font_family=fonts_regular)
    editor_center.execute(fs, output_naming, output_naming, tran_2, (2049, 1340 - fs / 2), (2341, 1340 - fs / 2), text_color=white, font_family=fonts_regular)
    editor_center.execute(fs, output_naming, output_naming, tran_3, (2049, 1504 - fs / 2), (2341, 1504 - fs / 2), text_color=white, font_family=fonts_regular)
    editor_center.execute(fs, output_naming, output_naming, payment, (2049, 1666 - fs / 2), (2341, 1666 - fs / 2), text_color=white, font_family=fonts_regular)

    editor_center.execute(fs, output_naming, output_naming, lead_bank, (1607, 845 - fs / 2), (1754, 845 - fs / 2), text_color=white, font_family=fonts_regular)
    editor_center.execute(fs, output_naming, output_naming, lead_bank, (1607, 1010 - fs / 2), (1754, 1010 - fs / 2), text_color=white, font_family=fonts_regular)
    editor_center.execute(fs, output_naming, output_naming, lead_bank, (1607, 1177 - fs / 2), (1754, 1177 - fs / 2), text_color=white, font_family=fonts_regular)
    editor_center.execute(fs, output_naming, output_naming, lead_bank, (1607, 1340 - fs / 2), (1754, 1340 - fs / 2), text_color=white, font_family=fonts_regular)
    editor_center.execute(fs, output_naming, output_naming, lead_bank, (1607, 1504 - fs / 2), (1754, 1504 - fs / 2), text_color=white, font_family=fonts_regular)
    editor_center.execute(fs, output_naming, output_naming, lead_bank, (1607, 1666 - fs / 2), (1754, 1666 - fs / 2), text_color=white, font_family=fonts_regular)

    editor_center.execute(fs, output_naming, output_naming, lead_number, (937, 845 - fs / 2), (1387, 845 - fs / 2), text_color=white, font_family=fonts_regular)
    editor_center.execute(fs, output_naming, output_naming, lead_number, (937, 1010 - fs / 2), (1387, 1010 - fs / 2), text_color=white, font_family=fonts_regular)
    editor_center.execute(fs, output_naming, output_naming, lead_number, (937, 1177 - fs / 2), (1387, 1177 - fs / 2), text_color=white, font_family=fonts_regular)
    editor_center.execute(fs, output_naming, output_naming, lead_number, (937, 1340 - fs / 2), (1387, 1340 - fs / 2), text_color=white, font_family=fonts_regular)
    editor_center.execute(fs, output_naming, output_naming, lead_number, (937, 1504 - fs / 2), (1387, 1504 - fs / 2), text_color=white, font_family=fonts_regular)
    editor_center.execute(fs, output_naming, output_naming, persa_number, (937, 1666 - fs / 2), (1387, 1666 - fs / 2), text_color=white, font_family=fonts_regular)

    editor.execute(fs, output_naming, output_naming, time_in_description, (416, 845), text_color=white, font_family=fonts_regular)
    editor.execute(fs, output_naming, output_naming, time_in_description, (416, 1010), text_color=white, font_family=fonts_regular)
    editor.execute(fs, output_naming, output_naming, time_in_description, (416, 1177), text_color=white, font_family=fonts_regular)
    editor.execute(fs, output_naming, output_naming, time_in_description, (416, 1340), text_color=white, font_family=fonts_regular)
    editor.execute(fs, output_naming, output_naming, time_in_description, (416, 1504), text_color=white, font_family=fonts_regular)
    editor.execute(fs, output_naming, output_naming, time_in_description, (416, 1666), text_color=white, font_family=fonts_regular)


    # reduce_image_size_by_half(output_naming, output_naming)

    img = cv2.imread(output_naming)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
    plt.imshow(img_rgb)
    plt.show()


if __name__ == "__main__":
    execute("12421", "234", "234",  "234", "234", "234",  "Rewfwef Fsdfsdfd", "423423432", "MXN", "SCREENSHOT/MXN_BYBIT_WITHDRAW_HISTORY.png", "output/MXN_BYBIT_WITHDRAW_HISTORY.png")
