import mimetypes
mimetypes.add_type('application/javascript', '.js')
import streamlit as st
import pandas as pd
import joblib

# ================= CONFIG =================
st.set_page_config(
    page_title="Prediksi Diabetes",
    page_icon="🧪",
    layout="wide"
)

# ================= STYLE =================
st.markdown("""
<style>

/* ================= GLOBAL ================= */
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

/* ================= TAB ================= */
div[data-baseweb="tab-list"] {
    justify-content: center;
    gap: 25px;
    border-bottom: 1px solid #e5e7eb;
}

/* TAB NORMAL */
button[data-baseweb="tab"] {
    background: none !important;
    border: none;
    font-size: 16px;
    color: #6b7280;
    padding: 10px 5px;
    transition: 0.3s;
}

/* TAB HOVER */
button[data-baseweb="tab"]:hover {
    color: #8b5cf6;
}

/* TAB AKTIF */
button[data-baseweb="tab"][aria-selected="true"] {
    color: #8b5cf6;
    border-bottom: 3px solid #8b5cf6;
    font-weight: 600;
}

/* ================= HEADER ================= */
.header-box {
    background: transparent;
    padding: 10px;
    border-radius: 0;
    color: #ffffff;
    text-align: left;
    box-shadow: none;
}

/* ================= CARD ================= */
.card {
    background: #ffffff;
    padding: 18px;
    border-radius: 15px;
    text-align: center;
    color: #374151;
    font-weight: 500;
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    transition: 0.3s;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 30px rgba(0,0,0,0.15);
}

/* ================= RECTANGLE GEJALA ================= */
.card-box {
    background: rgba(255, 255, 255, 0.05);
    padding: 20px;
    border-radius: 15px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    margin-bottom: 15px;
    color: #cbd5e1;
}

.card-title {
    font-weight: bold;
    color: #8b5cf6;
    margin-bottom: 10px;
    font-size: 1.1rem;
}

.gejala-item {
    background: rgba(139, 92, 246, 0.15);
    padding: 12px;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    margin-bottom: 10px;
    transition: 0.3s;
}

.gejala-item:hover {
    background: rgba(139, 92, 246, 0.25);
    transform: translateX(5px);
}

/* ================= BUTTON ================= */
.stButton>button {
    background: linear-gradient(135deg, #8b5cf6, #6366f1);
    color: white;
    border-radius: 10px;
    height: 45px;
    font-weight: bold;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
    opacity: 0.9;
}

/* ================= INPUT ================= */
input, textarea {
    border-radius: 10px !important;
    border: 1px solid #d1d5db !important;
}

input:focus, textarea:focus {
    border: 1px solid #8b5cf6 !important;
    box-shadow: 0 0 5px #8b5cf6;
}

/* ================= SELECTBOX ================= */
div[data-baseweb="select"] > div {
    border-radius: 10px !important;
}

/* ================= SLIDER ================= */
.css-1cpxqw2, .css-14xtw13 {
    color: #8b5cf6 !important;
}

/* ================= BADGE / TAG ================= */
.tag {
    display: inline-block;
    background: #ede9fe;
    color: #5b21b6;
    padding: 5px 10px;
    border-radius: 8px;
    margin: 5px;
    font-size: 12px;
}

/* ================= SCROLLBAR ================= */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: #8b5cf6;
    border-radius: 10px;
}


/* ================= FOOTER ================= */
footer {visibility: hidden;}

/* ================= ANIMASI ================= */
.fade-in {
    animation: fadeIn 1s ease-in;
}

@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}
            

section.main {
    background: radial-gradient(circle at top, #0f172a, #020617);
}

section.main > div {
    background: rgba(17, 24, 39, 0.6);
    backdrop-filter: blur(14px);
    border-radius: 16px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.05);
    box-shadow: 0 10px 40px rgba(0,0,0,0.4);
    margin-bottom: 20px;
    transition: all 0.3s ease;
}

section.main > div:hover {
    transform: translateY(-6px) scale(1.01);
    box-shadow: 0 20px 60px rgba(0,0,0,0.6);
}

h2 {
    font-size: 26px;
    font-weight: 700;
    background: linear-gradient(90deg, #8b5cf6, #22c55e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

h3 {
    font-size: 18px;
    font-weight: 600;
    color: #e5e7eb;
    position: relative;
    padding-left: 12px;
}

h3::before {
    content: "";
    position: absolute;
    left: 0;
    top: 4px;
    height: 16px;
    width: 4px;
    background: linear-gradient(180deg, #8b5cf6, #6366f1);
    border-radius: 2px;
}

p {
    color: #cbd5e1;
    line-height: 1.7;
}

div[data-testid="column"] {
    padding: 12px;
}

div[data-testid="column"] p {
    background: rgba(255,255,255,0.03);
    padding: 10px 14px;
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.05);
    margin-bottom: 8px;
    transition: 0.2s;
}

div[data-testid="column"] p:hover {
    background: rgba(139,92,246,0.1);
    transform: translateX(5px);
}

h2, h3 {
    display: flex;
    align-items: center;
    gap: 10px;
}

html {
    scroll-behavior: smooth;
}

/* ================= FOTO PROFIL LINGKARAN ================= */
.profil-lingkaran {
    display: block;
    margin-left: auto;
    margin-right: auto;
    width: 200px;
    height: 200px;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid #8b5cf6;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}

</style>
""", unsafe_allow_html=True)


# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("""
    <style>
    section[data-testid="stSidebar"]{
        background: linear-gradient(180deg, #3B82F6, #8B5CF6);
        color: white;
    }

    .mini-box{
        background: rgba(255,255,255,0.15);
        backdrop-filter: blur(10px);
        padding:16px;
        border-radius:18px;
        box-shadow:0 8px 20px rgba(0,0,0,0.15);
        border:1px solid rgba(255,255,255,0.25);
        margin-bottom:16px;
    }

    .judul-side{
        font-size:18px;
        font-weight:800;
        text-align:center;
        margin-bottom:10px;
        color:white;
    }

    .sub-side{
        text-align:center;
        font-size:14px;
        margin-top:6px;
        color:#E0E7FF;
    }

    .nama-dev{
        text-align:center;
        font-weight:700;
        font-size:15px;
        color:white;
    }

    .title-main{
        text-align:center;
        font-size:26px;
        font-weight:900;
        margin-top:10px;
        color:white;
    }

    .desc-main{
        text-align:center;
        font-size:14px;
        margin-top:4px;
        margin-bottom:18px;
        color:#E0E7FF;
    }

    [data-testid="metric-container"] {
        background: rgba(255,255,255,0.15);
        border-radius:12px;
        padding:10px;
        text-align:center;
        color:white;
        border:1px solid rgba(255,255,255,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

    try:
        st.image("logoAdel.png", width=120)
    except:
        pass

    st.markdown("""
        <div class="title-main">DIABETES PREDICT</div>
        <div class="desc-main">Machine Learning Classification App</div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="mini-box">
        <div class="judul-side">👩‍💻 Dibuat Oleh</div>
        <div class="nama-dev">Shahnaz Adelia Putri</div>
        <div class="sub-side">Student | Data Science Enthusiast</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="mini-box">
        <div class="judul-side">📊 Statistik Dataset</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    c1.metric("Data", "520")
    c2.metric("Positif", "34%")

    st.markdown("""
    <div class="mini-box">
        <div class="judul-side">🎯 Tujuan</div>
        <div class="sub-side">
        Memprediksi apakah seseorang berpotensi terkena diabetes 
        berdasarkan kondisi kesehatan dan gejala yang dimiliki.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ================= HEADER =================
col_text, col_kanan = st.columns([11, 1])

with col_text:
    st.markdown("""
    <div class="header-box" style="text-align:center;">
        <h1>🧪 Sistem Prediksi Risiko Diabetes</h1>
        <p>Deteksi dini berbasis Machine Learning</p>
    </div>
    """, unsafe_allow_html=True)

with col_kanan:
    try:
        st.image("logoSmega.png", width=70)
    except:
        pass

# ================= LOAD DATA & MODEL =================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("diabetes.csv")
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame()

@st.cache_resource
def load_model():
    try:
        return joblib.load("model_prediksi_diabetes.joblib")
    except:
        return None

df = load_data()
model = load_model()

# ================= NAVBAR =================
tab1, tab2, tab3, tab4 = st.tabs([
    "🩺 Prediksi Diabetes",
    "📊 Informasi Dataset",
    "💻 Source Code",
    "👨‍💻 About"
])

st.markdown("<hr style='margin-top:10px;'>", unsafe_allow_html=True)

# ================= TAB 1: PREDIKSI =================
with tab1:
    st.title("🧪 Form Prediksi")
    if model is None:
        st.error("⚠️ File 'model_prediksi_diabetes.joblib' tidak ditemukan!")
    else:
        input_data = {}
        col1, col2 = st.columns(2)
        with col1:
            input_data["Umur"] = st.slider("Umur", 1, 100, 25)
        with col2:
            input_data["Jenis Kelamin"] = st.radio("Jenis Kelamin", ["Perempuan", "Laki-laki"])

        st.markdown("### 🧪 Gejala")
        gejala_cols = [
            "Sering buang air kecil", "Sering haus berlebihan", "Penurunan berat badan tiba-tiba",
            "Kelemahan", "Sering lapar berlebihan", "Infeksi jamur genital",
            "Penglihatan kabur", "Gatal-gatal", "Mudah marah", "Luka lama sembuh",
            "Kelumpuhan sebagian", "Kekakuan otot", "Kerontokan rambut", "Obesitas"
        ]
        cols = st.columns(2)
        for i, col in enumerate(gejala_cols):
            with cols[i % 2]:
                input_data[col] = st.selectbox(col, ["Tidak", "Ya"])

        if st.button("🔍 Analisis Sekarang"):
            input_df = pd.DataFrame([input_data])
            hasil = model.predict(input_df)[0]
            classes = list(model.classes_)
            prob_positif_idx = classes.index("Positif") if "Positif" in classes else 1
            prob = model.predict_proba(input_df)[0][prob_positif_idx]

            if hasil == "Positif":
                st.error(f"⚠️ Risiko Tinggi Terkena Diabetes (Keyakinan: {prob*100:.2f}%)")
            else:
                st.success(f"✅ Risiko Rendah Terkena Diabetes (Keamanan: {(1-prob)*100:.2f}%)")


# ================= TAB 2: INFORMASI =================
with tab2:
    st.title("📊 Informasi Aplikasi")
    st.markdown("""
    <div class="card-box">
        <div class="card-title">🧠 Tentang Sistem</div>
        Sistem ini menggunakan algoritma Machine Learning yang telah ditraining untuk memprediksi risiko diabetes.
    </div>
    <div class="card-box">
        <div class="card-title">🩺 Tentang Diabetes</div>
        Diabetes adalah penyakit kronis akibat gangguan insulin sehingga kadar gula darah meningkat.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🧪 Gejala Diabetes")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="gejala-item"><b>Sering buang air kecil</b><br><small>→ Tubuh membuang kelebihan gula</small></div>
        <div class="gejala-item"><b>Sering haus berlebihan</b><br><small>→ Kehilangan cairan</small></div>
        <div class="gejala-item"><b>Penurunan berat badan tiba-tiba</b><br><small>→ Energi tidak terserap</small></div>
        <div class="gejala-item"><b>Kelemahan</b><br><small>→ Kurangnya energi</small></div>
        <div class="gejala-item"><b>Sering lapar berlebihan</b><br><small>→ Tubuh kekurangan energi</small></div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="gejala-item"><b>Gatal-gatal</b><br><small>→ Kulit kering/infeksi</small></div>
        <div class="gejala-item"><b>Mudah marah</b><br><small>→ Gula darah tidak stabil</small></div>
        <div class="gejala-item"><b>Luka lama sembuh</b><br><small>→ Proses penyembuhan terganggu</small></div>
        <div class="gejala-item"><b>Kelumpuhan sebagian</b><br><small>→ Gangguan saraf</small></div>
        <div class="gejala-item"><b>Kekakuan otot</b><br><small>→ Gangguan otot</small></div>
        """, unsafe_allow_html=True)

    if not df.empty:
        st.markdown('<div class="card-box">', unsafe_allow_html=True)
        st.subheader("📋 Dataset Training")
        st.dataframe(df)
        st.markdown('</div>', unsafe_allow_html=True)

# ================= SOURCE CODE JUPYTER NOTEBOOK =================
with tab3:
    with st.expander("1. Load Dataset"):
            st.code("""
    import pandas as pd
    df = pd.read_csv("diabetes.csv")
    df
    """, language="python")

            st.write("Output:")
            st.dataframe(df)

    # ----------------------------------------------------

    with st.expander("2. Menampilkan Shape Dataset"):
        st.code("""
    df.shape
    """, language="python")

        st.write("Output:")
        st.write(df.shape)

    # ----------------------------------------------------

    with st.expander("3. Menampilkan Nama Kolom"):
        st.code("""
    df.columns
    """, language="python")

        st.write("Output:")
        st.write(df.columns)

    # ----------------------------------------------------

    with st.expander("4. Statistik Deskriptif"):
        st.code("""
    df.describe()
    """, language="python")

        st.write("Output:")
        st.dataframe(df.describe())

    # ----------------------------------------------------

    with st.expander("5. Informasi Dataset"):
        st.code("""
    df.info()
    """, language="python")

        import io
        buffer = io.StringIO()
        df.info(buf=buffer)
        st.text(buffer.getvalue())

    # ----------------------------------------------------

    with st.expander("6. Jumlah Kelas"):
        st.code("""
    df["Kelas"].value_counts()
    """, language="python")

        st.write("Output:")
        st.dataframe(df["Kelas"].value_counts())

    # ----------------------------------------------------

    with st.expander("7. Jenis Kelamin"):
        st.code("""
    df["Jenis Kelamin"].value_counts()
    """, language="python")

        st.write("Output:")
        st.dataframe(df["Jenis Kelamin"].value_counts())

    # ----------------------------------------------------

    with st.expander("8. Sering Buang Air Kecil"):
        st.code("""
    df["Sering buang air kecil"].value_counts()
    """, language="python")

        st.write("Output:")
        st.dataframe(df["Sering buang air kecil"].value_counts())

    # ----------------------------------------------------

    with st.expander("9. Sering Haus Berlebihan"):
        st.code("""
    df["Sering haus berlebihan"].value_counts()
    """, language="python")

        st.write("Output:")
        st.dataframe(df["Sering haus berlebihan"].value_counts())

    # ----------------------------------------------------

    with st.expander("10. Obesitas"):
        st.code("""
    df["Obesitas"].value_counts()
    """, language="python")

        st.write("Output:")
        st.dataframe(df["Obesitas"].value_counts())

    # ----------------------------------------------------

    with st.expander("11. Head Dataset"):
        st.code("""
    df.head()
    """, language="python")

        st.write("Output:")
        st.dataframe(df.head())

    # ----------------------------------------------------

    with st.expander("12. Tail Dataset"):
        st.code("""
    df.tail()
    """, language="python")

        st.write("Output:")
        st.dataframe(df.tail())

    # ----------------------------------------------------

    with st.expander("13. Mengubah 0 dan 1 menjadi Ya dan Tidak"):
        st.code("""
    df = df.replace({
        1:"Ya",
        0:"Tidak"
    })
    """, language="python")

    # ----------------------------------------------------

    with st.expander("14. Mengubah Jenis Kelamin"):
        st.code("""
    df["Jenis Kelamin"] = df["Jenis Kelamin"].replace({
        1:"Laki-laki",
        0:"Perempuan"
    })
    """, language="python")

    # ----------------------------------------------------

    with st.expander("15. Scatter Plot Obesitas vs Haus Berlebihan"):
        st.code("""
    import matplotlib.pyplot as plt

    df["Obesitas"] = df["Obesitas"].map({"Ya":1, "Tidak":0})
    df["Sering haus berlebihan"] = df["Sering haus berlebihan"].map({"Ya":1, "Tidak":0})

    ya = df[df["Obesitas"]==1]
    tidak = df[df["Obesitas"]==0]

    plt.figure(figsize=(6,5))

    plt.scatter(ya["Umur"], ya["Sering haus berlebihan"], s=100, alpha=0.7, label="Obesitas")
    plt.scatter(tidak["Umur"], tidak["Sering haus berlebihan"], s=100, alpha=0.7, label="Tidak Obesitas")

    plt.xlabel("Umur")
    plt.ylabel("Sering Haus (0=Tidak, 1=Ya)")
    plt.title("Umur vs Sering Haus (dibagi Obesitas)")
    plt.grid(True, linestyle="--", alpha=0.3)
    plt.legend()
    plt.show()
    """, language="python")

    # ----------------------------------------------------

    with st.expander("16. Visualisasi Umur dan Haus Berlebihan"):
        st.code("""
    import matplotlib.pyplot as plt
    import pandas as pd

    df["Umur"] = pd.to_numeric(df["Umur"], errors="coerce")

    if df["Sering haus berlebihan"].dtype == "object":
        df["Sering haus berlebihan"] = df["Sering haus berlebihan"].astype(str)
        df["Sering haus berlebihan"] = df["Sering haus berlebihan"].str.strip().str.capitalize()
        df["Sering haus berlebihan"] = df["Sering haus berlebihan"].map({"Ya":1, "Tidak":0})

    muda = df[df["Umur"] < 30]
    dewasa = df[(df["Umur"] >= 30) & (df["Umur"] < 50)]
    tua = df[df["Umur"] >= 50]

    plt.figure(figsize=(6,5))

    plt.scatter(muda["Umur"], muda["Sering haus berlebihan"], s=100, alpha=0.7, label="Muda")
    plt.scatter(dewasa["Umur"], dewasa["Sering haus berlebihan"], s=100, alpha=0.7, label="Dewasa")
    plt.scatter(tua["Umur"], tua["Sering haus berlebihan"], s=100, alpha=0.7, label="Tua")

    plt.xlabel("Umur")
    plt.ylabel("Sering Haus")
    plt.title("Umur vs Sering Haus")
    plt.grid(True, linestyle="--", alpha=0.3)
    plt.legend()
    plt.show()
    """, language="python")

    # ----------------------------------------------------

    with st.expander("17. Cek 10 Data Pertama"):
        st.code("""
    print(df[["Umur","Sering haus berlebihan"]].head(10))
    print(df["Sering haus berlebihan"].unique())
    """, language="python")

    # ----------------------------------------------------

    with st.expander("18. Unique Value"):
        st.code("""
    print(df["Sering haus berlebihan"].astype(str).unique())
    """, language="python")

    # ----------------------------------------------------

    with st.expander("19. Model Logistic Regression"):
        st.code("""
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
    from sklearn.preprocessing import StandardScaler, OneHotEncoder
    from sklearn.pipeline import Pipeline
    from sklearn.compose import ColumnTransformer

    X = df[[
        "Umur",
        "Jenis Kelamin",
        "Sering buang air kecil",
        "Sering haus berlebihan",
        "Penurunan berat badan tiba-tiba",
        "Kelemahan",
        "Sering lapar berlebihan",
        "Infeksi jamur genital",
        "Penglihatan kabur",
        "Gatal-gatal",
        "Mudah marah",
        "Luka lama sembuh",
        "Kelumpuhan sebagian",
        "Kekakuan otot",
        "Kerontokan rambut",
        "Obesitas"
    ]]

    y = df["Kelas"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    numeric_columns = ["Umur"]

    categorical_columns = [
        "Jenis Kelamin",
        "Sering buang air kecil",
        "Sering haus berlebihan",
        "Penurunan berat badan tiba-tiba",
        "Kelemahan",
        "Sering lapar berlebihan",
        "Infeksi jamur genital",
        "Penglihatan kabur",
        "Gatal-gatal",
        "Mudah marah",
        "Luka lama sembuh",
        "Kelumpuhan sebagian",
        "Kekakuan otot",
        "Kerontokan rambut",
        "Obesitas"
    ]

    preprocessing = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_columns),
            ("cat", OneHotEncoder(), categorical_columns)
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessing", preprocessing),
            ("model", LogisticRegression(max_iter=1000, class_weight="balanced"))
        ]
    )

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    print("Accuracy Score :", accuracy_score(y_test, y_pred))
    print("\nClassification Report :\n", classification_report(y_test, y_pred))
    print("\nConfusion Matrix :\n", confusion_matrix(y_test, y_pred))
    """, language="python")

    # ----------------------------------------------------

    with st.expander("20. Model Decision Tree"):
        st.code("""
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
    from sklearn.preprocessing import StandardScaler, OneHotEncoder
    from sklearn.pipeline import Pipeline
    from sklearn.compose import ColumnTransformer

    # ================= DATA =================
    X = df[[
        "Umur",
        "Jenis Kelamin",
        "Sering buang air kecil",
        "Sering haus berlebihan",
        "Penurunan berat badan tiba-tiba",
        "Kelemahan",
        "Sering lapar berlebihan",
        "Infeksi jamur genital",
        "Penglihatan kabur",
        "Gatal-gatal",
        "Mudah marah",
        "Luka lama sembuh",
        "Kelumpuhan sebagian",
        "Kekakuan otot",
        "Kerontokan rambut",
        "Obesitas"
    ]]

    y = df["Kelas"]

    # ================= SPLIT =================
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # ================= PREPROCESS =================
    numeric_columns = ["Umur"]

    categorical_columns = [
        "Jenis Kelamin",
        "Sering buang air kecil",
        "Sering haus berlebihan",
        "Penurunan berat badan tiba-tiba",
        "Kelemahan",
        "Sering lapar berlebihan",
        "Infeksi jamur genital",
        "Penglihatan kabur",
        "Gatal-gatal",
        "Mudah marah",
        "Luka lama sembuh",
        "Kelumpuhan sebagian",
        "Kekakuan otot",
        "Kerontokan rambut",
        "Obesitas"
    ]

    preprocessing = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_columns),
            ("cat", OneHotEncoder(), categorical_columns)
        ]
    )

    # ================= MODEL =================
    model = Pipeline(
        steps=[
            ("preprocessing", preprocessing),
            ("model", DecisionTreeClassifier(random_state=42))
        ]
    )

    # ================= TRAIN =================
    model.fit(X_train, y_train)

    # ================= PREDIKSI =================
    y_pred = model.predict(X_test)

    # ================= EVALUASI =================
    print("=== DECISION TREE ===")
    print("Accuracy Score :", accuracy_score(y_test, y_pred))
    print("\nClassification Report :\n", classification_report(y_test, y_pred))
    print("\nConfusion Matrix :\n", confusion_matrix(y_test, y_pred))
    """, language="python")

    # ----------------------------------------------------

    with st.expander("21. Model Random Forest"):
        st.code("""
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
    from sklearn.preprocessing import StandardScaler, OneHotEncoder
    from sklearn.pipeline import Pipeline
    from sklearn.compose import ColumnTransformer

    # ================= DATA =================
    X = df[[
        "Umur",
        "Jenis Kelamin",
        "Sering buang air kecil",
        "Sering haus berlebihan",
        "Penurunan berat badan tiba-tiba",
        "Kelemahan",
        "Sering lapar berlebihan",
        "Infeksi jamur genital",
        "Penglihatan kabur",
        "Gatal-gatal",
        "Mudah marah",
        "Luka lama sembuh",
        "Kelumpuhan sebagian",
        "Kekakuan otot",
        "Kerontokan rambut",
        "Obesitas"
    ]]

    y = df["Kelas"]

    # ================= SPLIT =================
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # ================= PREPROCESS =================
    numeric_columns = ["Umur"]

    categorical_columns = [
        "Jenis Kelamin",
        "Sering buang air kecil",
        "Sering haus berlebihan",
        "Penurunan berat badan tiba-tiba",
        "Kelemahan",
        "Sering lapar berlebihan",
        "Infeksi jamur genital",
        "Penglihatan kabur",
        "Gatal-gatal",
        "Mudah marah",
        "Luka lama sembuh",
        "Kelumpuhan sebagian",
        "Kekakuan otot",
        "Kerontokan rambut",
        "Obesitas"
    ]

    preprocessing = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_columns),
            ("cat", OneHotEncoder(), categorical_columns)
        ]
    )

    # ================= MODEL =================
    model = Pipeline(
        steps=[
            ("preprocessing", preprocessing),
            ("model", RandomForestClassifier(n_estimators=100, random_state=42))
        ]
    )

    # ================= TRAIN =================
    model.fit(X_train, y_train)

    # ================= PREDIKSI =================
    y_pred = model.predict(X_test)

    # ================= EVALUASI =================
    print("=== RANDOM FOREST ===")
    print("Accuracy Score :", accuracy_score(y_test, y_pred))
    print("\nClassification Report :\n", classification_report(y_test, y_pred))
    print("\nConfusion Matrix :\n", confusion_matrix(y_test, y_pred))
    """, language="python")

    # ----------------------------------------------------

    with st.expander("22. Prediksi Data Baru"):
        st.code("""
    data_baru = pd.DataFrame(...)
    prediksi = model.predict(data_baru)[0]
    presentase = max(model.predict_proba(data_baru)[0])

    print(prediksi)
    print(presentase)
    """, language="python")

    # ----------------------------------------------------

    with st.expander("23. Menyimpan Model"):
        st.code("""
    import joblib
    joblib.dump(model,"model_prediksi_diabetes.joblib")
    """, language="python")

# ================= TAB 4: ABOUT =================
with tab4:
    col_foto, col_info = st.columns([1, 2])
    
    with col_foto:
        # Menggunakan HTML agar bisa memakai class profil-lingkaran
        # Pastikan file profil_adel.png tersedia di folder yang sama
        import base64

        def get_image_base64(path):
            try:
                with open(path, "rb") as image_file:
                    return base64.b64encode(image_file.read()).decode()
            except:
                return None

        img_base64 = get_image_base64("Adel1.jpeg")
        
        if img_base64:
            st.markdown(f"""
                <img src="data:image/png;base64,{img_base64}" class="profil-lingkaran">
            """, unsafe_allow_html=True)
        else:
            st.warning("Tambahkan file 'profil_adel.png' untuk menampilkan foto profil.")
    
    with col_info:
        st.markdown("## 👨‍💻 About Me")
        st.markdown("### 👋 Halo! Saya **Adel**")
        st.markdown("""
        Saya adalah seorang pelajar yang memiliki ketertarikan besar di dunia **teknologi**,  
        khususnya pada bidang **Machine Learning** dan **Data Science**.
        
        Perjalanan belajar saya dimulai dari kelas 11 SMK, dari rasa penasaran tentang bagaimana  
        data bisa diolah menjadi sesuatu yang **bermanfaat**.
        """)

    st.markdown("---")
    st.markdown("### 🚀 Apa yang saya kerjakan sekarang?")
    st.markdown("- 🧠 Sistem prediksi diabetes | - 📊 Analisis data | - 💻 Aplikasi Streamlit")
    
    st.markdown("""
    <div class="social-container">
        <a href="https://github.com/shananazz" target="_blank">💻 GitHub</a>
        <a href="https://www.instagram.com/shaahnaazza" target="_blank">📸 Instagram</a>
    </div>
    """, unsafe_allow_html=True)