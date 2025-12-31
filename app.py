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
    .strength-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #262730;
        border: 2px solid #FF4B4B;
        text-align: center;
        margin-bottom: 20px;
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
            for model in data.get('models', []):
                if 'generateContent' in model.get('supportedGenerationMethods', []):
                    return model['name'] 
    except:
        pass
    return "models/gemini-1.5-flash" 

# --- MAIN GENERATION FUNCTION ---
def get_prediction(name, resolution, key):
    model_name = find_working_model(key)
    url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent?key={key}"
    
    headers = {"Content-Type": "application/json"}
    
    # UPDATED PROMPT: Ask for Strength Rating
    prompt = (
        f"Act as a funny cartoon narrator. User {name} wants to '{resolution}'. "
        f"1. First, classify this resolution as exactly one of these three: '🔥 SUPER STRONG', '✨ SOLID & BALANCED', or '🐣 GENTLE / WEAK'. "
        f"2. Then, give a funny 'Future Prediction' scene for 2026. "
        f"3. End with a punchline. "
        f"Format the output clearly. Use emojis. Keep it under 150 words."
    )
    
    data = { "contents": [{ "parts": [{"text": prompt}] }] }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"Error: {response.status_code} - {response.text}"

# --- BUTTON ---
if st.button("Judge My Resolution! 🚀"):
    if not name or not resolution:
        st.error("Please enter a name and wish.")
    else:
        with st.spinner("The Genie is judging you... 🧐"):
            result = get_prediction(name, resolution, api_key)
            
            if "Error" in result:
                st.error("Connection failed.")
                st.code(result)
            else:
                st.balloons()
                st.success(f"✨ Judgment Day for {name}! ✨")
                
                # We display the whole result in a nice box
                st.markdown("### 🔮 The Genie Says:")
                st.markdown(f"{result}")
                
# --- FOOTER ---
st.markdown("---")
st.caption("✨ Made with AI for the Family New Year Party ✨")
