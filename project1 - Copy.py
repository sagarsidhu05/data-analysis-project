
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
merged_data=pd.read_csv('cleaned_olympic_data.csv')


def get_medal_counts(country):
            medal_counts = merged_data[merged_data['Team'] == country].groupby('Team').agg({'Gold': 'sum', 'Silver': 'sum', 'Bronze': 'sum'}).reset_index()
            if not medal_counts.empty:
                  return medal_counts.iloc[0]
            else:
                  return{'Team': country, 'Gold': 0, 'Silver': 0, 'Bronze': 0}
 
    



with st.sidebar:
   option=option_menu('Menu',("Home","Dataset","Graphs","Feedback & Queries","About us"),
   icons=["house","table","bar-chart","chat","people"],menu_icon="cast",default_index=0)
if option=="Home":

      st.title("Olympic Data Analysis 🏅")
      st.subheader("Dive deep into the history of the Olympic Games!")

      # Add an Olympic imag
      st.image("oly.png", caption="The Olympic Games", use_column_width=True)

      # Introduction
      st.markdown("""
      Welcome to the **Olympic Data Analysis** web application! This platform allows you to explore and analyze data from the Olympic Games, offering insights into athletes' performances, country statistics, historical trends, and more.

      ### Features:
      - **Athlete Performance**: Analyze individual athlete's achievements across different Olympic events.
      - **Country Statistics**: Explore the medal counts, participation, and performance trends by country.
      - **Historical Trends**: Discover how the Olympic Games have evolved over time in terms of sports, participation, and global reach.
      - **Medal Predictions**: Use machine learning models to predict future medal outcomes based on past performances.
      - **Interactive Visualizations**: Engage with dynamic charts and graphs to gain insights into the Olympic data.

      ### A Brief History of the Olympic Games:
      The **Olympic Games** have a long and storied history, dating back to ancient Greece in 776 BC, where they were held in Olympia. The modern Olympic Games were revived in 1896 by Baron Pierre de Coubertin and have since become a global event, bringing together athletes from all over the world. 

      The Games are divided into two main events: the **Summer Olympics** and the **Winter Olympics**, each held every four years. Over the decades, the Olympics have grown in size and significance, reflecting changes in global politics, technology, and culture.

      ### Get Started:
      Use the sidebar to navigate through different sections of the analysis. Choose the area that interests you the most, and start exploring!

      #### Data Sources:
      The data used in this application is sourced from reliable Olympic records and databases, ensuring accuracy and comprehensiveness.

      #### About the Developer:
      This application is developed by a passionate data scientist and machine learning enthusiast, aiming to bring the fascinating world of Olympic data to a wider audience.

      

      ---
      """)


      
         
elif option=="Dataset":
      st.title("**Dataset Overview**")
      df=pd.read_csv("cleaned_olympic_data.csv")
      st.dataframe(df)
      st.write("Tap to [link](https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results) for more info.")
      
      country = st.selectbox("Select a Country:", options=df['Team'].unique())
      year = st.selectbox("Select a Year:", options=sorted(df['Year'].unique()))
      filtered_data = df[(df['Team'] == country) & (df['Year'] == year)]
      st.dataframe(filtered_data)
      st.cache_data
      def convert_df_to_csv(data):


            return data.to_csv(index=False).encode('utf-8')
      csv = convert_df_to_csv(filtered_data)
      st.download_button("Download Dataset as CSV", csv, "olympic_data.csv", "text/csv", key='download-csv')
      




           
elif option=="Graphs":
      a=st.sidebar.selectbox("Select Analysis",options=["Country wise Analysis", "Overall Analysis", "Medal Leadboard", "Athlete wise Analysis"])
      if a=="Country wise Analysis":
            st.title('OLYMPIC GAME DATA ANALYSIS')



            b=selected_country = st.selectbox('Select a country', options=["United States","Germany",'Great Britain','France',"Italy",'China','Sweden','Japan','Norway','Australia','Russia','Canada','Hungary','Finland','Netherlands','Switzerland','South Korea','Austria','Poland','Romania','Cuba','Bulgaria','Denmark','Spain','Belgium','Brazil','Ukraine','New Zealand','Grecce','Kenya','Belarus','Turkey','Czeck Republic','South Africa','Jamaica','Kazakhstan','Argentina','Iran','Mexico','Ethiopia','North Korea','Croatia','Slovenia','Azerbaijan','Estonia','Slovaika','Georgia','Ireland','Indonesia','Uzbekistan','Egypt','India','Thailand','Colombia','Lativa','Mongolia','Portugal','Nigeria','Lithuania','Morocco','Serbia','Venezuela','Algeria','Bahamas','Tunisia','Philippines','Malaysia','Chile','Israel','Dominican Republic','Uganda','Pakistan','Puerto Rico','Hong Kong','Zimbabwe'])

            


           

