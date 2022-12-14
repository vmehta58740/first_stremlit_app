import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('Hello GitHub and stremlit')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avacodo Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
#streamlit.dataframe(my_fruit_list)

fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])

fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
    # write your own comment -what does the next line do? 
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
  
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get an information")
  else:
    back_from_function=get_fruityvice_data(fruit_choice)
    # write your own comment - what does this do?
    streamlit.dataframe(back_from_function)  

except URLError as e:
    streamlit.error()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)

streamlit.header("The fruit load list contains:")
#snowflake related functions
def get_fruit_load_list():
    with my_cnx2.cursor() as my_cur2:
        my_cur2.execute("SELECT * from pc_rivery_db.public.fruit_load_list")  
        return my_cur2.fetchall()
# Add a button to load the fruit
if streamlit.button('Get fruit load list'):
    my_cnx2 = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows =get_fruit_load_list()
    streamlit.dataframe(my_data_rows)

#Allow the end user to add a frit to the list
def insert_row_snowflake(new_fruit):
    with my_cnx2.cursor() as my_cur2:
        my_cur2.execute("insert into fruit_load_list values('"+new_fruit+"')")
        return "Thanks for adding " + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to Add?')    
if streamlit.button('Add a Fruit to the list'):
    my_cnx2 = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function =insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)

streamlit.stop()
