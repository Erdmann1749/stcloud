import streamlit as st
import datetime
import pandas as pd
import os

def load_data() -> pd.DataFrame:
    if os.path.exists("data.pickle"):
        data = pd.read_pickle("data.pickle")
    else:
        data = pd.DataFrame(columns=["amount", "last_time", "type"])
    return data

def save_data(new_data):
    df = load_data()
    df.loc[len(df.index)] = new_data
    df.to_pickle("data.pickle")

# App title
st.set_page_config(page_title="🤗💬 Stillplan")

#
st.title("Stillplan")

input, overview = st.tabs(["input", "overview"])
with input:
    with st.form("Eingabe"):
        amount = st.slider('Wieviel hat BG MOO getrunken?', 0, 150, step=10)
        date = st.date_input('An welchem Tag hat BG MOO getrunken?')
        time = st.time_input('Um wie viel Uhr hat BG MOO getrunken?')
        type = st.selectbox("Wie und was hat BG MOO getrunken?",
                            ('Pre-Milch', 'Mutter-Milch', 'Brust-Milch'),
                            )

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write("Am ", date, " um ", time, 'hat BG MOO ', amount, type, "getrunken")
            last_time = datetime.datetime.combine(date, time)
            save_data([amount, last_time, type])

with overview:
    data = load_data()
    if len(data) > 0:
        #t1 = datetime.datetime.strptime(str(datetime.datetime.now(), "%H:%M:%S")
        #t2 = datetime.datetime.strftime(str(list(data['time'])[-1]), "%H:%M:%S")
        #time_since_last_food = t1 - t2
        time_since_last_food = datetime.datetime.now() - list(data['last_time'])[-1]
        hours = int(time_since_last_food / datetime.timedelta(hours=1))
        minutes = int((time_since_last_food / datetime.timedelta(hours=1) - hours) * 60)
        #last_food = list(data['time'])[-1]
        #st.write("Letzte Mahlzeit war um ", last_food, ".")
        st.write("Letzte Mahlzeit ist ", hours, "Stunden und ", minutes, " Minuten her.")

    else:
        st.write("Keine Daten verfügbar.")




