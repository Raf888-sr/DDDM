import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st
import plotly.express as px
import datetime as dt

# Set the Page Layout
st.set_page_config(layout="wide")

# Sidebar Widgets
st.sidebar.image("https://gbsn.org/wp-content/uploads/2020/07/AUB-logo.png")
options = st.sidebar.radio("Explore",["Introduction","By Country","By Category","By Age and Gender"],help="Use one of the following radio buttons to explore Nobel Prize Winners")
st.sidebar.write("    ")
st.sidebar.write("Sources:")
st.sidebar.markdown("""
    >* [Kaggle](https://www.kaggle.com/nobelfoundation/nobel-laureates)
    >* [Nobel Prize](https://www.nobelprize.org/)""")
st.sidebar.write("Done By:")
st.sidebar.markdown("> Rafic Srouji")

# get dataset
@st.cache
def get_data():
    # Loading the Data
    df = pd.read_csv("https://raw.githubusercontent.com/Raf888-sr/DDDM/main/nobel.csv")
    # Some Manipulations
    df['usa_born_winner'] = df['birth_country'] == 'United States of America'
    df['decade'] = (np.floor(df['year']/10)*10).astype(int)
    df['birth_date'] = pd.to_datetime(df['birth_date'])
    df = df.dropna(subset=['birth_date'])
    df['age'] = (df['year'] - df['birth_date'].dt.year).astype(int)
    return df
nobel = get_data()

min_year = int(nobel['year'].min())
max_year = int(nobel['year'].max())


