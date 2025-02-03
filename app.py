import streamlit as st
import pandas as pd
import numpy as np
import os
from vectfit3 import vectfit
from vectfit3 import opts
from scipy.constants import pi
import skrf as rf

page1 = st.Page("page/feild2circuit.py", title="场路转换")
page2 = st.Page("page/spice_configure.py", title="电路仿真")
page3 = st.Page("page/database4aircraft.py", title="飞机数据库")

pg = st.navigation([page1, page2, page3])
pg.run()


