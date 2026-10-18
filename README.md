# Customer Churn Prediction Using Snowflake

## About the Project

This project predicts customer churn using machine learning and Snowflake. It helps identify customers who may leave a service.

## Dataset

The project uses the Telco Customer Churn dataset, which contains customer information, service details, contract types, payment methods, and churn status.

- Total Records: 7,043 customers
- Target Column: `CHURN`
- Target Values:
  - `0` – Customer stayed
  - `1` – Customer churned

## Features Used

- Customer demographics
- Customer tenure
- Contract type
- Payment method
- Internet and phone services
- Monthly charges
- Total charges

## Technologies Used

- Snowflake
- Snowflake SQL
- Pandas
- Scikit-learn
- Logistic Regression
- Streamlit

## Project Steps

1. Load customer data into Snowflake.
2. Clean and preprocess the data.
3. Train a machine learning model.
4. Predict customer churn.
5. Identify high-risk customers.
6. Analyze churn by contract type and payment method.

## Results

- Total customers: 7,043
- Model accuracy: 73.81%
- Predicted churn customers: 2,887
- High-risk customers: 1,783

## Conclusion

This project uses machine learning to predict customer churn and helps businesses identify customers who may need extra attention.
