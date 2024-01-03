import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

import random
from faker import Faker
from datetime import datetime, timedelta
from io import StringIO

# --- PAGE CONFIG ---
st.set_page_config(page_title="Covid-19 Testing Data", page_icon="🦠")

if 'clicked' not in st.session_state:
    st.session_state.clicked = False


def click_button():
    st.session_state.clicked = True


# --- SECTION 1: TITLE/EXPLANATION ---
col1, col2 = st.columns([0.15, 0.85])

with col1:
    page_image = Image.open('images/microbe.png')
    st.image(page_image, use_column_width='always')

st.title('Case Study: Covid-19 Testing Data', anchor=False)

''
'**The tool below simulates *Pillar 2* Covid-19 testing data that was submitted to Public Health England (PHE) by third-party testing providers.**'
'This placeholder data was used to test a data pipeline developed in response to a widely publicised error that resulted in the loss of thousands of positive Covid-19 test results. A full analysis of the error and a method for developing a solution can be found [here](https://www.richardhonour.com/projects/excel-a-data-pipeline-error-that-lost-thousands-of-covid-19-test-results).'
''
with st.expander('**Disclaimer:** Medical Data'):
    st.markdown('This data generator is designed for illustrative and educational purposes only. The medical data it produces is entirely fictitious and should not be considered authentic or valid for any medical, clinical, or research purposes. It is not a substitute for genuine patient information and must not be used in any inappropriate, unethical, or illegal manner.')

# --- SECTION 2: DATASET ---
with st.expander('**Breakdown:** Covid-19 Testing Dataset'):
    st.markdown("""
                **The following is (confirmed) data that would have been sent to PHE:**
                - NHS Number
                - Surname
                - Forename
                - Hospital Number
                - Date of Birth
                - Postcode
                - Test Number
                - Test Result
                """)
    ''
    '**This data was submitted in *CSV (comma-separated values)* format:**'

    st.code('''
            NHS_Number,Surname,Forename,Hospital_Number,Date_of_Birth,Postcode,Test_Number,Test_Result
            3746422982,Butt,Jorge,NL4746606,13/11/1995,UP27 OM7,T84589444058,Negative
            9288916883,Byrne,Talha,XT4430059,20/12/2002,BQ9 VD9,T40540777001,Positive''', language="csv", line_numbers=False)
    ''
    '**It would have then been displayed in *tabular* format (in Excel):**'
    example_data = {
        "NHS_Number": [3746422982, 9288916883],
        "Surname": ["Butt", "Byrne"],
        "Forename": ["Jorge", "Talha"],
        "Hospital_Number": ["NL4746606", "XT4430059"],
        "Date_of_Birth": ["13/11/1995", "20/12/2002"],
        "Postcode": ["UP27 OM7", "BQ9 VD9"],
        "Test_Number": ["T84589444058", "T40540777001"],
        "Test_Result": ["Negative", "Positive"]
    }
    example_table = pd.DataFrame(example_data)
    st.table(data=example_data)
''
# --- SECTION 3: DATA GENERATOR ---
if 'results' not in st.session_state:
    st.session_state.results = {'data': ''}

if 'button_press_count' not in st.session_state:
    st.session_state.button_press_count = 0

if 'date' not in st.session_state:
    st.session_state.date = {'date': datetime.now() - timedelta(days=7)}


def testing_data_generator(number):
    fake = Faker('en_GB')
    data = ""
    for _ in range(number):
        data += f'{str(random.randint(10**9, 10**10 - 1))},'
        data += f'{st.session_state.date["date"].strftime("%d/%m/%Y")},'
        data += f'{fake.last_name()},{fake.first_name()},'
        data += f'{random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + str(random.randint(10**6, 10**7 - 1))},'
        data += f'{fake.date_of_birth().strftime("%d/%m/%Y")},'
        data += f'{fake.postcode()},'
        data += f'{"T" + str(random.randint(10**10, 10**11 - 1))},'
        data += f'{random.choice(["Positive", "Negative"])}'
        data += "\n"

    st.session_state.date['date'] += timedelta(days=1)

    return data


