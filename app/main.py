from fastapi import FastAPI
from pydantic import BaseModel,Field
import mlflow
import numpy as np
import pandas as pd


model=mlflow.pyfunc.load_model('/app/model_artifacts')


class Data(BaseModel) :
    fixed_acidity : float = Field(alias='fixed acidity')
    volatile_acidity : float = Field(alias='volatile acidity')
    citric_acid : float = Field(alias='citric acid')
    residual_sugar : float = Field(alias='residual sugar')
    chlorides :float 
    free_sulfur_dioxide : float = Field(alias='free sulfur dioxide')
    total_sulfur_dioxide : float = Field(alias='total sulfur dioxide')
    density : float
    pH : float 
    sulphates : float
    alcohol :float

app = FastAPI()
@app.post("/predict",tags=["Prediction"])
async def InputData(data : Data) :
    input_dict = data.model_dump(by_alias=True)
    input_data = pd.DataFrame({k:[v] for k,v in input_dict.items()})
    input_data = input_data.astype(np.float32)


    prediction=model.predict(input_data)
    predicted_quality = prediction[0]

    return {"predicted_quality": predicted_quality.item()}




