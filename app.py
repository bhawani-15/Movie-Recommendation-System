import base64
import html
import streamlit as st
import pickle
import requests
import textwrap


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CineMatch",
    page_icon="🎬",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    movies = pickle.load(
        open("movie_list.pkl", "rb")
    )

    similarity = pickle.load(
        open("similarity.pkl", "rb")
    )

    return movies, similarity


try:
    df, similarity = load_data()

except FileNotFoundError:
    st.error(
        "movie_list.pkl or similarity.pkl not found. "
        "Put both files in the same folder as app.py."
    )
    st.stop()


# ============================================================
# TMDB POSTERS
# ============================================================

TMDB_API_KEY = st.secrets.get("TMDB_API_KEY", "")

@st.cache_data(show_spinner=False)
def get_poster(movie_id):
    """Fetch a movie poster URL from TMDB using the movie's TMDB ID."""

    if not TMDB_API_KEY or movie_id is None:
        return None

    try:
        movie_id = int(movie_id)
    except (ValueError, TypeError):
        return None

    url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    try:
        response = requests.get(
            url,
            params={"api_key": TMDB_API_KEY},
            timeout=10
        )

        if response.status_code != 200:
            return None

        data = response.json()
        poster_path = data.get("poster_path")

        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"

    except requests.RequestException:
        return None

    return None


# ============================================================
# CINEMATIC THEME
# ============================================================

