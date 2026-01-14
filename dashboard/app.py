import streamlit as st, os, requests
from dotenv import load_dotenv
load_dotenv()
API_BASE = os.getenv('API_BASE','http://localhost:8000/api/v1')

# init session state
if 'token' not in st.session_state:
    st.session_state['token'] = None
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None

st.set_page_config(page_title='Smart Vendor Dashboard', layout='wide')
st.title('Smart Vendor Dashboard')

# login
if not st.session_state['token']:
    st.sidebar.title('Login / Register')
    email = st.sidebar.text_input('Email')
    pwd = st.sidebar.text_input('Password', type='password')
    if st.sidebar.button('Login'):
        resp = requests.post(f"{API_BASE}/auth/token", data={'username': email, 'password': pwd})
        if resp.status_code==200:
            st.session_state['token'] = resp.json().get('access_token')
            # set user_id to 1 for testing; in production decode token to get user_id
            st.session_state['user_id'] = 1
            st.rerun()
        else:
            st.sidebar.error('Login failed')
    if st.sidebar.button('Register'):
        resp = requests.post(f"{API_BASE}/auth/register", json={'name':'Vendor','email':email,'password':pwd})
        if resp.status_code==200 or resp.status_code==201:
            st.sidebar.success('Registered - please login')
        else:
            st.sidebar.error('Registration failed')
    st.info('👈 Please login or register to continue')
else:
    st.sidebar.success(f'✅ Logged in')
    if st.sidebar.button('Logout'):
        st.session_state['token'] = None
        st.session_state['user_id'] = None
        st.rerun()
    
    st.write('Welcome to Smart Vendor Dashboard!')
    st.write('Use the sidebar to navigate to different sections.')
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info('📦 **Inventory**\nView and manage your product inventory')
    with col2:
        st.info('💰 **Add Bill**\nRecord bills using voice or upload audio files')
    with col3:
        st.info('📊 **Analytics**\nAnalyze sales data with AI-powered queries')

