import streamlit as st
import pandas as pd
import joblib

model = joblib.load("model.pkl")
encoders = joblib.load("encoders.pkl")

st.title("Credit Card Fraud Detector")

amount_usd = st.number_input("Amount (USD)", value=100.0)
merchant_category = st.selectbox("Merchant Category", encoders["merchant_category"].classes_)
card_type = st.selectbox("Card Type", encoders["card_type"].classes_)
auth_method = st.selectbox("Auth Method", encoders["auth_method"].classes_)
channel = st.selectbox("Channel", encoders["channel"].classes_)
device_type = st.selectbox("Device Type", encoders["device_type"].classes_)
is_foreign_transaction = st.selectbox("Foreign Transaction?", [False, True])
hours_since_last_txn = st.number_input("Hours Since Last Transaction", value=5.0)
txn_count_last_24h = st.number_input("Txn Count Last 24h", value=1)
distance_from_home_km = st.number_input("Distance From Home (km)", value=10.0)
card_age_months = st.number_input("Card Age (months)", value=24)
customer_age = st.number_input("Customer Age", value=30)
account_balance_usd = st.number_input("Account Balance (USD)", value=5000.0)
is_new_merchant = st.selectbox("New Merchant?", [False, True])
used_vpn = st.selectbox("Used VPN?", [False, True])
ip_country_mismatch = st.selectbox("IP Country Mismatch?", [False, True])
billing_shipping_mismatch = st.selectbox("Billing/Shipping Mismatch?", [False, True])
cvv_retry_count = st.number_input("CVV Retry Count", value=0)
velocity_score = st.number_input("Velocity Score", value=10.0)
time_of_day_hour = st.number_input("Time of Day (hour)", value=14, min_value=0, max_value=23)
day_of_week = st.number_input("Day of Week (0-6)", value=3, min_value=0, max_value=6)
is_ai_generated_scam_attempt = st.selectbox("AI-Generated Scam Attempt?", [False, True])
merchant_risk_score = st.number_input("Merchant Risk Score", value=15.0)
prior_disputes = st.number_input("Prior Disputes", value=0)

if st.button("Check Transaction"):
    row = {
        "transaction_id": 0,
        "amount_usd": amount_usd,
        "merchant_category": encoders["merchant_category"].transform([merchant_category])[0],
        "card_type": encoders["card_type"].transform([card_type])[0],
        "auth_method": encoders["auth_method"].transform([auth_method])[0],
        "channel": encoders["channel"].transform([channel])[0],
        "device_type": encoders["device_type"].transform([device_type])[0],
        "is_foreign_transaction": int(is_foreign_transaction),
        "hours_since_last_txn": hours_since_last_txn,
        "txn_count_last_24h": txn_count_last_24h,
        "distance_from_home_km": distance_from_home_km,
        "card_age_months": card_age_months,
        "customer_age": customer_age,
        "account_balance_usd": account_balance_usd,
        "is_new_merchant": int(is_new_merchant),
        "used_vpn": int(used_vpn),
        "ip_country_mismatch": int(ip_country_mismatch),
        "billing_shipping_mismatch": int(billing_shipping_mismatch),
        "cvv_retry_count": cvv_retry_count,
        "velocity_score": velocity_score,
        "time_of_day_hour": time_of_day_hour,
        "day_of_week": day_of_week,
        "is_ai_generated_scam_attempt": int(is_ai_generated_scam_attempt),
        "merchant_risk_score": merchant_risk_score,
        "prior_disputes": prior_disputes,
    }

    X_new = pd.DataFrame([row])
    prediction = model.predict(X_new)[0]

    if prediction == 0:
        st.success("Transaction is NOT Fraud")
    else:
        st.error("Transaction is FRAUD")
