import streamlit as st
import requests, os
from dotenv import load_dotenv
load_dotenv()
API_BASE = os.getenv('API_BASE','http://localhost:8000/api/v1')

st.set_page_config(page_title='Smart Vendor Dashboard', layout='wide')

st.sidebar.title("Vendor Login")
if 'token' not in st.session_state:
    email = st.sidebar.text_input("Email")
    pwd = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        resp = requests.post(f"{API_BASE}/auth/token", data={'username':email,'password':pwd})
        if resp.status_code==200:
            st.session_state['token'] = resp.json()['access_token']
        else:
            st.sidebar.error("Login failed")
else:
    st.sidebar.success("Logged in")

if 'token' in st.session_state:
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    st.title("Inventory")
    resp = requests.get(f"{API_BASE}/inventory/", headers=headers)
    if resp.status_code==200:
        items = resp.json()
        st.dataframe(items)
    else:
        st.write("Error fetching inventory")

    st.header('Analytics Views')
    if st.button('Top Selling Products'):
        resp = requests.post(f'{API_BASE}/analytics/text', json={'query':'show top selling products'}, headers=headers)
        st.write(resp.json())
    if st.button('Most Profitable Products'):
        resp = requests.post(f'{API_BASE}/analytics/text', json={'query':'show most profitable products'}, headers=headers)
        st.write(resp.json())
