import numpy as np
import sys
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import math
import enum

class Format(enum.Enum):
    free_text = 1
    yes_no = 2
    numeric = 3
    column_name = 4
    item_in_list = 5

class InputError(Exception):

    def __init__(self, msg): 
        self.msg = msg


def get_text_input(prompt, input_format, message='\n', validation=[]):
    print(message)

    while True:
        try:
            text_input = input(f'{prompt}\n')

            if input_format == 2:
                if text_input != 'yes' and text_input != 'no':
                    raise InputError("Please enter 'yes' or 'no'.")
                return text_input == 'yes'

            elif input_format == 3:
                try:
                    text_input = float(text_input)
                except:
                    raise InputError("Only numeric input accepted.")

            elif input_format == 4 and text_input not in validation:
                    raise InputError(f"Input must be one of the following: \n{validation}.")
                
            elif input_format == 5:
                if  text_input not in validation.keys():
                    raise InputError(f"Input must be one of the following: \n{validation.keys()}.")
                else:
                    return validation[text_input]

            return text_input
        
        except InputError as err:
            print(err.msg)


prompt = 'Enter the path to the file containing the data to be visualized:'
dataPath = get_text_input(prompt, Format.free_text.value)

message = '\n 1. Commas \n 2. Tabs \n 3. Pipe \n 4. Other'
prompt = 'Enter the number corresponding to the separation strategy of your file:'
separation_strategy_options = {
    '1': ',',
    '2': '\t',
    '3': '|',
    '4': get_text_input
}
separation_strategy = get_text_input(prompt, Format.item_in_list.value, message, separation_strategy_options)

if type(separation_strategy) != str:
    separation_strategy = get_text_input('Specify the separation strategy:', Format.free_text.value)

try:
    df = pd.read_csv(dataPath, sep=separation_strategy)
except:
    print('Check that the file path and separation strategy are correct!')
    sys.exit()

list_of_columns = list(df.columns)

prompt = 'Which column contains the values for the x axis:'
x_axis = get_text_input(prompt, Format.column_name.value, validation=list_of_columns)
prompt = 'Which column contains the values for the y axis:'
y_axis = get_text_input(prompt, Format.column_name.value, validation=list_of_columns)
prompt = 'Based on which column should the data points be grouped:'
group = get_text_input(prompt, Format.column_name.value, validation=list_of_columns)
prompt = 'Would you like to show the association direction in your figure:'
association_direction = get_text_input(prompt, Format.yes_no.value)

df.dropna(axis=0, subset=[y_axis], inplace=True)
df.dropna(axis=1, how='all', inplace=True)

prompt = 'Enter figure title:'
figure_title = get_text_input(prompt, Format.free_text.value)

print('\nNow choose what information you would like to be displayed when hovering over a data point.' + 
'\nPress enter after each column name. Enter "done" if you are done specifying the columns.')
prompt = 'Enter the next column or "done" if you are finished:'
list_of_columns.append('done')
show_on_hover = []
while True:
    col_name = get_text_input(prompt, Format.column_name.value, validation=list_of_columns)
    if col_name == 'done': break
    show_on_hover.append(col_name)
list_of_columns.remove('done')

prompt = 'Enter the -log10(p) for significant positive correlation:'
pos_threshold = get_text_input(prompt, Format.numeric.value)
prompt = 'Enter the -log10(p) for significant negative correlation:'
neg_threshold = get_text_input(prompt, Format.numeric.value)
prompt = 'Enter the -log10(p) threshold for annotating values on the figure:'
annotation_threshold = get_text_input(prompt, Format.numeric.value)
prompt = 'Which column would you like to use to annotate significant points:'
annotation_var = get_text_input(prompt, Format.column_name.value, validation=list_of_columns)
prompt = 'The number of annotations per figure is limited to 10 to prevent crowdedness. Would you like to change this limit:'
annotation_limit_change = get_text_input(prompt, Format.yes_no.value)
annotation_limit = 10
if annotation_limit_change:
    prompt = 'What is the maximum number of annotations you would like on your figure:'
    annotation_limit = int(get_text_input(prompt, Format.numeric.value, validation=list_of_columns))
    
prompt = 'Would you like to include a legend in your visualization:'
show_legend = get_text_input(prompt, Format.yes_no.value)

df['-log10(p)'] = df[df[y_axis].isna() == False][y_axis].apply(lambda x: -math.log(x, 10))

