#!/usr/bin/env python
# coding: utf-8

# 
# <b>
# 
# <p>
# <center>
# <font size="5">
# Project for Primary School Enrollment (DATS 6103)
# </font>
# </center>
# </p>
# 
# <p>
# <center>
# <font size="4">
# Project 2
# </font>
# </center>
# </p>
# 
# <p>
# <center>
# <font size="3">
# Data Source:The World Bank: https://data.worldbank.org/indicator/SE.PRM.ENRR
# </font>
# </center>
# </p>
# 
# <p>
# <center>
# <font size="3">
# Author: Xi Zhang
# </font>
# </center>
# </p>
# 
# </b>

# # 1 Overview
# 
# ![title](header.jpg)
# 
# Education as the ladder of human progress is an essential part of human civilization. Education affects every aspect of human society and is also influenced by it. As a beneficiary of education, I am very fortunate to be able to delve into what can affect education in this class. I hope we can see the direction of what can make education better.
# In this project, I'm going to show you an overview of primary school enrollment worldwide; GDP and enrollment rates interact; Gender differences in enrollment and the relationship between education spending and enrollment.

# ## 1.1 Data Preparing
# This part is data preparation and data cleaning: libraries import, authorization of tools, adjust DataFrame, fill the missing data and finally get the target data.

# In[57]:


#Import libraries
import math
import pandas as pd
import matplotlib.pyplot as plt
import plotly
import plotly.plotly as py
import plotly.graph_objs as go


# In[58]:


#Sign up for ploty
py.sign_in('nimazahadat','ipOFnMtBFXmO1MBguAN2')


# In[59]:


#Ignore the warnings below.
import warnings
warnings.filterwarnings('ignore')


# In[60]:


plotly.offline.init_notebook_mode()


# In[61]:


#Read raw data
enroll = pd.read_excel("overall.xls", header=3, index_col=0)
enroll.head()


# In[62]:


#Fill missing data to row mean value
enroll.fillna(enroll.mean(axis=0), axis=0)
m = enroll.mean(axis=1)
for i, col in enumerate(enroll):
    enroll.iloc[:, i] = enroll.iloc[:, i].fillna(m)
#enroll.T.fillna(enroll.mean(axis=1)).T


# In[63]:


enroll.head()


# In[64]:


#Set up columns
cols=[]
for i in range(1960,2018):
    cols.append(str(i))
cols


# In[65]:


enroll.dtypes


# In[66]:


#keep the data from 1960 to 2017
enroll = enroll[cols[:len(cols)]]
enroll.head()


# In[67]:


#Since the data for school populationment is in percentage, the illustration of difference won't be obvious.
#The unit should be converted to number of people.
#We add population data to make this happen.
#Read raw data
population = pd.read_excel("population.xls", header=3, index_col=0)
population.head()
#Fill missing data to row mean value
population.fillna(population.mean(axis=0), axis=0)
m = population.mean(axis=1)
for i, col in enumerate(population):
    population.iloc[:, i] = population.iloc[:, i].fillna(m)
population = population[cols[:len(cols)]]
population.head()    


# In[68]:


#Calculate the enrollment in population
enrollpop = enroll * population / 100
enrollpop.head()


# ## 1.2 The Top Ten School Enrollment in Selected Year 

# In[69]:


def topten(year, total=10):
    df = enrollpop[year]
    top = df.sort_values(ascending=False)
    top = top.reset_index().head(total)
    top.index = top.index + 1
    return top


# In[70]:


topten('1970')


# In[71]:


topten('2013')


# ## 1.3 Pie Chart of the Top 10 Primary School Enrollment
# 

# In[72]:


def PiePlot(year):
    df = enrollpop[year]
    top = df.sort_values(ascending=False)
    top = top.reset_index()
    top.index = top.index + 1
    others = top[10:].sum()[1]
    top = top[:10]
    top.loc[11] = ['All Other Countries', others]
    
    countryPlot = top[year].plot.pie(subplots=True,
                                     autopct='%0.1f',
                                     fontsize=10,
                                     figsize=(10,10),
                                     legend=False,
                                     labels=top['Country Name'],
                                     shadow=False,
                                     explode=(0.15,0,0,0,0,0,0,0,0,0,0),
                                     startangle=90)


# In[73]:


PiePlot('2013')
plt.show()


# ## 1.4 Comparision of the Top 10 Primary School Enrollment
# 

# In[74]:


