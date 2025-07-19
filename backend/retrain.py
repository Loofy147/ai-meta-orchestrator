import mlflow
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load the iris dataset
iris = load_iris()
X = iris.data
y = iris.target

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Start an MLflow run
with mlflow.start_run() as run:
    # Train a model
    n_estimators = 150  # Increase n_estimators for retraining
    model = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy}")

    # Log parameters and metrics
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_metric("accuracy", accuracy)

    # Register the model
    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="sklearn-model",
        registered_model_name="iris-model"
    )
