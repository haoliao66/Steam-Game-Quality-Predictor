<img width="1900" height="972" alt="Screenshot 2026-01-30 164607" src="https://github.com/user-attachments/assets/158172f1-946c-410d-a9da-21f25d0532c1" />

## Overview
Steam Game Quality Predictor is an XGBoost machine learning model trained on data from more than 25,000 commercial games on Steam that predicts how it will be received by players and whether it will achieve "Mostly Positive" reviews (70%+ positive rating with 10+ reviews) or above based on attributes available before launch.

The ML model is served on a FastAPI backend, and Streamlit frontend UI is built on top of the API to allow user interaction.


## Set-up
Clone the repo and set up the virtual environment:
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt #install requirements
```
Then run FastAPI backend:
```
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```
and run Streamlit frontend:
```
streamlit run app.py 
```

## Data
Training Data is obtained from the [Steamspy API](https://steamspy.com/api.php). To refresh the data, you can run:
```
python data/fetch.py
```
