import streamlit as st
import anthropic
import os

api_key = os.getenv("CLAUDE_API_KEY") # Retrieve API key from Hugging Face secrets


# Function to interact with Claude AI via the Anthropic API
def get_claude_response(prompt, api_key):
    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        temperature=0,
        system="You are a world-class nutritionist, offer expert advice on managing diabetes through a specialized meal planner. The planner should include balanced meal options designed to maintain stable blood sugar levels, support overall health, and cater to individual dietary needs. Provide detailed meal suggestions, including breakfast, lunch, dinner, and snacks, with a focus on low glycemic index foods, portion control, and nutritional balance.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )
    return message.content[0].text

# Title of the app
st.title("NutriBalance")

# Description
st.write("""
### Welcome to NutriBalance
NutriBalance is your personalized diabetes management tool. As an expert nutritionist, I help you balance your diet 
and manage your blood sugar levels. By inputting your age, weight, blood sugar levels 
(fasting, pre-meal, and post-meal), and dietary nutrition, NutriBalance provides tailored advice to support your health journey.
""")

# Sidebar input form
st.sidebar.header("Enter Your Details")

with st.sidebar.form("nutri_balance_form"):
    age = st.number_input("Age", min_value=0, step=1)
    weight = st.number_input("Weight (kg)", min_value=0.0, step=0.1)
    fasting_sugar = st.number_input("Fasting Sugar Level (mg/dL)", min_value=0, step=1)
    pre_meal_sugar = st.number_input("Pre-Meal Sugar Level (mg/dL)", min_value=0, step=1)
    post_meal_sugar = st.number_input("Post-Meal Sugar Level (mg/dL)", min_value=0, step=1)
    dietary_nutrition = st.text_area("Dietary Nutrition Details (e.g., meals, calories, etc.)")
    
    # Submit button
    submitted = st.form_submit_button("Generate Meal Plan")
if submitted:

    if api_key:
        # Prepare prompt
        prompt = f"Age: {age}, Weight: {weight} kg, Fasting Sugar Level: {fasting_sugar} mg/dL, Pre-Meal Sugar Level: {pre_meal_sugar} mg/dL, Post-Meal Sugar Level: {post_meal_sugar} mg/dL, Dietary Nutrition: {dietary_nutrition}. Provide expert nutritional advice."
        claude_response = get_claude_response(prompt, api_key)
        
        # Display Claude's response
        st.markdown("### Expert Nutritionist's Advice:")
        st.markdown(f"**{claude_response}**")
    else:
        st.error("API key is missing. Please add your Claude API Key to Hugging Face secrets.")
