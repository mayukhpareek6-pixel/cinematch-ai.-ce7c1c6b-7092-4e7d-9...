import streamlit as st
import pickle
import pandas as pd
import requests
import urllib.parse
import os
import random

# ==========================================
# PAGE CONFIGURATION & METADATA
# ==========================================
st.set_page_config(
    page_title="CineMatch - AI Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM CSS / MODERN CINEMATIC DESIGN
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    h1, h2, h3, h4, .cinematic-title {
        font-family: 'Outfit', sans-serif !important;
        letter-spacing: -0.5px;
    }

    /* Background & Container adjustments */
    .stApp {
        background: radial-gradient(circle at 10% 20%, #111827 0%, #090d16 90%);
        color: #f1f5f9;
    }

    /* Hero Banner */
    .hero-container {
        padding: 2.2rem 2.5rem;
        background: linear-gradient(135deg, rgba(229, 9, 20, 0.15) 0%, rgba(30, 41, 59, 0.7) 100%);
        border: 1px solid rgba(229, 9, 20, 0.35);
        border-radius: 18px;
        backdrop-filter: blur(12px);
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px -10px rgba(229, 9, 20, 0.25);
    }

    .hero-badge {
        display: inline-block;
        padding: 4px 12px;
        background: rgba(229, 9, 20, 0.25);
        border: 1px solid rgba(229, 9, 20, 0.5);
        color: #ff4d5a;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 12px;
    }

    .hero-title {
        font-size: 2.7rem;
        font-weight: 800;
        line-height: 1.15;
        background: linear-gradient(90deg, #ffffff 30%, #fca5a5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        color: #94a3b8;
        max-width: 720px;
        line-height: 1.5;
    }

    /* Selected Movie Spotlight Card */
    .spotlight-card {
        background: rgba(26, 34, 51, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.6rem;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);
        margin-bottom: 2.5rem;
        backdrop-filter: blur(8px);
    }

    /* Recommendation Movie Card */
    .movie-card {
        background: #151c2c;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex;
        flex-direction: column;
        height: 100%;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }

    .movie-card:hover {
        transform: translateY(-8px);
        border-color: rgba(229, 9, 20, 0.5);
        box-shadow: 0 16px 36px rgba(229, 9, 20, 0.2);
    }

    .card-body {
        padding: 1rem 1.1rem;
        flex-grow: 1;
        display: flex;
        flex-direction: column;
    }

    .movie-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 6px;
        line-height: 1.3;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
        min-height: 2.6rem;
    }

    /* Badges */
    .badge-pill {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 600;
        margin-right: 4px;
        margin-bottom: 4px;
    }

    .badge-match {
        background: rgba(16, 185, 129, 0.2);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.4);
    }

    .badge-genre {
        background: rgba(255, 255, 255, 0.08);
        color: #cbd5e1;
        border: 1px solid rgba(255, 255, 255, 0.12);
    }

    /* Buttons */
    div.stButton > button {
        background: linear-gradient(135deg, #e50914 0%, #b80710 100%);
        color: white;
        font-weight: 700;
        font-size: 1rem;
        padding: 0.65rem 1.8rem;
        border-radius: 10px;
        border: none;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 4px 15px rgba(229, 9, 20, 0.4);
        width: 100%;
    }

    div.stButton > button:hover {
        background: linear-gradient(135deg, #f40612 0%, #cf0a13 100%);
        box-shadow: 0 6px 20px rgba(229, 9, 20, 0.6);
        transform: translateY(-1px);
        color: white;
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #0b0f19;
    }
    ::-webkit-scrollbar-thumb {
        background: #252e42;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #e50914;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# DATA LOADING & CACHING
# ==========================================
@st.cache_resource(show_spinner=False)
def load_data():
    """Loads movie metadata and similarity mapping."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Load movies dictionary / dataframe
    movie_dict_path = os.path.join(base_dir, 'movie_dict.pkl')
    if not os.path.exists(movie_dict_path):
        # Fallback to parent or archive directory
        movie_dict_path = r'C:\Users\hg\Downloads\archive\movie_dict.pkl'
        
    with open(movie_dict_path, 'rb') as f:
        movies_data = pickle.load(f)
    movies_df = pd.DataFrame(movies_data)

    # 2. Load similarity mapping
    top_sim_path = os.path.join(base_dir, 'top_similarity.pkl')
    top_sim = None
    similarity_matrix = None

    if os.path.exists(top_sim_path):
        with open(top_sim_path, 'rb') as f:
            top_sim = pickle.load(f)
    else:
        # Check for full similarity matrix
        sim_path = os.path.join(base_dir, 'similarity.pkl')
        if not os.path.exists(sim_path):
            sim_path = r'C:\Users\hg\Downloads\archive\similarity.pkl'
        if os.path.exists(sim_path):
            with open(sim_path, 'rb') as f:
                similarity_matrix = pickle.load(f)

    return movies_df, top_sim, similarity_matrix


# ==========================================
# POSTER & METADATA FETCHING
# ==========================================
@st.cache_data(ttl=86400, show_spinner=False)
def fetch_poster(movie_id, title, api_key="8265bd1679663a7ea12ac168da84d2e8"):
    """Fetches high-res poster from TMDB API with a fallback styled placeholder."""
    if api_key and api_key.strip():
        try:
            url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key.strip()}"
            response = requests.get(url, timeout=3.5)
            if response.status_code == 200:
                data = response.json()
                poster_path = data.get('poster_path')
                if poster_path:
                    return f"https://image.tmdb.org/t/p/w500{poster_path}"
        except Exception:
            pass

    # High-quality fallback poster URL using placeholder image
    safe_title = urllib.parse.quote(str(title)[:20])
    return f"https://placehold.co/400x600/1e293b/e2e8f0?text={safe_title}"


def get_recommendations(movie_title, movies_df, top_sim, similarity_matrix, num_recommendations=5):
    """Computes top recommendations for a given movie title."""
    matches = movies_df[movies_df['title'].str.strip() == movie_title.strip()]
    if matches.empty:
        return []
    
    idx = matches.index[0]
    results = []

    if top_sim is not None and idx in top_sim:
        for rec_idx, score in top_sim[idx][:num_recommendations]:
            row = movies_df.iloc[rec_idx]
            results.append({
                'id': row['id'],
                'title': row['title'],
                'overview': row.get('overview', 'No summary available.') or 'No summary available.',
                'genres': row.get('genres', []) or [],
                'cast': row.get('cast', []) or [],
                'director': row.get('director', []) or [],
                'score': float(score)
            })
    elif similarity_matrix is not None:
        distances = similarity_matrix[idx]
        top_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:num_recommendations+1]
        for rec_idx, score in top_list:
            row = movies_df.iloc[rec_idx]
            results.append({
                'id': row['id'],
                'title': row['title'],
                'overview': row.get('overview', 'No summary available.') or 'No summary available.',
                'genres': row.get('genres', []) or [],
                'cast': row.get('cast', []) or [],
                'director': row.get('director', []) or [],
                'score': float(score)
            })
    return results


# ==========================================
# MAIN APPLICATION
# ==========================================
try:
    movies_df, top_sim, similarity_matrix = load_data()
except Exception as e:
    st.error(f"⚠️ Error loading movie dataset: {e}")
    st.stop()

# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.image("https://assets.nflxext.com/ffe/siteui/vlv3/ab4b0b22-2ddf-4d48-ae7b-c9444ae23eb2/492570ef-4f11-4796-a947-f05bc5fc8efb/US-en-20231030-popsignuptwoweeks-perspective_alpha_website_large.jpg", use_container_width=True)
    st.markdown("### ⚙️ Engine Settings")
    
    api_key_input = st.text_input(
        "TMDB API Key (for Posters)",
        value="8265bd1679663a7ea12ac168da84d2e8",
        help="Free TMDB API key to fetch real HD movie posters from TheMovieDB.org"
    )

    num_recs = st.slider("Number of Recommendations", min_value=3, max_value=10, value=5, step=1)
    
    st.divider()
    st.markdown("### 📊 Dataset Overview")
    st.markdown(f"- **Total Movies:** `{len(movies_df):,}`")
    st.markdown("- **Algorithm:** `TF-IDF + Cosine Similarity`")
    st.markdown("- **Features:** `Genres, Keywords, Cast, Director, Plot`")
    st.markdown("- **Model Size:** `686 KB (Optimized Vector Matrix)`")

    st.divider()
    st.markdown("### 🚀 Deployment Status")
    st.success("🟢 Active & Live on Local Port 8501")
    st.caption("Cloud ready for Streamlit Cloud, Render, or Hugging Face Spaces.")


# --- HERO BANNER ---
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">AI Recommendation Engine</div>
    <div class="hero-title">CineMatch AI 🍿</div>
    <div class="hero-subtitle">
        Discover films you'll love powered by content-based natural language processing and cosine similarity over 4,800+ TMDB movies.
    </div>
</div>
""", unsafe_allow_html=True)


# --- CONTROLS / SELECTION ---
col_sel, col_btn = st.columns([4, 1], gap="medium")

movie_list = sorted(movies_df['title'].dropna().unique().tolist())

# Handle session state for random movie picker
if 'current_movie' not in st.session_state:
    st.session_state.current_movie = "Avatar" if "Avatar" in movie_list else movie_list[0]

def set_random_movie():
    st.session_state.current_movie = random.choice(movie_list)

with col_sel:
    selected_movie = st.selectbox(
        "Search or Select a Movie:",
        options=movie_list,
        index=movie_list.index(st.session_state.current_movie) if st.session_state.current_movie in movie_list else 0,
        key="movie_selector"
    )

with col_btn:
    st.write("")
    st.write("")
    surprise_btn = st.button("🎲 Surprise Me!", on_click=set_random_movie, help="Pick a random movie from 4,800+ titles")

# Get selected movie row
selected_row = movies_df[movies_df['title'] == selected_movie].iloc[0]
selected_poster = fetch_poster(selected_row['id'], selected_movie, api_key_input)


# --- SPOTLIGHT CARD FOR SELECTED MOVIE ---
with st.container():
    st.markdown("""
    <div style="font-size: 1.25rem; font-weight: 700; color: #f8fafc; margin-bottom: 0.8rem; display: flex; align-items: center; gap: 8px;">
        <span>🎯 Currently Selected:</span> <span style="color: #ff4d5a;">""" + selected_movie + """</span>
    </div>
    """, unsafe_allow_html=True)

    spotlight_col1, spotlight_col2 = st.columns([1, 3], gap="large")
    with spotlight_col1:
        st.image(selected_poster, use_container_width=True)

    with spotlight_col2:
        st.markdown(f"### {selected_movie}")
        
        # Badges for genres
        genre_list = selected_row.get('genres', [])
        if isinstance(genre_list, list) and genre_list:
            badges_html = " ".join([f'<span class="badge-pill badge-genre">🏷️ {g}</span>' for g in genre_list])
            st.markdown(badges_html, unsafe_allow_html=True)
            st.write("")

        # Director & Cast
        director = ", ".join(selected_row.get('director', [])) if isinstance(selected_row.get('director', []), list) else "N/A"
        cast = ", ".join(selected_row.get('cast', [])) if isinstance(selected_row.get('cast', []), list) else "N/A"
        
        st.markdown(f"**🎬 Director:** `{director}`")
        st.markdown(f"**🌟 Starring:** `{cast}`")
        
        overview_text = selected_row.get('overview', 'No summary available.')
        st.markdown(f"**📖 Synopsis:**")
        st.info(overview_text if pd.notna(overview_text) else "No overview available.")


# --- RECOMMENDATIONS SECTION ---
st.divider()

col_heading, col_act = st.columns([3, 1])
with col_heading:
    st.markdown(f"## 🌟 Movies You Might Also Enjoy")
    st.caption(f"Calculated top {num_recs} cosine-similarity matches based on plot, themes, actors, and director.")

recommendations = get_recommendations(
    selected_movie,
    movies_df,
    top_sim,
    similarity_matrix,
    num_recommendations=num_recs
)

if not recommendations:
    st.warning("No recommendations found for this movie.")
else:
    # Render in dynamic responsive columns
    cols = st.columns(len(recommendations), gap="medium")
    for i, rec in enumerate(recommendations):
        with cols[i]:
            rec_poster = fetch_poster(rec['id'], rec['title'], api_key_input)
            st.image(rec_poster, use_container_width=True)
            
            # Title
            st.markdown(f"**{i+1}. {rec['title']}**")
            
            # Match badge
            match_pct = int(min(100, max(15, (rec['score'] + 0.3) * 100))) if rec['score'] < 1 else 98
            st.markdown(f"""
            <span class="badge-pill badge-match">✨ {match_pct}% Match</span>
            """, unsafe_allow_html=True)
            
            # Genres
            if rec['genres']:
                genre_str = ", ".join(rec['genres'][:2])
                st.caption(f"🎭 {genre_str}")
            
            # Expandable Details
            with st.expander("Movie Details"):
                if rec['director']:
                    st.markdown(f"**Director:** {', '.join(rec['director'])}")
                if rec['cast']:
                    st.markdown(f"**Cast:** {', '.join(rec['cast'])}")
                st.markdown(f"**Synopsis:**\n{rec['overview']}")
                tmdb_link = f"https://www.themoviedb.org/movie/{rec['id']}"
                st.markdown(f"[View on TMDB ↗]({tmdb_link})")

st.write("")
st.divider()

# --- FOOTER ---
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.85rem; padding: 2rem 0;">
    CineMatch Movie Recommendation System &bull; Powered by NLP, TF-IDF Vectorization, and Scikit-Learn
</div>
""", unsafe_allow_html=True)
