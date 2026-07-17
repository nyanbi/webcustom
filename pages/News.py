import streamlit as st
import feedparser
import webbrowser

# 1. Cấu hình trang
st.set_page_config(page_title="Multi News", layout="wide")

# --- DANH SÁCH RSS URL CỦA CÁC KÊNH ---
# Bây giờ chúng ta gộp chung thành 1 Dictionary lớn
RSS_FEEDS = {
    # Kênh VnExpress
    "VnExpress - Tin mới nhất": "https://vnexpress.net/rss/tin-moi-nhat.rss",
    "VnExpress - Thời sự": "https://vnexpress.net/rss/thoi-su.rss",
    "VnExpress - Thế giới": "https://vnexpress.net/rss/the-gioi.rss",
    "VnExpress - Kinh doanh": "https://vnexpress.net/rss/kinh-doanh.rss",
    "VnExpress - Khoa học": "https://vnexpress.net/rss/khoa-hoc.rss",
    "VnExpress - Công nghệ": "https://vnexpress.net/rss/cong-nghe.rss",
    "VnExpress - Giải trí": "https://vnexpress.net/rss/giai-tri.rss",
    "VnExpress - Thể thao": "https://vnexpress.net/rss/the-thao.rss",

    # Kênh VTV
    "VTV - Vươn mình bằng AI": "https://vtv.vn/rss/vuon-minh-bang-ai.rss",
    "VTV - Golf": "https://vtv.vn/rss/golf.rss",
    "VTV - Chính trị": "https://vtv.vn/rss/chinh-tri.rss",
    "VTV - Thể thao": "https://vtv.vn/rss/the-thao.rss",
    "VTV - Xã hội": "https://vtv.vn/rss/xa-hoi.rss",
    "VTV - Pháp luật": "https://vtv.vn/rss/phap-luat.rss",
    "VTV - Thế giới": "https://vtv.vn/rss/the-gioi.rss",
    "VTV - Kinh tế": "https://vtv.vn/rss/kinh-te.rss",
    "VTV - Truyền hình": "https://vtv.vn/rss/truyen-hinh.rss",
    "VTV - Văn hóa - Giải trí": "https://vtv.vn/rss/van-hoa-giai-tri.rss",
    "VTV - Đời sống": "https://vtv.vn/rss/doi-song.rss",
    "VTV - Công nghệ": "https://vtv.vn/rss/cong-nghe.rss",
    "VTV - Giáo dục": "https://vtv.vn/rss/giao-duc.rss",
    "VTV - Trực tuyến": "https://vtv.vn/rss/truc-tuyen.rss",
    "VTV - World Cup 2026™": "https://vtv.vn/rss/world-cup-2026.rss",
    "VTV - Vấn đề hôm nay": "https://vtv.vn/rss/van-de-hom-nay.rss",

    # newyorktimes
    "NYT - Tin mới nhất": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    "NYT - Thế giới": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "NYT - Kinh doanh": "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml",
    "NYT - Công nghệ": "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    "NYT - Sức khỏe": "https://rss.nytimes.com/services/xml/rss/nyt/Health.xml",
    "NYT - Thể thao": "https://rss.nytimes.com/services/xml/rss/nyt/Sports.xml",
    "NYT - Khoa học": "https://rss.nytimes.com/services/xml/rss/nyt/Science.xml",
    "NYT - Nghệ thuật": "https://rss.nytimes.com/services/xml/rss/nyt/Arts.xml",

}


