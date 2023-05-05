import requests
import csv
import pandas as pd
import io
import base64
import streamlit as st

# Define the function for getting opt-out cases for a given patent number
def get_opt_out_cases(patent_number):
    base_url = "https://api-pre-prod.unified-patent-court.org/upc/public/api"
    endpoint = "/v4/opt-out/list"
    url = base_url + endpoint

    params = {
        "patentNumber": patent_number
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code, response.text)
        return None

# Streamlit app
st.title("Patent Opt-Out Cases")

uploaded_file = st.file_uploader("Upload a CSV file with patent numbers", type="csv")

if uploaded_file:
    input_df = pd.read_csv(uploaded_file)
    result_rows = []

    for index, row in input_df.iterrows():
        patent_number = row["patentNumber"]
        opt_out_cases = get_opt_out_cases(patent_number)

        if opt_out_cases:
            for case in opt_out_cases:
                result_rows.append({
                    "patentNumber": patent_number,
                    "caseType": case["caseType"],
                    "dateOfLodging": case["dateOfLodging"]
                })
        else:
            result_rows.append({
                "patentNumber": patent_number,
                "caseType": "No OptOut",
                "dateOfLodging": ""
            })

    output_df = pd.DataFrame(result_rows)
    st.write(output_df)

    # Create a download link for the output CSV file
    csv_buffer = io.StringIO()
    output_df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    b64 = base64.b64encode(csv_buffer.getvalue().encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="output_patent_status.csv">Download Output CSV</a>'
    st.markdown(href, unsafe_allow_html=True)
