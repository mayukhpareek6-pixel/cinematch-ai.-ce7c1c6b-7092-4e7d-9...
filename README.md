# 🎬 CineMatch AI — Movie Recommendation System

A modern, high-performance content-based movie recommendation web application built with **Python**, **Streamlit**, **Scikit-Learn (TF-IDF & Cosine Similarity)**, and the **TMDB 5000 Movies Dataset**.

---

## 🌟 Features

- **NLP-Powered Similarity Engine**: Recommends movies based on plot overviews, genres, cast, crew, and keywords using TF-IDF vectorization and cosine similarity.
- **Cinematic Dark UI**: Modern streaming platform aesthetic with glassmorphic cards, responsive grid, dynamic hover effects, and movie match percentage badges.
- **Real-Time Poster Fetching**: Integrates with The Movie Database (TMDB) API to display high-resolution movie posters and synopses with an offline fallback.
- **Optimized for Cloud Deployment**: Precomputes top similarity scores, slashing model size from **184.5 MB down to 686 KB**, avoiding GitHub's 100 MB file size limit and enabling instant cloud cold starts.
- **Surprise Me 🎲**: One-click random movie discovery across all 4,803 titles.

---

## 🚀 Deployment Options

### 1. Local Deployment (Active Now)

The application is already running locally! You can view it by opening:
- **Local URL**: [http://localhost:8501](http://localhost:8501)
- **Network URL**: `http://192.168.6.230:8501`

To start it manually at any time:
```powershell
# From the project directory:
streamlit run app.py
```

---

### 2. Streamlit Community Cloud (Recommended — Free & 1-Click)

1. Create a new GitHub repository (e.g. `movie-recommendation-system`).
2. Push this project folder to your repository:
   ```bash
   git init
   git add .
   git commit -m "Deploy CineMatch Movie Recommender"
   git branch -M main
   git remote add origin https://github.com/<your-username>/movie-recommendation-system.git
   git push -u origin main
   ```
3. Visit [share.streamlit.io](https://share.streamlit.io/) and log in with GitHub.
4. Click **New app**, select your repository, set the main file path to `app.py`, and click **Deploy**!
5. Your app will receive a free public `https://<your-app>.streamlit.app` link.

---

### 3. Render.com / Railway Deployment

This project includes a `Procfile` and `Dockerfile`:
1. Link your GitHub repository in [Render.com](https://render.com).
2. Select **Web Service**.
3. Choose the Python environment and set:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
4. Click **Create Web Service**.

---

### 4. Docker Deployment

```bash
docker build -t cinematch-recommender .
docker run -p 8501:8501 cinematch-recommender
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📁 Project Structure

```
movie-recommender/
│
├── .streamlit/
│   └── config.toml          # Dark cinema theme & server settings
├── app.py                   # Main Streamlit web application
├── movie_dict.pkl           # Processed movie metadata dictionary (2.1 MB)
├── top_similarity.pkl       # Optimized top recommendation matrix (686 KB)
├── requirements.txt         # Python dependencies
├── Procfile                 # Deployment process command for cloud hosts
├── Dockerfile               # Container build configuration
├── .gitignore               # Excludes large raw datasets and cache
└── README.md                # Documentation & deployment guide
```
