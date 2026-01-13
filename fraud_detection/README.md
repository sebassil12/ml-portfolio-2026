# Fraud Detection System

## Project Overview
This project demonstrates a **Machine Learning (ML)** application designed to detect fraudulent financial transactions. It consists of two main parts:
1.  **Analysis & Training (`analysis_model.ipynb`)**: A notebook that explores historical data, finds patterns, and trains a mathematical model to recognize fraud.
2.  **Deployment App (`fraud_detection.py`)**: A user-friendly web application (using Streamlit) that allows users to input transaction details and get a prediction (Legitimate or Fraudulent) from the trained model.

## 🚀 Quick Start

### Prerequisites
Ensure you have Python installed along with the following libraries:
- `pandas` (for data handling)
- `scikit-learn` (for machine learning)
- `streamlit` (for the web app)
- `joblib` (for saving/loading the model)
- `seaborn` / `matplotlib` (for visualizations)

### Running the Application
To launch the interactive fraud detection dashboard, run this command in your terminal:
```bash
streamlit run fraud_detection.py
```
This will open a web browser tab where you can test the model.

---

## 🧠 Understanding the Machine Learning Workflow
*For Programmers new to Machine Learning*

The file `analysis_model.ipynb` contains the logic for creating the "brain" of this application. Since we cannot modify the notebook directly, here is a step-by-step guide to what is happening inside it and **why**.

### 1. Data Investigation (Exploratory Data Analysis)
Before writing algorithms, we must understand our data.
- **`df.head()` & `df.info()`**: These commands validate that the CSV loaded correctly and help us check data types. We look for "null" occurrences because ML models cannot handle missing data (it causes errors).
- **Correlation Matrix**: We perform correlation checks (the heatmaps) to see if variables like `amount` or `balance` move in sync with our `isFraud` label. High correlation suggests a strong predictor.

### 2. The Challenge: Class Imbalance
One of the most critical steps is checking `df["isFraud"].value_counts()`.
- **Observation**: You will see that ~99.9% of transactions are legitimate and only ~0.1% are fraud.
- **Why it matters**: If we just guessed "Legitimate" every time, we would be 99.9% accurate! But we would miss **every single fraud**. This is the "Accuracy Paradox." We solve this later using **Class Weights**.

### 3. Feature Engineering (Preprocessing)
Raw data often isn't ready for math.
- **One-Hot Encoding**: The `type` column contains text like "PAYMENT" or "TRANSFER". Computers need numbers. We convert these into binary columns (e.g., `type_PAYMENT`: 1 if yes, 0 if no).
- **Dropping Columns**: We remove `nameOrig` (Sender Name) and `nameDest` (Receiver Name).
    - *Why?* A specific user name (e.g., "User123") is unique and won't appear in future data. Including it would cause the model to memorize specific users rather than learning **general patterns** of fraud.

### 4. Model Training (`LogisticRegression`)
We use a **Pipeline** that combines preprocessing and the model into one object.
- **Scaling**: We use `StandardScaler` to normalize numerical values (like `amount`). This ensures a large transaction ($1,000,000) doesn't mathematically "drown out" a small but important feature.
- **The Model**: We use **Logistic Regression**. Think of it as finding a line that best separates "Fraud" points from "Legit" points in a multi-dimensional graph.
- **`class_weight='balanced'`**: This is our fix for the Class Imbalance (Step 2). It tells the model: *"Pay 100x more attention to a Fraud mistake than a Legitimate mistake."* This forces the model to learn the minority class.

### 5. Evaluation
We don't just look at Accuracy. We look at:
- **Precision**: When the model flags a transaction, how often is it actually fraud? (Low precision = False Alarms).
- **Recall**: Out of all actual frauds, how many did we catch? (Low recall = Missed Fraud).
- **F1-Score**: A balance of the two.

---

## 📂 File Structure
- `fraud_detection.py`: The user interface code. Read this to understand how we take user input and feed it to the model.
- `analysis_model.ipynb`: The training laboratory. Read this to see the raw data analysis and model creation steps described above.
- `fraud_detection_model.pkl`: The saved "brain" (model). This is created by the notebook and read by the python script.
- `data/`: Folder containing the dataset `AIML Dataset.csv`.

## Dataset
The dataset represents financial transactions.
Source: [Kaggle Fraud Detection Dataset](https://www.kaggle.com/datasets/amanalisiddiqui/fraud-detection-dataset?resource=download)
*Note: Dataset is not included in the repo due to size.*
