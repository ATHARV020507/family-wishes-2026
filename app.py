import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ---
try:
    # .strip() removes accidental spaces from your key!
    api_key = st.secrets["GEMINI_API_KEY"].strip()
except:
    st.warning("⚠️ No API Key found in Secrets.")
    api_key = "PLACEHOLDER"

genai.configure(api_key=api_key)

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

# --- THE MAGIC ---
if st.button("Get My Cartoon Prediction! 🚀"):
    if not name or not resolution:
        st.error("The Genie needs a name and a wish to work his magic! 🧞‍♂️")
    else:
        with st.spinner("Drawing a cartoon of your future... 🎨"):
            # List of models to try
            model_options = [
                "gemini-1.5-flash", 
                "gemini-1.5-flash-latest", 
                "gemini-1.5-pro", 
                "gemini-pro"
            ]
            
            response_text = None
            used_model = None
            last_error = "No attempts made."

            cartoon_prompt = (
                f"Imagine you are a hilarious, high-energy cartoon narrator. "
                f"The user {name} has this resolution: '{resolution}'. "
                f"1. Rate their resolution in a funny way. "
                f"2. Describe a funny cartoon scene of them in 2026. "
                f"3. End with a punchline. "
                f"Use emojis. Keep it under 150 words."
            )

            # Loop through models
            for model_name in model_options:
                try:
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(cartoon_prompt)
                    response_text = response.text
                    used_model = model_name
                    break # Success!
                except Exception as e:
                    last_error = e
                    continue # Try next model
            
            # --- DISPLAY RESULT ---
            if response_text:
                st.balloons()
                st.success(f"✨ The Genie has spoken! ✨")
                with st.container():
                    st.markdown("### 🎬 Scene: 2026")
                    st.markdown(f"*{response_text}*")
            else:
                # SHOW THE REAL ERROR SO WE CAN FIX IT
                st.error("🚫 Connection Failed.")
                st.warning(f"Debug Error Info: {last_error}")
                st.info("Check your API Key in Settings -> Secrets. It should look like: GEMINI_API_KEY = \"AIza...\"")

# --- FOOTER ---
st.markdown("---")
st.caption("✨ Made with AI for the Family New Year Party ✨")
