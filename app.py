import streamlit as st
import requests
import json

# --- CONFIGURATION ---
try:
    api_key = st.secrets["GEMINI_API_KEY"].strip()
except:
    st.warning("⚠️ No API Key found in Secrets.")
    api_key = "PLACEHOLDER"

# --- PAGE SETUP ---
st.set_page_config(page_title="2026 Wish Granter", page_icon="🧞‍♂️", layout="centered")

# Custom CSS for the cartoon look
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        font-size: 20px;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("🧞‍♂️ The 2026 Genie")
st.markdown("**Welcome, Mishra Family!** ✨")
st.info("🔒 **Privacy Note:** Your wish is secret. Only YOU see the result.")

# --- INPUTS ---
name = st.text_input("Name:", placeholder="e.g., Chintu")
resolution = st.text_area("Resolution:", placeholder="e.g., Study harder")

# --- AUTO-DISCOVERY FUNCTION ---
def find_working_model(key):
    # Ask Google which models are available for this key
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # Look for a model that supports generating content
            for model in data.get('models', []):
                if 'generateContent' in model.get('supportedGenerationMethods', []):
                    return model['name'] # Returns something like 'models/gemini-pro'
    except:
        pass
    return "models/gemini-1.5-flash" # Fallback if discovery fails

# --- MAIN GENERATION FUNCTION ---
def get_prediction(name, resolution, key):
    # Step 1: Find a valid model name
    model_name = find_working_model(key)
    
    # Step 2: Build the URL dynamically
    url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent?key={key}"
    
    headers = {"Content-Type": "application/json"}
    prompt = f"Act as a funny cartoon narrator. User {name} wants to '{resolution}'. Predict their 2026 in a funny, encouraging way. Use emojis. Max 100 words."
    
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text'], model_name
    else:
        return f"Error: {response.status_code} - {response.text}", model_name

# --- BUTTON ---
if st.button("Reveal My Destiny! 🚀"):
    if not name or not resolution:
        st.error("Please enter a name and wish.")
    else:
        with st.spinner("Consulting the stars..."):
            result, used_model = get_prediction(name, resolution, api_key)
            
            if "Error" in result:
                st.error("The Genie is stuck.")
                st.code(result) # Shows the exact technical error
                st.caption(f"Tried using model: {used_model}")
            else:
                st.balloons()
                st.success(f"✨ Prediction for {name} ✨")
                st.write(result)