# Pie plot function.
def fun_pie(data):
    #Set up the plot style.
    plt.style.use('ggplot')
    #Import labels from dataset to pie chart.
    labels = list(data.index.values) 
    #Import data from dataset that determines every wedge sizes. 
    sizes = data.ix[:,0]    
    colors = ['yellowgreen', 'gold', 'lightcoral', 'white', 'brown', 'lightgreen', 'silver', 'lightyellow', 'lightblue','pink']
    # "Explode" the 1st slice 
    explode = (0.1, 0, 0, 0,0,0,0,0,0,0)  
    fig1, ax1 = plt.subplots(figsize=(9, 10))
    #Since some wedges are narrow, I adjust the position of text.
    ax1.pie(sizes, explode=explode, colors=colors, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90, pctdistance=0.8)
    # Equal aspect ratio ensures that pie is drawn as a circle.
    ax1.axis('equal')  

    plt.title("Top 10 Primary School Enrollment in 2013", bbox={'facecolor':'1', 'pad':7})

    plt.show()


# In[75]:


#select the top ten countries in 2013
topenroll2013 = enrollpop.loc[['World','IDA & IBRD total','Low & middle income','Middle income',
                            'IBRD only','Early-demographic dividend','Lower middle income',
                            'Upper middle income',"East Asia & Pacific",'Late-demographic dividend'],
                           ['2013']]
                            
                            


# In[76]:


fun_pie(topenroll2013)


# ## 1.5 The School Enrollment Over Time
# This line chart shows the trend of whole world primary school enrollment. Beside of these straight lines(they are caused by the fillna method), the school enrollment of the world increases over the years.

# In[77]:


def line(data):
    ax = enroll.sum().plot(figsize=(12,7))
    ax.set_xlabel('Year')
    ax.set_ylabel("Total School enrollment, primary (% gross)")
return plt.show()


# In[78]:


line(enroll)


# In[79]:


#Reload the raw data and fill na again
df = pd.read_excel("overall.xls", header=3)
df.fillna(df.mean(axis=0), axis=0)
m = df.mean(axis=1)
for i, col in enumerate(df):
    df.iloc[:, i] = df.iloc[:, i].fillna(m)


# In[80]:


#World Choropleth Map
def mapper(year):
    data = [go.Choropleth(
        locations = df['Country Code'],
        z = df[year],
        text = df['Country Name'],
        colorscale=[[0.0, 'rgb(165,0,38)'], 
                    [0.1, 'rgb(215,48,39)'], 
                    [0.2, 'rgb(244,109,67)'], 
                    [0.3, 'rgb(253,174,97)'], 
                    [0.4, 'rgb(254,224,144)'], 
                    [0.5, 'rgb(224,243,248)'], 
                    [0.6, 'rgb(171,217,233)'], 
                    [0.7, 'rgb(116,173,209)'], 
                    [0.8, 'rgb(69,117,180)'], 
                    [1.0, 'rgb(49,54,149)']],
        autocolorscale = False,
        reversescale = True,
        marker = go.choropleth.Marker(
            line = go.choropleth.marker.Line(
                color = 'rgb(180,180,180)',
                width = 0.5
            )),
        colorbar = go.choropleth.ColorBar(
            tickprefix = '%',
            title = 'percentage of enrollment'),
    )]

    layout = go.Layout(
        title = go.layout.Title(
            text = 'Primary School Enrollment ' + str(year) + '<br> % gross'
        ),
        geo = go.layout.Geo(
            showframe = False,
            showcoastlines = False,
            projection = go.layout.geo.Projection(
                type = 'equirectangular'
            )
        ),
        annotations = [go.layout.Annotation(
            x = 0.55,
            y = 0.1,
            xref = 'paper',
            yref = 'paper',
            text = 'Source: <a href="https://www.cia.gov/library/publications/the-world-factbook/fields/2195.html">\
                CIA World Factbook</a>',
            showarrow = False
        )]
    )

    fig = go.Figure(data = data, layout = layout)
    return py.iplot(fig, filename = 'd3-world-map')


# In[81]:


mapper('1990')


# In[82]:


mapper('2013')


# # 2 Correlation between Enrollment and Economy Development
# ![title](gdpandenroll.png)
# According to the world choropleth Maps of 1960 and 2013, generally, primary school enrollment of most of developing counties (such as countries in Africa) increase, but a lot of developed countries (USA, France, Canada, etc) decrease. This trend may indicate the enrollment of primary school might be correlated to the development of the economy. Therefore, the following researches are based on this question.

# ## 2.1 Data Preparing

# In[83]:


