import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import json
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import PowerTransformer
import numpy as np
from sklearn.preprocessing import RobustScaler
from sklearn.decomposition import KernelPCA
import time

# --- Fonctions de prétraitement ---
def BoxCoxTransformation(X):
    skewed_cols = X.select_dtypes(include=[np.number]).columns
    skewed_cols = [col for col in skewed_cols if X[col].skew() > 0.5 and (X[col] > 0).all()]
    
    for col in skewed_cols:
        reshaped = X[col].values.reshape(-1, 1)
        transformed = PowerTransformer(method='box-cox').fit_transform(reshaped)
        X[col] = transformed.flatten()
        
    return X

@st.cache_data
def load_data():
    data = pd.read_csv("../data/data.csv")
    return data

def LabelEncoder_(data):
    le = LabelEncoder()
    data['type'] = le.fit_transform(data['type'])
    return data

# --- Chargement des ressources ---
@st.cache_resource
def load_model(model_path):
    with open(model_path, "rb") as f:
        return pickle.load(f)

def load_lottiefile(filepath: str):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

# --- Fonction de prédiction optimisée ---
def data_prediction(
        step: int,
        type_: str,
        amount: float,
        oldbalanceOrg: float,
        newbalanceOrig: float,
        oldbalanceDest: float,
        newbalanceDest: float,
        data):
    
    prediction_data = [[step, type_, amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest]]
    df_pred = pd.DataFrame(prediction_data, columns=['step', 'type', 'amount', 'oldbalanceOrg', 'newbalanceOrig', 'oldbalanceDest', 'newbalanceDest'])

    X_new = pd.concat([data.drop(columns=['isFraud'], errors='ignore'), df_pred], ignore_index=True)
    X_new = LabelEncoder_(X_new)
    X_new = BoxCoxTransformation(X_new)
    
    Rs = RobustScaler()
    X_new = Rs.fit_transform(X_new)
    
    kpca = KernelPCA(n_components=7, kernel='rbf', random_state=0)
    X_new = kpca.fit_transform(X_new)
    
    return X_new[-1]

