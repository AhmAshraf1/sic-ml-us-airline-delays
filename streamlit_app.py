import pickle
import streamlit as st
import pandas as pd
import xgboost

# Page config
st.set_page_config(
    page_title="US Airline Flight Delays",
#    page_icon="images/image.jpg",
    # layout="wide",
)

# Page title
st.title('US Airline Flight Delays')
#st.image('images/image.jpg')
st.write("\n\n")

st.markdown(
    """
    This app aims to assist in three things:
    1- Predict if there is delay in the departure of the flight.
    2- how many minutes there will be a delay in the departure?
    3- How much time there will be as a delay in the arrival of flight?
    """
)

# Load our three models
with open('models/xgb_class_model.pkl', 'rb') as model_clf:
    clf = pickle.load(model_clf)

with open('models/gb_reg_model.pkl', 'rb') as model_dep:
    reg_dep = pickle.load(model_dep)
    
with open('models/gb_arr_model.pkl', 'rb') as model_arr:
    reg_arr = pickle.load(model_arr)
    
# Streamlit interface to input data
col1, col2= st.columns(2)

with col1:
    day_of_week = st.number_input(label='Consider 1 for Monday and 7 for Sunday')
    airline = st.selectbox(label='Airline Company', options=['Southwest Airlines Co.', 'Endeavor Air', 'Delta Air Lines Inc',
                                                            'United Air Lines Inc.', 'Frontier Airlines Inc.','Skywest Airlines Inc.', 'American Airlines Inc.', 'Allegiant Air', 'JetBlue Airways', 'PSA Airlines', 'American Eagle Airlines Inc.',
                                                            'Spirit Air Lines', 'Republic Airways', 'Alaska Airlines Inc.', 'Hawaiian Airlines Inc.'])
    dep_time = st.selectbox(label='Dearture Time Period', options=['Evening', 'Morning', 'Night', 'Afternoon'])
    dep_type = st.selectbox(label='Departure Delay Type', options=['Low <5min', 'Medium >15min', 'Hight >60min'])

with col2:
    arr_type = st.selectbox(label='Loan Purpose', options=['Low <5min', 'Medium >15min', 'Hight >60min'])
    flight_dur = st.number_input(label='Flight Duration in min')
    dist = st.selectbox(label='Flight Distance', options=['Short Haul >1500Mi', 'Medium Haul <3000Mi', 'Long Haul <6000Mi'])
    month = st.number_input(label='Month as number')
    day = st.number_input(label="Day")

mapping_airlines = {'Southwest Airlines Co.':12, 'Endeavor Air':5, 'Delta Air Lines Inc':4,
                                                            'United Air Lines Inc.':14, 'Frontier Airlines Inc.':6,'Skywest Airlines Inc.':11, 'American Airlines Inc.':2, 'Allegiant Air':1, 'JetBlue Airways':8, 'PSA Airlines':9, 'American Eagle Airlines Inc.':3,
                                                            'Spirit Air Lines':13, 'Republic Airways':10, 'Alaska Airlines Inc.':0, 'Hawaiian Airlines Inc.':7}

mapping_time = {'Evening':1, 'Morning':2, 'Night':3, 'Afternoon':0}

mapping_type = {'Low <5min':1, 'Medium >15min':2, 'Hight >60min':0}

mapping_dist = {'Short Haul >1500Mi':2, 'Medium Haul <3000Mi':1, 'Long Haul <6000Mi':0}
# Function to predict the input
def class_prediction(day_of_week, airline, dep_time, dep_type, arr_cityname,
               arr_airport, arr_type, flight_dur, dist, month,
               day):

    
    airline = airline.map(mapping_airlines)
    dep_time = dep_time.map(mapping_time)
    dep_type = dep_type.map(mapping_type)
    arr_type = arr_type.map(mapping_type)
    dist = dist.map(mapping_dist)
    
    # Create a df with input data
    df_input = pd.DataFrame({
        'Day_Of_Week': [day_of_week],
        'Airline': [airline],
        'DepTime_label': [dep_time],
        'Dep_Delay_Type': [dep_type],
        'Arr_Delay_Type': [arr_type],
        'Flight_Duration': [flight_dur],
        'Distance_type': [dist],
        'Month':[month],
        'Day':[day]
    })

    prediction = clf.predict(df_input)

    if prediction[0] == 1:
        prediction = "There is Departure Delay"
        
#        delay_min = reg_dep.predict(df_reg)
        
    else:
        prediction = "No Departure Delay"
    return prediction


# Botton to predict
if st.button('Predict'):
    predict = class_prediction(day_of_week, airline, dep_time, dep_type, arr_cityname,
               arr_airport, arr_type, flight_dur, dist, month,day)
    st.write("For your flight {}".format(predict))
    st.success(predict)