#Read the raw data of GDP enpenditure
GDP = pd.read_excel("GDP.xls", header=3, index_col=0)
#Fill na to the mean value
GDP.fillna(GDP.mean(axis=0), axis=0)
m = GDP.mean(axis=1)
for i, col in enumerate(GDP):
    GDP.iloc[:, i] = GDP.iloc[:, i].fillna(m)
GDP.head()


# In[84]:


#Only illustrate the data of GDP from 1960 to 2017
GDP = GDP[cols[:len(cols)]]
GDP.head()


# ## 2.2  Trend of Primary School Enrollment and development of GDP.
# According to the line charts of enrollment and GDP, they clearly show the increasing trend over the years. It firstly indicates the relationship between them.

# In[85]:


#Trend of whole world GDP last 45 years
#Since the straight lines caused by fillna make the plot inaccurate, we only select the last 45 years data
sumGDP = GDP.sum()
ax = sumGDP[-45:-1].plot(figsize=(12,7))
ax.set_xlabel('Year')
ax.set_ylabel("GDP current US$")
plt.show()


# In[86]:


#Trend of primary school enrollment last 45 years
sumenroll = enroll.sum()
ax = sumenroll[-45: -1].plot(figsize=(12,7))
ax.set_xlabel('Year')
ax.set_ylabel("Total School enrollment, primary (% gross)")
plt.show()


# Further, the scatter plot shows the primary school enrollment and GDP are positively related.

# In[87]:


def fun_scatter(d_1,d_2):
    
    
    #Set up the title.
    plt.title('Correlation', bbox={'facecolor':'1', 'pad':7})

    #Import Data and adjust visual effect. 
    plt.scatter(d_1, d_2, c="g",s=90, alpha=1, marker=r'$\clubsuit$',
            label="Luck")

        
    plt.show()

#Set up the labels of x-axis and y-axis.
plt.xlabel("Sum of Enrollment in the Last 45 Years")
plt.ylabel("Sum of GDP in the Last 45 Years")
  
fun_scatter(sumenroll[-45: -1],sumGDP[-45:-1])


# ## 2.3 Difference of Primary School Enrollment in High and Low GDP Countries

# In[88]:


#Find the median gdp all over the world 
GDPcountries = GDP.sum(axis=1)
GDPcountries.median()


# In[89]:


gdpenroll = pd.DataFrame({'Enrollment': enroll.sum(axis=1)})
#Add GDP to the DataFrame and standerdize the data
gdpenroll['GDP'] = GDPcountries
gdpenroll.head()


# In[90]:


#Divide all countries into two groups using median GDP
highGDP = gdpenroll.ix[(gdpenroll['GDP'] >= GDPcountries.median())]
lowGDP = gdpenroll.ix[(gdpenroll['GDP'] < GDPcountries.median())]
hg = highGDP.sum(axis=0)
lg = lowGDP.sum(axis=0)
#Sum of primary school enrollment in high GDP countries
hg['Enrollment']


# In[91]:


#Sum of primary school enrollment in low GDP countries
lg['Enrollment']


# In[92]:


#Difference of primary school enrollment in high and low GDP countries
hg['Enrollment'] - lg['Enrollment']


# By comparing the enrollment of countries with high GDP and low GDP, the final calculation results are in line with expectations. The economy largely determines primary school enrollment. So if you want to improve the level of national education, vigorously develop the economy is essential.

# # 3 Gender Equality in Primary School Enrollment
# ![title](educationgender.jpg)
# Today, it is widely recognized that there is gender discrimination in admission right. As the starting point of academic career, the primary school can directly reflect whether people can get the right to education. Is it true that there is widespread education inequality between the sexes in the world? The following research will be illustrated by data.

# ## 3.1 Data Preparing

# In[93]:


#Read the raw data of male
male = pd.read_excel("male.xls", header=3, index_col=0)
#Fill na to the mean value
male.fillna(male.mean(axis=0), axis=0)
m = male.mean(axis=1)
for i, col in enumerate(male):
    male.iloc[:, i] = male.iloc[:, i].fillna(m)
    
#Read the raw data of female
female = pd.read_excel("female.xls", header=3, index_col=0)
#Fill na to the mean value
female.fillna(female.mean(axis=0), axis=0)
m = female.mean(axis=1)
for i, col in enumerate(female):
    female.iloc[:, i] = female.iloc[:, i].fillna(m)


# In[94]:


male.head()


# In[95]:


female.head()


# In[96]:


male = male[cols[:len(cols)]]
male.head()


# In[97]:


