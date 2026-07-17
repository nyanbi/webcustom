import streamlit as st
import feedparser
import re

# 1. Cấu hình trang hiển thị rộng rãi giống giao diện video
st.set_page_config(page_title="Multi News - Peek Style", layout="wide")

# --- DANH SÁCH RSS URL CỦA CÁC KÊNH ---
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

# --- PHẦN CSS ĐỔI MÀU DARK MODE GIỐNG PEEK ---
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
    
    /* 4. Tùy chỉnh các khối khung hiển thị tin tức */
    .news-card {
        background-color: #1A1A1A !important;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        border: 1px solid #2D2D2D !important;
    }
    .news-title {
        font-size: 20px;
        font-weight: bold;
        color: #FFFFFF !important;
        text-decoration: none !important;
    }
    .news-title:hover {
        color: #FACC15 !important;
    }
    .news-meta {
        font-size: 13px;
        color: #A3A3A3 !important;
        margin-top: 5px;
        margin-bottom: 10px;
    }
    
    /* 5. Tùy chỉnh khối Tin Nóng bên cột phải */
    .hot-news-box {
        background-color: #1E1E1E !important;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #2D2D2D !important;
        margin-bottom: 15px;
    }
    .hot-title {
        font-size: 14px;
        font-weight: 600;
        color: #EAEAEA !important;
        text-decoration: none !important;
    }
    .hot-title:hover {
        color: #FACC15 !important;
    }
    .badge-live {
        background-color: #DC3545;
        color: white !important;
        padding: 2px 6px;
        font-size: 10px;
        font-weight: bold;
        border-radius: 4px;
        float: right;
    }

    /* 6. Đổi màu các nút bấm mặc định của Streamlit */
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
    
    /* NÚT ĐỌC BÀI VIẾT (Link giả lập Button để hoạt động chuẩn trên trình duyệt) */
    .read-btn {
        display: inline-block;
        background-color: #FACC15 !important;
        color: #000000 !important;
        padding: 8px 16px;
        font-weight: bold;
        border-radius: 6px;
        text-decoration: none !important;
        margin-top: 10px;
        font-size: 14px;
    }
    .read-btn:hover {
        background-color: #EAB308 !important;
    }
    
    /* 7. NÚT MÀU XANH LÁ (Chỉ dành cho nút ở Sidebar) */
    section[data-testid="stSidebar"] div.stButton > button {
        background-color: #238636 !important; /* Màu xanh lá */
        color: #FFFFFF !important; /* Chữ trắng */
    }
    section[data-testid="stSidebar"] div.stButton > button:hover {
        background-color: #2EA043 !important;
    }
</style>
""", unsafe_allow_html=True)

# Hàm dọn dẹp các thẻ HTML/Thẻ ảnh lỗi trong phần mô tả RSS
def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

# 2. Hàm lấy dữ liệu từ RSS
@st.cache_data(ttl=600)
def get_articles_from_rss(feed_url, keyword=""):
    feed = feedparser.parse(feed_url)
    articles = []
    
    for entry in feed.entries:
        title = entry.title
        link = entry.link
        summary = clean_html(entry.summary) if hasattr(entry, 'summary') else ""
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
    if st.button("Quay lại đầu trang"):
        st.components.v1.html("<script>window.parent.scrollTo(0,0);</script>", height=0)
    st.write("---")
    st.header("🔍 Bộ lọc tin")
    
    channel_names = ["VnExpress", "VTV", "NYT"]
    selected_channel_name = st.selectbox("Chọn kênh", channel_names)
    
    # Lọc chuyên mục tự động dựa trên kênh đã chọn
    category_options = [k for k in RSS_FEEDS.keys() if k.startswith(f"{selected_channel_name} -")]
    selected_category_name = st.selectbox("Chọn chuyên mục", category_options)
    
    selected_url = RSS_FEEDS[selected_category_name]
    search_keyword = st.text_input("Tìm từ khóa", "")
    
    if st.button("Lấy tin mới") or 'news_data' not in st.session_state:
        with st.spinner(f"Đang tải dữ liệu từ {selected_channel_name}..."):
            articles = get_articles_from_rss(selected_url, search_keyword)
            st.session_state['news_data'] = articles
            st.session_state['current_category'] = selected_category_name

# Lấy dữ liệu tin đã lưu trong session_state
data = st.session_state.get('news_data', [])
display_category_name = st.session_state.get('current_category', selected_category_name)

# --- BỐ CỤC HAI CỘT SÁT NHAU (Tỉ lệ 3.5 : 1.5 chuẩn phong cách Video) ---
col_main, col_right = st.columns([3.5, 1.5], gap="large")

# --- CỘT PHẢI: TIN NÓNG LIVE & CHUYÊN MỤC ---
with col_right:
    st.markdown("### 🔥 Tin nóng <span class='badge-live'>LIVE</span>", unsafe_allow_html=True)
    st.write("---")
    
    # Tạo danh sách tin nóng (lấy từ bài thứ 10 trở đi hoặc lấy 5 bài đầu nếu danh sách ngắn)
    hot_entries = data[10:15] if len(data) > 12 else data[:5]
    
    if hot_entries:
        for idx, article in enumerate(hot_entries):
            st.markdown(f"""
                <div class='hot-news-box'>
                    <span style='color: #888888; font-size: 12px; font-weight: bold;'>#{idx+1} Xu hướng</span><br>
                    <a class='hot-title' href='{article["Link"]}' target='_blank'>{article["Tiêu đề"]}</a>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.caption("Chưa có danh sách tin nóng xu hướng.")
        
    st.write("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.write("📂 Danh sách chuyên mục")
        st.write("---")
        for cat in category_options:
            st.write(f"- {cat.replace(selected_channel_name + ' - ', '')}")
        st.write("")
        st.caption("💡 Mẹo: Chọn kênh & chuyên mục ở thanh Sidebar bên trái rồi nhấn 'Lấy tin mới'.")

# --- CỘT CHÍNH: BẢNG TIN Ở GIỮA ---
with col_main:
    st.markdown(f"<h1 style='margin-bottom:0px;'>📰 {display_category_name}</h1>", unsafe_allow_html=True)
    st.write("---")
    
    if data:
        # Hiển thị tối đa 10 bài viết ở luồng tin chính
        for article in data[:10]:
            st.markdown(f"""
                <div class='news-card'>
                    <a class='news-title' href='{article["Link"]}' target='_blank'>{article["Tiêu đề"]}</a>
                    <div class='news-meta'>🕒 {article["Thời gian"]}</div>
                    <p style='color: #CCCCCC; font-size: 15px; line-height: 1.6;'>{article["Tóm tắt"][:280]}...</p>
                    <a class='read-btn' href='{article["Link"]}' target='_blank'>📖 Đọc bài viết</a>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("👈 Hãy chọn kênh, chuyên mục và bấm 'Lấy tin mới' để bắt đầu trải nghiệm hệ thống cập nhật.")