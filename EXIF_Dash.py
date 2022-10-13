#Import Modules
import pandas as pd
import numpy as np
import geopandas
import geopy
import io
import os
import folium
import folium.plugins as plugins
import xlrd
import streamlit as st
import PIL
from exif import Image
from collections import defaultdict

import streamlit_folium as st_folium
import os.path

st.set_page_config(page_title="Geolocating Photos Application",
                   page_icon=Image.open(r"ArrowheadFavicon.png"),
                   layout="wide",
                   initial_sidebar_state="expanded")

left, right = st.columns([5, 3])

st.sidebar.title("Geolocating Photos Application")
st.sidebar.markdown("Upload an Image and Get Its location on a Map")


#Files upload/copy
uploaded = st.sidebar.file_uploader(label="Choose a file", accept_multiple_files=True)
save_path = '/images'

#EXCEL FILES
#Files upload/copy
#uploaded = st.sidebar.file_uploader(label="Choose a XLSX file:", type="xlsx", #accept_multiple_files=False)
#if uploaded is not None:
#    df = pd.read_excel(uploaded)
#    st.dataframe(df)



def decimal_coords(coords, ref):
    decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
    if ref == "S" or ref == "W":
        decimal_degrees = -decimal_degrees
    return decimal_degrees


info_dict = defaultdict(list)

def collect_info_dict(file, image):
    info_dict["name"].append(file.name)

    if "make" in dir(image):
        info_dict["make"].append(image.make)
    if "model" in dir(image):
        info_dict["model"].append(image.model)
    if "datetime" in dir(image):
        info_dict["datetime"].append(image.datetime)

    if "gps_latitude" in dir(image):
        info_dict["latitude"].append(decimal_coords(
            image.gps_latitude, image.gps_latitude_ref))
        info_dict["longitude"].append(decimal_coords(
            image.gps_longitude, image.gps_longitude_ref))
    else:
        right.error("The Image have No Coordinates")

    return info_dict


def create_df(d):
    return pd.DataFrame.from_dict(d)



df = pd.DataFrame()



if uploaded is not None:
    for file in uploaded:
        img = Image(file)
        left.image(PIL.Image.open(file))
        if img.has_exif:
            st.write("This image **has** EXIF Metadata. Hold on...:",file)
            result = collect_info_dict(file, img)
            #right.write(result)
            right.write(result)
            #df = df.append(result, ignore_index=True) #works but needs parsing of lat/lon
            df = create_df(result)            
            left.write('---')
            right.write('---')
            #if 'latitude' in result.keys():
            #    st.map(df)
            #st.dataframe(data=df)
                
        else:
            st.write("The Image has **NO** EXIF information:",file)
            #st.dataframe(data=df)
        #st.dataframe(data=df)

else:
    st.write("Upload File/Files to Analyze!")


#Renders single df bc outside loop

st.dataframe(data=df)
#renders single map bc outside loop
st.map(df)

#
cwd = os.getcwd()
imgdir = '/images'

save_path = os.path.join(cwd+imgdir)

#Saves copy of files
#for file in uploaded:
#    with open(file.name, "wb") as f:
#        try:
#            os.makedirs('images', exist_ok=True)
#            f.write(file.getbuffer())
#            f.close()
#        except: 
#            pass

#__new

#function to save files and create 'images' dir to save them into
def save_uploadedfile(uploaded):
    with open(os.path.join('images',uploaded.name), "wb") as f:
        f.write(uploaded.getbuffer())
        #return st.success("Saved:{} to Data".format(uploaded.name))

for file in uploaded:
    try:
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        if uploaded is not None:
           save_uploadedfile(file)
    except:
        pass