# Display medal counts for the selected country
            st.header(f'Medal Counts for {selected_country}')
            medal_counts = get_medal_counts(selected_country)
            st.write(f"Gold: {medal_counts['Gold']}")
            st.write(f"Silver: {medal_counts['Silver']}")
            st.write(f"Bronze: {medal_counts['Bronze']}")

            df = pd.read_csv('cleaned_olympic_data.csv')


                  # Filter data for China
            china_df = df[df['Team'] == b]

            # 1. Medal Count Over Years
            medal_count = china_df[china_df['Medal'] != 'Unknown'].groupby('Year')['Medal'].count().reset_index()
            fig1 = px.line(medal_count, x='Year', y='Medal', title=f"{b}: Medal Count Over Years",
                        labels={'Medal': 'Number of Medals', 'Year': 'Year'},
                        line_shape='linear', render_mode='svg')
            # pio.write_html(fig1, file='china_medal_count_over_years.html')
            print("Created line chart of",b,"'s medal count over years")
            st.plotly_chart(fig1)

            # 2. Medal Distribution
            medal_distribution = china_df[china_df['Medal'] != 'Unknown']['Medal'].value_counts()
            fig2 = px.pie(values=medal_distribution.values, names=medal_distribution.index, 
                        title=f"{b}: Medal Distribution",
                        color=medal_distribution.index,
                        color_discrete_map={'Gold': '#FFD700', 'Silver': '#C0C0C0', 'Bronze': '#CD7F32'})
            # pio.write_html(fig2, file='china_medal_distribution.html')
            print("Created pie chart of" ,b,"'s medal distribution")
            st.plotly_chart(fig2)

            # 3. Top 10 Sports by Medal Count
            top_sports = china_df[china_df['Medal'] != 'Unknown'].groupby('Sport')['Medal'].count().sort_values(ascending=False).head(10)
            fig3 = px.bar(top_sports, x=top_sports.index, y='Medal', 
                        title=f"{b}: Top 10 Sports by Medal Count",
                        labels={'Medal': 'Number of Medals', 'index': 'Sport'},
                        color='Medal',
                        color_continuous_scale='Viridis')
            # pio.write_html(fig3, file='china_top_10_sports.html')
            print("Created bar chart of",b,"'s top 10 sports by medal count")
            st.plotly_chart(fig3)

            # 4. Participants Over Years
            participants = china_df.groupby('Year').size().reset_index(name='Count')
            fig4 = px.line(participants, x='Year', y='Count', 
                        title=f'{b}: Number of Participants Over Years',
                        labels={'Count': 'Number of Participants', 'Year': 'Year'},
                        line_shape='linear', render_mode='svg')
            pio.write_html(fig4, file='china_participants_over_years.html')
            print("Created line chart of",b,"'s participants over years")
            st.plotly_chart(fig4)

            # 5. Age Distribution of Medalists
            medalists = china_df[china_df['Medal'] != 'Unknown']
            fig5 = px.histogram(medalists, x='Age', color='Medal', 
                              title=f'{b}: Age Distribution of Medalists',
                              labels={'Age': 'Age', 'count': 'Number of Medals'},
                              color_discrete_map={'Gold': '#FFD700', 'Silver': '#C0C0C0', 'Bronze': '#CD7F32'},
                              nbins=20)
            pio.write_html(fig5, file='china_medalists_age_distribution.html')
            print("Created histogram of",b,"'s medalists age distribution")
            st.plotly_chart(fig5)

                 
                 

      elif a=="Overall Analysis":
            st.title("Overall Analysis")

            file_path = 'athlete_events.csv'
            data = pd.read_csv(file_path)

            # 1. Participation Trend Over Years
            participation_trend = data.groupby('Year')['ID'].nunique().reset_index(name='Participants')
            fig1 = px.line(participation_trend, x='Year', y='Participants', title='Number of Participants Over Years')
            fig1.write_html("participation_trend.html")

            st.plotly_chart(fig1)


            # 2. Medal Distribution by Country (Top 20)
            medal_distribution = data[data['Medal'].notna()].groupby('NOC')['Medal'].count().sort_values(ascending=False).head(20).reset_index()
            fig2 = px.bar(medal_distribution, x='NOC', y='Medal', title='Medal Distribution by Country (Top 20)')
            fig2.write_html("medal_distribution.html")
            st.plotly_chart(fig2)


            # 3. Top 10 Sports by Number of Events
            top_sports = data.groupby('Sport')['Event'].nunique().sort_values(ascending=False).head(10).reset_index()
            fig3 = px.bar(top_sports, x='Sport', y='Event', title='Top 10 Sports by Number of Events')
            fig3.write_html("top_sports.html")
            st.plotly_chart(fig3)


            # 4. Gender Distribution Over Time
            gender_distribution = data.groupby(['Year', 'Sex'])['ID'].nunique().unstack().reset_index()
            gender_distribution['Total'] = gender_distribution['F'] + gender_distribution['M']
            gender_distribution['Female_Percentage'] = gender_distribution['F'] / gender_distribution['Total'] * 100
            gender_distribution['Male_Percentage'] = gender_distribution['M'] / gender_distribution['Total'] * 100

            fig4 = go.Figure()
            fig4.add_trace(go.Scatter(x=gender_distribution['Year'], y=gender_distribution['Female_Percentage'], name='Female', mode='lines'))
            fig4.add_trace(go.Scatter(x=gender_distribution['Year'], y=gender_distribution['Male_Percentage'], name='Male', mode='lines'))
            fig4.update_layout(title='Gender Distribution Over Time', yaxis_title='Percentage', xaxis_title='Year')
            fig4.write_html("gender_distribution.html")
            st.plotly_chart(fig4)

                  
      elif a=="Medal Leadboard":
            st.title("Medal leaderboard")
            data = pd.read_csv('athlete_events.csv')

            # Create a medal count dataframe
            medal_counts = data[data['Medal'].notna()].groupby(['NOC', 'Medal'])['Medal'].count().unstack(fill_value=0).reset_index()
            medal_counts['Total'] = medal_counts['Gold'] + medal_counts['Silver'] + medal_counts['Bronze']
            medal_counts = medal_counts.sort_values('Total', ascending=False).reset_index(drop=True)

            # Select top 15 countries
            top_15 = medal_counts.head(15)
            top_15.head(15)

            # Create a stacked bar chart
            fig = px.bar(top_15, x='NOC', y=['Gold', 'Silver', 'Bronze'],
                        title='Olympic Medal Leaderboard (Top 15 Countries)',
                        labels={'value': 'Number of Medals', 'NOC': 'Country'},
                        color_discrete_map={'Gold': '#FFD700', 'Silver': '#C0C0C0', 'Bronze': '#CD7F32'})
            st.plotly_chart(fig)
            fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})

            # Add total medal count as text on the bars
            for i, row in top_15.iterrows():
                  fig.add_annotation(x=row['NOC'], y=row['Total'],
                                    text=str(row['Total']),
                                    font=dict(family="Arial", size=12, color="black"),
                                    showarrow=False, yshift=10)

            # # Save the figure as an HTML file
            # fig.write_html("medal_leaderboard.html")
      
      elif a=="Athlete wise Analysis":
            st.title("Athlete wise Analysis")
            data = pd.read_csv('athlete_events.csv')

            # Create a dataframe for athletes with medals
            athlete_medals = data[data['Medal'].notna()].groupby('Name')['Medal'].count().reset_index()
            athlete_medals = athlete_medals.sort_values('Medal', ascending=False).head(15)
            athlete_medals.head(15)

            # Create a bar chart for top athletes by number of medals
            fig = px.bar(athlete_medals, x='Name', y='Medal',
                        title='Top 15 Athletes by Number of Medals',
                        labels={'Medal': 'Number of Medals', 'Name': 'Athlete'},
                        color='Medal',
                        color_continuous_scale=px.colors.sequential.Plasma)
            st.plotly_chart(fig)

            fig.update_layout(xaxis={'categoryorder':'total descending'})
