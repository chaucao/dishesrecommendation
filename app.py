import streamlit as st
from openai import OpenAI
import base64

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def encode_image_to_base64(image_file):
    return base64.b64encode(image_file.getvalue()).decode('utf-8')

def get_dish_recommendations(image_base64, additional_requirements):
    # Construct the prompt with additional requirements
    prompt = "Look at this image of ingredients and suggest 3 Vietnamese dishes I could make with them. Provide a brief description and basic instructions for each dish. Answer in Vietnamese."
    if additional_requirements:
        prompt += f"Please consider these additional requirements: {additional_requirements}. "
    prompt += "For each dish, provide a brief description and basic instructions."

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    }
                ]
            }
        ],
        max_tokens=1000
    )
    return response.choices[0].message.content

def main():
    st.title("🍳 Dish Recommendation App")
    st.write("Upload a photo of your ingredients, and I'll suggest dishes you can prepare!")

    # Text input for additional requirements
    additional_requirements = st.text_area(
        "Additional Requirements (Optional)",
        placeholder="E.g., vegetarian, low-carb, spicy, quick to prepare, etc.",
        help="Enter any dietary restrictions, preferences, or other requirements"
    )

    # File uploader
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display the uploaded image
        st.image(uploaded_file, caption="Uploaded Ingredients", use_container_width=True)
        
        # Add a button to trigger the analysis
        if st.button("Get Recommendations"):
            with st.spinner("Analyzing your ingredients..."):
                # Convert image to base64
                image_base64 = encode_image_to_base64(uploaded_file)
                
                try:
                    # Get recommendations with additional requirements
                    recommendations = get_dish_recommendations(image_base64, additional_requirements)
                    
                    # Display recommendations
                    st.subheader("📝 Recommended Dishes:")
                    st.write(recommendations)
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 