import numpy as np
import sys
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
# %matplotlib inline
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import math

separationStrategy = ''

print('\nPlease make sure that the file containing the data that you want to visualize is in the same folder as this program.')
dataPath = input('\nEnter the name of the file containing the data to be visualized:\n')

print('\n 1. Commas \n 2. Tabs \n 3. Pipe \n 4. Other')
separationStrategyInput = input('\nEnter the number corresponding to the separation strategy of your file:\n')

if '1' in separationStrategyInput:
    separationStrategy = ','
elif '2' in separationStrategyInput:
    separationStrategy = '\t'
elif '3' in separationStrategyInput:
    separationStrategy = '|'
elif '4' in separationStrategyInput:
    separationStrategy = input('\nEnter the delimeter used:\n')
try:
    df = pd.read_csv(dataPath, sep=separationStrategy)
except:
    sys.exit()

x_axis = input('\nEnter the name of the column containing the values for the x axis:\n')
y_axis = input('\nEnter the name of the column containing the values for the y axis:\n')
group = input('\nEnter the name of the column containing the values based on which the data points will be grouped:\n')
associationDirection = input('\nWould you like to show an association direction in your data(yes/no)?\n')

df.dropna(axis=0, subset=[y_axis], inplace=True)
df.dropna(axis=1, how='all', inplace=True)

figure_title = input('\nEnter the title you would like the figure to have:\n')

print('\nNow choose what information you would like to be displayed when hovering over a data point.' + 
'\nPress enter after each column name. Enter "done" if you are done specifying the columns.')
show_on_hover = []
while True:
    colName = input('\nEnter the name of the next column or "done" if you are finished:\n')
    if colName.lower() == 'done': break
    show_on_hover.append(colName)

posThreshold = float(input('\nEnter the -log10(p) threshold for the positive corelation in the visualization:\n'))
negThreshold = float(input('\nEnter the -log10(p) threshold for the negative corelation in the visualization:\n'))
show_legendInput = input('\nWould you like a legend to be included in your visualization (yes/no)? You can see what the legend looks like here.\n')
show_legend = True

if show_legendInput == 'no':
    show_legend = False

df['y'] = df[df[y_axis].isna() == False][y_axis].apply(lambda x: -math.log(x, 10))

if associationDirection.lower() == 'yes':
    associationVar = input('\nEnter name of the column that determines the direction of the association:\n')
    if associationVar.lower() == 'beta':
        df['symbol'] = df[associationVar].apply(lambda x: 'positive' if x >= 0 else 'negative')
    else:
        df['symbol'] = df[associationVar].apply(lambda x: 'positive' if x >= 1 else 'negative')
else:
    df['symbol'] = 'no_corr'

x_numeric = input('\nIs your x variable numeric (yes/no)?\n')
x_numeric = False if x_numeric == 'no' else True
tick_location = []

if x_numeric:
    for i in df[group].unique():
        tick_location.append(df[df[group] == i][x_axis].mean())
else:
    tick_vals = {}
    for i in df[group].unique():
        tick_vals[i] = 0
    length = len(df.index)
    for i in range(length):
        row = df.iloc[i]
        tick_vals[row[group]] += 1
    prev = 0
    for i in tick_vals.values():
        i += prev
        tick_location.append((prev + i)/2)
        prev = i

above_thresh = []
above = df[df.y >= posThreshold]
length = len(above.index)
for i in range(length):
    annot = above.iloc[i]
    above_thresh.append(go.layout.Annotation(
            x=annot[x_axis],
            y=annot.y,
            text=annot[group]
    ))

fig = px.scatter(df, x = x_axis, y = 'y', color = group,
                 hover_data = show_on_hover,
                 template ='plotly_white')

fig.update_layout(
    margin=dict(pad=0),
    title_text = figure_title,
    autosize = False,
    width = 1300,
    height = 700,
    yaxis = go.layout.YAxis(
        title=r'$-\log_{10} p$'
    ),
    xaxis = go.layout.XAxis(
        automargin = True,
        showgrid = False,
        title = x_axis,
        tickangle = 60,
        ticktext = df[group].unique(),
        tickvals = tick_location,
        tickfont = go.layout.xaxis.Tickfont(
            size = 10
        )
    ),
    showlegend = show_legend,
    legend=go.layout.Legend(
        font = dict(
            size = 10
        ),
        itemclick='toggleothers',
        itemdoubleclick='toggle',
        tracegroupgap=1
    ),
    annotations = above_thresh
)

if x_numeric:
    fig.update_layout(
        shapes=[
        go.layout.Shape(
            type="line",
            x0=0,
            y0=posThreshold,
            x1=df[x_axis].max(),
            y1=posThreshold,
            line=dict(
                color="red",
                width=1
            )
        ),
        go.layout.Shape(
            type="line",
            x0=0,
            y0=negThreshold,
            x1=df[x_axis].max(),
            y1=negThreshold,
            line=dict(
                color="blue",
                width=1
            )
        )]
    )
else:
    fig.update_layout(
        shapes=[
        go.layout.Shape(
            type="line",
            x0=0,
            y0=posThreshold,
            x1=df[x_axis].nunique(),
            y1=posThreshold,
            line=dict(
                color="red",
                width=1
            )
        ),
        go.layout.Shape(
            type="line",
            x0=0,
            y0=negThreshold,
            x1=df[x_axis].nunique(),
            y1=negThreshold,
            line=dict(
                color="blue",
                width=1
            )
        )]
    )
    
fig.update_traces(
    marker = go.scatter.Marker(
#         symbol=df['correlation']
        size=12,
#         opacity = 0.5,
#         line=dict(width=1, color='black'),
    ))

preview = input('\nWould you like to preview the figure before exporting it (yes/no)?\n')
if preview == 'yes':
    fig.show()


visName = input('Enter the name of the file you would like to export:')
    
print('\n 1. html file \n 2. png \n 3. jpg \n 4. svg \n 5. pdf \n 6. JSON')
output_format = input('\nEnter the number corresponding to the output file format you prefer (intercative features only available with html):\n')

if '1' in output_format:
    pio.write_html(fig, file = visName+'.html', auto_open=True)
elif '2' in output_format:
    pio.write_image(fig, file = visName+'.png', format='png')
elif '3' in output_format:
    pio.write_image(fig, file = visName+'.jpg', format='jpg')
elif '4' in output_format:
    pio.write_image(fig, file = visName+'.svg', format='svg')
elif '5' in output_format:
    pio.write_image(fig, file = visName+'.pdf', format='pdf')
elif '6' in output_format:
    pio.write_json(fig, file = visName)