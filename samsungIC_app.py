import streamlit as st
import  base64
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from PIL import Image
import pickle
from streamlit_autorefresh import st_autorefresh
from streamlit_option_menu import option_menu


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: "%.3f" % x)
pd.set_option('display.width', 500)

st.set_page_config(
    page_title="Impact of Dune Plants on Caretta Caretta",
    page_icon="🐢️",
    initial_sidebar_state="expanded",
)

sidebar_bg_image = "side-bar.png"


def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = f"""
    <style>
    [data-testid="stSidebar"] > div:first-child {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        border-radius: 15px;
        overflow: visible;

    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)


set_png_as_page_bg(sidebar_bg_image)

with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["Introduction", "Plants", "EDA", "Model Prediction", "Model Evaluation", "Our Team"],
        default_index=0
    )

def get_raw_data():
    """
    This function returns a pandas DataFrame with the raw data.
    """
    raw_df = pd.read_csv('ReddingRootsCaseStudy22_csv.csv')
    raw_df = raw_df[0:93]
    raw_df = raw_df.drop(columns=["Comments", "Notes", "Unnamed: 42"])
    raw_df = raw_df.drop(columns=["Species", "Key"])
    return raw_df

def get_cleaned_data():
    """
    This function return a pandas DataFrame with the cleaned data.
    """
    clean_data = pd.read_csv('cleaned_df.csv')
    return clean_data
df_c = get_cleaned_data()
def summary_table(df):
    """
    Return a summary table with the descriptive statistics about the dataframe.
    """
    summary = {
    "Number of Variables": [len(df.columns)],
    "Number of Observations": [df.shape[0]],
    "Missing Cells": [df.isnull().sum().sum()],
    "Missing Cells (%)": [round(df.isnull().sum().sum() / df.shape[0] * 100, 2)],
    "Duplicated Rows": [df.duplicated().sum()],
    "Duplicated Rows (%)": [round(df.duplicated().sum() / df.shape[0] * 100, 2)],
    "Categorical Variables": [len([i for i in df.columns if df[i].dtype==object])],
    "Numerical Variables": [len([i for i in df.columns if df[i].dtype!=object])],
    }
    return pd.DataFrame(summary).T.rename(columns={0: 'Values'})

def grab_col_names(dataframe, cat_th=10, car_th=20):  #kategorik, nümerik değişkenleri ayıklamak için
  ###cat_cols
  cat_cols = [col for col in dataframe.columns if dataframe[col].dtypes == "O"]
  num_but_cat = [col for col in dataframe.columns if dataframe[col].nunique() < cat_th and
                 dataframe[col].dtypes != "O"]
  cat_but_car = [col for col in dataframe.columns if dataframe[col].nunique() > car_th and
                 dataframe[col].dtypes == "O"]
  cat_cols = cat_cols + num_but_cat
  cat_cols = [col for col in cat_cols if col not in cat_but_car]
  ###num_cols
  num_cols = [col for col in dataframe.columns if dataframe[col].dtypes != "O"]
  num_cols = [col for col in num_cols if col not in num_but_cat]
  print(f"observations: {dataframe.shape[0]}")
  print(f"variables: {dataframe.shape[1]}")
  print(f"cat_cols: {len(cat_cols)}")
  print(f"num_cols: {len(num_cols)}")
  print(f"cat_but_car: {len(cat_but_car)}", f"cat_but_car name: {cat_but_car}")
  print(f"num_but_cat: {len(num_but_cat)}", f"num_but_cat name: {num_but_cat}")
  return cat_cols, num_cols, cat_but_car




########################## INTRODUCTION ###################################


#SLide show fotoğrafları
slide_images = [
    "slideshow_images/photo1.jpg",
    "slideshow_images/photo2.jpg",
    "slideshow_images/photo3.jpg",
    "slideshow_images/photo4.jpg",
    "slideshow_images/photo5.jpg",
    "slideshow_images/photo6.jpg",
    "slideshow_images/photo7.jpg",
    "slideshow_images/photo8.jpg",
    "slideshow_images/photo9.jpg",
    "slideshow_images/photo10.jpg",
    "slideshow_images/photo11.jpg",
    "slideshow_images/photo12.jpg",
    "slideshow_images/photo13.jpg",
    "slideshow_images/photo14.jpg",
]

refresh_rate = 3
# Introduction kısmı
if selected == 'Introduction':
    count = st_autorefresh(interval=refresh_rate * 1000, key="slideshow")
    col1, col2 = st.columns([2, 8])
    with col1:
        st.image("CarettaCarettaTurtle-Photoroom.png", width=165)
    with col2:
        st.title("Impact of Dune Plants on Loggerhead Sea Turtles")
    st.write("An explanatory website for our Samsung IC capstone project.")
    st.header("Introduction")

    #SLAYT
    slide_index = count % len(slide_images)
    slide_image = Image.open(slide_images[slide_index])
    slide_image = slide_image.resize((400, 250))
    st.image(slide_image, use_column_width=True)
    st.markdown("""(The images above are generated by using Midjourney.)""")
    st.markdown("""
        In this project, observing the effects of dune plants on loggerhead sea turtle eggs hatching success is aimed. 
        The nesting success of loggerhead sea turtles (Caretta caretta) is highly dependent on dune plant
        roots, since they lay their eggs near dunes. Dune plant roots can cause harm to the eggs and reduce
        the chances of hatching by breaking them. Therefore, it is crucial to analyze and optimize the effect of
        dune plants upon the hatching of the eggs.
    """)

    image1 = Image.open('seaturtle_img.jpg')
    width, height = image1.size
    image1 = image1.resize((420, 300))
    st.image(image1, caption='Loggerhead Sea Turtle')

    col1, col2 = st.columns([1, 2])

    with col1:
        st.image("invadedeggs.jpg", width=200, caption='Eggs ruined by roots [1]')
    with col2:
        st.image("ruinedeggs_hatchling.jpg", width=403, caption='Invaded eggs by roots and trapped loggerhead hatchling [1]')

    st.markdown("""
        ### About the Dataset
        The dataset is publicly available in the Dryad data repository. It is published in 2024 and there is also
        a reference paper describing the process of data collection and statistical analysis of the data [2]. In
        the process of creating the data, they monitored 93 nests for 6 months in 2022. The data are in tabular
        form and there are 42 features and 93 samples.
        [Link to the Dataset](https://datadryad.org/stash/dataset/doi:10.5061/dryad.zw3r228dk)
        """)


    st.markdown("""
    ### Plant Types in Pie Chart
    The plants classified as "Others" includes plant types such as: palm, christmas cactus, unknown, dune sunflower,
    seaside spurge (sandmat). These are not shown in the pie chart since their percentage is really low.
    """)

    image2 = Image.open('piechart.png')
    width, height = image2.size
    image2 = image2.resize((550, 500))
    st.image(image2, caption='Pie chart to show different plant types in the dataset ')

    st.markdown("""
        ### Sustainable Development Goal (SDG) of the Project
        Since the main objective of the project is loggerhead sea turtles, this project falls within the scope of
        SDG-14 (life under water).
        [For further information about SDG-14](https://sdgs.un.org/goals/goal14)
        """)

    image3 = Image.open('sdg14.png')
    width, height = image3.size
    image3 = image3.resize((200, 200))
    st.image(image3, caption='SDG-14 Logo')

    st.markdown("""
        ### Article About the Dataset
        To learn more about the dataset you can access the dataset article (referenced as [1]) : [Link to the Article](https://onlinelibrary.wiley.com/doi/full/10.1002/ece3.11207)
        """)

######################### PLANTS ################################

elif selected == 'Plants':
    col1, col2 = st.columns([2, 7])

    with col1:
        st.image("CarettaCarettaTurtle-Photoroom.png", width=185)
    with col2:
        # Başlık ve Açıklama
        st.markdown("<h1 style='margin-top: 40px;'>Dune Plants</h1>", unsafe_allow_html=True)

    plants_info = {
        "Beach Naupaka": {
            "images": ["plant_images/beach-naupka.jpg", "plant_images/beach-naupaka-2.jpg",
                       "plant_images/beach-naupaka-3.jpg"],
            "description": "Beach naupaka is a shrub found in coastal areas. It has white to pale yellow flowers and is known for its salt tolerance. It helps stabilize sand dunes, which is crucial for the nesting success of Caretta carettas."
        },
        "Christmas Cactus": {
            "images": ["plant_images/christmas-cactus.jpg","plant_images/christmas-cactus-2.jpg","plant_images/christmas-cactus-3.png"],
            "description": "Christmas cactus is a popular houseplant known for its beautiful flowers that bloom around Christmas time. It can grow in coastal areas and contributes to dune stabilization, indirectly supporting the nesting habitats of Caretta carettas."
        },
        "Crested Saltbush": {
            "images": ["plant_images/crested-saltbush.jpg","plant_images/crested-saltbush-2.jpg","plant_images/crested-saltbush-3.jpg"],
            "description": "Crested saltbush is a perennial shrub that grows in saline soils. It helps stabilize coastal soils, reducing erosion and providing a safer nesting ground for Caretta carettas."
        },
        "Dune Sunflower": {
            "images": ["plant_images/dune-sunflower.jpg","plant_images/dune-sunflower-2.jpg","plant_images/dune-flowers-3.jpg"],
            "description": "Dune sunflower is a flowering plant that grows in sandy soils along the coast. Its root systems help to stabilize dunes, which is essential for the nesting success of Caretta carettas."
        },
        "Palm": {
            "images": ["plant_images/palmtree.jpg","plant_images/palm-2.jpg","plant_images/palm-3.jpg"],
            "description": "Palms are a diverse group of plants that are commonly found in tropical and subtropical regions. Certain palm species can help stabilize coastal dunes, providing a supportive environment for Caretta caretta nesting."
        },
        "Railroad Vine": {
            "images": ["plant_images/railroad-vine.jpeg","plant_images/railroad-vine-2.jpg","plant_images/railroad-vine-3.jpeg"],
            "description": "Railroad vine, also known as beach morning glory, is a fast-growing vine that helps stabilize sand dunes. Its extensive root system prevents erosion, creating a more stable nesting area for Caretta carettas."
        },
        "Salt Grass": {
            "images": ["plant_images/salt-grass.jpg","plant_images/salt-grass-2.jpg","plant_images/salt-grass-3.jpeg"],
            "description": "Salt grass is a halophytic grass species that grows in saline environments. It plays a crucial role in coastal ecosystems by stabilizing soil and reducing erosion, thereby supporting the nesting success of Caretta carettas."
        },
        "Sea Grapes": {
            "images": ["plant_images/sea-grapes.jpeg","plant_images/sea-grapes-2.jpeg","plant_images/sea-grapes-3.jpeg"],
            "description": "Sea grapes are coastal plants that grow in sandy soils. They help prevent beach erosion and provide shade and protection for Caretta caretta nests."
        },
        "Sea Oats": {
            "images": ["plant_images/sea-oats.jpg","plant_images/sea-oats-2.jpeg","plant_images/sea-oats-3.jpg"],
            "description": "Sea oats are a grass species that grow on sand dunes. Their root systems help to stabilize the dunes, which is vital for providing a safe nesting habitat for Caretta carettas."
        },
        "Sea Purslane": {
            "images": ["plant_images/sea-purslane.jpg","plant_images/sea-purslane-2.jpg","plant_images/sea-purslane-3.jpg"],
            "description": "Sea purslane is a succulent plant found in coastal areas. It helps to stabilize sand and prevent erosion, providing a more secure environment for Caretta caretta nesting."
        },
        "Seaside Sandmat": {
            "images": ["plant_images/seaside-sandmat.jpg","plant_images/seaside-sandmat-2.jpg","plant_images/seaside-sandmat-3.jpg"],
            "description": "Seaside sandmat is a groundcover plant that grows in coastal regions. It helps stabilize sandy soils, reducing erosion and supporting the nesting habitats of Caretta carettas."
        }
    }


    def resize_image(image_path, output_size=(300, 200)):
        with Image.open(image_path) as img:
            resized_img = img.resize(output_size)
            return resized_img


    for plant_name, plant_data in plants_info.items():
        st.write(f"### {plant_name}")
        cols = st.columns(3)
        images = [resize_image(image) for image in plant_data["images"]]
        for col, image in zip(cols, images):
            with col:
                st.image(image)
        st.write(plant_data["description"])





    ########################## EDA ###################################

elif selected == 'EDA':
 
    col1, col2 = st.columns([1, 4])
     
    with col1:
        st.image("CarettaCarettaTurtle-Photoroom.png", width=165)
        
    with col2:
         
        st.markdown("<h1 style='margin-top: 40px;'>Exploratory Data Analysis</h1>", unsafe_allow_html=True)
         
        
       



    df_c = get_cleaned_data()
    df_raw = get_raw_data()
    st.header("Dataset Review")
    
    dataset_choice = st.radio("Choose Dataset Preview", ("Original Dataset", "Cleaned and Processed Dataset"))

    #Kullanıcının seçimine göre dataset'i gösterelim
    if dataset_choice == "Original Dataset":
            if st.button("Head"):
                st.write(df_raw.head())

            if st.button("Tail"):
                st.write(df_raw.tail())

            if st.button("Show All DataFrame"):
                st.dataframe(df_raw)

    elif dataset_choice == "Cleaned and Processed Dataset":
        if st.button("Head"):
            st.write(df_c.head())
        if st.button("Tail"):
            st.write(df_c.tail())
        if st.button("Show All DataFrame"):
            st.dataframe(df_c)

    st.header("Summary of the Dataset Properties")
    if st.button("Summary of original dataset"):
        st.write(summary_table(df_raw))
        cat_cols, num_cols, cat_but_car = grab_col_names(df_raw)
        df_cat_cols = pd.DataFrame({"Categorical Columns": cat_cols})
        df_num_cols = pd.DataFrame({"Numeric Columns": num_cols})
        df_car_cols = pd.DataFrame({"Numeric Columns": cat_but_car})
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(df_cat_cols)

        with col2:
            st.write(df_num_cols)

        with col3:
            st.write(df_car_cols)
    if st.button("Summary of cleaned dataset"):
        st.write(summary_table(df_c))
        cat_cols, num_cols, cat_but_car = grab_col_names(df_c)
        df_cat_cols = pd.DataFrame({"Categorical Columns": cat_cols})
        df_num_cols = pd.DataFrame({"Numeric Columns": num_cols})
        df_car_cols = pd.DataFrame({"Numeric Columns": cat_but_car})
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(df_cat_cols)

        with col2:
            st.write(df_num_cols)

        with col3:
            st.write(df_car_cols)

    st.header("Scatter Plot")
    cat_cols, num_cols, cat_but_car = grab_col_names(df_c)
    x_axis = st.selectbox('Please select X axis', num_cols)
    y_axis = st.selectbox('Please select Y axis', num_cols)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x=df_c[x_axis], y=df_c[y_axis], ax=ax, color="#4b7369")
    plt.title(f'Scatter Plot: {x_axis} vs. {y_axis}', fontsize=15)
    plt.xlabel(x_axis, fontsize=14)
    plt.ylabel(y_axis, fontsize=14)
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(fig)

    st.header("Histogram")
    selected_column = st.selectbox('Please select a categorical column', cat_cols)
    fig, ax = plt.subplots(figsize=(15, 6))
    sns.countplot(x=df_c[selected_column], ax=ax)
    plt.title(f'Histogram: {selected_column}', fontsize=15)
    plt.xlabel(selected_column, fontsize=17)
    plt.ylabel('Frequency', fontsize=17)
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(fig)

    st.header("Visualizing Missing Values")
    import missingno as msno
    st.set_option('deprecation.showPyplotGlobalUse', False)
    if st.button("Matrix Rep."):
        msno.matrix(df_raw)
        st.pyplot()
    if st.button("Bar Plot Rep."):
        msno.bar(df_raw)
        st.pyplot()

    st.header("Visualizing Outliers")

########### outlierları görme: ##############
    cat_cols, num_cols, cat_but_car = grab_col_names(df_raw)
    def outlier_thresholds(dataframe, col_name, q1=0.05, q3=0.95):
      quartile1 = dataframe[col_name].quantile(q1)
      quartile3 = dataframe[col_name].quantile(q3)
      IQR_range = quartile3 - quartile1
      up_lim = quartile3 + 1.5 * IQR_range
      low_lim = quartile1 - 1.5 * IQR_range
      return low_lim, up_lim

    for col in num_cols:
      low, up = outlier_thresholds(df_raw, col)

      def grab_outliers(dataframe, col_name, index=False):
        low, up = outlier_thresholds(dataframe, col_name)
        count = dataframe[(dataframe[col_name] < low) | (dataframe[col_name] > up)][col_name].shape[0]
        print(col_name.upper(), f" has {count} outliers.")
        if dataframe[(dataframe[col_name] < low) | (dataframe[col_name] > up)].shape[0] != 0:
          if dataframe[(dataframe[col_name] < low) | (dataframe[col_name] > up)].shape[0] > 10:
            print(dataframe[(dataframe[col_name] < low) | (dataframe[col_name] > up)].head(5))
          else:
            print(dataframe[(dataframe[col_name] < low) | (dataframe[col_name] > up)])
        if index:
          outlier_index = (dataframe[(dataframe[col_name] < low) | (dataframe[col_name] > up)]).index
          return outlier_index

    for col in num_cols:
      grab_outliers(df_raw, col, index=True)


    def check_outlier(dataframe, col_name):
        low, up = outlier_thresholds(dataframe, col_name)
        if dataframe[(dataframe[col_name] < low) | (dataframe[col_name] > up)].any(axis=None):
          return True
        else:
          return False
    for col in num_cols:
      print(col, check_outlier(df_raw, col))

    ################ outlierları baskılama (threshold ile): ################
    def replace_with_thresholds(dataframe, variable, q1=0.05, q3=0.90):
      low, up = outlier_thresholds(dataframe, variable, q1=0.05, q3=0.90)
      dataframe.loc[(dataframe[variable] < low), variable] = low
      dataframe.loc[(dataframe[variable] > up), variable] = up

    #outlier boxplot göstereceğimiz bir dropdown elementi:
    selected_column = st.selectbox('Please select a numerical column', num_cols)
    outliers = grab_outliers(df_raw, selected_column)
    fig = plt.figure(figsize=(10, 6))
    sns.boxplot(x=df_raw[selected_column], color="#4b7369")
    plt.title(f'Box Plot: {selected_column}', fontsize=15)
    plt.xlabel(selected_column, fontsize=14)
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(fig)
    st.header("Target Summary with Numeric Columns")

    col1, col2 = st.columns(2)

    selected_column = col1.selectbox('Please select a numerical column', num_cols, key='num_col_select')
    target_value = col2.text_input("Target", value="HS", disabled=True)


    def target_summary_with_num(dataframe, target, numerical_col):
        temp_df = dataframe.groupby(target).agg({numerical_col: "mean"})
        print(temp_df)
        fig, ax = plt.subplots(figsize=(15, 7))
        temp_df.plot(kind="bar", y=numerical_col, color="#4b7369", ax=ax)
        st.pyplot(fig)  #


    target_summary_with_num(df_raw, "HS", selected_column)

    st.header("Correlation Analysis")

    if st.checkbox("Correlation Matrix"):
        st.image("corr_map.png")
        # plt.figure(figsize=(10, 8))
        # sns.heatmap(df_raw[num_cols].corr(), annot=True, cmap='coolwarm',
        #            cbar_kws={'label': 'Korelasyon'})
        # plt.title('Korelasyon Matrisi (Heatmap)', fontsize=15)
        # plt.xticks(fontsize=12)
        # plt.yticks(fontsize=12)
        # st.pyplot()

########################## MODEL PREDICTION ###################################
elif selected == 'Model Prediction':
    col1, col2 = st.columns([2, 7])
    with col1:
        st.image("CarettaCarettaTurtle-Photoroom.png", width=185)
    with col2:
        
     st.markdown("<h1 style='margin-top: 40px;'>Model Prediction</h1>", unsafe_allow_html=True)
    st.markdown("""
            This section is made to help scientists who work in related projects. """)

    def load_model(modelfile):
        loaded_model = pickle.load(open(modelfile, 'rb'))
        return loaded_model

    model_option = st.selectbox(
        "Select Machine Learning Model:",
        ("Random Forest", "Decision Tree", "Linear Regression")
    )

    html_temp = """
            <div>
            <h1 style="color:BLACK;text-align:left;"> Enter New Data and Predict</h1>
            </div>
            """
    st.markdown(html_temp, unsafe_allow_html=True)
    with st.expander(" ℹ️ Information About the Features", expanded=False):
     st.write("""
            <ol>
            <li>ZoneID - Zone of nest locations</li>
            <li>Lat - Latitude of nest</li>
            <li>Long - Longitude of nest</li>
            <li>VegPresence - Presence/absence (1/0) of vegetation around nest</li>
            <li>VegType - Species of vegetation around nest</li>
            <li>RootPresence - Presence/absence (1/0) of roots around nest</li>
            <li>PlantRoot - Species of plant roots belonged to</li>
            <li>DistBarrier - Distance of nest to the barrier (m)</li>
            <li>DistHighWater - Distance of nest to the high water mark (m)</li>
            <li>TotalDist - Total width of beach (m)</li>
            <li>LocOnBeach - Location of nest on the beach</li>
            <li>Division - Which division nest was located on beach; beach was divided into thirds</li>
            <li>SurfaceDepth - Depth from surface to first egg (cm)</li>
            <li>BottomDepth - Depth from surface to bottom of nest chamber (cm)</li>
            <li>InternalDepth - Internal nest chamber depth (cm)</li>
            <li>CavityWidth - Width of the nest cavity, from wall to wall (cm)</li>
            <li>Hatched - Number of eggs hatched</li>
            <li>Unhatched - Number of eggs unhatched</li>
            <li>Developed_UH - Number of unhatched eggs with developed hatchling</li>
            <li>LivePip - Number of live pipped hatchlings</li>
            <li>DeadPip - Number of dead pipped hatchlings</li>
            <li>Yolkless - Number of yolkless eggs</li>
            <li>EncasedTotal - Number of total root-encased eggs</li>
            <li>DevEnc_UH - Number of root-encased unhatched eggs with developed hatchling</li>
            <li>H_Encased - Number of root-encased hatched eggs</li>
            <li>UH_Encased - Number of root-encased unhatched eggs</li>
            <li>InvadedTotal - Number of total root-invaded eggs</li>
            <li>H_Invaded - Number of root-invaded hatched eggs</li>
            <li>UH_Invaded - Number of root-invaded unhatched eggs</li>
            <li>Live - Number of live hatchlings</li>
            <li>Dead - Number of dead hatchlings</li>
            <li>Depredated - Depredation of nest (yes/no; 1/0)</li>
            <li>RootDamageProp - Proportion of root damaged eggs</li>
            <li>HS - Hatch success</li>
            <li>ES - Emergence success</li>
            <li>TotalEggs - Total eggs within the nest</li>
            </ol>
            """, unsafe_allow_html=True)

    st.subheader("Please enter information about the data 🐢🌿")

    col1, col2 = st.columns([2, 2])
    with col1:
        zone = st.number_input("ZoneID", 1, 10, value=5)
        lat = st.number_input("Lat", 1.0, 50.0, value=27.14)
        long = st.number_input("Long", -100.0, 0.0, value=-82.48)
        vegpresence = st.number_input("VegPresence ", 0, 1, value=1)
        vegtype_options = ['-railroad vine', '-sea oats', 'no', '-sea purslane', "-sea grapes"]
        vegtype = st.selectbox("VegType", options=vegtype_options)
        rootpres = st.number_input("RootPresence", 0, 1, value=1)
        roottype_options = ['Railroad Vine', 'Sea Oats', 'no']
        roottype = st.selectbox("PlantRoot", options=roottype_options)
        distbarr = st.number_input("DistBarrier", -20.0, 20.0, value=1.52)
        disthighw = st.number_input("DistHighWater", 0.0, 1000.0, value=14.05)
        totaldist = st.number_input("TotalDist", 0.0, 50.0, value=15.54)
        LocOnBeach = st.number_input("LocOnBeach ", 0.0, 5.0, value=1.02)
        division_options = ['M', 'U', 'L']
        Division = st.selectbox("Division", options=division_options)
        SurfaceDepth = st.number_input("SurfaceDepth ", 0.0, 1000.0, value=20.0)
        BottomDepth = st.number_input("BottomDepth", 0.0, 1000.0, value=33.0)
        InternalDepth = st.number_input("InternalDepth ", 0.0, 1000.0, value=20.0)
        CavityWidth = st.number_input("CavityWidth ", 0.0, 1000.0, value=23.0)
        Hatched = st.number_input("Hatched ", 0.0, 1000.0, value=45.0)
        Unhatched = st.number_input("Unhatched", 0.0, 1000.0, value=6.0)

    with col2:
        Developed_UH = st.number_input("Developed_UH ", 0.0, 1000.0, value=16.0)
        LivePip = st.number_input("LivePip", 0.0, 1000.0, value=1.0)
        DeadPip = st.number_input("DeadPip ", 0.0, 1000.0, value=5.0)
        Yolkless = st.number_input("Yolkless  ", 0.0, 1000.0, value=0.0)
        EncasedTotal = st.number_input("EncasedTotal  ", 0.0, 1000.0, value=0.0)
        DevEnc_UH = st.number_input("DevEnc_UH", 0.0, 1000.0, value=0.0)
        H_Encased = st.number_input("H_Encased  ", 0.0, 1000.0, value=0.0)
        UH_Encased = st.number_input("UH_Encased ", 0.0, 1000.0, value=3.0)
        InvadedTotal = st.number_input("InvadedTotal  ", 0.0, 1000.0, value=0.0)
        H_Invaded = st.number_input("H_Invaded", 0.0, 1000.0, value=0.0)
        UH_Invaded = st.number_input("UH_Invaded", 0.0, 1000.0, value=0.0)
        Live = st.number_input("Live", 0.0, 1000.0, value=3.0)
        Dead = st.number_input("Dead", 0.0, 1000.0, value=2.0)
        Depredated = st.number_input("Depredated  ", 0.0, 1000.0, value=0.0)
        RootDamageProp = st.number_input("RootDamageProp", 0.0, 1000.0, value=0.0125)
        ES = st.number_input("ES ", 0.0, 1000.0, value=95.0)
        TotalEggs = st.number_input("TotalEggs", 0.0, 1000.0, value=65.0)
        MultiVegNum = 0.0
        feature_list = [zone, lat, long, vegpresence, vegtype, rootpres, roottype, distbarr, disthighw,
                            totaldist, LocOnBeach, Division, SurfaceDepth, BottomDepth, InternalDepth,
                            CavityWidth, Hatched, Unhatched, Developed_UH, LivePip, DeadPip, Yolkless,
                            EncasedTotal, DevEnc_UH, H_Encased, UH_Encased, InvadedTotal, H_Invaded, UH_Invaded,
                            Live, Dead, Depredated, RootDamageProp, ES, TotalEggs, MultiVegNum
                            ]
        cat_cols, num_cols, cat_but_car = grab_col_names(df_c)

        from sklearn.preprocessing import RobustScaler, OneHotEncoder
        from sklearn.compose import ColumnTransformer

        columns = ['ZoneID', 'Lat', 'Long', 'VegPresence', 'VegType', 'RootPresence', 'PlantRoot', 'DistBarrier', 'DistHighWater', 'TotalDist',
                   'LocOnBeach', 'Divisions', 'SurfaceDepth', 'BottomDepth', 'InternalDepth', 'CavityWidth', 'Hatched', 'Unhatched', 'Developed_UH',
                   'LivePip', 'DeadPip', 'Yolkless', 'EncasedTotal', 'DevEnc_UH',
                   'H_Encased', 'UH_Encased', 'InvadedTotal', 'H_Invaded', 'UH_Invaded', 'Live', 'Dead', 'Depredated', 'RootDamageProp'
                   , 'ES', 'TotalEggs', 'MultiVegNum']

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', RobustScaler(), num_cols),
                ('cat', OneHotEncoder(), cat_cols)
            ])

        def one_hot_encoder(dataframe, categoric_cols, drop_first=False):
            dataframe = pd.get_dummies(dataframe, columns=categoric_cols, drop_first=drop_first, dtype=int)
            return dataframe

        expected_names = ['VegPresence', 'RootPresence', 'DistBarrier', 'DistHighWater', 'TotalDist', 'LocOnBeach', 'SurfaceDepth', 'BottomDepth', 'InternalDepth', 'CavityWidth', 'Hatched', 'Unhatched', 'Developed_UH', 'DeadPip', 'EncasedTotal', 'H_Encased', 'UH_Encased', 'Live', 'RootDamageProp', 'ES', 'TotalEggs', 'VegType_-christmas cactus', 'VegType_-crested saltbrush', 'VegType_-dune sunflower', 'VegType_-palm', 'VegType_-railroad vine', 'VegType_-salt grass', 'VegType_-sea grapes', 'VegType_-sea oats',
       'VegType_-sea purslane', 'VegType_-seaside spurge (sandmat)', 'VegType_-unknown', 'VegType_no', 'PlantRoot_Sea Oats', 'PlantRoot_no', 'Divisions_M', 'Divisions_U', 'ZoneID_4.0', 'ZoneID_5.0', 'ZoneID_6.0', 'ZoneID_7.0', 'ZoneID_8.0', 'ZoneID_9.0', 'Lat_27.13', 'Lat_27.14', 'Lat_27.15', 'Lat_27.16', 'Long_-82.49', 'Long_-82.48', 'Long_-82.47', 'LivePip_1.0', 'LivePip_2.0', 'LivePip_3.0', 'LivePip_7.0', 'Yolkless_1.0', 'Yolkless_2.0', 'DevEnc_UH_0.1956521739130435', 'DevEnc_UH_1.0',
       'DevEnc_UH_3.0', 'DevEnc_UH_6.0', 'InvadedTotal_1.0', 'InvadedTotal_2.0', 'InvadedTotal_3.0', 'InvadedTotal_5.0', 'InvadedTotal_6.0', 'InvadedTotal_10.0', 'InvadedTotal_19.0', 'H_Invaded_5.0', 'H_Invaded_6.0', 'H_Invaded_12.0', 'UH_Invaded_0.30434782608695654', 'UH_Invaded_1.0', 'UH_Invaded_2.0', 'UH_Invaded_3.0', 'UH_Invaded_7.0', 'UH_Invaded_10.0', 'Dead_1.0', 'Dead_2.0', 'Dead_3.0', 'Dead_4.0', 'Dead_5.0', 'Dead_7.0', 'MultiVegNum_1', 'MultiVegNum_2', 'MultiVegNum_3',
       'MultiVegNum_4']

        df_c = get_cleaned_data()
        cat_cols, num_cols, cat_but_car = grab_col_names(df_c)

        if st.button('Predict'):
            new_data = pd.DataFrame([feature_list], columns=columns)
            df_c = df_c.drop("HS",axis=1)
            df_c = pd.concat([df_c, new_data], ignore_index=True)
            df_c = one_hot_encoder(df_c, cat_cols, drop_first=True)
            scaler = RobustScaler()
            num_cols.remove('HS')
            df_c[num_cols] = scaler.fit_transform(df_c[num_cols])
            last_row = df_c.iloc[-1:]
            last_row = last_row.rename(columns=dict(zip(last_row.columns, expected_names)))
            if model_option == "Linear Regression":
                model = load_model("IC_lin_reg_model.pkl")
                prediction = model.predict(last_row)
                st.write('## Result')
                st.success(f"Hatching Success Prediction: {prediction.item()}")
            elif model_option == "Decision Tree":
                model = load_model("IC_cart_model.pkl")
                prediction = model.predict(last_row)
                st.write('## Result:')
                st.success(f"Hatching Success Prediction: {prediction.item()}")
            elif model_option == "Random Forest":
                model = load_model("IC_rf_model.pkl")
                prediction = model.predict(last_row)
                st.write('## Result:')
                st.success(f"Hatching Success Prediction: {prediction.item()}")

    hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """

    hide_menu_style = """
            <style>
            #MainMenu {visibility: hidden;}
            </style>
            """
    st.markdown(hide_menu_style, unsafe_allow_html=True)

########################## MODEL EVALUATION ###################################
elif selected == 'Model Evaluation':
    col1, col2 = st.columns([2, 7])
    with col1:
        st.image("CarettaCarettaTurtle-Photoroom.png", width=185)
    with col2:
         
        st.markdown("<h1 style='margin-top: 40px;'>Model Evaluation</h1>", unsafe_allow_html=True)
    st.markdown("""In this section, performance results of different models will be shown and visualized.""")

    st.markdown("""
            ### Performance Metrics""")
    col1, col2, col3 = st.columns([3,3, 3])
    with col1:
        st.markdown("""Root Mean Squared Error (RMSE)""")
        st.image("rmse.jpg", width=220)

    with col2:
        st.markdown("""Mean Squared Error (MSE)""")
        st.image("MSE.png", width=220)
    with col3:
        st.markdown("""R2 Score""")
        st.image("R2formula.png", width=220)

    model_option = st.selectbox(
        "Select machine learning model to see its results:",
        ("Random Forest", "Decision Tree", "Linear Regression", "SVR", "ElasticNet", "XGBRegressor")
    )

    if model_option == "Random Forest":
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            st.markdown("""Train Results:""")
            rf_res = {
                'Metric': ["MSE", "RMSE", "R2"],
                'Result': [0.01077, 0.1037, 0.9945]
            }
            rfres1 = pd.DataFrame(rf_res)
            st.write(rfres1)
        with col2:
            st.markdown("""Test Results:""")
            rf_res = {
                'Metric': ["MSE", "RMSE", "R2"],
                'Result': [0.0276, 0.1663, 0.9837]
            }
            rfres1 = pd.DataFrame(rf_res)
            st.write(rfres1)
        with col3:
            st.markdown("""5 fold CV + HP Tuning Results:""")
            rf_res = {
                'Metric': ["MSE", "RMSE", "R2"],
                'Result': [0.37484, 0.0560, 0.9581]
            }
            rfres1 = pd.DataFrame(rf_res)
            st.write(rfres1)

    if model_option == "Decision Tree":
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            st.markdown("""Train Results:""")
            dt_res = {
                'Metric': ["MSE", "RMSE", "R2"],
                'Result': ["2.045e-35", "4.522e-18", 1.0]
            }
            dtres1 = pd.DataFrame(dt_res)
            st.write(dtres1)
        with col2:
            st.markdown("""Test Results:""")
            dt_res = {
                'Metric': ["MSE", "RMSE", "R2"],
                'Result': [0.0084, 0.0924, 0.9949]
            }
            dtres1 = pd.DataFrame(dt_res)
            st.write(dtres1)
        with col3:
            st.markdown("""5 fold CV + HP Tuning Results:""")
            dt_res = {
                'Metric': ["MSE", "RMSE", "R2"],
                'Result': [0.35915, 0.15984, 0.87666]
            }
            dtres1 = pd.DataFrame(dt_res)
            st.write(dtres1)

    if model_option == "Linear Regression": #MSE VE RMSE DEĞERLERİNİ HENÜZ YOK.
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                st.markdown("""Train Results:""")
                dt_res = {
                    'Metric': ["MSE", "RMSE", "R2"],
                    'Result': [0, 0, 0.999]
                }
                dtres1 = pd.DataFrame(dt_res)
                st.write(dtres1)
            with col2:
                st.markdown("""Test Results:""")
                dt_res = {
                    'Metric': ["MSE", "RMSE", "R2"],
                    'Result': [0, 0, 1.0]
                }
                dtres1 = pd.DataFrame(dt_res)
                st.write(dtres1)
            with col3:
                st.markdown("""5 fold CV + HP Tuning Results:""")
                dt_res = {
                    'Metric': ["MSE", "RMSE", "R2"],
                    'Result': [0.3867, 0.48432, 0.7738]
                }
                dtres1 = pd.DataFrame(dt_res)
                st.write(dtres1)

    if model_option == "SVR":
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                st.markdown("""Train Results:""")
                dt_res = {
                    'Metric': ["MSE", "RMSE", "R2"],
                    'Result': [0.5799, 0.7615, 0.7069]
                }
                dtres1 = pd.DataFrame(dt_res)
                st.write(dtres1)
            with col2:
                st.markdown("""Test Results:""")
                dt_res = {
                    'Metric': ["MSE", "RMSE", "R2"],
                    'Result': [0.5454, 0.7385, 0.6802]
                }
                dtres1 = pd.DataFrame(dt_res)
                st.write(dtres1)
            with col3:
                st.markdown("""5 fold CV + HP Tuning Results:""")
                dt_res = {
                    'Metric': ["MSE", "RMSE", "R2"],
                    'Result': [0.1108, 0.0152, 0.9913]
                }
                dtres1 = pd.DataFrame(dt_res)
                st.write(dtres1)



    # Örnek veriler oluşturalım
    model_names = ['RANDOM FOREST', 'DECISION TREE', 'LINEAR REGRESSION', 'SVR']
    mse_scores = [0.05607,0.15984, 0.38674, 0.01528]
    rmse_scores = [0.37484, 0.35915, 0.48432, 0.11087]
    r2_scores = [0.95814, 0.87666, 0.77388, 0.99136]

    # DataFrame oluşturalım
    df_scores = pd.DataFrame({
        'Model': model_names,
        'MSE': mse_scores,
        'RMSE': rmse_scores,
        'R2': r2_scores
    })

    df_scores.set_index('Model', inplace=True)
    fig, ax = plt.subplots(figsize=(10, 6))

    bar_width = 0.2
    model_indices = range(len(df_scores.index))
    metrics = ['MSE', 'RMSE', 'R2']
    colors = [(102/255, 204/255, 102/255), (0/255, 102/255, 204/255), (255/255, 128/255, 192/255)]

    for i, metric in enumerate(metrics):
        bars = ax.bar([p + i * bar_width for p in model_indices],
               df_scores[metric],
               width=bar_width,
               color=colors[i],
               label=metric)

    ax.set_xlabel('Models')
    ax.set_ylabel('Scores')
    ax.set_title('Model Performances')
    ax.set_xticks([p + 1.5 * bar_width for p in model_indices])
    ax.set_xticklabels(df_scores.index)
    ax.legend()

    st.pyplot(fig)
##########################OUR TEAM ###################################
elif selected == 'Our Team':
    count = st_autorefresh(interval=refresh_rate * 1000, key="our-team-slideshow")
    st.markdown(
        """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        """,
        unsafe_allow_html=True
    )
    image_col, title_col = st.columns([1, 3])

    with image_col:
        st.image("CarettaCarettaTurtle-Photoroom.png", width=185)

    with title_col:
        st.markdown("<h1 style='text-align: left; margin-top: 50px;'>Our Team</h1>", unsafe_allow_html=True)


    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("our_team/mihriban-ozdemir.jpeg", width=200)
        st.markdown(
            "<b>Mihriban Özdemir</b>&nbsp;&nbsp;<a href='www.linkedin.com/in/mihribanozdemir' class='fa fa-linkedin'></a>&nbsp;<a href='https://github.com/mihribanozdemir' class='fa fa-github'></a>",
            unsafe_allow_html=True)

    with col2:
        st.image("our_team/ceren-kilic.jpeg", width=200)
        st.markdown(
            "<b>Ceren Kılıç</b>&nbsp;&nbsp;<a href='https://www.linkedin.com/in/cernkilic/' class='fa fa-linkedin'></a>&nbsp;<a href='https://github.com/cerenkilic' class='fa fa-github'></a>",
            unsafe_allow_html=True)

    with col3:
        st.image("our_team/turkan-risvan.jpeg", width=200)
        st.markdown(
            "<b>Türkan Rişvan</b>&nbsp;&nbsp;<a href='https://www.linkedin.com/in/t%C3%BCrkan-ri%C5%9Fvan/' class='fa fa-linkedin'></a>&nbsp;<a href='https://github.com/turkan-risvan' class='fa fa-github'></a>",
            unsafe_allow_html=True)

    our_team_slide_images = [
        "our-team-slideshow/1.jpg",
        "our-team-slideshow/2.jpg",
        "our-team-slideshow/3.jpg",
        "our-team-slideshow/4.jpg",
    ]

    slide_index = count % len(our_team_slide_images)
    slide_image = Image.open(our_team_slide_images[slide_index])
    slide_image = slide_image.resize((700, 400))
    st.image(slide_image, use_column_width=True)



