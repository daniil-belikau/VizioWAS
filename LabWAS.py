import sys
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import math
import enum

import vizutil.util as util
import vizutil.data as data
import vizutil.plot as plot


def run():
    path = util.get_text_input('Enter the path to the file containing the data to be visualized:', util.Format.free_text.value)
    separation_strategy = util.get_text_input('\n 1. Commas \n 2. Tabs \n 3. Pipe \n 4. Other', util.Format.item_in_list.value, 
                                        'Enter the number corresponding to the separation strategy of your file:', 
                                        { '1': ',', '2': '\t', '3': '|', '4': 'other' })
    if separation_strategy == 'other':
        separation_strategy = util.get_text_input('Specify the separation strategy:', util.Format.free_text.value)
    
    df = data.data_import(path, separation_strategy, True)

    available_cols = list(df.columns)
    x_axis = util.get_text_input('Which column contains the values for the x axis:', util.Format.column_name.value, 
                            message=f'This is the list of available columns: \n {available_cols}', validation=available_cols)
    y_axis = util.get_text_input('Which column contains the values for the y axis:', util.Format.column_name.value, 
                            validation=available_cols)
    group = util.get_text_input('Based on which column should the data points be grouped:', util.Format.column_name.value, 
                            validation=available_cols)
    association_direction = util.get_text_input('Would you like to show the association direction in your figure (yes/no):', util.Format.yes_no.value)

    df = data.data_clean(df, [x_axis, y_axis, group], y_axis)

    available_cols = list(df.columns)
    association_var=''
    if association_direction:
        association_var = util.get_text_input('Which column determines the direction of association:', util.Format.column_name.value, validation=available_cols)
    df = data.format_yaxis(df, y_axis, association_var)

    print('\nNow choose what information you would like to be displayed when hovering over a data point. Press enter after each column name. Enter "done" if you are done specifying the columns.')
    hover_data = plot.assemble_hover_data(available_cols)

    if association_direction:
        pos = util.get_text_input('Enter the -log10(p) for significant positive correlation:', util.Format.numeric.value)
        neg = util.get_text_input('Enter the -log10(p) for significant negative correlation:', util.Format.numeric.value)
        lines = [(pos, 'red'), (-neg, 'blue')]
    else:
        pos = util.get_text_input('Enter the -log10(p) for significant correlation:', util.Format.numeric.value)
        lines = [(pos, 'red')]
    annotation_threshold_column = util.get_text_input('Do you have a column that determines if a data point should be annotated (yes/no):', util.Format.yes_no.value)
    if not annotation_threshold_column:
        annotation_threshold = util.get_text_input('Enter the -log10(p) threshold for annotating values on the figure:', util.Format.numeric.value)
    else: 
        annotation_threshold = util.get_text_input('Which column column would you like to use for that:', util.Format.column_name.value, validation=available_cols)
    annotation_var = util.get_text_input('Which column would you like to use to annotate significant points:', util.Format.column_name.value, validation=available_cols)
    annotation_limit_change = util.get_text_input('The 10 most significant points will be annotated to prevent crowdedness. Would you like to change this limit (yes/no):', util.Format.yes_no.value)
    annotation_limit = 10
    if annotation_limit_change:
        annotation_limit = int(util.get_text_input('What is the maximum number of annotations you would like on your figure:', util.Format.numeric.value, validation=available_cols))
    annotations = data.create_annotations(df, x_axis, annotation_var, annotation_threshold, annotation_limit, not annotation_threshold_column)

    title = util.get_text_input('Enter figure title:', util.Format.free_text.value)
    marker_size = util.get_text_input('Choose the corresponding number:', util.Format.item_in_list.value, '\nHow big would you like the data point markers to be? \n 1. Small \n 2. Medium \n 3. Large', 
                                { '1':8, '2':12, '3':16 })
    show_legend = util.get_text_input('Would you like to include a legend in your visualization (yes/no):', util.Format.yes_no.value)
    width = util.get_text_input('The width in pixels:', util.Format.numeric.value, '\nEnter the dimensions for the figure.')
    height = util.get_text_input('The height in pixels:', util.Format.numeric.value)

    df = data.transform_hover_data(df, hover_data[2])

    fig = plot.produce_figure(df, x_axis, group, hover_data[0])
    fig = plot.customize_markers(fig, df[group].unique(), group, hover_data[1], marker_size)
    fig = plot.customize_layout(fig, title, annotations, x_axis, show_legend, df[x_axis].nunique(), True, width, height, lines, association_direction)
    
    util.get_text_input('Press Enter to review the plot:', util.Format.press_enter.value)
    plot.preview_figure(fig)
    print('You can output this plot in multiple files and formats.')
    plot.export_plot(fig)