elif option=="Feedback & Queries"  :
      st.title('Feedback & Queries')  
      st.write("### Please provide your feedback.")
      st.write("We value your feedback and suggestion to improve our platform. ") 
      with st.form(key="feedback_form") :
            name=st.text_input("Name") 
            email=st.text_input("Email")
            feedback_type=st.selectbox("Feedback Type",["Suggestion","Issue","General Feedback"]) 
            feedback=st.text_area("Your Feedback")

            st.write("### Did you find our platform Helpful?")
            helpful =st.radio("",['Yes 👍','No 👎'],index=0)
            if helpful=='Yes 👍':
                  st.markdown('<p style="color:green; font- weight:bold;</p>', unsafe_allow_html=True)
            elif helpful=='No 👎':
                  st.markdown('<p style="color:red; font-weight:bold;"></p>', unsafe_allow_html=True)

            submit_button=st.form_submit_button(label="Submit")

            if submit_button:
                  st.success("Thank you for your Feedback!")
                              
    
elif option=="About us":
      st.title("About us")
      st.markdown("""
      This web application was developed by Sagar Sidhu. This platform was created with a passion for combining data science, sports, and history to bring the fascinating world of the Olympics closer to you.

Our mission is to provide a comprehensive and interactive way to explore the achievements of athletes, the history of countries' performances, and the evolution of one of the world's most celebrated events. From understanding medal trends to exploring athlete insights, this application is your one-stop destination for everything Olympics!
                  
### Why Choose Us?
- **Interactive Visualizations**: Dive into the data through dynamic and visually appealing graphs and charts.
- **Data Accuracy**: All insights are powered by robust data sourced from reliable Olympic databases.
- **User-Centric Design**: Whether you're a sports enthusiast, researcher, or casual browser, our platform caters to all levels of interest and expertise.
- **Passion for Excellence**: Just like the Olympic spirit, we strive for excellence in bringing engaging and meaningful content to our users.
                  
### Behind the Project:
This project is the brainchild of a data science enthusiast with a keen interest in making data accessible and insightful. Combining a love for sports and analytics, the application was built using cutting-edge tools like Python, Streamlit, and Plotly to ensure a seamless user experience.

### **🌐 Connect with Me**:

- **GitHub**:sagarsidhu05
- **Email**:sagarsidhu33321@gmail.com
- **Phone**: +91 9779017505






 ### **🎊Thank You for visiting!🎊**
                  
      

""")




      
    