if association_direction:
    prompt = 'Which column determines the direction of association:'
    association_var = get_text_input(prompt, Format.column_name.value, validation=list_of_columns)
    if 'beta' in association_var.lower():
        df['symbol'] = df[association_var].apply(lambda val: 'triangle-up' if val >= 0 else 'triangle-down')
        
    else:
        df['symbol'] = df[association_var].apply(lambda val: 'triangle-up' if val >= 1 else 'triangle-down')

prompt = 'Is your x variable numeric:'
x_numeric = get_text_input(prompt, Format.yes_no.value)
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
above = df[df['-log10(p)'] >= annotation_threshold]
above.sort_values(by=['-log10(p)'])
above = above.iloc[:annotation_limit]
length = len(above.index)
for i in range(length):
    
    annot = above.iloc[i]
    above_thresh.append(go.layout.Annotation(
            x=annot[x_axis],
            y=annot['-log10(p)'],
            text=annot[annotation_var],
            font=go.layout.annotation.Font(size=8)
    ))


fig = px.scatter(df, x = x_axis, y = '-log10(p)', color = group,
                 hover_data = show_on_hover,
                 template ='plotly_white',
                )

hover_info_list = []
hover_info_size = len(show_on_hover)
for i in range(hover_info_size):
    if i != hover_info_size - 1:
        hover_info_list.append(f'{show_on_hover[i]}=%{{customdata[{i}]}}<br>')
    else:
        hover_info_list.append(f'{show_on_hover[i]}=%{{customdata[{i}]}}')

hover_info_template = ''.join(hover_info_list)

fig.update_traces(patch=dict(
    hovertemplate=hover_info_template,
    marker={'size':12}
))

if association_direction:
    for gr in df[group].unique():
        fig.update_traces(patch=dict(
            legendgroup=gr,
            name=gr,
            marker={'symbol': list(df[df[group]==gr]['symbol'])},
        ), selector=dict(
            legendgroup=f'{group}={gr}'
        ))
        
else:
    for gr in df[group].unique():
        fig.update_traces(patch=dict(
            legendgroup=gr,
            name=gr,
        ), selector=dict(
            legendgroup=f'{group}={gr}'
        ))

fig.update_layout(
    margin=dict(pad=0),
    title_text = figure_title,
    autosize = False,
    width = 1300,
    height = 700,
    yaxis = go.layout.YAxis(
        title='-log10(p)'
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
        itemclick=False,
        itemdoubleclick=False,
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
            y0=pos_threshold,
            x1=df[x_axis].max(),
            y1=pos_threshold,
            line=dict(
                color="red",
                width=1
            )
        ),
        go.layout.Shape(
            type="line",
            x0=0,
            y0=neg_threshold,
            x1=df[x_axis].max(),
            y1=neg_threshold,
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
            y0=pos_threshold,
            x1=df[x_axis].nunique(),
            y1=pos_threshold,
            line=dict(
                color="red",
                width=1
            )
        ),
        go.layout.Shape(
            type="line",
            x0=0,
            y0=neg_threshold,
            x1=df[x_axis].nunique(),
            y1=neg_threshold,
            line=dict(
                color="blue",
                width=1
            )
        )]
    )
    
fig.layout

prompt = 'Would you like to preview the figure before exporting it:'
preview = get_text_input(prompt, Format.yes_no.value)
if preview:
    fig.show(config={'editable':True})

prompt = 'Enter the name of the file you would like to export:'
vis_name = get_text_input(prompt, Format.free_text.value)
    
message = '\n 1. html file \n 2. png \n 3. jpg \n 4. svg \n 5. pdf \n 6. JSON'
prompt = 'Enter the number corresponding to the output file format you prefer (intercative features only available with html):'
list_of_options = ['1', '2', '3', '4', '5', '6'] 
output_format = get_text_input(prompt, Format.column_name.value, message, list_of_options)

if '1' in output_format:
    pio.write_html(fig, file = vis_name+'.html', auto_open=True)
elif '2' in output_format:
    pio.write_image(fig, file = vis_name+'.png', format='png')
elif '3' in output_format:
    pio.write_image(fig, file = vis_name+'.jpg', format='jpg')
elif '4' in output_format:
    pio.write_image(fig, file = vis_name+'.svg', format='svg')
elif '5' in output_format:
    pio.write_image(fig, file = vis_name+'.pdf', format='pdf')
elif '6' in output_format:
    pio.write_json(fig, file = vis_name)


