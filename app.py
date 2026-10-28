import streamlit as st
import pandas as pd
import plotly.express as px
from database import connect_db

st.set_page_config(page_title="Expense Tracker", layout="wide")

st.title("💰 Expense Tracker Pro")

menu = st.sidebar.selectbox(
    "Select Option",
    [
        "Add Expense",
        "View Expenses",
        "Update Expense",
        "Delete Expense",
        "Dashboard"
    ]
)

# ADD EXPENSE

if menu == "Add Expense":

    st.subheader("➕ Add Expense")

    expense_date = st.date_input("Date")

    category = st.selectbox(
        "Category",
        ["Food", "Travel", "Shopping", "Bills", "Other"]
    )

    amount = st.number_input(
        "Amount",
        min_value=0.0
    )

    description = st.text_input(
        "Description"
    )

    if st.button("Save Expense"):

        conn = connect_db()
        cursor = conn.cursor()

        query = """
        INSERT INTO expenses
        (expense_date, category, amount, description)
        VALUES (%s,%s,%s,%s)
        """

        cursor.execute(
            query,
            (
                expense_date,
                category,
                amount,
                description
            )
        )

        conn.commit()
        conn.close()

        st.success("Expense Added Successfully ✅")

# VIEW EXPENSES

elif menu == "View Expenses":

    st.subheader("📋 All Expenses")

    conn = connect_db()

    query = "SELECT * FROM expenses"

    df = pd.read_sql(query, conn)

    st.dataframe(df)

    conn.close()

# UPDATE EXPENSE

elif menu == "Update Expense":

    st.subheader("✏️ Update Expense")

    expense_id = st.number_input(
        "Expense ID",
        min_value=1
    )

    new_amount = st.number_input(
        "New Amount",
        min_value=0.0
    )

    if st.button("Update"):

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE expenses SET amount=%s WHERE id=%s",
            (
                new_amount,
                expense_id
            )
        )

        conn.commit()
        conn.close()

        st.success("Expense Updated ✅")

# DELETE EXPENSE

elif menu == "Delete Expense":

    st.subheader("🗑 Delete Expense")

    expense_id = st.number_input(
        "Expense ID",
        min_value=1
    )

    if st.button("Delete Expense"):

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM expenses WHERE id=%s",
            (expense_id,)
        )

        conn.commit()
        conn.close()

        st.success("Expense Deleted ✅")

# DASHBOARD

elif menu == "Dashboard":

    st.subheader("📊 Dashboard")

    conn = connect_db()

    df = pd.read_sql(
        "SELECT * FROM expenses",
        conn
    )

    conn.close()

    if not df.empty:

        total_expense = df["amount"].sum()

        st.metric(
            "Total Expense",
            f"₹ {total_expense:.2f}"
        )

        fig = px.pie(
            df,
            names="category",
            values="amount",
            title="Category Wise Expenses"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.warning("No Expense Data Available")