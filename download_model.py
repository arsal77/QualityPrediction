import mlflow
import os
import shutil

MLFLOW_TRACKING_URI = os.environ.get("MLFLOW_TRACKING_URI","http://localhost:5000")
MODEL_NAME = os.environ.get("MLFLOW_MODEL_NAME", "quality-predictor")
MODEL_ALIAS = os.environ.get("MLFLOW_MODEL_ALIAS", "production")
OUTPUT_PATH = "./model_artifacts" # The local folder where the model will be saved
# ---------------------

def download_production_model():
    """
    Connects to the MLflow server, downloads the production model,
    and saves it to a local directory.
    """
    print(f"Connecting to MLflow at: {MLFLOW_TRACKING_URI}")
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    
    model_uri = f"models:/{MODEL_NAME}@{MODEL_ALIAS}"
    
    # Clean up any old model artifacts before downloading
    if os.path.exists(OUTPUT_PATH):
        print(f"Removing existing model directory: {OUTPUT_PATH}")
        shutil.rmtree(OUTPUT_PATH)
        
    print(f"Downloading model from '{model_uri}' to '{OUTPUT_PATH}'...")
    
    # This is the key MLflow command to download the files
    mlflow.artifacts.download_artifacts(
        artifact_uri=model_uri,
        dst_path=OUTPUT_PATH
    )
    
    print("Model downloaded successfully.")

if __name__ == "__main__":
    download_production_model()
    