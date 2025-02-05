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
    st.title("🍳 Gợi ý món ăn")
    st.write("Chụp hình nguyên liệu bạn có trong tủ lạnh và chúng tôi sẽ gợi ý 3 món ăn Việt Nam bạn có thể làm với chúng.")

    # Text input for additional requirements
    additional_requirements = st.text_area(
        "Yêu cầu thêm",
        placeholder="ví dụ: ăn chay, low-carb, ăn cay, món bắc, món nam, nhanh chóng",
        help="Nhập thêm yêu cầu bổ sung cho món ăn (ví dụ: ăn chay, low-carb, ăn cay, món bắc, món nam, nhanh chóng, etc.)"
    )

    # File uploader
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display the uploaded image
        st.image(uploaded_file, caption="Uploaded Ingredients", use_container_width=True)
        
        # Add a button to trigger the analysis
        if st.button("Gợi ý cho tôi"):
            with st.spinner("Đang phân tích hình ảnh của bạn..."):
                # Convert image to base64
                image_base64 = encode_image_to_base64(uploaded_file)
                
                try:
                    # Get recommendations with additional requirements
                    recommendations = get_dish_recommendations(image_base64, additional_requirements)
                    
                    # Display recommendations
                    st.subheader("📝 Món ăn được gợi ý:")
                    st.write(recommendations)
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 