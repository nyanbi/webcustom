import streamlit as st
import feedparser
import re
from collections import Counter

# 1. Page Configuration
st.set_page_config(page_title="Multi News - Peek Style", layout="wide")

# --- RSS FEEDS DICTIONARY ---
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

# --- PEEK DARK MODE CSS CUSTOMIZATION ---
st.markdown("""
<style>
    .stApp { background-color: #121212 !important; }
    
    .stApp, h1, h2, h3, h4, h5, p, div, span, .stMarkdown {
        color: #EAEAEA !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif !important;
    }
    
    section[data-testid="stSidebar"] { background-color: #1E1E1E !important; }
    
    .news-card {
        background-color: #1A1A1A !important;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        border: 1px solid #2D2D2D !important;
    }
    .news-title { font-size: 20px; font-weight: bold; color: #FFFFFF !important; text-decoration: none !important; }
    .news-title:hover { color: #FACC15 !important; }
    .news-meta { font-size: 13px; color: #A3A3A3 !important; margin-top: 5px; margin-bottom: 10px; }
    
    .hot-news-box {
        background-color: #1E1E1E !important;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #2D2D2D !important;
        margin-bottom: 15px;
    }
    .hot-title { font-size: 14px; font-weight: 600; color: #EAEAEA !important; text-decoration: none !important; }
    .hot-title:hover { color: #FACC15 !important; }
    .badge-live { background-color: #DC3545; color: white !important; padding: 2px 6px; font-size: 10px; font-weight: bold; border-radius: 4px; float: right; }

    /* Default Yellow Button */
    div.stButton > button {
        background-color: #FACC15 !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: bold !important;
    }
    div.stButton > button:hover { background-color: #EAB308 !important; }
    
    /* Secondary Button Style (Quick Summary) */
    .stButton > button[data-testid="baseButton-secondary"] {
        background-color: #2D2D2D !important;
        color: #FFFFFF !important;
        border: 1px solid #404040 !important;
    }
    .stButton > button[data-testid="baseButton-secondary"]:hover {
        background-color: #404040 !important;
    }

    /* Read Article Link Styled As Button */
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
    .read-btn:hover { background-color: #EAB308 !important; }
    
    section[data-testid="stSidebar"] div.stButton > button { background-color: #238636 !important; color: #FFFFFF !important; }
    section[data-testid="stSidebar"] div.stButton > button:hover { background-color: #2EA043 !important; }
    
    /* Summary Container Box */
    .summary-box {
        background-color: #1E293B !important;
        border-left: 4px solid #38BDF8 !important;
        padding: 12px 15px;
        border-radius: 6px;
        margin-top: 15px;
        font-size: 14.5px;
        color: #E2E8F0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Clean raw HTML tags from RSS feed data
def clean_html(raw_html):
    clean_regex = re.compile('<.*?>')
    return re.sub(clean_regex, '', raw_html)

# Extract core sentences based on keyword frequency algorithms
def create_summary(text, num_sentences=2):
    if not text or len(text) < 50:
        return text
    
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]
    if len(sentences) <= num_sentences:
        return text

    words = re.findall(r'\w+', text.lower())
    filtered_words = [w for w in words if len(w) > 3]
    word_frequencies = Counter(filtered_words)

    sentence_scores = {}
    for sentence in sentences:
        sentence_scores[sentence] = sum(word_frequencies[w] for w in re.findall(r'\w+', sentence.lower()) if w in word_frequencies)

    top_sentences = sorted(sentences, key=lambda s: sentence_scores[s], reverse=True)[:num_sentences]
    ordered_summary = [s for s in sentences if s in top_sentences]
    
    return " ".join(ordered_summary)

# Fetch and filter items from specific RSS URL
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
            'title': title,
            'summary': summary,
            'link': link,
            'time': published_time
        })
        
    return articles

# 3. Sidebar Filtering Component
with st.sidebar:
    if st.button("Quay lại đầu trang"):
        st.components.v1.html("<script>window.parent.scrollTo(0,0);</script>", height=0)
    st.write("---")
    st.header("🔍 Bộ lọc tin")
    
    channel_names = ["VnExpress", "VTV", "NYT"]
    selected_channel_name = st.selectbox("Chọn kênh", channel_names)
    
    category_options = [k for k in RSS_FEEDS.keys() if k.startswith(f"{selected_channel_name} -")]
    selected_category_name = st.selectbox("Chọn chuyên mục", category_options)
    
    selected_url = RSS_FEEDS[selected_category_name]
    search_keyword = st.text_input("Tìm từ khóa", "")
    
    if st.button("Lấy tin mới") or 'news_data' not in st.session_state:
        with st.spinner(f"Đang tải dữ liệu từ {selected_channel_name}..."):
            fetched_articles = get_articles_from_rss(selected_url, search_keyword)
            st.session_state['news_data'] = fetched_articles
            st.session_state['current_category'] = selected_category_name

# Retrieve stored session properties
news_data = st.session_state.get('news_data', [])
display_category_name = st.session_state.get('current_category', selected_category_name)

if 'show_summary' not in st.session_state:
    st.session_state['show_summary'] = {}

# --- TWO-COLUMN RESPONSIVE LAYOUT ---
col_main, col_right = st.columns([3.5, 1.5], gap="large")

# --- RIGHT COLUMN: TRENDING HOT STORIES ---
with col_right:
    st.markdown("### 🔥 Tin nóng <span class='badge-live'>LIVE</span>", unsafe_allow_html=True)
    st.write("---")
    
    hot_entries = news_data[10:15] if len(news_data) > 12 else news_data[:5]
    
    if hot_entries:
        for idx, article in enumerate(hot_entries):
            st.markdown(f"""
                <div class='hot-news-box'>
                    <span style='color: #888888; font-size: 12px; font-weight: bold;'>#{idx+1} Xu hướng</span><br>
                    <a class='hot-title' href='{article["link"]}' target='_blank'>{article["title"]}</a>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.caption("Chưa có danh sách tin nóng xu hướng.")

# --- MIDDLE MAIN COLUMN: FEEDS CONTAINER ---
with col_main:
    st.markdown(f"<h1 style='margin-bottom:0px;'>📰 {display_category_name}</h1>", unsafe_allow_html=True)
    st.write("---")
    
    if news_data:
        for idx, article in enumerate(news_data[:10]):
            state_key = f"summary_active_{idx}"
            
            st.markdown(f"""
                <div class='news-card' style='margin-bottom: 5px;'>
                    <a class='news-title' href='{article["link"]}' target='_blank'>{article["title"]}</a>
                    <div class='news-meta'>🕒 {article["time"]}</div>
                    <p style='color: #CCCCCC; font-size: 15px; line-height: 1.6;'>{article["summary"][:280]}...</p>
                </div>
            """, unsafe_allow_html=True)
            
            col_btn1, col_btn2, _ = st.columns([1, 1.2, 3])
            with col_btn1:
                st.markdown(f"<a class='read-btn' href='{article['link']}' target='_blank'>📖 Đọc bài</a>", unsafe_allow_html=True)
            with col_btn2:
                if st.button("✨ Tóm tắt nhanh", key=f"btn_sum_{idx}", type="secondary"):
                    st.session_state['show_summary'][state_key] = not st.session_state['show_summary'].get(state_key, False)
            
            if st.session_state['show_summary'].get(state_key, False):
                extracted_summary = create_summary(article['summary'])
                st.markdown(f"""
                    <div class='summary-box'>
                        <strong>💡 Điểm tin chính:</strong> {extracted_summary}
                    </div>
                """, unsafe_allow_html=True)
                
            st.write("<br>", unsafe_allow_html=True)
    else:
        st.info("👈 Hãy chọn kênh, chuyên mục và bấm 'Lấy tin mới' để bắt đầu.")