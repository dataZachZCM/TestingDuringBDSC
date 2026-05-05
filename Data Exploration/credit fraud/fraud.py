import pandas as pd 
import matplotlib as mlt
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import nbformat

all_df = pd.read_csv('credit fraud\\credit_fraud.csv')
all_df['age_numeric'] = pd.to_numeric(all_df['age'], errors='coerce')


bins = [0,2500, 5000, 7500, 10000, 15000]
labels = ['$0-2.5k', '$2.5-5k', '$5-7.5k', '$7.5-10k', '$10-15k']

age_bins = [17, 35, 60, 75]
age_labels = ['Young Adult', 'Middle Aged', 'Senior']

#BINNING DEBT BY FRAUD 
all_df["amount_bracket"] = pd.cut(all_df["transaction_amount"], bins=bins, labels=labels)
#DETRMINE THE PATTERNS
fraud_rate_map = all_df.groupby('amount_bracket', observed=True)['is_fraud'].mean().round(4)
all_df['amount_bracket_fraud_rate'] = all_df['amount_bracket'].map(fraud_rate_map)

#BINNING AGE BY FRAUD 
all_df["age_bracket"] = pd.cut(all_df['age_numeric'], bins= age_bins, labels=age_labels)
#Determine the patterns
fraud_age_map = all_df.groupby('age_bracket', observed=True )['is_fraud'].mean().round(4)
all_df['age_amount_bracket_fraud'] = all_df['age_bracket'].map(fraud_age_map)

#CONVERTING THE MESSY DATA INTO A NUMERIC VALUE
all_df['amount_bracket_fraud_rate'] = pd.to_numeric(all_df['amount_bracket_fraud_rate'], errors='coerce')
all_df['age_amount_bracket_fraud'] = pd.to_numeric(all_df['age_amount_bracket_fraud'], errors='coerce')

#COMBINING THE TWO BINS INTO A NEW COLUMN
all_df["Total_Risk_Score"] = (all_df['amount_bracket_fraud_rate'] * .70) + all_df['age_amount_bracket_fraud']

#USER INPUT 
user_age = int(input("Please enter your age: "))
user_balance = int(input("Please enter your account balance: "))

#COMPARING THE THE BINS CREATED EARLIER
u_amt_bracket = pd.cut([user_balance], bins=bins, labels=labels)[0]
u_age_bracket = pd.cut([user_age], bins=age_bins, labels=age_labels)[0]

#DETERMINING THE RISK PROFILE FOR THE USER
if pd.notna(u_amt_bracket) and pd.notna(u_age_bracket):
    risk_amt = fraud_rate_map[u_amt_bracket]
    risk_age = fraud_age_map[u_age_bracket]

    total_risk = (risk_amt  + risk_age).round(4)

    print(f"\n--- Risk Profile ---")
    print(f"Age Group: {u_age_bracket}")
    print(f"Balance Group: {u_amt_bracket}")
    print(f"Combined Risk Score: {total_risk:.2%}")
    fig = px.scatter_3d(
        all_df, 
        x='age_numeric', 
        y='transaction_amount', 
        z='Total_Risk_Score',
        color='Total_Risk_Score',
        title="Fraud Risk Landscape",
        labels={'age_numeric': 'Age', 'transaction_amount': 'Balance', 'Total_Risk_Score': 'Risk Score'},
        opacity=0.6)
    fig.show() 
else:
    print("\nError: Age or Balance falls outside of defined brackets.")
