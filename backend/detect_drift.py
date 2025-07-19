import pandas as pd
from sklearn import datasets
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab, CatTargetDriftTab
import mlflow

mlflow.set_tracking_uri("http://mlflow:5000")
mlflow.set_experiment("iris-classification")

with mlflow.start_run():
    # Load the iris dataset
    iris_data = datasets.load_iris(as_frame=True)
    iris_frame = iris_data.frame

    # Split the data into two parts
    reference_data = iris_frame.iloc[:100]
    current_data = iris_frame.iloc[100:]

    # Create a dashboard
    drift_dashboard = Dashboard(tabs=[DataDriftTab(), CatTargetDriftTab(verbose_level=1)])
    drift_dashboard.calculate(reference_data, current_data, column_mapping=None)

    # Save the dashboard and log it as an artifact
    report_path = "drift_report.html"
    drift_dashboard.save(report_path)
    mlflow.log_artifact(report_path)

    print(f"Drift report saved to {report_path} and logged to MLflow.")
