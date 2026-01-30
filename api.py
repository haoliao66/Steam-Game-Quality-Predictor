from fastapi import FastAPI, APIRouter
import pandas as pd
import cloudpickle
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/steam/v1")

app = FastAPI()

# request/response schemas
class PredictionRequest(BaseModel):
    price: float
    initialprice: float
    languages: list[str]
    genre: list[str]
    tags: list[str]

class PredictionOutput(BaseModel):
    target: int
    probability: list[float]

@router.post("/predict", response_model=PredictionOutput)
def predict_class(payload: PredictionRequest):
    data_dict = {
        'price': payload.price,
        'initialprice': payload.initialprice,
        'languages': payload.languages,  
        'genre': payload.genre,
        'tags': payload.tags
    }
    data_to_predict = pd.DataFrame([data_dict])

    f_in = open('model.bin', 'rb')
    model = cloudpickle.load(f_in)

    prediction = model.predict(data_to_predict)
    proba = model.predict_proba(data_to_predict).tolist()[0]
    print(prediction, proba)
    return {
        "target": int(prediction[0]),
        "probability": proba
    }

app.include_router(router=router)