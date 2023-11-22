import streamlit as st
import openai
from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv, set_key

st.set_page_config(page_title="You Sure About That?", page_icon="🤷")
st.image("ysat.png", width=400)

load_dotenv('.env')
openai.api_key = os.environ.get('OPENAI_API_KEY')

if not openai.api_key:
    openai.api_key = st.text_input("Enter OPENAI_API_KEY")
    set_key('.env', 'OPENAI_API_KEY', openai.api_key)
    os.environ['OPENAI_API_KEY'] = openai.api_key

# OpenAI API function
def call_openai_api(user_input):
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=user_input,
            max_tokens=1000  
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return str(e)

def call_google_api(user_input):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        search_url = f"https://www.google.com/search?q={user_input}"
        search_response = requests.get(search_url, headers=headers)
        search_soup = BeautifulSoup(search_response.text, 'html.parser')

        first_result = search_soup.find('div', class_='tF2Cxc')
        if first_result:
            page_url = first_result.find('a')['href']

            page_response = requests.get(page_url, headers=headers)
            page_soup = BeautifulSoup(page_response.text, 'html.parser')

            page_text = page_soup.get_text(separator=' ', strip=True)
            
            return f"URL: {page_url}\n\nContent:\n\n{page_text}"
        else:
            return "No results found"
    except Exception as e:
        return str(e)


    
with st.form("query_form"):
    user_input = st.text_input("Enter your query:")
    submitted = st.form_submit_button("Submit")

if submitted:
    openai_response = call_openai_api(user_input)
    google_response = call_google_api(user_input)

    col1, col2 = st.columns(2)

    with col1:
        st.image("openai_logo.png", width=50)  # Replace with path to OpenAI logo
        st.success(openai_response)

    with col2:
        st.image("google_logo.png", width=150)  # Replace with path to Google logo
        st.info(google_response)
