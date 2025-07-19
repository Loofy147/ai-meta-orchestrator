import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
import pandas as pd

mlflow.set_tracking_uri("http://mlflow:5000")
mlflow.set_experiment("iris-classification")

# In a real scenario, this would be a check against a production model and recent data
def check_for_drift():
    """
    Checks for data drift. In a real application, this would compare
    the current production data with a reference dataset.
    For this example, we'll just simulate a drift detection.
    """
    iris = load_iris(as_frame=True)
    reference_data = iris.frame.iloc[:75]
    current_data = iris.frame.iloc[75:]

    profile = Profile(sections=[DataDriftProfileSection()])
    profile.calculate(reference_data, current_data, None)
    result = profile.json()

    # For simplicity, we'll just say drift is detected.
    # In a real scenario, you would parse the result to check for drift.
    print("Drift detected. Retraining model.")
    return True

def retrain_model():
    """
    Retrains the model and registers the new version in the MLflow model registry.
    """
    with mlflow.start_run():
        # Load data
        iris = load_iris()
        X, y = iris.data, iris.target
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train model
        n_estimators = 150 # Using more estimators for the new model
        model = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
        model.fit(X_train, y_train)

        # Evaluate model
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        # Log params, metrics, and model
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="sklearn-model",
            registered_model_name="iris-model"
        )

        print(f"Model retrained with accuracy: {accuracy}")
        print(f"New model version registered as 'iris-model'")

if __name__ == "__main__":
    if check_for_drift():
        retrain_model()