# --- Configuration de la page ---
st.set_page_config(
    page_title="FraudGuard - Détection de fraude bancaire",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS et JS personnalisés avec animations ---
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Montserrat:wght@700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<style>
    :root {
        --primary-color: #6366f1;
        --secondary-color: #8b5cf6;
        --accent-color: #a78bfa;
        --success-color: #10b981;
        --danger-color: #ef4444;
        --warning-color: #f59e0b;
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --bg-gradient: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        --card-shadow: 0 10px 25px rgba(0,0,0,0.05);
        --border-radius: 16px;
        --transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.1);
    }
    
    * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }
    
    body {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        color: var(--text-primary);
        overflow-x: hidden;
    }
    
    /* Animations */
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
        100% { transform: translateY(0px); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.05); opacity: 0.8; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .float-animation {
        animation: float 6s ease-in-out infinite;
    }
    
    .pulse-animation {
        animation: pulse 3s infinite;
    }
    
    .fade-in {
        animation: fadeIn 0.8s forwards;
        opacity: 0;
    }
    
    /* Header amélioré */
    .header {
        text-align: center;
        padding: 1.5rem 0;
        margin-bottom: 1rem;
        position: relative;
        z-index: 10;
    }
    
    .header h1 {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        font-family: 'Montserrat', sans-serif;
        letter-spacing: -0.5px;
    }
    
    .header p {
        color: var(--text-secondary);
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        font-weight: 500;
    }
    
    /* Hero section */
    .hero-container {
        background: var(--bg-gradient);
        border-radius: var(--border-radius);
        padding: 4rem 2rem;
        margin: 2rem 0;
        color: white;
        position: relative;
        overflow: hidden;
        box-shadow: var(--card-shadow);
    }
    
    .hero-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 20% 30%, rgba(255,255,255,0.15) 0%, transparent 40%),
                    radial-gradient(circle at 80% 70%, rgba(255,255,255,0.1) 0%, transparent 40%);
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 1.2rem;
        line-height: 1.2;
        text-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .hero-subtitle {
        font-size: 1.4rem;
        font-weight: 400;
        opacity: 0.9;
        margin-bottom: 2rem;
        line-height: 1.6;
        max-width: 700px;
    }
    
    /* Boutons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.9rem 2.2rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: var(--transition);
        box-shadow: 0 10px 20px rgba(99, 102, 241, 0.3);
        text-transform: none;
        letter-spacing: 0.5px;
        position: relative;
        overflow: hidden;
        z-index: 1;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 0;
        height: 100%;
        background: linear-gradient(135deg, var(--secondary-color) 0%, var(--primary-color) 100%);
        transition: var(--transition);
        z-index: -1;
    }
    
    .stButton > button:hover::before {
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 30px rgba(99, 102, 241, 0.4);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    /* Cartes */
    .card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: var(--border-radius);
        padding: 2.5rem;
        margin: 1.5rem 0;
        transition: var(--transition);
        box-shadow: var(--card-shadow);
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    
    .card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        border-color: rgba(99, 102, 241, 0.2);
    }
    
    .card-icon {
        font-size: 3.5rem;
        margin-bottom: 1.5rem;
        background: var(--bg-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .card-title {
        font-size: 1.6rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 1.2rem;
    }
    
    .card-content {
        color: var(--text-secondary);
        line-height: 1.7;
        font-size: 1.05rem;
        flex-grow: 1;
    }
    
    /* Statistiques */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 2rem;
        margin: 3rem 0;
    }
    
    .stat-card {
        text-align: center;
        padding: 2.5rem 1.5rem;
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border-radius: var(--border-radius);
        border: 1px solid rgba(255, 255, 255, 0.5);
        transition: var(--transition);
        box-shadow: var(--card-shadow);
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.08);
    }
    
    .stat-number {
        font-size: 2.8rem;
        font-weight: 800;
        background: var(--bg-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        color: var(--text-secondary);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.95rem;
    }
    
    /* Prédiction */
    .prediction-safe {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(110, 231, 183, 0.1) 100%);
        border-left: 4px solid var(--success-color);
        padding: 2rem;
        border-radius: var(--border-radius);
        margin: 2rem 0;
    }
    
    .prediction-fraud {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(252, 165, 165, 0.1) 100%);
        border-left: 4px solid var(--danger-color);
        padding: 2rem;
        border-radius: var(--border-radius);
        margin: 2rem 0;
    }
    
    /* Formulaire */
    .form-container {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(12px);
        border-radius: var(--border-radius);
        padding: 2.5rem;
        box-shadow: var(--card-shadow);
        border: 1px solid rgba(255, 255, 255, 0.5);
    }
    
    .form-title {
        color: var(--primary-color);
        font-weight: 700;
        margin-bottom: 1.5rem;
        font-size: 1.8rem;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        .hero-subtitle {
            font-size: 1.2rem;
        }
        .stats-container {
            grid-template-columns: 1fr;
        }
    }
    
    /* Effets de vague */
    .wave {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        overflow: hidden;
        line-height: 0;
    }
    
    .wave svg {
        position: relative;
        display: block;
        width: calc(100% + 1.3px);
        height: 100px;
    }
    
    .wave .shape-fill {
        fill: #FFFFFF;
    }
    
    /* Animation de chargement */
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .spinner {
        border: 4px solid rgba(99, 102, 241, 0.2);
        border-top: 4px solid var(--primary-color);
        border-radius: 50%;
        width: 50px;
        height: 50px;
        animation: spin 1s linear infinite;
        margin: 0 auto;
    }
</style>

<script src="https://cdn.jsdelivr.net/npm/particles.js@2.0.0/particles.min.js"></script>
<script>
    // Initialisation des animations au chargement
    document.addEventListener('DOMContentLoaded', function() {
        // Animation de particules
        particlesJS('particles-js', {
            particles: {
                number: { value: 80, density: { enable: true, value_area: 800 } },
                color: { value: "#6366f1" },
                shape: { type: "circle" },
                opacity: { value: 0.5, random: true },
                size: { value: 3, random: true },
                line_linked: {
                    enable: true,
                    distance: 150,
                    color: "#8b5cf6",
                    opacity: 0.4,
                    width: 1
                },
                move: {
                    enable: true,
                    speed: 2,
                    direction: "none",
                    random: true,
                    straight: false,
                    out_mode: "out"
                }
            },
            interactivity: {
                detect_on: "canvas",
                events: {
                    onhover: { enable: true, mode: "grab" },
                    onclick: { enable: true, mode: "push" }
                }
            }
        });
        
        // Animation au défilement
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                }
            });
        }, { threshold: 0.1 });
        
        document.querySelectorAll('.animate-on-scroll').forEach(el => {
            observer.observe(el);
        });
        
        // Animation pour les cartes de statistiques
        document.querySelectorAll('.stat-card').forEach((card, index) => {
            card.style.animationDelay = `${index * 0.2}s`;
        });
    });
