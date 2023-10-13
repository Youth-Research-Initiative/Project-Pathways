import streamlit as st
import pandas as pd
import math

st.set_page_config(
    page_title="Project Pathways Alpha",
    layout="wide"
)

# Load the CSV files
dfFairdata = pd.read_csv("fair_data.csv")
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


# Streamlit Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select Page", ["Home", "About"])

# Home Page
if page == "Home":
    st.title("Project Pathways Alpha")
    st.header("Region Selection")

    inputRegion = st.selectbox("Select Your Region", dfPopulation.county.unique())
    year = st.selectbox("Select Year", ['2016', '2017', '2018', '2019', '2020', '2021'])

    if inputRegion:
        filtered_population = dfPopulation[dfPopulation['county'].str.contains(inputRegion, case=False, na=False)]
        if not filtered_population.empty:
            st.subheader("Matching Counties:")
            unique_columns = filtered_population.columns
            st.write(filtered_population[unique_columns].drop_duplicates())
        else:
            st.write("No matching counties found.")

    inputState = inputRegion.split(", ")[1]
    stateAbrev = us_state_to_abbrev[inputState]

    button = st.button("Show results")

    if button:
        st.header("Results")

        def getDifficulty(inputRegion, inputState, year):
            populationRegion = dfPopulation[dfPopulation['county'] == inputRegion]
            populationMetric = populationRegion[year].values[0]
            populationState = dfPopulation[dfPopulation['county'].str.contains(inputState)].sum()[year]
            isefFinalistsState = dfIsefdb[dfIsefdb['awards'] != "['nan']"]
            isefFinalistsState = isefFinalistsState[isefFinalistsState['country'] == "United States of America"]
            isefFinalistsState = isefFinalistsState[isefFinalistsState['State'].str.contains(stateAbrev)]
            isefFinalistsState = isefFinalistsState[isefFinalistsState['year'] == int(year)]
            noIsefFinalistsState = isefFinalistsState.shape[0]
            finalistState = dfIsefdb[(dfIsefdb['country'] == "United States of America") & (dfIsefdb['State'].str.contains(stateAbrev)) & dfIsefdb['year'] == int(year)]
            noFinalistsState = finalistState.shape[0]
            st.write(f"population of {inputRegion}: {populationMetric}")
            st.write(f"population of {inputState} {populationState}")
            st.write(f"number of ISEF Finalists: {noIsefFinalistsState}")
            st.write(f"number of Finalists from {inputState} : {noFinalistsState}")
            isefFinalistsRegional = (populationMetric * noIsefFinalistsState) / populationState
            FinalistsRegional = (populationMetric * noFinalistsState) / populationState
            st.write(f"the number of successful ISEF finalists from {inputRegion}: {math.ceil(isefFinalistsRegional)}")
            st.write(f"the number of ISEF finalists from {inputRegion}: {math.ceil(FinalistsRegional)}")

            # Calculate the difficulty
            difficulty = (math.log(populationMetric, 10)) / (math.sqrt(FinalistsRegional + 1) * (1 + math.pow(math.e, -isefFinalistsRegional)))
            st.write(f"Difficulty: {round(difficulty, 3)}")

            # Update the state abbreviation lookup to get the state name from the abbreviation.
            stateName = None
            for state, abbrev in us_state_to_abbrev.items():
                if abbrev == stateAbrev:
                    stateName = state
                    break

                if stateName:
                    # Calculate the counties in the state manually
                    counties_in_state = dfPopulation[dfPopulation['county'].str.contains(stateName)]['county']

                    # Create a list to store individual difficulty values for each county in the state
                    difficulty_values = []

                    for county in counties_in_state:
                                            # Calculate difficulty for each county
                        county_difficulty = (math.log(populationMetric, 10)) / (math.sqrt(FinalistsRegional + 1) * (1 + math.pow(math.e, -isefFinalistsRegional)))
                        difficulty_values.append(county_difficulty)

                    populationRegion = dfPopulation[dfPopulation['county'] == county]
                    populationMetric = populationRegion[year].values[0]
                    populationState = dfPopulation[dfPopulation['county'].str.contains(stateName)].sum()[year]
                    normalized_difficulty = sum(difficulty_values) / len(difficulty_values)

                    # Display the results for each county
                    st.write(f"County: {county}")
                    st.write(f"population of {county}: {populationMetric}")
                    st.write(f"population of {stateName} {populationState}")
                    st.write(f"number of ISEF Finalists: {noIsefFinalistsState}")
                    st.write(f"number of Finalists from {county} : {noFinalistsState}")
                    st.write(f"the number of successful ISEF finalists from {county}: {math.ceil(isefFinalistsRegional)}")
                    st.write(f"the number of ISEF finalists from {county}: {math.ceil(FinalistsRegional)}")
                    st.write(f"Difficulty: {round(county_difficulty, 3)}")
                    st.write(f"Normalized Difficulty Heuristic for {stateName}: {round(normalized_difficulty, 3)}")


                    # Calculate the normalized difficulty heuristic by averaging the individual difficulties


        getDifficulty(inputRegion, inputState, year)

# About Page
elif page == "About":
    st.title("About Project Pathways Alpha")
    st.markdown("""
    Project Pathways Alpha is a Streamlit web application that provides information on the difficulty of achieving success
    in science fairs based on the population of a selected region and the number of finalists from that region.
    It uses data from various sources to calculate the difficulty score.
    """)
