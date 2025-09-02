import streamlit as st
from scrape import scrape_website, split_dom_content, clean_body_content, extract_body_content
from parse import parse_with_ollama
import pandas as pd
import io

st.title("*******AI Web Scraper*******")
url = st.text_input("Enter the URL to scrape:")

if st.button("Scrape"):
    st.write(f"Scraping content from: {url}")
    result = scrape_website(url)
    body_content = extract_body_content(result)
    cleaned_content = clean_body_content(body_content)

    st.session_state.dom_content = cleaned_content

    with st.expander("View DOM content"):
        st.text_area("DOM Content", cleaned_content, height=300)

if "dom_content" in st.session_state:
    parse_description = st.text_area("Prompt to the LLM, what you want to extract...")

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing content...")

            dom_chunks = split_dom_content(st.session_state.dom_content)
            result = parse_with_ollama(dom_chunks, parse_description)
            st.write(result)


            if isinstance(result, list):
                df = pd.DataFrame(result)
            elif isinstance(result, dict):
                df = pd.DataFrame([result])
            else:
                df = pd.DataFrame([{"Extracted Data": str(result)}])

            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            st.download_button(
                label="Download Extracted Data as CSV",
                data=csv_buffer.getvalue(),
                file_name="extracted_data.csv",
                mime="text/csv"
            )