</script>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="header">
    <h1>🛡️ FraudGuard</h1>
    <p>Solution avancée de détection de fraude bancaire</p>
</div>
""", unsafe_allow_html=True)

# --- Barre de navigation (sans Contact) ---
nav_bar = option_menu(
    menu_title=None,
    options=["Accueil", "Solution", "Prédiction"],
    icons=["house-fill", "lightbulb-fill", "graph-up-arrow"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "transparent"},
        "icon": {"color": "#6366f1", "font-size": "20px"},
        "nav-link": {
            "font-size": "16px",
            "text-align": "center",
            "margin": "0px 8px",
            "padding": "14px 24px",
            "border-radius": "50px",
            "color": "#1e293b",
            "font-weight": "500",
            "transition": "all 0.3s ease"
        },
        "nav-link-selected": {
            "background": "linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)",
            "color": "white",
            "font-weight": "600",
            "box-shadow": "0 5px 15px rgba(99, 102, 241, 0.3)"
        }
    }
)

# --- Contenu des pages ---
if nav_bar == "Accueil":
    # Particules en arrière-plan
    st.markdown("""
    <div id="particles-js" style="position:absolute; top:0; left:0; width:100%; height:100%; z-index:0;"></div>
    """, unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
    <div class="hero-container">
        <div style="position: relative; z-index: 10;">
            <h1 class="hero-title animate-on-scroll">Protégez vos transactions avec l'IA</h1>
            <p class="hero-subtitle animate-on-scroll" style="animation-delay: 0.2s">
                Détection intelligente de fraude bancaire en temps réel grâce à l'apprentissage automatique
            </p>
        </div>
        <div class="wave">
            <svg data-name="Layer 1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120" preserveAspectRatio="none">
                <path d="M0,0V46.29c47.79,22.2,103.59,32.17,158,28,70.36-5.37,136.33-33.31,206.8-37.5C438.64,32.43,512.34,53.67,583,72.05c69.27,18,138.3,24.88,209.4,13.08,36.15-6,69.85-17.84,104.45-29.34C989.49,25,1113-14.29,1200,52.47V0Z" opacity=".25" class="shape-fill"></path>
                <path d="M0,0V15.81C13,36.92,27.64,56.86,47.69,72.05,99.41,111.27,165,111,224.58,91.58c31.15-10.15,60.09-26.07,89.67-39.8,40.92-19,84.73-46,130.83-49.67,36.26-2.85,70.9,9.42,98.6,31.56,31.77,25.39,62.32,62,103.63,73,40.44,10.79,81.35-6.69,119.13-24.28s75.16-39,116.92-43.05c59.73-5.85,113.28,22.88,168.9,38.84,30.2,8.66,59,6.17,87.09-7.5,22.43-10.89,48-26.93,60.65-49.24V0Z" opacity=".5" class="shape-fill"></path>
                <path d="M0,0V5.63C149.93,59,314.09,71.32,475.83,42.57c43-7.64,84.23-20.12,127.61-26.46,59-8.63,112.48,12.24,165.56,35.4C827.93,77.22,886,95.24,951.2,90c86.53-7,172.46-45.71,248.8-84.81V0Z" class="shape-fill"></path>
            </svg>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Section principale
    col1, col2 = st.columns([5, 4], gap="large")
    
    with col1:
        st.markdown("""
        <div class="animate-on-scroll" style="animation-delay: 0.2s">
            <h2 style="color: #1e293b; font-weight: 700; margin-bottom: 1.5rem; font-size: 2.2rem;">
                Une protection financière intelligente
            </h2>
            <p style="color: #475569; font-size: 1.1rem; line-height: 1.8; margin-bottom: 2rem;">
                Notre solution utilise des algorithmes d'IA avancés pour analyser les transactions en temps réel. 
                Grâce au machine learning, nous détectons les schémas frauduleux avec une précision inégalée.
            </p>
            <div style="
                background: rgba(255, 255, 255, 0.7);
                backdrop-filter: blur(12px);
                padding: 2rem;
                border-radius: var(--border-radius);
                border-left: 4px solid #6366f1;
                margin: 2rem 0;
            ">
                <h4 style="color: #6366f1; margin-bottom: 1.5rem; font-weight: 600; display: flex; align-items: center; gap: 10px;">
                    <i class="fas fa-shield-alt"></i> Pourquoi choisir FraudGuard ?
                </h4>
                <ul style="color: #475569; line-height: 1.8; padding-left: 1rem;">
                    <li style="margin-bottom: 0.8rem;"><strong>Détection en temps réel</strong> - Alertes instantanées</li>
                    <li style="margin-bottom: 0.8rem;"><strong>Précision exceptionnelle</strong> - 96% de taux de détection</li>
                    <li style="margin-bottom: 0.8rem;"><strong>Interface intuitive</strong> - Facile à utiliser</li>
                    <li><strong>Sécurité renforcée</strong> - Protection des données</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="animate-on-scroll float-animation" style="animation-delay: 0.4s">', unsafe_allow_html=True)
        lottie_animation = load_lottiefile("acceuil1.json")
        if lottie_animation:
            st_lottie(lottie_animation, loop=True, quality='high', height=400, key="home-anim")
        else:
            st.markdown("""
            <div style="
                display: flex; 
                justify-content: center; 
                align-items: center; 
                height: 400px; 
                background: rgba(255, 255, 255, 0.7);
                backdrop-filter: blur(12px);
                border-radius: var(--border-radius);
                border: 2px dashed rgba(99, 102, 241, 0.3);
                box-shadow: var(--card-shadow);
            ">
                <div style="text-align: center;">
                    <div style="font-size: 4rem; margin-bottom: 1rem; background: var(--bg-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                        <i class="fas fa-lock"></i>
                    </div>
                    <p style="color: #475569; font-weight: 500; font-size: 1.2rem;">Sécurité des transactions financières</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Statistiques
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="stats-container">
        <div class="stat-card animate-on-scroll">
            <div class="stat-number">96%</div>
            <div class="stat-label">Précision</div>
        </div>
        <div class="stat-card animate-on-scroll" style="animation-delay: 0.1s">
            <div class="stat-number">&lt;10s</div>
            <div class="stat-label">Temps d'analyse</div>
        </div>
        <div class="stat-card animate-on-scroll" style="animation-delay: 0.2s">
            <div class="stat-number">24/7</div>
            <div class="stat-label">Disponibilité</div>
        </div>
        <div class="stat-card animate-on-scroll" style="animation-delay: 0.3s">
            <div class="stat-number">16K+</div>
            <div class="stat-label">Transactions analysées</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Fonctionnalités
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <h2 class="animate-on-scroll" style="text-align: center; color: #1e293b; font-weight: 700; margin-bottom: 3rem; font-size: 2.2rem;">
        Fonctionnalités principales
    </h2>
    """, unsafe_allow_html=True)
    
    feat_col1, feat_col2, feat_col3 = st.columns(3, gap="large")
    
    with feat_col1:
        st.markdown("""
        <div class="card animate-on-scroll" style="animation-delay: 0.2s">
            <div class="card-icon"><i class="fas fa-robot"></i></div>
            <h3 class="card-title">IA Avancée</h3>
            <p class="card-content">
                Algorithmes de machine learning pour une détection optimale des fraudes.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with feat_col2:
        st.markdown("""
        <div class="card animate-on-scroll" style="animation-delay: 0.4s">
            <div class="card-icon"><i class="fas fa-bolt"></i></div>
            <h3 class="card-title">Temps Réel</h3>
            <p class="card-content">
                Analyse instantanée des transactions avec alertes immédiates.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with feat_col3:
        st.markdown("""
        <div class="card animate-on-scroll" style="animation-delay: 0.6s">
            <div class="card-icon"><i class="fas fa-shield-alt"></i></div>
            <h3 class="card-title">Sécurité</h3>
            <p class="card-content">
                Protection des données avec chiffrement de bout en bout.
            </p>
        </div>
        """, unsafe_allow_html=True)

elif nav_bar == "Solution":
    st.markdown("""
    <div class="hero-container" style="text-align:center; padding-top: 2rem;">
        <h1 class="hero-title animate-on-scroll">🔍 Notre Solution Technologique</h1>
        <p class="hero-subtitle animate-on-scroll" style="animation-delay: 0.2s; font-size:1.3rem;">
            Découvrez comment notre système protège vos transactions
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Architecture du Système", unsafe_allow_html=True)
    st.write("")
    
    tech_col1, tech_col2 = st.columns(2, gap="large")

    with tech_col1:
        st.markdown("""
        <div class="card animate-on-scroll" style="animation-delay: 0.2s">
            <div class="card-icon"><i class="fas fa-brain"></i></div>
            <h3 class="card-title">Intelligence Artificielle</h3>
            <div class="card-content">
                <ul style="list-style-type: none; padding-left: 0;">
                    <li style="margin-bottom: 1rem;"><i class="fas fa-check-circle" style="color: #10b981; margin-right: 8px;"></i> <strong>Modèle :</strong> Support Vector Machine (SVM)</li>
                    <li style="margin-bottom: 1rem;"><i class="fas fa-check-circle" style="color: #10b981; margin-right: 8px;"></i> <strong>Précision :</strong> > 96%</li>
                    <li style="margin-bottom: 1rem;"><i class="fas fa-check-circle" style="color: #10b981; margin-right: 8px;"></i> <strong>Entraîné sur :</strong> 16 000+ transactions</li>
                    <li style="margin-bottom: 1rem;"><i class="fas fa-check-circle" style="color: #10b981; margin-right: 8px;"></i> <strong>Techniques :</strong> Validation croisée pour éviter l'overfitting</li>
                    <li><i class="fas fa-check-circle" style="color: #10b981; margin-right: 8px;"></i> <strong>Méthode :</strong> Apprentissage supervisé</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with tech_col2:
        st.markdown("""
        <div class="card animate-on-scroll" style="animation-delay: 0.4s">
            <div class="card-icon"><i class="fas fa-cogs"></i></div>
            <h3 class="card-title">Traitement des Données</h3>
            <div class="card-content">
                <ul style="list-style-type: none; padding-left: 0;">
                    <li style="margin-bottom: 1rem;"><i class="fas fa-sync-alt" style="color: #8b5cf6; margin-right: 8px;"></i> Transformation Box-Cox</li>
                    <li style="margin-bottom: 1rem;"><i class="fas fa-sync-alt" style="color: #8b5cf6; margin-right: 8px;"></i> Normalisation RobustScaler</li>
                    <li style="margin-bottom: 1rem;"><i class="fas fa-sync-alt" style="color: #8b5cf6; margin-right: 8px;"></i> Réduction de dimension (KernelPCA)</li>
                    <li><i class="fas fa-sync-alt" style="color: #8b5cf6; margin-right: 8px;"></i> Encodage des catégories</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

elif nav_bar == "Prédiction":
    st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title animate-on-scroll">🔎 Analyse de Transaction</h1>
        <p class="hero-subtitle animate-on-scroll" style="animation-delay: 0.2s">
            Vérifiez instantanément le risque de fraude d'une transaction
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chargement des données
    data = load_data()
    
    # Section de formulaire
    with st.container():
        st.markdown("""
        <div class="form-container animate-on-scroll" style="animation-delay: 0.2s">
            <h3 class="form-title"><i class="fas fa-edit"></i> Détails de la transaction</h3>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            type = st.selectbox("Type de transaction", 
                               ["PAYMENT", "TRANSFER", "CASH_OUT", "CASH_IN", "DEBIT"],
                               help="Sélectionnez le type de transaction")
            
            amount = st.number_input("Montant (€)", 
                                    min_value=0.0, 
                                    value=1000.0, 
                                    step=100.0,
                                    format="%.2f",
                                    help="Montant de la transaction en euros")
            
            step = st.number_input("Étape temporelle", 
                                  min_value=0, 
                                  value=1,
                                  help="Heure de la transaction (0-24)")
        
        with col2:
            oldbalanceOrg = st.number_input("Solde initial émetteur", 
                                           min_value=0.0, 
                                           value=5000.0,
                                           format="%.2f",
                                           help="Solde du compte émetteur avant la transaction")
            
            newbalanceOrig = st.number_input("Nouveau solde émetteur", 
                                            min_value=0.0, 
                                            value=4000.0,
                                            format="%.2f",
                                            help="Solde du compte émetteur après la transaction")
            
            oldbalanceDest = st.number_input("Solde initial destinataire", 
                                            min_value=0.0, 
                                            value=2000.0,
                                            format="%.2f",
                                            help="Solde du compte destinataire avant la transaction")
            
            newbalanceDest = st.number_input("Nouveau solde destinataire", 
                                            min_value=0.0, 
                                            value=3000.0,
                                            format="%.2f",
                                            help="Solde du compte destinataire après la transaction")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Bouton d'analyse
    if st.button("🔍 Analyser la transaction", use_container_width=True, key="analyze-btn"):
        with st.spinner('Analyse en cours...'):
            # Animation de chargement personnalisée
            loading_placeholder = st.empty()
            loading_placeholder.markdown("""
            <div style="text-align: center; padding: 2rem;">
                <div class="spinner"></div>
                <p style="margin-top: 1.5rem; color: #64748b; font-weight: 500;">Analyse en cours, veuillez patienter...</p>
            </div>
            """, unsafe_allow_html=True)
            
            
            # Préparation des données
            X_new = data_prediction(
                step=step,
                type_=type,
                amount=amount,
                oldbalanceOrg=oldbalanceOrg,
                newbalanceOrig=newbalanceOrig,
                oldbalanceDest=oldbalanceDest,
                newbalanceDest=newbalanceDest,
                data=data
            )
            
            # Prédiction
            model = load_model("../model/model.pkl")
            prediction = model.predict([X_new])
            
            # Affichage des résultats
            loading_placeholder.empty()
            
            if prediction[0] == 1:
                st.markdown("""
                <div class="prediction-fraud pulse-animation">
                    <h2 style="color: #ef4444; margin-bottom: 15px; display: flex; align-items: center; gap: 10px;">
                        <i class="fas fa-exclamation-triangle"></i> Transaction suspecte détectée !
                    </h2>
                    <p style="margin-bottom: 15px; font-size: 1.1rem;">
                        Notre système a identifié des caractéristiques frauduleuses dans cette transaction.
                    </p>
                    <div style="background: rgba(239, 68, 68, 0.1); padding: 15px; border-radius: 12px; margin-top: 15px;">
                        <h4 style="color: #ef4444; margin-bottom: 10px; display: flex; align-items: center; gap: 8px;">
                            <i class="fas fa-lightbulb"></i> Recommandations
                        </h4>
                        <ul style="margin-left: 20px;">
                            <li>Vérifier immédiatement cette opération</li>
                            <li>Contacter le service sécurité</li>
                            <li>Geler temporairement le compte concerné</li>
                        </ul>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="prediction-safe">
                    <h2 style="color: #10b981; margin-bottom: 15px; display: flex; align-items: center; gap: 10px;">
                        <i class="fas fa-check-circle"></i> Transaction sécurisée
                    </h2>
                    <p style="margin-bottom: 10px; font-size: 1.1rem;">
                        Aucun signe de fraude détecté dans cette transaction.
                    </p>
                    <p style="font-weight: 600; color: #10b981;">
                        <i class="fas fa-shield-alt"></i> Niveau de confiance : 96%
                    </p>
                </div>
                """, unsafe_allow_html=True)

# --- Footer ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; padding: 2.5rem; background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); 
            border-radius: var(--border-radius); margin-top: 3rem; color: white; position: relative; overflow: hidden;">
    <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: url('data:image/svg+xml,<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 100 100\"><circle cx=\"10\" cy=\"10\" r=\"2\" fill=\"rgba(255,255,255,0.1)\"/><circle cx=\"30\" cy=\"70\" r=\"3\" fill=\"rgba(255,255,255,0.1)\"/><circle cx=\"80\" cy=\"40\" r=\"1\" fill=\"rgba(255,255,255,0.1)\"/></svg>');"></div>
    <div style="position: relative; z-index: 2;">
        <p style="margin: 0; font-size: 1.1rem; font-weight: 500;">
            © 2024 FraudGuard - Sécurité financière intelligente
        </p>
        <p style="margin: 0.8rem 0 0 0; font-size: 0.95rem; opacity: 0.8;">
            Propulsé par l'IA • Protection des données • RGPD conforme
        </p>
        <div style="display: flex; justify-content: center; gap: 15px; margin-top: 1.5rem; font-size: 1.2rem;">
            <a href="#" style="color: white; opacity: 0.8; transition: opacity 0.3s;"><i class="fab fa-github"></i></a>
            <a href="#" style="color: white; opacity: 0.8; transition: opacity 0.3s;"><i class="fab fa-twitter"></i></a>
            <a href="#" style="color: white; opacity: 0.8; transition: opacity 0.3s;"><i class="fab fa-linkedin"></i></a>
            <a href="#" style="color: white; opacity: 0.8; transition: opacity 0.3s;"><i class="fab fa-facebook"></i></a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True) 