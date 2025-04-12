# -*- coding: utf-8 -*-
"""Untitled3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1exTKRNEQRrTpgAdRdmX-5sHkXdAAvehI
"""

import pandas as pd

df = pd.read_csv("/content/Titanic-Dataset.csv")
df.head()

### Model Comparison Project - Jupyter Notebook

# Problem Statement
"""
In many real-world scenarios, having multiple candidate machine learning models allows data scientists to compare and choose the best performing approach for a given classification task.

This project aims to:
1. Divide the dataset into training and testing subsets.
2. Train at least five different classification models.
3. Record and compare their performances based on key evaluation metrics.
4. Perform hyper-parameter tuning for each model.
5. Build a dashboard that visualizes and compares the performance of these models.
"""

# 1. Import Libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

# Models
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns

# 2. Load Dataset
df = pd.read_csv("/content/Titanic-Dataset.csv")  # Updated path to dataset

# 3. Data Preprocessing
# Drop irrelevant or highly missing columns
if 'Name' in df.columns: df.drop(['Name'], axis=1, inplace=True)
if 'Cabin' in df.columns: df.drop(['Cabin'], axis=1, inplace=True)
if 'Ticket' in df.columns: df.drop(['Ticket'], axis=1, inplace=True)
if 'PassengerId' in df.columns: df.drop(['PassengerId'], axis=1, inplace=True)

# Fill missing values
if 'Age' in df.columns: df['Age'].fillna(df['Age'].median(), inplace=True)
if 'Embarked' in df.columns: df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)

# Encode categorical variables
if 'Sex' in df.columns: df['Sex'] = df['Sex'].map({'male': 0, 'female': 1})
if 'Embarked' in df.columns: df['Embarked'] = df['Embarked'].map({'C': 0, 'Q': 1, 'S': 2})

# Features and target
X = df.drop('Survived', axis=1)
y = df['Survived']

# Scale features
scaler = StandardScaler()
X = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

# 4. Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Define Models
models = {
    "Logistic Regression": LogisticRegression(),
    "Decision Tree": DecisionTreeClassifier(),
    "Random Forest": RandomForestClassifier(),
    "SVM": SVC(probability=True),
    "Gradient Boosting": GradientBoostingClassifier()
}

# 6. Train and Evaluate Models
def evaluate_models(models, X_train, X_test, y_train, y_test):
    results = []
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None

        results.append({
            "Model": name,
            "Accuracy": accuracy_score(y_test, y_pred),
            "Precision": precision_score(y_test, y_pred),
            "Recall": recall_score(y_test, y_pred),
            "F1 Score": f1_score(y_test, y_pred),
            "ROC AUC": roc_auc_score(y_test, y_prob) if y_prob is not None else None
        })
    return pd.DataFrame(results)

metrics_df = evaluate_models(models, X_train, X_test, y_train, y_test)
print(metrics_df)

# 7. Hyperparameter Tuning Example
# For simplicity, we'll do tuning on one model
param_grid_rf = {
    'n_estimators': [50, 100],
    'max_depth': [3, 5, None],
    'min_samples_split': [2, 5]
}
grid_rf = GridSearchCV(RandomForestClassifier(), param_grid_rf, cv=5, scoring='accuracy')
grid_rf.fit(X_train, y_train)
print("Best RF Params:", grid_rf.best_params_)

# 8. Visualization
sns.barplot(data=metrics_df.melt(id_vars='Model'), x='Model', y='value', hue='variable')
plt.title('Model Performance Comparison')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 9. Dashboard Concept (Supaboard)
"""
The model metrics can be pushed to a Supabase database.
Supaboard reads from this database to create visual comparison dashboards.
Each model's performance across different metrics will be visualized.
"""

# 10. Conclusion
"""
This notebook demonstrates how to compare different classification models using standard metrics and visualization. Hyper-parameter tuning can further enhance model performance and guide optimal selection.
"""

metrics_df.to_csv("/content/model_metrics.csv", index=False)

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load model performance metrics
st.title("Titanic ML Model Comparison Dashboard")

# File path
file_path = "/content/model_metrics.csv"

try:
    df = pd.read_csv(file_path)
    st.success("Metrics loaded successfully!")

    # Display data
    st.subheader("📋 Model Evaluation Metrics")
    st.dataframe(df)

    # Metric selector
    selected_metric = st.selectbox("📊 Select Metric to Compare", df.columns[1:])

    # Plot
    st.subheader(f"📈 Comparison of Models by {selected_metric}")
    fig, ax = plt.subplots()
    sns.barplot(data=df, x="Model", y=selected_metric, ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

except FileNotFoundError:
    st.error(f"Metrics file not found at {file_path}")

dashboard_code = """
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load model performance metrics
st.title("Titanic ML Model Comparison Dashboard")

# File path
file_path = "/content/model_metrics.csv"

try:
    df = pd.read_csv(file_path)
    st.success("Metrics loaded successfully!")

    # Display data
    st.subheader("📋 Model Evaluation Metrics")
    st.dataframe(df)

    # Metric selector
    selected_metric = st.selectbox("📊 Select Metric to Compare", df.columns[1:])

    # Plot
    st.subheader(f"📈 Comparison of Models by {selected_metric}")
    fig, ax = plt.subplots()
    sns.barplot(data=df, x="Model", y=selected_metric, ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

except FileNotFoundError:
    st.error(f"Metrics file not found at {file_path}")
"""

# Save the file
with open("dashboard.py", "w") as f:
    f.write(dashboard_code)

print("✅ dashboard.py created successfully.")

!streamlit run dashboard.py

