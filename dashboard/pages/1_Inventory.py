import streamlit as st, os, requests
from dotenv import load_dotenv

load_dotenv()
API_BASE = os.getenv('API_BASE','http://localhost:8000/api/v1')

st.set_page_config(page_title='Inventory', layout='wide')
st.title('📦 Inventory Management')

if not st.session_state.get('token'):
    st.error('Please login first')
    st.stop()

headers = {'Authorization': f"Bearer {st.session_state['token']}"}

# Inventory section
st.header('Current Inventory')
resp = requests.get(f"{API_BASE}/inventory/", headers=headers)
if resp.status_code == 200:
    inventory_data = resp.json()
    if inventory_data:
        st.dataframe(inventory_data, use_container_width=True)
    else:
        st.info('No inventory items found')
else:
    st.error('Could not fetch inventory')

st.divider()

# Bill submission section
st.header('Add Bill by Voice')
st.write('Record or upload an audio file describing the bill details')

input_method = st.radio('Choose input method:', ['Record Voice', 'Upload Audio File'])

audio_data = None
audio_name = None

if input_method == 'Record Voice':
    st.write('Click the button below to start recording')
    audio_data = st.audio_input('Record your bill details', label_visibility='collapsed')
    if audio_data:
        audio_name = 'recorded_bill.wav'
else:
    audio_file = st.file_uploader('Upload bill audio (.wav/.mp3)', type=['wav','mp3'])
    if audio_file is not None:
        audio_data = audio_file.getvalue()
        audio_name = audio_file.name

if st.button('Submit Bill') and audio_data is not None:
    with st.spinner('Processing bill...'):
        resp = requests.post(f"{API_BASE}/bills/speech", 
                            files={'audio': (audio_name, audio_data)}, 
                            data={'user_id': st.session_state['user_id']}, 
                            headers=headers)
        if resp.status_code == 200:
            st.success('✅ Bill submitted successfully!')
            st.json(resp.json())
        else:
            st.error(f'Error: {resp.status_code}')
            st.write(resp.text)
