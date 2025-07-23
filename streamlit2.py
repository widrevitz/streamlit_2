import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.title("Baba Ben's Magic Image Improver Show")

# Load default image from local file
DEFAULT_IMAGE_PATH = "potatohead.png"  # Make sure this is in the same folder or subfolder

st.subheader("Baba Ben thinking about next big Computer Vision Trick!")
default_img = cv2.imread(DEFAULT_IMAGE_PATH)
if default_img is not None:
    default_img_rgb = cv2.cvtColor(default_img, cv2.COLOR_BGR2RGB)
    st.image(default_img_rgb, caption="Default Image", use_container_width=True)
else:
    st.warning("Default image not found!")

# File uploader for user to select an image
uploaded_file = st.file_uploader("Upload an image from your own files!   Baba will show it, then show his improved version.  Try to upload a pooly lit one to see full effect", type=["png", "jpg", "jpeg"])

if uploaded_file:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    user_img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if user_img is not None:
        user_img_rgb = cv2.cvtColor(user_img, cv2.COLOR_BGR2RGB)
        st.subheader("Uploaded Image:")
        st.image(user_img_rgb, caption="Original", use_container_width=True)

        # Histogram Equalization
        st.subheader("Equalized Image: ... artificially 'improve' your picture. Improvement will improve some sections and worsen others!")

        def equalize_image(img):
            if len(img.shape) == 2:
                return cv2.equalizeHist(img)
            elif len(img.shape) == 3 and img.shape[2] == 3:
                ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
                ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
                return cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)
            else:
                return img

        equalized = equalize_image(user_img)
        equalized_rgb = cv2.cvtColor(equalized, cv2.COLOR_BGR2RGB)
        st.image(equalized_rgb, caption="Equalized", use_container_width=True)

    else:
        st.error("Could not read uploaded image.")
