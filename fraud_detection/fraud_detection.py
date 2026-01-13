"""
Fraud Detection Application
---------------------------
This application uses a pre-trained Machine Learning model to predict whether a financial transaction 
is fraudulent or legitimate based on user inputs.

Designed for: Non-ML programmers to understand the flow of data from input to prediction.
"""

import streamlit as st  # Streamlit is a framework to build web apps for ML/Data Science with simple Python scripts.
import pandas as pd     # Pandas is used here to structure the user input into a table (DataFrame) that the model can understand.
import joblib           # Joblib is efficiently used to save and load Python objects, specifically our trained ML model.

# 1. LOAD THE TRAINED MODEL
# We load the 'fraud_detection_model.pkl' file which contains the "rules" the computer learned during training.
# This allows us to make predictions on new data without retraining.
model = joblib.load('fraud_detection_model.pkl')

st.title("Fraud Detection App")

st.markdown("""
This app detects fraudulent transactions using a machine learning model.
Input the transaction details below to see the result.
""")

st.divider()

# 2. COLLECT USER INPUTS
# We provide fields for the user to enter transaction details. These must match the features the model was trained on.

# 'selectbox' creates a dropdown menu. The model uses the transaction type as a key indicator.
transaction_type = st.selectbox("Transaction Type", ["PAYMENT", "TRANSFER", "CASH_OUT", "DEBIT"])

# 'number_input' fields for numerical values. 
# It is crucial to have the same data points (amount, balances) as used in the training phase.
amount = st.number_input("Transaction Amount", min_value=0.0, value=1000.0)

oldbalanceOrg = st.number_input("Old Balance of Origin Account", min_value=0.0, value=10000.0)
newbalanceOrig = st.number_input("New Balance of Origin Account", min_value=0.0, value=9000.0)

oldbalanceDest = st.number_input("Old Balance of Destination Account", min_value=0.0, value=0.0)
newbalanceDest = st.number_input("New Balance of Destination Account", min_value=0.0, value=0.0)

# 3. MAKE PREDICTION
if st.button("Predict Fraud"):
    # Create a DataFrame from the inputs. 
    # IMPORTANT: The column names and order must strictly match what the model expects.
    input_data = pd.DataFrame([{
        'type': transaction_type,
        'amount': amount,
        'oldbalanceOrg': oldbalanceOrg,
        'newbalanceOrig': newbalanceOrig,
        'oldbalanceDest': oldbalanceDest,
        'newbalanceDest': newbalanceDest
    }])

    # Use the model to predict. 
    # predict() returns an array (e.g., [1]), so we take the first item with [0].
    # 1 usually represents "Fraud", and 0 represents "Legitimate".
    prediction = model.predict(input_data)[0]

    st.subheader(f"Prediction Result: {int(prediction)}")

    # 4. DISPLAY RESULT
    # Interpret the numerical prediction for the user.
    if prediction == 1:
        st.error("The transaction is predicted to be FRAUDULENT.")
    else:
        st.success("The transaction is predicted to be LEGITIMATE.")