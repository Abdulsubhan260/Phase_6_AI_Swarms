import streamlit as st
import requests
import time

API_URL="https://subii-1-travel-ai-swarm-325dc94.hf.space/plan-trip"

st.title("Travel Planner")
st.subheader("plan your trip!!!!")
st.write("Powered by LangGraph on cloud")

city=st.text_input("Enter city you want to travel")
days=st.slider("Select days",1,14)
if st.button("Plan My Trip!!!"):
    if city:
        with st.spinner(f"Sending request to cloud AI for {city}"):
            time.sleep(2)
            payload={
                "city":city,
                "days":days
            }

            try:
                response=requests.post(API_URL,json=payload)
                if response.status_code==200:
                    data=response.json()
                    st.success("Trip Planned Successfully...")

                    st.markdown(data["itenerary"])
                    st.info(data["budget"])


                else:
                    st.error(f"cloud server error!!!{response.status_code}")
                    st.write(response.text)
            except Exception as e:
                st.error(f"Failed to connect to backend Error: {e}")
    else:
            st.warning("Please enter city or days first.....")


