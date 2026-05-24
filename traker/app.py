import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
from database import (create_tables, add_transaction, 
                      get_all_transactions, get_total_by_type,
                      get_spending_by_category)

# Setup
create_tables()
st.title("💰 Personal Finance Tracker")

# --- ADD TRANSACTION SECTION ---
st.header("Add New Transaction")

col1, col2 = st.columns(2)

with col1:
    trans_date = st.date_input("Date", value=date.today())
    description = st.text_input("Description", placeholder="e.g. Grocery shopping")
    amount = st.number_input("Amount (MDL)", min_value=0.0, step=0.5)

with col2:
    trans_type = st.selectbox("Type", ["Expense", "Income"])
    category = st.selectbox("Category", [
        "Food", "Transport", "Education", 
        "Entertainment", "Health", "Salary", "Other"
    ])

if st.button("Add Transaction"):
    if description and amount > 0:
        add_transaction(str(trans_date), description, 
                       amount, trans_type, category)
        st.success("Transaction added!")
    else:
        st.error("Please fill in all fields.")

# --- SUMMARY SECTION ---
st.header("📊 Summary")

col3, col4, col5 = st.columns(3)

total_income = get_total_by_type("Income")
total_expense = get_total_by_type("Expense")
balance = total_income - total_expense

with col3:
    st.metric("Total Income", f"{total_income:.2f} MDL")
with col4:
    st.metric("Total Expenses", f"{total_expense:.2f} MDL")
with col5:
    st.metric("Balance", f"{balance:.2f} MDL")

# --- CHART SECTION ---
st.header("📈 Spending by Category")

category_data = get_spending_by_category()

if category_data:
    categories = [row[0] for row in category_data]
    amounts = [row[1] for row in category_data]
    
    fig, ax = plt.subplots()
    ax.pie(amounts, labels=categories, autopct='%1.1f%%')
    ax.set_title("Where your money goes")
    st.pyplot(fig)
else:
    st.info("No expense data yet.")

# --- TRANSACTIONS TABLE ---
st.header("📋 All Transactions")

rows = get_all_transactions()

if rows:
    df = pd.DataFrame(rows, columns=[
        "ID", "Date", "Description", "Amount", "Type", "Category"
    ])
    st.dataframe(df, use_container_width=True)
else:
    st.info("No transactions yet. Add your first one above!")