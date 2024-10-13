import streamlit as st
from openpyxl import load_workbook
from core.extractor.extractor import extract_data_from_sheet

st.title(
    'Calculation of a capped pile'
)

st.header(
    'Input data'
)

with open(r'templates\template.xlsx', 'rb') as file:
    st.download_button(':material/download: Download Template',
                       file, file_name='template.xlsx',
                       use_container_width=True)

file = st.file_uploader('Upload', type=['xls', 'xlsx'], label_visibility='collapsed')

if file:
    st.toast('File successfully uploaded', icon='🔥')

    workbook = load_workbook(file, data_only=True)
    data = extract_data_from_sheet(workbook['PileData'], 'PileData')

    st.sidebar.markdown(f"{data}")
