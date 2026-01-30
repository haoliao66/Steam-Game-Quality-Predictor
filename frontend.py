import streamlit as st
import httpx
from streamlit_tags import st_tags
import pandas as pd

url = "http://127.0.0.1:8000/api/steam/v1/predict"

def predict_class(payload):
    try:
        with httpx.Client(timeout=60) as client:
            response = client.post(url, json=payload)
            response.raise_for_status()
            return response
    except Exception as e:
        st.error(f"Error during prediction: {e}")
        return None

st.set_page_config(
    page_title="Steam Predictor",
    layout="wide" 
)

left, right = st.columns([4, 3])

with left:
    col1, col2 = st.columns([8 , 1])

    with col1:
        st.title("Steam Game Quality Predictor")
    with col2:
        st.markdown("<p style='text-align: right; color: #888; font-size: 1.1rem; margin-top: 1.2rem;'>v0.0.1</p>", unsafe_allow_html=True)

#Input form 
    with st.form("game_data"):
        price = st.number_input(
            "Current Price(USD)", min_value=0.0, max_value=100.0, value=2.99, step=1.0
        )
        initial_price = st.number_input(
            "Initial Release Price(USD)", min_value=0.0, max_value=100.0, value=2.99, step=1.0
        )

        languages = st_tags(
        label='Languages:',
        text='Press enter to add (e.g., Japanese, Spanish)',
        value=['English'],  
        suggestions=[
            'English', 'Simplified Chinese', 'Spanish', 'Japanese', 
            'Russian', 'German', 'French', 'Portuguese', 'Korean',
            'Italian', 'Polish'
        ],
        maxtags=20,  
        key='game_languages'
        )

        genres = st_tags(
        label='Genres:',
        text='Press enter to add (e.g., Action, RPG)',
        value=['Indie'], 
        suggestions=[
            'Action', 'Adventure', 'RPG', 'Strategy', 'Simulation'
        ],
        maxtags=10,
        key='game_genres'
    )

        tags = st_tags(
        label='Tags:',
        text='Press enter to add (e.g., FPS, Moddable)',
        value=['Indie', 'Action'], 
        suggestions=['FPS', 'RPG', 'Pixel Graphics', 'Multiplayer', 'Moddable'],
        maxtags=50,  
        key='game_tags'
        )

        submitted = st.form_submit_button("PREDICT")

    if submitted:
        with st.spinner("Calculating...", show_time=True):
            payload = {
            'price': price,
            'initialprice': initial_price,
            'languages': languages,  
            'genre': genres,
            'tags': tags
            }

        
            response = predict_class(payload=payload).json()
            prob = response.get("probability")[1]
                    
            # Use Streamlit native components only
            st.metric(
                label="Probability to get 'Mostly Positive' Reviews",
                value=f"{prob:.1%}")


with right:
    # Executive Summary
    st.markdown("""
        ### What is this?
        Steam Game Quality Predictor is an **XGBoost machine learning model** trained on data from more than 25,000 commercial games on Steam that predicts how it will be received
        by players and whether it will achieve **"Mostly Positive"** reviews (70%+ positive rating with 10+ reviews) or above based on 
        attributes available before launch.
                
        Simply input your game's planned price, supported languages, genres, and Steam tags to get a prediction of its likelihood to be well-received by players.
                """)

    # Data Transparency
    with st.expander("Data Source & Methodology", expanded=False):
        st.markdown("""
        **Training Data:** SteamSpy API  
        **Filter:** Games with ≥20,000 owners (filtering out ultra-niche/unreleased titles)  
        **Target Variable:** "Mostly Positive" or better Steam rating (70%+ positive)  
        **Algorithm:** XGBoost (Tuned)  
        
        **Why 20K owners?** Games below this threshold often have too few reviews for statistically 
        meaningful ratings, or may be abandoned projects rather than commercial releases.
        """)
    with st.expander("Model Performance", expanded=False):
        cols = st.columns(5)
        metrics = {
        "Precision": "76.3%",
        "Recall": "83.1%", 
        "F1-Score": "79.6%",
        "Accuracy": "73.3%",
        "ROC-AUC": "70.0%"
        }
        
        for col, (metric, value) in zip(cols, metrics.items()):
            with col:
                st.metric(label=metric, value=value)

    with st.expander("Top 25 important features for quality", expanded=False):
            
        top_features = pd.DataFrame({
                'feature': [
                    'Great Soundtrack', 'Classic', 'Initial Price', 'Hentai', 
                    'Massively Multiplayer', 'Free to Play', 'Sexual Content',
                    'Japanese Language', 'Moddable', 'Difficult', 'Cats', 'Cute',
                    'Visual Novel', 'Massively Multiplayer (Genre)', 'Romance',
                    'Short', 'Political Sim', 'Funny', 'Emotional', 'Portuguese (BR)',
                    'Extraction Shooter', 'Politics', '3D Vision', 'Anime', 'Psychological Horror'
                ],
                'importance': [
                    1.59, 0.72, 0.67, 0.63, 0.58, 0.53, 0.50,
                    0.49, 0.48, 0.47, 0.44, 0.43, 0.42, 0.40,
                    0.40, 0.38, 0.38, 0.38, 0.37, 0.37,
                    0.35, 0.34, 0.34, 0.34, 0.33
                ]
            })
            
        st.bar_chart(top_features.set_index('feature'), height=400)
