import streamlit as st
from query_engine import run_visibility_check

st.title("Restaurant AI Visibility Checker")
st.write("See if your restaurant gets recommended by AI assistants.")

restaurant_name = st.text_input("Restaurant Name", placeholder="e.g. 14 Prime")
city = st.text_input("City", placeholder="e.g. Jacksonville")
cuisine_type = st.text_input("Cuisine Type", placeholder="e.g. Steak")

if st.button("Check Visibility"):
    if restaurant_name and city and cuisine_type:
        with st.spinner("Asking AI assistants..."):
            results = run_visibility_check(restaurant_name, city, cuisine_type)

        st.subheader("Results")
        for r in results:
            st.write(f"**Query:** {r['query']}")
            col1, col2 = st.columns(2)
            with col1:
                if r['claude_mentioned']:
                    st.success("Claude mentioned it")
                else:
                    st.error("Claude did NOT mention it")
            with col2:
                if r['chatgpt_mentioned']:
                    st.success("ChatGPT mentioned it")
                else:
                    st.error("ChatGPT did NOT mention it")
            st.divider()
    else:
        st.warning("Please fill in all three fields.")