female = female[cols[:len(cols)]]
female.head()


# In order to compare the difference clearly, there data will be merged into a same DataFrame.

# In[98]:


summale = male.sum()
sumfemale = female.sum()
#Build DataFrame
mix = pd.DataFrame({'Male': summale})
#Add Female to the DataFrame 
mix['Female'] = sumfemale
mix.head()


# ## 3.2 Time Series that Displays Male and Female of Primary School Enrollment
# As can be clearly seen from this graph, the primary school enrollment rate of women never exceeded that of men from 1960 to 2017. This graph has clearly indicated the difference in educational rights between men and women.

# In[99]:


#Creating a time series (last 45 years) that displays male and female of primary school enrollment
ax = mix[-45:-1].plot(figsize=(20,10), fontsize=13)
plt.legend(loc='best', fontsize=13)
ax.set_xlabel('Year', fontsize=13)
ax.set_ylabel('Enrollment', fontsize=13)
plt.show()


# ## 3.3 Display of the Difference in Different genders(last 15 years) in Bar Chart
# In this bar chart, we can see that in the past 15 years, although there is no significant difference between male and female enrollment, female enrollment has never caught up with male enrollment.

# In[100]:


#Creating a bar chart to display the difference in different genders(last 15 years)
mix[-15:-1].plot(kind='bar', figsize=(10,6), title='Difference of School Enrollment in Genders')
plt.show()


# ## 3.4 Cumulative Primary Scholl Enrollment in Male and Female from 1960 to 2017
# If we add up the cumulative data from 1960 to 2017, the gap becomes even more pronounced.

# In[101]:


#Cumulative primary scholl enrollment in male and female from 1960 to 2017
mixsum = mix.sum()
#plot the data frame
mixsum.plot(kind='bar')
plt.show()


# Through the data analysis of this part, we can see the significant gap between male and female primary school enrollment rate. We can then infer that the right to education has sexist in most of the world. Although only the average and the overall situation can be seen from my analysis, it can also indicate that gender discrimination in education will be more serious in many countries.

# # 4 Expenditure and Enrollment on Primary Education
# <img src="educationspending.png" width="60%">
# The national economy influences primary school enrollment, but the national education policy is different, so the national economy is not a very intuitive factor to predict education. So the next thing we're going to look at is the relationship between education expenditure and enrollment.

# ## 4.1 Data Preparing

# In[102]:


#Read the raw data of Education Expenditure(% of GDP)
spend = pd.read_excel("spend.xls", header=3, index_col=0)
#Fill na to the mean value
spend.fillna(spend.mean(axis=0), axis=0)
m = spend.mean(axis=1)
for i, col in enumerate(spend):
    spend.iloc[:, i] = spend.iloc[:, i].fillna(m)
    
spend = spend[cols[:len(cols)]]


# In[103]:


spend.head()


# Since the unit of data is the percentage of GDP, the unit should be converted to US Dollar.

# In[104]:


spendUSD = spend*GDP/100
spendUSD.head()


# ## 4.2 Trend of The Whole World Education Expenditure in Last 45 Years
# As the number of years increases, so does spending on education. This trend is also consistent with primary school enrollment.

# In[105]:


sumspend = spendUSD.sum()
sumspend = sumspend[-45:-1]
ax = sumspend.plot(figsize=(12,7))
ax.set_xlabel('Year')
ax.set_ylabel("Education Expenditure(USD)")
plt.show()


# # 5 Persistence to the Last Grade
# <img src="graduation.png" width="40%">
# Even if enrollment is high, the future of all students is not guaranteed. Students may face a variety of problems that prevent them from completing their studies. Once a student drops out of school, it is difficult to define whether he or she has received a good education. So in the next study, we're going to use data to show how many people end up finishing primary school.

# ## 5.1 Data Preparing

# In[106]:


#Read the raw data of Persistence to last grade of primary, total (% of cohort)
graduation = pd.read_excel("graduation.xls", header=3, index_col=0)
#Fill na to the mean value
graduation.fillna(graduation.mean(axis=0), axis=0)
m = graduation.mean(axis=1)
for i, col in enumerate(graduation):
    graduation.iloc[:, i] = graduation.iloc[:, i].fillna(m)
    
graduation = graduation[cols[:len(cols)]]


# In[107]:


graduation.head()


# ## 5.2 How Many Student Remaining in the Last Grade(% gross)
# In order to get a better representation on the graph, we need to convert units into number of people.

# In[108]:


finalenroll = enroll * graduation/ 100
finalenroll.head()


# In[109]:


