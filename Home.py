import streamlit as st
import time

# 1. Cấu hình trang
st.set_page_config(page_title="Thuần Python UI", layout="wide")

# --- HIỆU ỨNG GÕ CHỮ ---
placeholder = st.empty()
typed_text = ""
text = "Welcome to website"

for char in text:
    typed_text += char
    placeholder.markdown(f"<h1 style=''>{typed_text}</h1>", unsafe_allow_html=True)
    time.sleep(0.05)

# 2. Khởi tạo session state
if 'output_content' not in st.session_state:
    st.session_state.output_content = ""

# 3. Chia layout GIỮ NGUYÊN 3 cột
col_main, col_spacer, col_right = st.columns([5, 1, 2])

# --- CỘT SPACER ---
with col_spacer:
    st.write("") # Khoảng trắng giữa


# --- CỘT CHÍNH (Bên trái) ---
with col_main:
    st.write("")
    st.write("")
    
    # Hộp Output
    output_box = st.text_area("", value=st.session_state.output_content, height=200)
    st.write("") 

    # Input và Button
    col_input, col_button = st.columns([4, 1])
    with col_input:
        user_input = st.text_input("", placeholder="input", label_visibility="collapsed")
    with col_button:
        clicked = st.button("btn")

    # Logic xử lý
    if clicked and user_input:
        st.session_state.output_content += user_input + "\n"
        st.rerun()