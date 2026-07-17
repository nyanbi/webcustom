import streamlit as st
import feedparser
import webbrowser

# 1. Cấu hình trang
st.set_page_config(page_title="VnExpress News", layout="wide")
st.markdown('<div id="top"></div>', unsafe_allow_html=True)

# --- DANH SÁCH RSS URL CỦA VNEXPRESS ---
RSS_FEEDS = {
    "Tin mới nhất": "https://vnexpress.net/rss/tin-moi-nhat.rss",
    "Thời sự": "https://vnexpress.net/rss/thoi-su.rss",
    "Thế giới": "https://vnexpress.net/rss/the-gioi.rss",
    "Kinh doanh": "https://vnexpress.net/rss/kinh-doanh.rss",
    "Khoa học": "https://vnexpress.net/rss/khoa-hoc.rss",
    "Công nghệ": "https://vnexpress.net/rss/cong-nghe.rss",
    "Giải trí": "https://vnexpress.net/rss/giai-tri.rss",
    "Thể thao": "https://vnexpress.net/rss/the-thao.rss",
}

# --- CSS TẠO HIỆU ỨNG STICKY CHO CỘT PHẢI ---
st.markdown("""
<style>
    /* Chỉ áp dụng cho cột bên phải (Dựa vào vị trí thứ 3 trong layout [5, 1, 2]) */
    div[data-testid="stVerticalBlock"] > div:nth-child(3) > div {
        position: sticky !important;
        top: 70px !important; /* Cách đỉnh màn hình 70px để không che tiêu đề */
        height: fit-content !important;
        max-height: 85vh !important; /* Không cho khung cao quá 85% màn hình */
        overflow-y: auto !important; /* Thêm thanh cuộn nếu nội dung quá dài */
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
    st.markdown(
        "<div style='text-align:center; margin-bottom: 10px;'>"
        "<a href='#top' style='display:block; width:100%; padding:8px 0; background:#f0f2f6; border-radius:8px; text-decoration:none; color:#000; font-weight:600;'>🔼 Quay lại đầu trang</a>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.write("---")
    st.header("🔍 Bộ lọc tin")
    selected_category_name = st.selectbox("Chọn chuyên mục", list(RSS_FEEDS.keys()))
    selected_url = RSS_FEEDS[selected_category_name]
    
    search_keyword = st.text_input("Tìm từ khóa", "")
    
    if st.button("Lấy tin mới"):
        with st.spinner("Đang tải dữ liệu RSS..."):
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
    # CSS Sticky ở trên sẽ giữ cột này lơ lửng cố định khi cuộn chuột
    with st.container(border=True):
        st.write("")
        st.write("📂 Chuyên mục")
        st.write("---")
        
        
        for cat in RSS_FEEDS.keys():
            st.write(f"- {cat}")
        st.write("")
        st.write("💡 Hướng dẫn:")
        st.write("Chọn chuyên mục ở bên trái.")

# --- CỘT CHÍNH (Hiển thị tin tức) ---
with col_main:
    st.write("")
    st.write("")
    st.title("📰 Báo VnExpress")
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
        st.info("👈 Chọn chuyên mục và bấm 'Lấy tin mới' để bắt đầu.")