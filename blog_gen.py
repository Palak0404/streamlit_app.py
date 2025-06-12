import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets["gcp"]["gemini_api_key"])
st.set_page_config(page_title="Blog Outline Generator", layout="centered")

st.title("Blog Outline Generator")

topic = st.text_input("Enter your blog topic:")

if st.button("Generate Outline"):
    if topic.strip():
        prompt = f"""
**Role:**  
You are an expert SEO professional blog writer with deep knowledge of content structure, and user intent.

**Task:**  
Your task is to generate a detailed, SEO blog outline for the topic: **{topic}** by analyzing the top 10 Google search results.

**Instructions:**  
1. Read the topic carefully.  
2. Assume you have reviewed and extracted key points from the top 10 Google search results related to the topic.  
3. Begin with a short summary paragraph (2-3 sentences) introducing the blog and explaining why it's important.  
4. Create a clear, keyword-rich, **main title** (H1) for the blog post.  
5. Generate a well-structured **Table of Contents (TOC)** formatted with numbered H2 sections and relevant H3 subsections that cover the topic.  
6. Include detailed subsections that give important aspects, benefits, or examples.  
7. Add a **Frequently Asked Questions (FAQs)** section with at least 10 friendly questions.  
8. Conclude the outline with a **Conclusion** section summarizing the key takeaways or recommendations.  
9. When needed, include emojis to highlight.  
10. Format the entire output in clean markdown:
   - # for the blog title  
   - ## for numbered H2 sections (12 minimum)  
   - ### for H3-level breakdowns  
   - Bullet points for FAQs  
11. Do not add any additional information or commentary.
"""
      

        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
        response = model.generate_content(prompt)

        # Show the actual blog outline
        st.markdown("Generated Blog Outline")
        st.markdown(response.text)
    else:
        st.warning("Please enter a topic to generate the outline.")
