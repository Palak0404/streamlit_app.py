import streamlit as st
import google.generativeai as genai
import re

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
        outline_text = response.text

        st.markdown("### Generated Blog Outline")

        # Convert newlines and spaces for HTML rendering
        safe_outline = outline_text.replace("  ", "&nbsp;&nbsp;")
        safe_outline = safe_outline.replace("\n", "<br>")

        # Display formatted outline with forced styles
        st.markdown(
            f'''
            <div id="outline-text" style="
                font-family: monospace;
                font-size: 16px;
                color: black !important;
                background-color: #f8f8f8 !important;
                white-space: normal;
                line-height: 1.6;
                padding: 16px;
                border-radius: 8px;
                border: 1px solid #ddd;
                max-height: 400px;
                overflow-y: auto;
                margin-bottom: 20px;">
                {safe_outline}
            </div>
            ''',
            unsafe_allow_html=True
        )

        # Copy button with toast
        copy_html = f"""
            <script>
            function copyToClipboard() {{
                const text = document.getElementById('outline-text').innerText;
                navigator.clipboard.writeText(text).then(function() {{
                    var toast = document.getElementById("toast");
                    toast.className = "toast show";
                    setTimeout(function(){{ toast.className = toast.className.replace("show", ""); }}, 2000);
                }});
            }}
            </script>

            <style>
            .toast {{
                visibility: hidden;
                min-width: 120px;
                background-color: #4CAF50;
                color: white;
                text-align: center;
                border-radius: 8px;
                padding: 10px;
                position: fixed;
                z-index: 1;
                right: 30px;
                bottom: 30px;
                font-size: 16px;
            }}
            .toast.show {{
                visibility: visible;
                animation: fadein 0.5s, fadeout 0.5s 1.5s;
            }}
            @keyframes fadein {{
                from {{bottom: 0; opacity: 0;}} 
                to {{bottom: 30px; opacity: 1;}}
            }}
            @keyframes fadeout {{
                from {{bottom: 30px; opacity: 1;}} 
                to {{bottom: 0; opacity: 0;}}
            }}
            </style>

            <button onclick="copyToClipboard()" style="
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                font-size: 16px;
                border: none;
                border-radius: 8px;
                cursor: pointer;">
                Copy to Clipboard
            </button>

            <div id="toast" class="toast">Copied!</div>
        """
        st.markdown(copy_html, unsafe_allow_html=True)
