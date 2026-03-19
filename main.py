import streamlit as st
from few_shot import FewShotPost
from post_generator import generate_post


def main():
    st.title("LinkedIn Post Generator")
    col1, col2, col3 = st.columns(3)
    fs = FewShotPost()
    with col1:
        selected_tag = st.selectbox("Title", options = fs.get_tags())
    with col2:
        selected_length = st.selectbox("Length", options = fs.get_lengths())
    with col3:
        selected_language = st.selectbox("Language", options = fs.get_languages())
    if st.button("Generate Post"):
        post = generate_post(selected_length, selected_language, selected_tag)
        st.write(post)
        
if __name__ == "__main__":
    main()