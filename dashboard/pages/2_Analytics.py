import streamlit as st, os, requests
from dotenv import load_dotenv

load_dotenv()
API_BASE = os.getenv('API_BASE','http://localhost:8000/api/v1')

st.set_page_config(page_title='Analytics', layout='wide')
st.title('📊 Analytics')

if not st.session_state.get('token'):
    st.error('Please login first')
    st.stop()

headers = {'Authorization': f"Bearer {st.session_state['token']}"}

tab1, tab2 = st.tabs(['Views', 'AI Query'])

with tab1:
    st.header('Predefined Analytics Views')
    view = st.selectbox('Choose view', ['top_selling_products','most_profitable_products','monthly_sales_summary'])
    
    if st.button('Load View'):
        with st.spinner('Loading view...'):
            resp = requests.get(f"{API_BASE}/analytics/views/{view}", headers=headers)
            if resp.status_code == 200:
                st.dataframe(resp.json(), use_container_width=True)
            else:
                st.error('Error loading view')

with tab2:
    st.header('Ask Analytics Questions via Speech or Text')
    st.write('Ask questions about your sales data using natural language. The AI will convert it to SQL and show results.')
    
    query_type = st.radio('Choose query method:', ['Speech', 'Text'], horizontal=True)
    
    if query_type == 'Speech':
        analytics_input = st.radio('Choose input method:', ['Record Question', 'Upload Audio File'], key='analytics_input')
        
        analytics_audio = None
        analytics_audio_name = None
        
        if analytics_input == 'Record Question':
            st.write('Click the button below to start recording your question')
            analytics_audio = st.audio_input('Record your analytics question', label_visibility='collapsed', key='analytics_record')
            if analytics_audio:
                analytics_audio_name = 'analytics_question.wav'
        else:
            audio_file2 = st.file_uploader('Upload analytics question (.wav/.mp3)', type=['wav','mp3'], key='analytics_upload')
            if audio_file2 is not None:
                analytics_audio = audio_file2.getvalue()
                analytics_audio_name = audio_file2.name
        
        if st.button('Ask via speech') and analytics_audio is not None:
            with st.spinner('Processing your question...'):
                resp = requests.post(f"{API_BASE}/analytics/speech", files={'audio': (analytics_audio_name, analytics_audio)})
                data = resp.json()
                if isinstance(data, list) and len(data) > 0:
                    st.dataframe(data, use_container_width=True)
                else:
                    st.write(data)
    else:
        text_query = st.text_area('Ask your analytics question:', placeholder='e.g., What are the top 5 selling products?')
        if st.button('Ask via text') and text_query:
            with st.spinner('Processing your question...'):
                resp = requests.post(f"{API_BASE}/analytics/text", data={'query': text_query})
                data = resp.json()
                if isinstance(data, list) and len(data) > 0:
                    st.dataframe(data, use_container_width=True)
                else:
                    st.write(data)
