import streamlit as st
import sqlite3
import time
import pandas as pd

con=sqlite3.connect("ledger.db")
cur=con.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS ledger_table (
        id INTEGER PRIMARY KEY,
        booking_date TEXT,
        pnr TEXT,
        service_charge REAL,
        ticket_type TEXT,
        travel_date TEXT,
        guest_name TEXT,
        trainflight_number TEXT,
        phone_number INTEGER,
        amount REAL,
        total REAL,
        payment_status
    )
''')
con.commit()

st.set_page_config(
    page_title=None,
    page_icon=None,
    layout="wide",
    )

st.title("Ledger DB")
st.subheader("Add Entry")
with st.form("ledger_form"):
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        booking_date = st.date_input("Date", format="DD/MM/YYYY")
        pnr = st.text_input("PNR")
        service_charge = st.number_input("Service Charge")
    with col2:
        ticket_type = st.selectbox("Ticket Type", options=['Rail', 'Domestic Air', 'International Air'])
        travel_date = st.date_input("Date of Travel", format="DD/MM/YYYY")
        payment_status = st.selectbox("Payment Status", options=['Paid', 'Unpaid'])
    with col3:
        guest_name = st.text_input("Name of Guest")
        trainflight_number = st.text_input("Train/Flight Number")
    with col4:
        phone_number = st.number_input("Phone number", step=1, min_value=1000000000, max_value=9999999999)
        amount = st.number_input("Amount")
    
    val_press = st.form_submit_button("Submit")
    if val_press:
        cur.execute(
            """
            INSERT INTO ledger_table (booking_date, pnr, service_charge, ticket_type, travel_date, guest_name, trainflight_number, phone_number, amount, total, payment_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (booking_date, pnr, service_charge, ticket_type, travel_date, guest_name, trainflight_number, phone_number, amount, amount+service_charge, payment_status)
        )
        con.commit()
        message = st.empty()
        message.text("Entry added")
        time.sleep(1.5)
        message.empty()
        
st.subheader("View All Entries")
df = pd.read_sql_query("SELECT * FROM ledger_table", con)
st.table(df)


st.subheader('Fetch Entry')
search = st.text_input('Enter Guest Name')
if search:
    cur.execute('SELECT * FROM ledger_table WHERE guest_name=?', (search,))
    results = cur.fetchall()
    
    if results:
        df_search = pd.DataFrame(results, columns=[col[0] for col in cur.description])
        st.write(df_search)
    else:
        st.write("No results found.")


st.subheader('Dowaload ledger as CSV')
@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf-8')

csv = convert_df(df)

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='ledger.csv',
    mime='text/csv',
)

con.close()