#https://github.com/Kanaries/pygwalker?tab=readme-ov-file
# https://github.com/Kanaries/graphic-walker
# Online cloud PyGWalker https://graphic-walker.kanaries.net/
# permission of Kanaries to my github account for creating chart https://github.com/settings/connections/applications/fcb8c65be04ed9dca575
import pandas as pd
import streamlit.components.v1 as components
import streamlit as st
from pygwalker.api.streamlit import init_streamlit_comm, get_streamlit_html
 
#The following code is from Kanaries documentation https://docs.kanaries.net/pygwalker/api-reference/streamlit
 
st.set_page_config(
    page_title="Use Pygwalker In Streamlit",
    layout="wide"
)
 
st.title("ETEC Data Visualization using Streamlit and PyGWalker")
 
# Initialize pygwalker communication
init_streamlit_comm()
 
# When using `use_kernel_calc=True`, you should cache your pygwalker html, if you don't want your memory to explode
@st.cache_resource
def get_pyg_html(df: pd.DataFrame) -> str:
    # When you need to publish your application, you need set `debug=False`,prevent other users to write your config file.
    # If you want to use feature of saving chart config, set `debug=True`
    html = get_streamlit_html(df, spec="./gw0.json", use_kernel_calc=True, debug=False)
    return html
 
@st.cache_data
def get_df() -> pd.DataFrame:
    return pd.read_csv("/Users/nemaaa/github/ETEC/etec_energy_data.csv")
 
df = get_df()
 
components.html(get_pyg_html(df), width=1300, height=1000, scrolling=True) 





''' How to turn pygwalker into a web application that can be shared with others?
import pygwalker as pyg
import pandas as pd
import streamlit.components.v1 as components
# Import your data
df = pd.read_csv("/<your_data>.csv")
# Generate the HTML using Pygwalker
pyg_html = pyg.to_html(df)
 
# Embed the HTML into the Streamlit app
components.html(pyg_html, height=1000, scrolling=True) '''




#https://github.com/Kanaries/graphic-walker/wiki/How-to-Create-Computed-field-in-Graphic-Walker

# For created data field in the Streamlit+PyGWalker app: go to the create field on the web interface (chrome browser)
# CASE WHEN measurement_type = 'W_TOT' THEN 1 ELSE 0 END
# CASE WHEN measurement_type = 'kWh' THEN 1 ELSE 0 END
# CASE WHEN measurement_type = 'AL1' THEN 1 ELSE 0 END
# CASE WHEN measurement_type = 'VL1N' THEN 1 ELSE 0 END
# CASE WHEN measurement_type = 'AL2' THEN 1 ELSE 0 END
# CASE WHEN measurement_type = 'VL2N' THEN 1 ELSE 0 END
# CASE WHEN measurement_type = 'AL3' THEN 1 ELSE 0 END
# CASE WHEN measurement_type = 'VL3N' THEN 1 ELSE 0 END