# GENERATE DATA BUTTON
st.code('''import random
from faker import Faker
        
def testing_data_generator(number):
    fake = Faker('en_GB')
    data = ""
    for _ in range(number):
        data += f'{str(random.randint(10**9, 10**10 - 1))},'
        data += f'{fake.last_name()},{fake.first_name()},'
        data += f'{random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + str(random.randint(10**6, 10**7 - 1))},'
        data += f'{fake.date_of_birth().strftime("%d/%m/%Y")},'
        data += f'{fake.postcode()},'
        data += f'{"T" + str(random.randint(10**10, 10**11 - 1))},'
        data += f'{random.choice(["Positive", "Negative"])}'
        data += "\\n"
    return data
        '''
        )

runs_remaining = 0

if st.button('**Run**', on_click=click_button, type='primary', use_container_width=True) and st.session_state['button_press_count'] < 7:
    st.session_state.clicked = True
    st.session_state.results['data'] += testing_data_generator(random.randint(100, 200))
    st.session_state['button_press_count'] += 1
    runs_remaining = 7 - st.session_state['button_press_count']

if st.button('Reset', use_container_width=True):
    st.session_state.button_press_count = 0
    st.session_state.results['data'] = ''
    st.session_state.clicked = False
    st.session_state.date = {'date': datetime.now() - timedelta(days=7)}
    st.info('Session data reset.')

if st.session_state.clicked == True and st.session_state.button_press_count < 7:
    st.success(f"**{runs_remaining}** runs remaining.")
elif st.session_state.clicked == True:
    st.warning('**Reached maximum allowed runs** *(generated 1 week of data)*', icon='✋')


# DISPLAY RESULTS (AS CSV/DATAFRAME)
if st.session_state.clicked:
    ''
    display_data = st.session_state.results['data'].splitlines()[:10]
    with st.status('CSV Data (*first 10 records*)') as status:
        for record in display_data:
            st.text(record)
    df = pd.read_csv(StringIO(st.session_state.results['data']), header=None, names=[
                     "NHS Number", "Date", "Surname", "Forename", "Hospital Number", "D.O.B", "Postcode", "Test Number", "Test Result"])

    total_tests = (df.shape[0])

    with st.status(f"Dataframe (*{total_tests} records created*)") as status:
        st.dataframe(
            df,
            column_config={
                "NHS Number": st.column_config.NumberColumn(
                    format="%d",
                )},
        )

    # DOWNLOAD DATA BUTTON
    csv_data = st.session_state.results['data'].encode('utf-8')

    st.download_button(
        label="⬇️ Download",
        data=csv_data,
        file_name='covid_testing_data.csv',
        key='download_button'
    )
    ''
    ':gray[***Note:** An additional value \'date\' has been added in order to simulate the collection of testing data across the span of a week. With each run the date increments by one day (starting from 7 days previous to the current date). This is for the purposes of recreating the UK Government dashboard for testing data, which can be found [here](https://coronavirus.data.gov.uk/details/testing?areaType=nation&areaName=England).*]'
    ':gray[***Note:** Each run will generate testing records for between 100 to 200 people.*]'


    st.divider()

    # SUMMARY STATISTICS
    st.subheader('Testing in England', anchor=False)
    total_positive_cases = (df['Test Result'] == 'Positive').sum()
    total_positive_percentage = (total_positive_cases / total_tests * 100)
    # *CALCULATE PERCENTAGE INCREASE/DECREASE AS DELTA

    col3, col4, col5 = st.columns(3)

    with col3:
        st.metric(label='Virus tests reported *(last 7 days)*', value=total_tests)
    with col4:
        st.metric(label='Positive cases rolling sum', value=total_positive_cases)
    with col5:
        st.metric(label='Case positivity by date rolling sum',
                  value=f"{round(total_positive_percentage, 2)}%")
    
    total_tests_df = df.groupby('Date').size().reset_index(name='Total Tests')

    total_tests_graph = px.line(total_tests_df, x='Date', y='Total Tests', title='Weekly number of people receiving a PCR test')
    st.plotly_chart(total_tests_graph)