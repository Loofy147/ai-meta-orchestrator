import pandas as pd
from sklearn import datasets
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab, CatTargetDriftTab

# Load the iris dataset
iris_data = datasets.load_iris(as_frame=True)
iris_frame = iris_data.frame

# Split the data into two parts
reference_data = iris_frame.iloc[:100]
current_data = iris_frame.iloc[100:]

# Create a dashboard
drift_dashboard = Dashboard(tabs=[DataDriftTab(), CatTargetDriftTab(verbose_level=1)])
drift_dashboard.calculate(reference_data, current_data, column_mapping=None)

# Save the dashboard
drift_dashboard.save("drift_report.html")
