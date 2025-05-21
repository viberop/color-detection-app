import cv2
import streamlit as st
import numpy as np
from utils import load_colors, get_closest_color_name

st.set_page_config(page_title="Color Detection App", layout="centered")

st.title("🎨 Color Detection from Image")

uploaded_file = st.file_uploader("Upload an Image", type=['jpg', 'png', 'jpeg'])

colors_df = load_colors()

if uploaded_file is not None:
    # Convert the file to a numpy array and decode it
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)

    # Resize for display
    image_display = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    st.image(image_display, channels="RGB", use_column_width=True)

    st.write("Click anywhere on the image to detect a color.")
    
    clicked = st.experimental_data_editor(
        pd.DataFrame({"Click the image above to detect a color": [""]}),
        disabled=True,
    )

    # Use Streamlit's mouse click event with OpenCV window
    def click_event(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            b, g, r = image[y, x]
            color_name = get_closest_color_name(r, g, b, colors_df)
            st.session_state['clicked_color'] = {
                'name': color_name,
                'rgb': (r, g, b)
            }

    cv2.namedWindow("Image")
    cv2.setMouseCallback("Image", click_event)

    if 'clicked_color' in st.session_state:
        color_info = st.session_state['clicked_color']
        st.markdown(f"**Color Name:** {color_info['name']}")
        st.markdown(f"**RGB:** {color_info['rgb']}")
        st.markdown(
            f"<div style='width:100px;height:100px;background-color:rgb{color_info['rgb']};'></div>",
            unsafe_allow_html=True,
        )
else:
    st.info("Please upload an image to start detecting colors.")

