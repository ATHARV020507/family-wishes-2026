import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
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
            # --- THE ROBUST FIX: Try multiple models until one works ---
            model_options = [
                "gemini-1.5-flash", 
                "gemini-1.5-flash-latest", 
                "gemini-1.5-pro", 
                "gemini-pro"
            ]
            
            response_text = None
            used_model = None

            cartoon_prompt = (
                f"Imagine you are a hilarious, high-energy cartoon narrator (like a mix of a Disney sidekick and an Anime hero). "
                f"The user {name} has this resolution: '{resolution}'. "
                f"1. Rate their resolution in a funny way (e.g., 'Ambitious Level: Over 9000!'). "
                f"2. Give them a 'Future Prediction' describing a funny cartoon scene of them succeeding (or struggling hilariously) in 2026. "
                f"3. End with a motivating, warm punchline. "
                f"Use lots of emojis. Keep it under 150 words. Make it feel like a happy comic book script."
            )

            # Loop through models to find one that works
            for model_name in model_options:
                try:
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(cartoon_prompt)
                    response_text = response.text
                    used_model = model_name
                    break # It worked! Stop the loop.
                except Exception:
                    continue # Try the next model
            
            # --- DISPLAY RESULT ---
            if response_text:
                st.balloons()
                st.success(f"✨ The Genie has spoken! (Using magic: {used_model}) ✨")
                with st.container():
                    st.markdown("### 🎬 Scene: 2026")
                    st.markdown(f"*{response_text}*")
            else:
                st.error("🚫 The Genie is having connection issues with Google. Please check your API Key in secrets!")

# --- FOOTER ---
st.markdown("---")
st.caption("✨ Made with AI for the Family New Year Party ✨")