st.markdown("""
<style>

[data-testid="stAppViewContainer"],
.stApp {
    color: #f6f0e6 !important;
    background:
        radial-gradient(ellipse at 50% -18%, rgba(155, 91, 32, .19), transparent 48%),
        radial-gradient(ellipse at 0% 44%, rgba(92, 29, 23, .10), transparent 34%),
        #090909 !important;
}

[data-testid="stMain"],
[data-testid="stMainBlockContainer"],
section.main {
    background: transparent !important;
}

.block-container {
    max-width: 1440px;
    padding: 38px clamp(20px, 5vw, 76px) 54px;
}

[data-testid="stHeader"] {
    background: transparent;
}

.cine-header {
    position: relative;
    overflow: hidden;
    padding: clamp(38px, 7vw, 84px) 24px clamp(36px, 6vw, 68px);
    margin: 0 0 34px;
    text-align: center;
    border: 1px solid rgba(211, 162, 92, .17);
    border-radius: 24px;
    background:
        linear-gradient(180deg, rgba(18, 15, 12, .48), rgba(9, 9, 9, .93)),
        radial-gradient(ellipse at 50% 0%, rgba(196, 129, 61, .18), transparent 63%);
    box-shadow: inset 0 1px rgba(255, 255, 255, .035), 0 20px 70px rgba(0, 0, 0, .28);
}

.cine-header:before,
.cine-header:after {
    position: absolute;
    top: 0;
    bottom: 0;
    width: 1px;
    content: "";
    background: linear-gradient(transparent, rgba(230, 180, 104, .42), transparent);
}

.cine-header:before { left: 8%; }
.cine-header:after { right: 8%; }

.brand-kicker,
.section-kicker {
    color: #e2b976;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: .24em;
    text-transform: uppercase;
}

.brand-mark {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 46px;
    height: 46px;
    margin: 0 auto 17px;
    border: 1px solid rgba(218, 175, 111, .42);
    border-radius: 50%;
    color: #e4bd7d;
    font-size: 20px;
    box-shadow: 0 0 28px rgba(194, 125, 53, .16);
}

.brand-title {
    margin: 13px 0 8px;
    color: #fbf6ed;
    font-family: Georgia, "Times New Roman", serif;
    font-size: clamp(42px, 7vw, 76px);
    font-weight: 500;
    letter-spacing: -.055em;
    line-height: 1;
}

.brand-title span {
    color: #d9a860;
}

.brand-subtitle {
    margin: 14px 0 0;
    color: #d0c8bd;
    font-size: clamp(14px, 2vw, 17px);
    letter-spacing: .025em;
}

.selection-heading {
    margin: 0 0 4px;
    color: #fffaf1;
    font-family: Georgia, "Times New Roman", serif;
    font-size: clamp(25px, 3vw, 34px);
    font-weight: 500;
}

.selection-copy {
    margin: 0 0 16px;
    color: #c2b9ad;
    font-size: 14px;
}

[data-testid="stSelectbox"] label {
    color: #e0d8cc !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}

div[data-baseweb="select"] > div {
    min-height: 52px;
    border: 1px solid #62513b !important;
    border-radius: 10px;
    background: #171512 !important;
    color: #fff8ed !important;
    transition: border-color .2s ease, box-shadow .2s ease;
}

div[data-baseweb="select"] > div:focus-within {
    border-color: #d4a35f !important;
    box-shadow: 0 0 0 3px rgba(189, 139, 76, .2) !important;
}

[data-testid="stSelectbox"] input,
[data-testid="stSelectbox"] [data-baseweb="select"] span {
    color: #fff8ed !important;
    -webkit-text-fill-color: #fff8ed;
}

[data-testid="stSelectbox"] [role="group"] {
    border: 1px solid #62513b !important;
    border-radius: 10px !important;
    background-color: #171512 !important;
    color: #fff8ed !important;
    box-shadow: none !important;
}

[data-testid="stSelectbox"] [role="group"]:focus-within {
    border-color: #d4a35f !important;
    box-shadow: 0 0 0 3px rgba(189, 139, 76, .2) !important;
}

[data-testid="stSelectbox"] [role="group"] input {
    background-color: transparent !important;
    color: #fff8ed !important;
    -webkit-text-fill-color: #fff8ed !important;
}

[data-baseweb="popover"],
[data-baseweb="popover"] ul,
[data-baseweb="menu"] {
    border: 1px solid #62513b !important;
    background-color: #171512 !important;
    color: #fff8ed !important;
}

[data-baseweb="popover"] [role="option"] {
    color: #fff8ed !important;
}

[data-baseweb="popover"] [role="option"]:hover,
[data-baseweb="popover"] [aria-selected="true"] {
    background-color: #392a19 !important;
    color: #fff8ed !important;
}

[role="listbox"] {
    border: 1px solid #62513b !important;
    border-radius: 8px !important;
    background-color: #171512 !important;
    color: #fff8ed !important;
}

[role="listbox"] [role="option"] {
    background-color: #171512 !important;
    color: #fff8ed !important;
}

[role="listbox"] [role="option"]:hover,
[role="listbox"] [role="option"][aria-selected="true"] {
    background-color: #392a19 !important;
    color: #fff8ed !important;
}

.stButton > button {
    width: 100%;
    min-height: 52px;
    border: 1px solid #d6a45d;
    border-radius: 10px;
    background: linear-gradient(135deg, #d4a35f, #a96f35);
    color: #160f08;
    font-size: 14px;
    font-weight: 800;
    letter-spacing: .035em;
    box-shadow: 0 6px 24px rgba(174, 112, 47, .18);
    transition: transform .2s ease, box-shadow .2s ease, filter .2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    border-color: #f0c982;
    background: linear-gradient(135deg, #e5b873, #bd8141);
    color: #160f08;
    box-shadow: 0 10px 30px rgba(200, 137, 65, .28);
}

.stButton > button:focus-visible {
    outline: 2px solid #f0c982;
    outline-offset: 3px;
}

.selection-spacer {
    height: 18px;
}

.picked-movie {
    display: flex;
    align-items: center;
    gap: 16px;
    margin: 34px 0 42px;
    padding: 18px 22px;
    border: 1px solid rgba(207, 158, 91, .22);
    border-left: 3px solid #c9924f;
    border-radius: 12px;
    background: linear-gradient(100deg, rgba(100, 67, 34, .17), rgba(20, 18, 16, .72) 52%);
}

.picked-icon {
    display: grid;
    flex: 0 0 42px;
    height: 42px;
    place-items: center;
    border: 1px solid rgba(207, 158, 91, .27);
    border-radius: 50%;
    color: #d6aa6d;
    font-size: 18px;
}

.picked-label {
    color: #c8b89f;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: .19em;
}

.picked-title {
    margin-top: 5px;
    color: #f6f0e6;
    font-family: Georgia, "Times New Roman", serif;
    font-size: clamp(19px, 3vw, 25px);
}

.recommendations-heading {
    display: flex;
    align-items: end;
    justify-content: space-between;
    gap: 16px;
    margin: 0 0 20px;
}

.recommendations-heading h2 {
    margin: 5px 0 0;
    color: #f7f0e5;
    font-family: Georgia, "Times New Roman", serif;
    font-size: clamp(28px, 4vw, 38px);
    font-weight: 500;
    letter-spacing: -.035em;
}

.recommendations-note {
    padding-bottom: 5px;
    color: #c2b9ad;
    font-size: 12px;
}

.poster-grid {
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    gap: clamp(13px, 2vw, 24px);
}

.poster-card {
    position: relative;
    overflow: hidden;
    min-width: 0;
    border: 1px solid rgba(220, 182, 127, .18);
    border-radius: 13px;
    background: #15120f;
    box-shadow: 0 14px 34px rgba(0, 0, 0, .32);
    animation: poster-rise .55s both;
    transition: transform .28s ease, border-color .28s ease, box-shadow .28s ease;
}

.poster-card:hover {
    z-index: 1;
    transform: translateY(-7px);
    border-color: rgba(224, 174, 104, .58);
    box-shadow: 0 20px 42px rgba(0, 0, 0, .48), 0 0 25px rgba(190, 127, 57, .12);
}

.poster-art {
    position: relative;
    overflow: hidden;
    aspect-ratio: 2 / 3;
    background:
        radial-gradient(ellipse at 50% 30%, rgba(199, 142, 70, .19), transparent 42%),
        linear-gradient(145deg, #292019, #11100f 72%);
}

.poster-art:after {
    position: absolute;
    inset: 35% 0 0;
    content: "";
    background: linear-gradient(transparent, rgba(8, 8, 8, .96));
    pointer-events: none;
}

.poster-art img {
    display: block;
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform .6s cubic-bezier(.2, .7, .2, 1), filter .4s ease;
}

.poster-card:hover .poster-art img {
    transform: scale(1.045);
    filter: saturate(1.08);
}

.poster-fallback {
    display: grid;
    width: 100%;
    height: 100%;
    place-items: center;
    color: rgba(226, 189, 130, .66);
    font-size: 46px;
}

.poster-rank {
    position: absolute;
    z-index: 1;
    top: 12px;
    left: 12px;
    display: grid;
    width: 31px;
    height: 31px;
    place-items: center;
    border: 1px solid rgba(235, 198, 139, .48);
    border-radius: 50%;
    background: rgba(10, 9, 8, .75);
    color: #e6bd7d;
    font-family: Georgia, "Times New Roman", serif;
    font-size: 14px;
    backdrop-filter: blur(8px);
}

.similarity-badge {
    position: absolute;
    z-index: 1;
    top: 12px;
    right: 10px;
    padding: 6px 8px;
    border: 1px solid rgba(235, 198, 139, .35);
    border-radius: 999px;
    background: rgba(10, 9, 8, .72);
    color: #f0cb8c;
    font-size: 10px;
    font-weight: 700;
    backdrop-filter: blur(8px);
}

.poster-caption {
    position: absolute;
    z-index: 1;
    right: 0;
    bottom: 0;
    left: 0;
    padding: 34px 14px 16px;
}

.poster-caption-label {
    margin-bottom: 6px;
    color: #efc67f;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: .18em;
    text-transform: uppercase;
}

.poster-title {
    display: -webkit-box;
    overflow: hidden;
    color: #fff9ef;
    font-family: Georgia, "Times New Roman", serif;
    font-size: clamp(15px, 1.45vw, 19px);
    line-height: 1.25;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
}

.about-section {
    margin-top: 74px;
    padding-top: 34px;
    border-top: 1px solid rgba(216, 185, 143, .14);
}

.about-heading {
    margin: 7px 0 24px;
    color: #f7f0e5;
    font-family: Georgia, "Times New Roman", serif;
    font-size: clamp(26px, 3vw, 34px);
    font-weight: 500;
}

.info-box {
    min-height: 154px;
    padding: 22px;
    border: 1px solid rgba(216, 185, 143, .15);
    border-radius: 12px;
    background: linear-gradient(145deg, rgba(28, 24, 19, .92), rgba(16, 15, 14, .92));
    color: #c7beb2;
    font-size: 14px;
    line-height: 1.7;
    transition: border-color .2s ease, transform .2s ease;
}

.info-box:hover {
    transform: translateY(-3px);
    border-color: rgba(216, 169, 99, .38);
}

.info-box h4 {
    margin: 0 0 9px;
    color: #e7c28a;
    font-family: Georgia, "Times New Roman", serif;
    font-size: 18px;
    font-weight: 500;
}

.cine-footer {
    margin-top: 64px;
    padding-top: 22px;
    border-top: 1px solid rgba(216, 185, 143, .13);
    color: #b5aca0;
    font-size: 12px;
    line-height: 1.8;
    text-align: center;
}

.cine-footer strong {
    color: #c4a16d;
    font-weight: 600;
}

@keyframes poster-rise {
    from { opacity: 0; transform: translateY(14px); }
    to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 1000px) {
    .poster-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }
}

@media (max-width: 640px) {
    .block-container { padding: 20px 16px 38px; }
    .cine-header { border-radius: 17px; margin-bottom: 27px; }
    .cine-header:before { left: 5%; }
    .cine-header:after { right: 5%; }
    .poster-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }
    .poster-caption { padding: 27px 11px 12px; }
    .poster-title { font-size: 15px; }
    .similarity-badge { top: 9px; right: 8px; font-size: 9px; }
    .poster-rank { top: 9px; left: 8px; width: 28px; height: 28px; }
    .recommendations-note { display: none; }
    .about-section { margin-top: 50px; }
}

@media (max-width: 390px) {
    .poster-grid { grid-template-columns: 1fr; }
}

@media (prefers-reduced-motion: reduce) {
    *, *:before, *:after {
        scroll-behavior: auto !important;
        animation-duration: .01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: .01ms !important;
    }
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="cine-header">
        <div class="brand-mark">✦</div>
        <div class="brand-kicker">Your personal film curator</div>
        <div class="brand-title">Cine<span>Match</span></div>
        <p class="brand-subtitle">Find your next favourite, one great story at a time.</p>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# MOVIE SELECTION
# ============================================================

st.markdown(
    """
    <div class="section-kicker">Set the scene</div>
    <div class="selection-heading">What are you in the mood for?</div>
    <div class="selection-copy">Pick a film you love and we’ll find your next watch.</div>
    """,
    unsafe_allow_html=True
)

movie_list = sorted(
    df["title"].dropna().unique().tolist()
)

selected_movie = st.selectbox(
    "Select a movie you like:",
    movie_list,
    index=None,
    placeholder="Search for a movie..."
)

st.markdown('<div class="selection-spacer"></div>', unsafe_allow_html=True)


# ============================================================
# RECOMMENDATION FUNCTION
# ============================================================

def recommend(movie):

    movie_index = df[df["title"] == movie].index

    if len(movie_index) == 0:
        return []

    index = movie_index[0]

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommendations = []

    for i in distances[1:6]:

        movie_index = i[0]

        movie_name = df.iloc[movie_index]["title"]
        movie_id = df.iloc[movie_index]["movie_id"]
        score = i[1]

        recommendations.append(
            {
                "title": movie_name,
                "movie_id": movie_id,
                "score": score,
                "poster": get_poster(movie_id)
            }
        )

    return recommendations


# ============================================================
# BUTTON
# ============================================================

def make_fallback_poster(title, index):
    """Create a locally rendered poster when TMDB has no image available."""

    palettes = [
        ("#7e452b", "#d5a35d"),
        ("#244c4b", "#9fc1a5"),
        ("#633a51", "#d99a9d"),
        ("#34466a", "#a8b7df"),
        ("#765b2e", "#e0c47a"),
    ]
    background, accent = palettes[index % len(palettes)]
    title_lines = textwrap.wrap(str(title), width=17, max_lines=3, placeholder="…")
    title_svg = "".join(
        f'<text x="34" y="{392 + line_number * 48}">{html.escape(line)}</text>'
        for line_number, line in enumerate(title_lines)
    )
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 600">
        <defs>
            <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0" stop-color="{background}"/>
                <stop offset="1" stop-color="#100e0c"/>
            </linearGradient>
            <radialGradient id="glow">
                <stop offset="0" stop-color="{accent}" stop-opacity=".55"/>
                <stop offset="1" stop-color="{accent}" stop-opacity="0"/>
            </radialGradient>
        </defs>
        <rect width="400" height="600" fill="url(#bg)"/>
        <circle cx="260" cy="220" r="190" fill="url(#glow)"/>
        <path d="M0 420 Q120 340 210 420 T400 400 V600 H0Z" fill="#090908" fill-opacity=".58"/>
        <circle cx="276" cy="203" r="104" fill="none" stroke="{accent}" stroke-opacity=".42" stroke-width="2"/>
        <circle cx="276" cy="203" r="78" fill="none" stroke="{accent}" stroke-opacity=".24"/>
        <path d="M34 55 H366" stroke="{accent}" stroke-opacity=".7"/>
        <text x="34" y="42" fill="{accent}" font-family="Arial,sans-serif" font-size="12" letter-spacing="4">CINEMATCH  •  FILM PICK</text>
        <text x="34" y="348" fill="{accent}" font-family="Georgia,serif" font-size="16" letter-spacing="5">YOUR NEXT FEATURE</text>
        <g fill="#fff5e4" font-family="Georgia,serif" font-size="34" font-weight="bold">{title_svg}</g>
        <text x="34" y="555" fill="{accent}" font-family="Arial,sans-serif" font-size="11" letter-spacing="3">A STORY WORTH WATCHING</text>
    </svg>"""
    encoded_svg = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{encoded_svg}"


if st.button("🎯 Recommend Movies"):

    if selected_movie is None:

        st.warning("Please select a movie first.")

    else:

        recommendations = recommend(selected_movie)

        if not recommendations:

            st.error("No recommendations found.")

        else:

            # ================================================
            # SELECTED MOVIE
            # ================================================

            st.html(
                f"""
                <div class="picked-movie">
                    <div class="picked-icon">✦</div>
                    <div>
                        <div class="picked-label">BECAUSE YOU LIKED</div>
                        <div class="picked-title">{html.escape(str(selected_movie))}</div>
                    </div>
                </div>
                """
            )


            # ================================================
            # HEADING
            # ================================================

            st.markdown(
                """
                <div class="recommendations-heading">
                    <div>
                        <div class="section-kicker">Handpicked for your next movie night</div>
                        <h2>You may also like</h2>
                    </div>
                    <div class="recommendations-note">Five films, chosen for you</div>
                </div>
                """,
                unsafe_allow_html=True
            )


            # ================================================
            # MOVIE CARDS
            # ================================================

            poster_cards = []

            for i, movie in enumerate(recommendations):
                similarity_percentage = movie["score"] * 100
                title = html.escape(str(movie["title"]))
                using_fallback = not movie["poster"]

                if not using_fallback:
                    poster_url = html.escape(str(movie["poster"]), quote=True)
                else:
                    poster_url = make_fallback_poster(movie["title"], i)

                poster_image = (
                    f'<img src="{poster_url}" alt="Poster for {title}" '
                    'loading="lazy">'
                )
                poster_caption = ""
                if not using_fallback:
                    poster_caption = f"""
                        <div class="poster-caption">
                            <div class="poster-caption-label">Recommended for you</div>
                            <div class="poster-title">{title}</div>
                        </div>
                    """

                poster_cards.append(
                    f"""
                    <article class="poster-card">
                        <div class="poster-art">
                            {poster_image}
                            <div class="poster-rank">{i + 1:02d}</div>
                            <div class="similarity-badge">{similarity_percentage:.1f}% match</div>
                            {poster_caption}
                        </div>
                    </article>
                    """
                )

            st.html(
                f'<div class="poster-grid">{"".join(poster_cards)}</div>'
            )



# ============================================================
# PROJECT INFORMATION
# ============================================================

st.markdown(
    """
    <div class="about-section">
        <div class="section-kicker">Behind the curtain</div>
        <div class="about-heading">A little movie magic</div>
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown(
        """
        <div class="info-box">
        <h4>Content, not coincidence</h4>
        Recommendations are based on the stories, themes, and characteristics
        that make a movie feel like your kind of film.
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        """
        <div class="info-box">
        <h4>Similarity, thoughtfully scored</h4>
        Movie features are represented as vectors and compared using cosine
        similarity to surface films with a familiar feel.
        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        """
        <div class="info-box">
        <h4>Made with machine learning</h4>
        The recommendation engine is built with Python, Pandas, and
        Scikit-learn.
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="cine-footer">
        <strong>CineMatch</strong> &nbsp;·&nbsp; Content-based movie recommendations
        <br>
        This product uses the TMDB API but is not endorsed or certified by TMDB.
    </div>
    """,
    unsafe_allow_html=True
)