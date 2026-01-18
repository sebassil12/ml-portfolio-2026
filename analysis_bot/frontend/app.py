import streamlit as st
import requests
import json
import pandas as pd

st.set_page_config(page_title="The Pain Hunter", layout="wide")
st.title("🎯 The Pain Hunter: Competitor Analysis Bot")
st.markdown("Analyze competitor reviews to find **Pain Points** and **Marketing Hooks**.")

# Input
col_input, col_btn = st.columns([4, 1])
with col_input:
    url = st.text_input("Enter Product URL", placeholder="https://amazon.com/dp/...", label_visibility="collapsed")
with col_btn:
    analyze_btn = st.button("Hunt for Pain 🏹", use_container_width=True)

if analyze_btn:
    if not url:
        st.warning("Please enter a URL")
    else:
        with st.spinner(f"Scraping & Analyzing... This can take up to a minute."):
            try:
                # Call backend
                # Assuming backend is running on port 8000
                response = requests.post("http://localhost:8000/analyze", json={"url": url, "platform": "amazon"})
                
                if response.status_code == 200:
                    result = response.json()
                    data = result.get("data", {})
                    
                    if "error" in data:
                        st.error(f"Analysis Error: {data['error']}")
                    else:
                        complaints = data.get("complaints", [])
                        hooks = data.get("hooks", [])
                        
                        # Display Results
                        st.success("Analysis Complete!")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("😡 Pain Points (Complaints)")
                            if not complaints:
                                st.info("No major complaints found.")
                            for item in complaints:
                                with st.expander(f"⚠️ {item.get('insight', 'N/A')}"):
                                    st.write(f"**Frequency:** {item.get('frequency', 'N/A')}")
                                    st.info(f"**Copy Idea:** {item.get('suggested_copy', 'N/A')}")

                        with col2:
                            st.subheader("🎣 Hooks (Selling Points)")
                            if not hooks:
                                st.info("No hooks found.")
                            for item in hooks:
                                with st.expander(f"✨ {item.get('insight', 'N/A')}"):
                                    st.write(f"**Frequency:** {item.get('frequency', 'N/A')}")
                                    st.success(f"**Copy Idea:** {item.get('suggested_copy', 'N/A')}")
                        
                        # Raw Data View
                        with st.expander("View Raw JSON Data"):
                            st.json(data)
                            
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to backend. Is FastAPI running? (uvicorn app.main:app --reload)")
            except Exception as e:
                st.error(f"An error occurred: {e}")

st.divider()
st.caption("Powered by Playwright, FastAPI, and Gemini 1.5 Flash")
