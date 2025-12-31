import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ---
# REMEMBER: Add your API key in Streamlit Secrets on the web dashboard
# Secrets format: GEMINI_API_KEY = "your_key"
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    # Fallback for local testing if you haven't set secrets yet
    # Remove this line before deploying if you want to be extra safe
    st.warning("⚠️ No API Key found in Secrets. Using placeholder (App won't generate).")
    api_key = "PLACEHOLDER"

genai.configure(api_key=api_key)

# --- PAGE SETUP ---
st.set_page_config(page_title="2026 Wish Granter", page_icon="🧞‍♂️", layout="centered")

# Custom CSS to make it look friendly and cartoony
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

# --- THE MAGIC ---
if st.button("Get My Cartoon Prediction! 🚀"):
    if not name or not resolution:
        st.error("The Genie needs a name and a wish to work his magic! 🧞‍♂️")
    else:
        with st.spinner("Drawing a cartoon of your future... 🎨"):
            try:
                # --- THE PROMPT RE-ENGINEERED FOR CARTOONS ---
                model = genai.GenerativeModel('gemini-pro')
                
                cartoon_prompt = (
                    f"Imagine you are a hilarious, high-energy cartoon narrator (like a mix of a Disney sidekick and an Anime hero). "
                    f"The user {name} has this resolution: '{resolution}'. "
                    f"1. Rate their resolution in a funny way (e.g., 'Ambitious Level: Over 9000!'). "
                    f"2. Give them a 'Future Prediction' describing a funny cartoon scene of them succeeding (or struggling hilariously) in 2026. "
                    f"3. End with a motivating, warm punchline. "
                    f"Use lots of emojis. Keep it under 150 words. Make it feel like a happy comic book script."
                )
                
                response = model.generate_content(cartoon_prompt)
                
                # --- DISPLAY ---
                st.balloons()
                st.success("✨ Your 2026 Cartoon Forecast is Ready! ✨")
                
                # Using a container for a nice card effect
                with st.container():
                    st.markdown("### 🎬 Scene: 2026")
                    st.markdown(f"*{response.text}*")
                    
            except Exception as e:
                st.error(f"Oops! The Genie is on a chai break. (Error: {e})")

# --- FOOTER ---
st.markdown("---")
st.caption("✨ Made with AI for the Family New Year Party ✨")