if options == "Introduction":
    st.title("Nobel Prizes")

    col1,col2 = st.columns([4,1])

    with col1:
        st.markdown("""

        <div style="text-align: justify"><p> In this exercise we will dive into the Nobel prize Laureats dataset by the Nobel Prize Foundation. This dataset lists all prize winners from the start of the prize in 1901 till 2016.</p>
        <p> The Nobel prize is one of the most famous and prestigious intellectual awards. It is awarded annually for 6 different categories. From Stockholm, the Royal Swedish Academy of Sciences confers the prizes for physics, chemistry, and economics, the Karolinska Institute confers the prize for physiology or medicine, and the Swedish Academy confers the prize for literature. The Norwegian Nobel Committee based in Oslo confers the prize for peace.</p>

        <p>A person or organization awarded the Nobel Prize is called a Nobel Laureate. The word "laureate" refers to the laurel wreath (إكليل الغار) that was considered as "a trophy" in ancient greek, given to victors of competitions (image to the right).</p><br></div>

        """,unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <p><img style="float: right;margin:0.5px 20px 10px 20px; max-width: 200px;height: 220px;display: inline-block" src="Nobel_Prize.png"></p>""",unsafe_allow_html=True)
        #http://assets.stickpng.com/images/587516c119ef112e47c6964d.png


    st.markdown("--------")

    st.title("Brief History of Nobel Prize")
    st.video("https://www.youtube.com/watch?v=c0ou3X9SfB8&ab_channel=NationalGeographic")



if options == "By Country":

    st.title("Nobel Prize Winners By Country of Birth")
    st.subheader("This page inspects the winners of Nobel Prize based on their country of birth from 1901 until 2016. You can use the slider to filter the range of years.")

    slider_year = st.slider("Select Time Period",min_year,max_year,value=[min_year,max_year])

    df_selected = nobel[(nobel['year']>=int(slider_year[0])) & (nobel['year']<=int(slider_year[1]))]

    top_countries = df_selected['birth_country'].value_counts().head(10)
    country_names = top_countries.index

    df = df_selected.groupby(['birth_country'],as_index=False).size().sort_values(by='size',ascending=False).head(10)

    col3,col4 = st.columns([2,1])

    with col3:
        st.subheader(f"Bar Chart showing top 10 countries of birth of the prize winners from {slider_year[0]} to {slider_year[1]}")
        # Plotting a Bar Plot
        fig = px.bar(df,x="size",y="birth_country",orientation='h',color='birth_country',
                    width=800,height=600)

        # Updating Figure and Axes Layouts
        fig.update_layout(showlegend=False,xaxis=dict(title="Number of Prizes",showgrid=False),yaxis=dict(showgrid=False),
                         font = dict(
                                    family = "Open Sans",
                                    size = 15


                         ))
        # fig.update_xaxes(title="Number of Prizes")
        st.write(fig)

    with col4:
        st.subheader("Number of Prizes Per Country")
        st.write("   ")
        st.write("   ")
        st.write("   ")
        st.write("    ")
        st.write("    ")
        st.dataframe(top_countries,height=500)

    st.write("""Just looking at the first couple of prize winners, or Nobel laureates as they are also called, we already see a celebrity: Wilhelm Conrad Röntgen, the guy who discovered X-rays. And actually, we see that all of the winners in 1901 were guys that came from Europe.
     But that was back in 1901, looking at all winners in the dataset, from 1901 to 2016, USA clearly dominates over time.""")

    st.markdown("-------")

    st.subheader("US Laureats Domination")
    # proportions of USA born winners per decade
    prop_usa_winners= nobel.groupby('decade',as_index=False)['usa_born_winner'].mean()

    # Plotting a Line Plot
    fig2 = px.line(prop_usa_winners,x="decade",y="usa_born_winner",width=1200,height=700)
    # Updating axes layout
    fig2.update_layout(yaxis=dict(title="Percentage of US Born Winners",tickformat=".2%",showgrid=False),
        title="Percentage of US born Nobel Prize winners per decade",
        xaxis=dict(title="Decade",showgrid=False),
        font = dict(
            family = "Open Sans",
            size = 15
            ))
    st.write(fig2)

    st.write("USA began to dominate the Nobel Prize in the 1930s accounting for 25% of the total prizes during this decade. It continued ever since until reaching a new peak during the 2000s.")


elif options == "By Category":
    st.title("Nobel Prize Winners by Category")
    st.markdown("""
    <h3 style: "text-align: justify">
        This page inspects Nobel Prize winners according to the field. Since 1901, the Nobel Prize has been awarded in the fields of physics, chemistry, physiology or medicine, literature and peace,
         while a memorial prize in economic sciences was added in 1968.</h3>""",unsafe_allow_html=True)
    st.subheader("Use the slider and selectbox to filter by year and category respectively.")

    col5,col6 = st.columns([1,1])

    with col5:
        year = st.slider("Select Time Period",int(min_year),int(max_year),value=[min_year,max_year])

        df_field = nobel[(nobel['year']>=int(year[0])) & (nobel['year']<=int(year[1]))]
        # grouped = df_field.groupby('category',as_index=False).size()

    with col6:
        selected_field=st.selectbox("Select Category",nobel['category'].unique())

    st.subheader("Nobel Prize Winners By Category")

    col7,col8 = st.columns([1,1])

    with col7:
        # Number of Chemsitry Prizes
        if 'Chemistry' in df_field['category'].unique():
            st.write(f"""
                <div>
                    <div style="display:inline-block;vertical-align:center;">
                    <img src="https://www.svgrepo.com/show/58697/chemistry.svg" width=100/>
                    </div>
                    <div style="display:inline-block;vertical-align:center;font-size:50px;padding-left: 30px;margin-left:1em";>
                    Chemistry
                    </div>
                    <div style="display:inline-block;vertical-align:center;font-size:50px;padding-left: 30px;margin-left:1em";>
                    {df_field['category'].value_counts()['Chemistry']}
                    </div>""", unsafe_allow_html=True)
        else:
            st.write(f"""
                <div>
                    <div style="display:inline-block;vertical-align:center;">
                    <img src="https://www.svgrepo.com/show/58697/chemistry.svg" width=100/>
                    </div>
                    <div style="display:inline-block;vertical-align:center;font-size:50px;padding-left: 30px;margin-left:1em";>
                    Chemistry
                    </div>
                    <div style="display:inline-block;vertical-align:center;font-size:50px;padding-left: 30px;margin-left:1em";>
                    0
                    </div>""", unsafe_allow_html=True)
        st.write("""
        """)
        # Number of Physics Prizes
        if 'Physics' in df_field['category'].unique():
            st.write(f"""
                <div>
                    <div style="display:inline-block;vertical-align:center;">
                    <img src="https://www.svgrepo.com/show/108617/physics.svg" width=100/>
                    </div>
                    <div style="display:inline-block;vertical-align:center;font-size:50px;padding-left: 30px;margin-left:1em";>
                    Physics
                    </div>
                    <div style="display:inline-block;vertical-align:center;font-size:50px;padding-left: 30px;margin-left:2.1em";>
                    {df_field['category'].value_counts()['Physics']}
                    </div>
                    """,unsafe_allow_html=True)
        else:
            st.write(f"""
                <div>
                    <div style="display:inline-block;vertical-align:center;">
                    <img src="https://www.svgrepo.com/show/108617/physics.svg" width=100/>
                    </div>
                    <div style="display:inline-block;vertical-align:center;font-size:50px;padding-left: 30px;margin-left:1em";>
                    Physics
                    </div>
                    <div style="display:inline-block;vertical-align:center;font-size:50px;padding-left: 30px;margin-left:2.1em";>
                    0
                    </div>
                    """,unsafe_allow_html=True)
        st.write("""

        """)

            # Number of Medicine Prizes
        if 'Medicine' in df_field['category'].unique():
            st.write(f"""
                    <div>
                        <div style="display:inline-block;vertical-align:center;">
                        <img src="https://www.svgrepo.com/show/22871/medicine.svg" width=100/>
                        </div>
                        <div style="display:inline-block;vertical-align:center;font-size:50px;padding-left: 30px;margin-left:1em";>
                        Medicine
                        </div>
                        <div style="display:inline-block;vertical-align:center;font-size:50px;padding-left: 30px;margin-left:1.5em";>
                        {df_field['category'].value_counts()['Medicine']}
                        </div>
                        """,unsafe_allow_html=True)
        else:
            st.write(f"""
                    <div>
                        <div style="display:inline-block;vertical-align:center;">
                        <img src="https://www.svgrepo.com/show/22871/medicine.svg" width=100/>
                        </div>
                        <div style="display:inline-block;vertical-align:center;font-size:50px;padding-left: 30px;margin-left:1em";>
                        Medicine
                        </div>
                        <div style="display:inline-block;vertical-align:center;font-size:50px;padding-left: 30px;margin-left:1.5em";>
                        0
                        </div>
                        """,unsafe_allow_html=True)


    with col8:
            # Number of Peace Prizes
            if 'Peace' in df_field['category'].unique():
                st.write(f"""
                        <div>
                            <div style="display:inline-block;vertical-align:center;">
                            <img src="https://www.svgrepo.com/show/381729/peace.svg" width=100/>
                            </div>
                            <div style="display:inline-block;vertical-align:center;font-size:50px;padding-left: 30px;margin-left:1em";>
                            Peace
                            </div>
                            <div style="display:inline-block;vertical-align:center;font-size:50px;padding-left: 30px;margin-left:2.1em";>
                            {df_field['category'].value_counts()['Medicine']}
                            </div>
                            """,unsafe_allow_html=True)
            else:
                st.write(f"""
                        <div>
                            <div style="display:inline-block;vertical-align:center;">
                            <img src="https://www.svgrepo.com/show/381729/peace.svg" width=100/>
                            </div>
                            <div style="display:inline-block;vertical-align:center;font-size:50px;padding-left: 30px;margin-left:1em";>
                            Peace
                            </div>
                            <div style="display:inline-block;vertical-align:center;font-size:50px;padding-left: 30px;margin-left:2.1em";>
                            0
                            </div>
                            """,unsafe_allow_html=True)

            st.write("""
            """)
            # Number of Literature Prizes
            if 'Literature' in df_field['category'].unique():
                st.write(f"""
                        <div>
                            <div style="display:inline-block;vertical-align:center;">
                            <img src="https://www.svgrepo.com/show/177930/literature-paper.svg" width=100/>
                            </div>
                            <div style="display:inline-block;vertical-align:center;font-size:50px;padding-left: 30px;margin-left:1em";>
                            Literature
                            </div>
                            <div style="display:inline-block;vertical-align:center;font-size:50px;padding-left: 30px;margin-left:0.5em";>
                            {df_field['category'].value_counts()['Literature']}
                            </div>
                            """,unsafe_allow_html=True)
            else:
                st.write(f"""
                        <div>
                            <div style="display:inline-block;vertical-align:center;">
                            <img src="https://www.svgrepo.com/show/177930/literature-paper.svg" width=100/>
                            </div>
                            <div style="display:inline-block;vertical-align:center;font-size:50px;padding-left: 30px;margin-left:1em";>
                            Literature
                            </div>
                            <div style="display:inline-block;vertical-align:center;font-size:50px;padding-left: 30px;margin-left:0.5em";>
                            0
                            </div>
                            """,unsafe_allow_html=True)
            st.write("""
            """)
            # Number of Economics prizes

            if 'Economics' in df_field['category'].unique():
                st.write(f"""
                        <div>
                            <div style="display:inline-block;vertical-align:center;">
                            <img src="https://www.svgrepo.com/show/11834/economy.svg" width=100/>
                            </div>
                            <div style="display:inline-block;vertical-align:center;font-size:50px;padding-left: 30px;margin-left:1em";>
                            Economics
                            </div>
                            <div style="display:inline-block;vertical-align:center;font-size:50px;padding-left: 30px;margin-left:0.1em";>
                            {df_field['category'].value_counts()['Economics']}
                            </div>
                            """,unsafe_allow_html=True)
            else:
                st.write(f"""
                        <div>
                            <div style="display:inline-block;vertical-align:center;">
                            <img src="https://www.svgrepo.com/show/11834/economy.svg" width=100/>
                            </div>
                            <div style="display:inline-block;vertical-align:center;font-size:50px;padding-left: 30px;margin-left:1em";>
                            Economics
                            </div>
                            <div style="display:inline-block;vertical-align:center;font-size:50px;padding-left: 30px;margin-left:0.1em";>
                            0
                            </div>
                            """,unsafe_allow_html=True)

    st.markdown('---------')

    # Filtering based on the user selection
    field_df = nobel[(nobel['year']>=year[0]) & (nobel['year']<=year[1]) & (nobel['category']==selected_field)]

    field_by_country = field_df.groupby('birth_country',as_index=False).size().sort_values('size',ascending=False).head(10)

    st.subheader(f"Number of Winners in {selected_field} by Birth Country")

    fig3 = px.bar(field_by_country,x="birth_country",y="size",template='plotly_white',
                    color_discrete_sequence=px.colors.qualitative.Set1,width=1500,height=800)
    fig3.update_layout(xaxis=dict(title="Country"),yaxis=dict(title="Number of Prizes"),
                        font = dict(family="Open Sans",size=15))
    st.write(fig3)

# By Age and Gender
elif options == "By Age and Gender":

    st.title("Nobel Prize By Age Group and Gender")
    st.subheader("This page inspects the distribution of the age of Nobel Prize Winners based on their gender. Use the slider and selection box to filter by age and gender respectively.")
    min_age = int(nobel['age'].min())
    max_age = int(nobel['age'].max())


    col9,col10 = st.columns([1,1])

    with col9:
        age_slider = st.slider("Select Age Range:",min_age,max_age,value=[min_age,max_age])

    with col10:
        gender_selection = st.selectbox("Select Gender:",['Female','Male','Both'])

    age_gender_df = nobel[(nobel['age']>=int(age_slider[0])) & (nobel['age']<=int(age_slider[1]))]

    if gender_selection != "Both":
        st.subheader(f"Age Distribution For {gender_selection} Nobel Prize Winners")
        age_gender_df = nobel[nobel['sex']==gender_selection]
        fig4 = px.histogram(age_gender_df,x="age",nbins=20,width=1500,height=600,template='simple_white')
        fig4.update_layout(yaxis=dict(title="Number of Prizes"),xaxis=dict(title="Age"), font = dict(size=15,family="Open Sans"))
        st.write(fig4)
    else:
        st.subheader("Age Distribution For Female and Male Nobel Prize Winners")
        fig4 = px.histogram(age_gender_df,x="age",color='sex',nbins=20,width=1500,height=600,template='simple_white')
        fig4.update_layout(yaxis=dict(title="Number of Prizes"),xaxis=dict(title="Age"), font = dict(size=15,family="Open Sans"))
        st.write(fig4)


    st.markdown('--------')
    st.subheader("Number of Female and Male Nobel Prize Based on Age Range")
    col11,col12 = st.columns([1,1])

    age_gender_df = nobel[(nobel['age']>=int(age_slider[0])) & (nobel['age']<=int(age_slider[1]))]

    with col11:
            st.write(f"""
                    <div>
                        <div style="display:inline-block;vertical-align:center;">
                        <img src="https://www.svgrepo.com/show/327761/female.svg" width=100/>
                        </div>
                        <div style="display:inline-block;vertical-align:center;font-size:50px;padding-left: 30px;margin-left:1em";>
                        Females
                        </div>
                        <div style="display:inline-block;vertical-align:center;font-size:50px;padding-left: 30px;margin-left:0.1em";>
                        {age_gender_df['sex'].value_counts()['Female']}
                        </div>
                        """,unsafe_allow_html=True)
    with col12:
        st.write(f"""
                <div>
                    <div style="display:inline-block;vertical-align:center;">
                    <img src="https://www.svgrepo.com/show/391004/male.svg" width=100/>
                    </div>
                    <div style="display:inline-block;vertical-align:center;font-size:50px;padding-left: 30px;margin-left:1em";>
                    Males
                    </div>
                    <div style="display:inline-block;vertical-align:center;font-size:50px;padding-left: 30px;margin-left:0.1em";>
                    {age_gender_df['sex'].value_counts()['Male']}
                    </div>
                    """,unsafe_allow_html=True)
    st.write("    ")
    st.write("It seems men have strongly dominated this precious award regardless of the age range. Of all 883 Nobel Laureats, only 49 women have won the prize.")
    st.markdown("-------")
    col13,col14 = st.columns((1,1))

    with col13:
            with st.expander("Youngest Nobel Laureate"):

                st.write("""
                <img style ="padding-right: 10px" src="https://cdn.britannica.com/71/179071-050-CF95982C/Malala-Yousafzai-2013.jpg?w=400&h=300&c=crop" align="left" width = 300 height =400>
                <p style = "text-align:justify"><strong>Malala Yousafzai</strong>, (born July 12, 1997, Mingora, Swat valley, Pakistan), Pakistani activist who, while a teenager, spoke out publicly against the prohibition on the education of girls that was imposed by the Tehrik-e-Taliban Pakistan (TTP; sometimes called Pakistani Taliban). She gained global attention when she survived an assassination attempt at age 15. In 2014 Yousafzai and Kailash Satyarthi were jointly awarded the Nobel Prize for Peace in recognition of their efforts on behalf of children’s rights.</p>
                <a href = "https://www.britannica.com/biography/Malala-Yousafzai">Click to read more</a>
                """,unsafe_allow_html=True)

    with col14:
            with st.expander("Oldest Nobel Laureate"):
                st.write("""
                <img style ="padding-right: 10px" src="https://nationalmedals.org/wp-content/uploads/2020/07/Leonid-Hurwicz-1.jpg" align="left" width = 300 height =400>
                <p style = "text-align:justify"><strong>Leonid Hurwicz</strong>, (born Aug. 21, 1917, Moscow, Russia—died June 24, 2008, Minneapolis, Minn., U.S.),
                 Russian-born American economist who, with Eric S. Maskin and Roger B. Myerson, received a share of the 2007 Nobel Prize for
                 Economics for his formulation of mechanism design theory, a microeconomic model of resource allocation that attempts to produce
                  the best outcome for market participants under nonideal conditions.</p>
                <a href = "https://www.britannica.com/biography/Leonid-Hurwicz">Click to read more</a>
                """,unsafe_allow_html=True)
