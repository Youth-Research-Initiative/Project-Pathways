import streamlit as st
import pandas as pd
import math

dfFairdata = pd.read_csv("fair_data.xlsx - Sheet1 (1).csv")
dfIsefdb = pd.read_csv("isef-database.csv")
dfPopulation = pd.read_csv("population-metrics.csv")

us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}
stateAbrev = us_state_to_abbrev[inputState]
year = 2023

st.set_page_config(
        page_title="Project Pathways Alpha",
)
st.title("Project Pathways Alpha")

st.header("Region")
inputRegion = st.selectbox("Select Your region", dfPopulation.region.unique())
inputState = inputRegion.split(", ")[1]
stateAbrev = us_state_to_abbrev[inputState]


def getDifficulty(inputRegion, inputState, year=2023):
    populationRegion = dfPopulation[dfPopulation['county'].str.contains(inputRegion,na=False)]
    populationMetric =  populationRegion.iloc[0]['2021']
    populationState = dfPopulation[dfPopulation['county'].str.contains(inputState,na=False)]['2021'].sum()
    isefFinalistsState = dfIsefdb[dfIsefdb['awards'] != "['nan']"] # isefFinalistsState['country'] == "United States"
    isefFinalistsState = isefFinalistsState[isefFinalistsState['country'] == "United States of America"]
    isefFinalistsState = isefFinalistsState[isefFinalistsState['State'].str.contains(stateAbrev)]
    isefFinalistsState = isefFinalistsState[isefFinalistsState['year'] == year]
    finalistState = dfIsefdb[dfIsefdb['country'] == "United States of America"]
    finalistState = finalistState[finalistState['State'].str.contains(stateAbrev)]
    finalistState = finalistState[finalistState['year'] == year]
    noFinalistsState = finalistState.shape[0]
    noIsefFinalistsState = isefFinalistsState.shape[0]
    st.write(f"population of {inputRegion}: {populationMetric}")
    st.write(f"population of {inputState} {populationState}")
    st.write(f"number of ISEF Finalists: {noIsefFinalistsState}")
    st.write(f"number of Finalists from {inputState} : {noFinalistsState} ")
    isefFinalistsRegional = (populationMetric*noIsefFinalistsState)/populationState
    FinalistsRegional = (populationMetric*noFinalistsState)/populationState
    st.write(f"the number of successful isef finalists from {inputRegion}: {math.ceil(isefFinalistsRegional)}")
    st.write(f"the number of isef finalists from {inputRegion}: {math.ceil(FinalistsRegional)}")

    difficulty = (math.log(populationMetric, 10))/ (math.sqrt(FinalistsRegional + 1) * (1 + math.pow(math.e,-isefFinalistsRegional)))
    st.write(f"difficulty: {difficulty}")
    
button = st.button("Temporary please remove: raw data")

if button:
    getDifficulty(inputRegion, inputState, year=2023)


    