# --- PHẦN CSS ĐỔI MÀU GIỐNG PEEK ---
st.markdown("""
<style>
    /* 1. Đổi nền tổng thể sang màu tối */
    .stApp {
        background-color: #121212 !important;
    }
    
    /* 2. Đổi màu chữ sang trắng/xám sáng cho toàn bộ trang web */
    .stApp, h1, h2, h3, h4, h5, p, div, span, .stMarkdown {
        color: #EAEAEA !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif !important;
    }
    
    /* 3. Đổi nền Sidebar sang tối hơn chút */
    section[data-testid="stSidebar"] {
        background-color: #1E1E1E !important;
    }
    
    /* 4. Đổi màu các khung viền (Border) sang xám tối */
    .stVerticalBlockBorderWrapper, div[data-testid="stVerticalBlock"] > div {
        background-color: transparent !important;
        border-color: #333333 !important;
    }
    
    /* 5. Đổi màu nút bấm */
    div.stButton > button {
        background-color: #FACC15 !important; /* Màu vàng neon */
        color: #000000 !important; /* Chữ đen */
        border: none !important;
        border-radius: 6px !important;
        font-weight: bold !important;
    }
    div.stButton > button:hover {
        background-color: #EAB308 !important;
    }
    
    /* 6. NÚT MÀU XANH LÁ (Chỉ dành cho nút ở Sidebar) */
    section[data-testid="stSidebar"] div.stButton > button {
        background-color: #238636 !important; /* Màu xanh lá */
        color: #FFFFFF !important; /* Chữ trắng */
    }
    section[data-testid="stSidebar"] div.stButton > button:hover {
        background-color: #2EA043 !important;
    }
    
    /* 7. Chỉnh màu tiêu đề */
    .stTitle, .stHeader {
        color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)


# 2. Hàm lấy dữ liệu từ RSS
@st.cache_data(ttl=600)
def get_articles_from_rss(feed_url, keyword=""):
    feed = feedparser.parse(feed_url)
    articles = []
    
    for entry in feed.entries:
        title = entry.title
        link = entry.link
        summary = entry.summary if hasattr(entry, 'summary') else ""
        published_time = entry.published if hasattr(entry, 'published') else "Không rõ"
        
        if keyword:
            if keyword.lower() not in title.lower() and keyword.lower() not in summary.lower():
                continue
        
        articles.append({
            'Tiêu đề': title,
            'Tóm tắt': summary,
            'Link': link,
            'Thời gian': published_time
        })
        
    return articles


# 3. Giao diện Bộ lọc ở Sidebar
with st.sidebar:
    st.button("Quay lại đầu trang")
    st.write("---")
    st.header("🔍 Bộ lọc tin")
    
    # 1. Chọn kênh (VnExpress hoặc Skysports)
    # Chúng ta tạo list tên kênh để người dùng chọn
    channel_names = ["VnExpress", "VTV", "NYT"]
    selected_channel_name = st.selectbox("Chọn kênh", channel_names)
    
    # 2. Dựa vào kênh đã chọn để lọc ra các chuyên mục tương ứng
    # Nếu chọn VnExpress, lấy các key có chữ "VnExpress -"
    if selected_channel_name == "VnExpress":
        category_options = [k for k in RSS_FEEDS.keys() if k.startswith("VnExpress -")]
    elif selected_channel_name == "VTV": # Nếu chọn VTV
        category_options = [k for k in RSS_FEEDS.keys() if k.startswith("VTV -")]
    elif selected_channel_name == "NYT": # Nếu chọn NYT
        category_options = [k for k in RSS_FEEDS.keys() if k.startswith("NYT -")]
        
    selected_category_name = st.selectbox("Chọn chuyên mục", category_options)
    
    # Lấy URL từ key đã chọn
    selected_url = RSS_FEEDS[selected_category_name]
    
    search_keyword = st.text_input("Tìm từ khóa", "")
    
    if st.button("Lấy tin mới"):
        with st.spinner(f"Đang tải dữ liệu từ {selected_channel_name}..."):
            articles = get_articles_from_rss(selected_url, search_keyword)
            if articles:
                st.session_state['news_data'] = articles
                st.success(f"Đã tải {len(articles)} bài báo!")
            else:
                st.warning("Không tìm thấy bài báo nào.")


# --- LAYOUT 3 CỘT ---
col_main, col_spacer, col_right = st.columns([5, 1, 2])

# --- CỘT SPACER ---
with col_spacer:
    st.write("")


with col_right:
    with st.container(border=True):
        st.write("")
        st.write("📂 Chuyên mục")
        st.write("---")
        # Hiển thị các chuyên mục của kênh hiện tại
        for cat in category_options:
            st.write(f"- {cat.replace(selected_channel_name + ' - ', '')}")
        st.write("")
        st.write("💡 Hướng dẫn:")
        st.write("Chọn kênh & chuyên mục ở bên trái.")

# --- CỘT CHÍNH ---
with col_main:
    st.write("")
    st.write("")
    st.title("📰 Tin tức tổng hợp")
    st.write("---")
    
    if 'news_data' in st.session_state and st.session_state['news_data']:
        data = st.session_state['news_data']
        
        for idx, article in enumerate(data):
            with st.container(border=True):
                st.subheader(article['Tiêu đề'])
                st.caption(f"🕒 {article['Thời gian']}")
                st.write(article['Tóm tắt'])
                
                if st.button(f"📖 Đọc bài viết", key=f"btn_{idx}"):
                    webbrowser.open(article['Link'])
                
                st.write("---")
    else:
        st.info("👈 Chọn kênh, chuyên mục và bấm 'Lấy tin mới' để bắt đầu.")