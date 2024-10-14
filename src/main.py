# TODO: Add new functionality from calculate.py
import streamlit as st
from openpyxl import load_workbook

from core.extractor.extractor import extract_data_from_sheet
from core.calculate import MainCalculation


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
    pile_data = extract_data_from_sheet(workbook['PileData'], 'PileData')
    load_data = extract_data_from_sheet(workbook['LoadData'], 'LoadData')
    foundation_data = extract_data_from_sheet(workbook['FoundationData'], 'FoundationData')

    result = MainCalculation().calculate(pile_data, load_data, foundation_data)

    if result.get('is_passed'):
        st.success('Calculation successful')
        st.json(result)
    else:
        st.error('Calculation failed')
        st.json(result)