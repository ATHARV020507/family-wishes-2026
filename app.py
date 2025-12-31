import streamlit as st
import requests
import json

# --- CONFIGURATION ---
try:
    # Get the key and remove any accidental spaces
    api_key = st.secrets["GEMINI_API_KEY"].strip()
except:
    st.warning("⚠️ No API Key found in Secrets.")
    api_key = "PLACEHOLDER"

# --- PAGE SETUP ---
st.set_page_config(page_title="2026 Wish Granter", page_icon="🧞‍♂️", layout="centered")

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
    .big-font {
        font-size:20px !important;
        font-family: 'Comic Sans MS', 'Comic Sans', cursive;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("🧞‍♂️ The 2026 Genie")
st.markdown("**Welcome, Mishra Family!** ✨")
st.info("🔒 **Privacy Note:** Your wish is secret. Only YOU can see the Genie's reply on your screen.")

# --- INPUTS ---
name = st.text_input("What is your name?", placeholder="e.g., Chintu")
resolution = st.text_area("What is your Resolution for 2026?", placeholder="e.g., Stop eating so much Gulab Jamun and study harder.")

# --- THE MAGIC FUNCTION (DIRECT API CALL) ---
def get_gemini_response(name, resolution, key):
    # This URL forces the use of the 1.5 Flash model directly
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
    
    headers = {"Content-Type": "application/json"}
    
    prompt_text = (
        f"Imagine you are a hilarious, high-energy cartoon narrator. "
        f"The user {name} has this resolution: '{resolution}'. "
        f"1. Rate their resolution in a funny way. "
        f"2. Describe a funny cartoon scene of them in 2026. "
        f"3. End with a punchline. "
        f"Use emojis. Keep it under 150 words."
    )
    
    data = {
        "contents": [{
            "parts": [{"text": prompt_text}]
        }]
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        # If it fails, return the exact error from Google
        return f"Error: {response.status_code} - {response.text}"

# --- BUTTON ACTION ---
if st.button("Get My Cartoon Prediction! 🚀"):
    if not name or not resolution:
        st.error("The Genie needs a name and a wish to work his magic! 🧞‍♂️")
    else:
        with st.spinner("Drawing a cartoon of your future... 🎨"):
            try:
                # Call the direct function
                result = get_gemini_response(name, resolution, api_key)
                
                if "Error:" in result:
                    st.error("🚫 The Genie couldn't connect.")
                    st.code(result) # Show exact error code for debugging
                else:
                    st.balloons()
                    st.success("✨ The Genie has spoken! ✨")
                    with st.container():
                        st.markdown("### 🎬 Scene: 2026")
                        st.markdown(f"*{result}*")
                        
            except Exception as e:
                st.error(f"Something went wrong: {e}")

# --- FOOTER ---
st.markdown("---")
st.caption("✨ Made with AI for the Family New Year Party ✨")