sumfinalenroll = finalenroll.sum()
sumfinalenroll = sumfinalenroll[-45:-1]
ax = sumfinalenroll.plot(figsize=(12,7))
ax.set_xlabel('Year')
ax.set_ylabel("Student Remaining in the Last Grade(% gross)")
plt.show()


# ## 5.3 The Contrast of Students in the First Grade and the Last Grade (% gross)
# This chart illustrates the prevalence and severity of primary school dropouts. On average, students in the last grade were a quarter fewer than in the first.

# In[110]:


#Build DataFrame
FL = pd.DataFrame({'First Grade': sumenroll})
#Add Last Grade to the DataFrame 
FL['Last Grade'] = sumfinalenroll

#Creating a time series (last 45 years) that displays first and last grade of primary school enrollment
ax = FL[-45:-1].plot(figsize=(20,10), fontsize=13)
plt.legend(loc='best', fontsize=13)
ax.set_xlabel('Year', fontsize=13)
ax.set_ylabel('Enrollment', fontsize=13)
plt.show()


# ## 5.4 The Contrast of Different Genders in the Last Grade (% gross)
# Surprisingly, these figures show that far more girls than boys stick to elementary school. 
# Because of gender discrimination, I expect that female primary school drop-out rates will be much higher than male primary school drop-out rates ，but just the opposite.Is it because girls are more diligent and persistent in primary school? Or because once enrolled, they are no longer subject to sexism? I can't get exact results here because of the data and length, but I'll keep trying to keep the topic going.

# In[111]:


#Data Preparing
lastfemale = pd.read_excel("lastfemale.xls", header=3, index_col=0)
lastfemale.fillna(lastfemale.mean(axis=0), axis=0)
m = lastfemale.mean(axis=1)
for i, col in enumerate(lastfemale):
    lastfemale.iloc[:, i] = lastfemale.iloc[:, i].fillna(m)
lastfemale = lastfemale[cols[:len(cols)]]
sumlastfemale = lastfemale.sum()
sumlastfemale = sumlastfemale[-45:-1]
#Female
lastfemale = pd.read_excel("lastfemale.xls", header=3, index_col=0)
lastfemale.fillna(lastfemale.mean(axis=0), axis=0)
m = lastfemale.mean(axis=1)
for i, col in enumerate(lastfemale):
    lastfemale.iloc[:, i] = lastfemale.iloc[:, i].fillna(m)
lastfemale = lastfemale[cols[:len(cols)]]
sumlastfemale = lastfemale.sum()
sumlastfemale = sumlastfemale[-45:-1]


# In[112]:


#Build DataFrame
lastMF = pd.DataFrame({'Male': sumlastmale})
#Add Female in Last Grade to the DataFrame 
lastMF['Female'] = sumlastfemale

#Creating a time series (last 45 years) that displays first and last grade of primary school enrollment
ax = lastMF[-45:-1].plot(figsize=(20,10), fontsize=13)
plt.legend(loc='best', fontsize=13)
ax.set_xlabel('Year', fontsize=13)
ax.set_ylabel('Different Genders in Last Grade', fontsize=13)
plt.show()


# In[ ]:


sumlastMF=lastMF.sum()
sumlastMF.plot(kind='bar')
plt.show()


# # 6, Conclusion

# ## 6.1, Summary 
# By studying primary school enrollment, GDP, the gender difference in education and government education expenditure, we can find that primary school enrollment rate is closely related to the national economy, government education policy and gender equality consciousness. There is a significant difference in the approach to primary education between countries with high GDP and those with low GDP. In contrast to different genders in the final grade, we find that more girls try to finish primary school. It also shows the perseverance of girls in the study.They deserve equal access to education.

# ## 6.2, Prediction
# <img src="mix.jpg" width="80%">
# Through research, we can find that the primary school enrollment rate in developed countries is leveling off, I believe there will not be much change in the future; GDP is increasing year by year, and the primary school enrollment rate will increase because of the positive correlation. The gender gap is narrowing year by year. Government spending on education may fall in the future, but the trend is upward. More and more girls will finish their primary school education. The plot shows that this kind of gender gap will be bigger and bigger.

# ## 6.3, What I Have Learned
# Firstly, I'm very grateful to learn the skill of illustrating data on a map and have learned how to present different data with multiple visualization methods. Secondly, I have learned how to deal with data frames, how to use multiple data at the same time, and how to filter data accurately. Finally, I have learned what factors can affect education, and if one day I am lucky enough to participate in education career, this research gives me a direction.
