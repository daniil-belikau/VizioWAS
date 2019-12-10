import sys
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import math
import enum


# class Format(enum.Enum):
#     free_text = 1
#     yes_no = 2
#     numeric = 3
#     column_name = 4
#     item_in_list = 5
#     press_enter = 6


# class InputError(Exception):

#     def __init__(self, msg): 
#         self.msg = msg


# def get_text_input(prompt, input_format, message='\n', validation=[]):
#     print(message)

#     while True:
#         try:
#             text_input = input(f'{prompt}\n')

#             if input_format == 2:
#                 if text_input != 'yes' and text_input != 'no':
#                     raise InputError("Please enter 'yes' or 'no'.")
#                 return text_input == 'yes'

#             elif input_format == 3:
#                 try:
#                     text_input = float(text_input)
#                 except:
#                     raise InputError("Only numeric input accepted.")

#             elif input_format == 4 and text_input not in validation:
#                     raise InputError(f"Input must be one of the following: \n{validation}.")
                
#             elif input_format == 5:
#                 if  text_input not in validation.keys():
#                     raise InputError(f"Input must be one of the following: \n{validation.keys()}.")
#                 else:
#                     return validation[text_input]

#             return text_input
        
#         except InputError as err:
#             print(err.msg)
            




# 
# 
def determine_offset(state, y_axis_positive):
    if state == 0:
        if y_axis_positive:
            return (-25, -4, 1)
        else:
            return (-25, 4, 1)
    elif state == 1:
        if y_axis_positive:
            return (0, -15, 2)
        else:
            return (0, 15, 2)
    elif state == 2:
        if y_axis_positive:
            return (25, -4, 0)
        else:
            return (25, 4, 0)
# 
# 




        


# 
# 
def output_plot_file(figure):
    vis_name = get_text_input('Enter a name for the file that will be exported:', 
                            Format.free_text.value)
    output_format = get_text_input('Enter the number corresponding to the output file format you prefer (interactive features only available with html):', 
                                Format.column_name.value, 
                                '\n 1. html file \n 2. png (small file, but lower image quality) \n 3. jpg (small file, but lower image quality) \n 4. svg \n 5. pdf \n 6. JSON', 
                                ['1', '2', '3', '4', '5', '6'])
    if '1' in output_format:
        pio.write_html(figure, file = vis_name+'.html', config={'editable':True, 'displaylogo' : False, 'responsive' : True,
                     'toImageButtonOptions': {
        'format' : 'svg',
#       'format' : 'pgn',
#       'format' : 'jpeg',
#       'format' : 'pdf',
        'width'  : 2000,
        'height' : 1200
    }, 'showSendToCloud' : True})
    elif '2' in output_format:
        pio.write_image(figure, file = vis_name+'.png', format='png')
    elif '3' in output_format:
        pio.write_image(figure, file = vis_name+'.jpg', format='jpg')
    elif '4' in output_format:
        pio.write_image(figure, file = vis_name+'.svg', format='svg')
    elif '5' in output_format:
        pio.write_image(figure, file = vis_name+'.pdf', format='pdf')
    elif '6' in output_format:
        pio.write_json(figure, file = vis_name)
# 
# 






def main():
    # MAIN SCRIPT
    dataPath = get_text_input('Enter the path to the file containing the data to be visualized:', 
                            Format.free_text.value)
    separation_strategy = get_text_input('\n 1. Commas \n 2. Tabs \n 3. Pipe \n 4. Other', 
                                        Format.item_in_list.value, 
                                        'Enter the number corresponding to the separation strategy of your file:', 
                                        { '1': ',',
                                        '2': '\t',
                                        '3': '|',
                                        '4': 'other' })
    if separation_strategy == 'other':
        separation_strategy = get_text_input('Specify the separation strategy:', Format.free_text.value)




# 
# 
    try:
        df = pd.read_csv(dataPath, sep=separation_strategy)
        df = df.sample(frac=1).reset_index(drop=True)
    except:
        print('Check that the file path and separation strategy are correct!')
        sys.exit()
# 
# 





    # MAIN SCRIPT
    list_of_columns = list(df.columns)
    x_axis = get_text_input('Which column contains the values for the x axis:', 
                            Format.column_name.value, 
                            message=f'This is the list of available columns: \n {list_of_columns}',
                            validation=list_of_columns)
    y_axis = get_text_input('Which column contains the values for the y axis:', 
                            Format.column_name.value, 
                            validation=list_of_columns)
    group = get_text_input('Based on which column should the data points be grouped:', 
                            Format.column_name.value, 
                            validation=list_of_columns)
    association_direction = get_text_input('Would you like to show the association direction in your figure (yes/no):', 
                                            Format.yes_no.value)








# 
# 
    df.dropna(axis=0, subset=[y_axis], inplace=True)
    df.dropna(axis=1, how='all', inplace=True)
    if df[df[y_axis] == 0].shape[0] > 0:
        print('Please make sure there are no P-values equal to 0 in your data.')
        sys.exit()
# 
# 







#     y_value_min = df[df[y_axis] != 0].min()[y_axis]
#     df[y_axis] = df[df[y_axis].isna() == False][y_axis].apply(lambda y: y if y != 0 else y_value_min)
    df['-log10(p)'] = df[df[y_axis].isna() == False][y_axis].apply(lambda x: -math.log(x, 10))


    list_of_columns = list(df.columns)

    if association_direction:
        association_var = get_text_input('Which column determines the direction of association:', 
                                        Format.column_name.value,
                                        validation=list_of_columns)
        if 'beta' in association_var.lower():
            df['-log10(p)'] = df['-log10(p)']*df[association_var].apply(lambda val: 1 if val >= 0 else -1)
        else:
            df['-log10(p)'] = df['-log10(p)']*df[association_var].apply(lambda val: 1 if val >= 1 else -1)

    # 
    # 




    

    # 
    #   
    x_numeric = get_text_input('Is your x variable numeric (yes/no):', 
                                Format.yes_no.value)
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
# 
# 





    # PLACE THIS PART INTO THE VIZ.PY FILE, WITH OTHER PROMPTS THAT DON'T CHANGE
    list_of_columns = list(df.columns)
    print('\nNow choose what information you would like to be displayed when hovering over a data point.' + 
    '\nPress enter after each column name. Enter "done" if you are done specifying the columns.')
    list_of_columns.append('done')
    show_on_hover = []
    show_on_hover_titles = []
    while True:
        col_name = get_text_input('Enter the next column or "done" if you are finished:', 
                                Format.column_name.value, 
                                validation=list_of_columns)
        if col_name == 'done': break
        col_title = get_text_input('Enter the name that this column will be displayed under:',
                                  Format.free_text.value)
        show_on_hover.append(col_name)
        show_on_hover_titles.append(col_title)

    print('\nName any columns for which you would like to specify a significant digit cutoff or scientific notation.' + 
    '\nPress enter after each column name. Enter "done" if you are done specifying the columns.')
    column_transformations = []
    while True:
        col_name = get_text_input('Enter the next column or "done" if you are finished:', 
                                Format.column_name.value, 
                                validation=list_of_columns)
        if col_name == 'done': break
        sig_digs = get_text_input('Would you like to set a number of significant digits (yes/no):',
                                  Format.yes_no.value)
        if sig_digs:
            sig_digs = get_text_input('How many significant digits would you like to show for this column:',
                                     Format.numeric.value)
        scientific_notation = get_text_input('Would you like to show this column using scientific notation (yes/no):',
                                            Format.yes_no.value)
        column_transformations.append((col_name, sig_digs, scientific_notation))
        
    list_of_columns.remove('done')
# 
# 






    # Goes into the VIZ.PY   
    if association_direction:
        pos_threshold = get_text_input('Enter the -log10(p) for significant positive correlation:', 
                                        Format.numeric.value)
        neg_threshold = get_text_input('Enter the -log10(p) for significant negative correlation:', 
                                        Format.numeric.value)
    else:
        association_threshold = get_text_input('Enter the -log10(p) for significant correlation:', 
                                        Format.numeric.value)
    annotation_threshold_column = get_text_input('Do you have a column that determines if a data point should be annotated (yes/no):', 
                                                  Format.yes_no.value)
    if not annotation_threshold_column:
        annotation_threshold = get_text_input('Enter the -log10(p) threshold for annotating values on the figure:', 
                                              Format.numeric.value)
    else: 
        annotation_threshold = get_text_input('Which column column would you like to use for that:', 
                                              Format.column_name.value, 
                                              validation=list_of_columns)
    annotation_var = get_text_input('Which column would you like to use to annotate significant points:', 
                                    Format.column_name.value, validation=list_of_columns)
    annotation_limit_change = get_text_input('The 10 most significant points will be annotated to prevent crowdedness. Would you like to change this limit (yes/no):', 
                                             Format.yes_no.value)
    
    # SET UP AS GLOBAL VAR IN VIZ.PY 
    annotation_limit = 10
    if annotation_limit_change:
        annotation_limit = int(get_text_input('What is the maximum number of annotations you would like on your figure:', 
                                            Format.numeric.value, 
                                            validation=list_of_columns))









# 
# 
    above_thresh = []
    if not annotation_threshold_column:
        above = df[(df['-log10(p)'] >= annotation_threshold) | (df['-log10(p)'] <= -annotation_threshold)]
    else:
        above = df[df[annotation_threshold] == True]
    above = above.sort_values(by=['pvalue'], ascending=True)
    above = above.iloc[:annotation_limit]
    length = len(above.index)
    state = 0
    for i in range(length):
        annot = above.iloc[i]
        offset = determine_offset(state, annot['-log10(p)']>0)
        above_thresh.append(go.layout.Annotation(
                x=annot[x_axis],
                y=annot['-log10(p)'],
                ayref='pixel',
                ay=offset[1],
                axref='pixel',
                ax=offset[0],
                text=annot[annotation_var],
                font=go.layout.annotation.Font(size=10)
        ))
        state = offset[2]
# 
# 







    figure_title = get_text_input('Enter figure title:', 
                                Format.free_text.value)
    marker_size = get_text_input('Choose the corresponding number:', 
                                Format.item_in_list.value, 
                                '\nHow big would you like the data point markers to be? \n 1. Small \n 2. Medium \n 3. Large', 
                                { '1':8, 
                                '2':12, 
                                '3':16 })
    show_legend = get_text_input('Would you like to include a legend in your visualization (yes/no):', 
                                Format.yes_no.value)
    figure_width = get_text_input('The width in pixels:', 
                                Format.numeric.value, 
                                '\nEnter the dimensions for the figure.')
    figure_height = get_text_input('The height in pixels:', 
                                    Format.numeric.value)







# 
# 
    for spec in column_transformations:
        if spec[2]:
            temp = f'.{int(spec[1])}e'
            df[spec[0]] = df[spec[0]].apply(lambda x: format(x, temp))
        else:
            df[spec[0]] = df[spec[0]].apply(lambda x: round(x, -int(math.floor(math.log10(abs(x)))-spec[1] + 1) ))
#     df[y_axis] = df[y_axis].apply(lambda x: format(x,".2e"))    
#     df['effect_estimate'] = df['effect_estimate'].apply(lambda x: -int(math.floor(math.log10(abs(x))) - 2)))
#     df['std_error'] = df['std_error'].apply(lambda x: round(x, -int(math.floor(math.log10(abs(x))) - 2)))












    fig = px.scatter(df, x = x_axis, y = '-log10(p)', color = group,
                    hover_data = show_on_hover,
                    template ='plotly_white',
                    )

    hover_info_list = []
    hover_info_size = len(show_on_hover_titles)
    for i in range(hover_info_size):
        if i != hover_info_size - 1:
            hover_info_list.append(f'{show_on_hover_titles[i]}=%{{customdata[{i}]}}<br>')
        else:
            hover_info_list.append(f'{show_on_hover_titles[i]}=%{{customdata[{i}]}}')
    hover_info_template = ''.join(hover_info_list)

    fig.update_traces(patch=dict(
        hovertemplate=hover_info_template,
        marker={'size': marker_size}
    ))

#     if association_direction:
#         for gr in df[group].unique():
#             fig.update_traces(patch=dict(
#                 legendgroup=gr,
#                 name=gr,
#                 marker={'symbol': list(df[df[group]==gr]['symbol'])},
#             ), selector=dict(
#                 legendgroup=f'{group}={gr}'
#             ))      
#     else:

    for gr in df[group].unique():
        color_hex = fig.select_traces(selector=dict(
            legendgroup=f'{group}={gr}'
        ))
        color_hex = next(color_hex).marker.color.lstrip('#')
        color_rgba = []
        for i in (0, 2, 4):
            color_rgba.append(int(color_hex[i:i+2], 16))
        color_rgba.append(0.5)
        color_rgba = tuple(color_rgba)
        fig.update_traces(patch=dict(
            legendgroup=gr,
            name=gr,
            marker={'color' : f'rgba{color_rgba}', 'line' : {'color' : 'black', 'width' : 2}}
        ), selector=dict(
            legendgroup=f'{group}={gr}'
        ))

#     for gr in df[group].unique():
#         fig.update_traces(patch=dict(
#             legendgroup=gr,
#             name=gr,
#             marker={'opacity' : 0.5, 'line' : {'color' : 'black', 'width' : 2}}
#         ), selector=dict(
#             legendgroup=f'{group}={gr}'
#         ))

    fig.update_layout(
        margin=dict(pad=0),
        title_text = figure_title,
        autosize = False,
        width = figure_width,
        height = figure_height,
        yaxis = go.layout.YAxis(
            title='-log10(p)'
        ),
        xaxis = go.layout.XAxis(
            automargin = True,
            showgrid = False,
            title = x_axis,
            showticklabels = False,
#             tickangle = 60,
#             ticktext = df[group].unique(),
#             tickvals = tick_location,
#             tickfont = go.layout.xaxis.Tickfont(
#                 size = 10
#             )
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

    if association_direction:
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
                    y0=-neg_threshold,
                    x1=df[x_axis].max(),
                    y1=-neg_threshold,
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
                    y0=-neg_threshold,
                    x1=df[x_axis].nunique(),
                    y1=-neg_threshold,
                    line=dict(
                        color="blue",
                        width=1
                    )
                )]
            )
    else:
        if x_numeric:
            fig.update_layout(
                shapes=[
                go.layout.Shape(
                    type="line",
                    x0=0,
                    y0=association_threshold,
                    x1=df[x_axis].max(),
                    y1=association_threshold,
                    line=dict(
                        color="red",
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
                    y0=association_threshold,
                    x1=df[x_axis].nunique(),
                    y1=association_threshold,
                    line=dict(
                        color="red",
                        width=1
                    )
                )]
            )

    get_text_input('Press Enter to review the plot:', 
                            Format.press_enter.value)
    
    fig.show(config={'editable':True, 'displaylogo' : False, 'responsive' : True,
                     'toImageButtonOptions': {
        'format' : 'svg',
#       'format' : 'png',
#       'format' : 'jpeg',
#       'format' : 'pdf',
        'width'  : 2000,
        'height' : 1200
    }, 'showSendToCloud' : True})

    print('You can output this plot in multiple files and formats.')
    export_file = True
    while export_file:
        output_plot_file(fig)
        export_file = get_text_input('Would you like to export this plot to another file (yes/no):',
                        Format.yes_no.value)
#         vis_name = get_text_input('Enter a name for the file that will be exported:', 
#                                 Format.free_text.value)
#         output_format = get_text_input('Enter the number corresponding to the output file format you prefer (intercative features only available with html):', 
#                                     Format.column_name.value, 
#                                     '\n 1. html file \n 2. png \n 3. jpg \n 4. svg \n 5. pdf \n 6. JSON', 
#                                     ['1', '2', '3', '4', '5', '6'])
#         if '1' in output_format:
#             pio.write_html(fig, file = vis_name+'.html', auto_open=True)
#         elif '2' in output_format:
#             pio.write_image(fig, file = vis_name+'.png', format='png')
#         elif '3' in output_format:
#             pio.write_image(fig, file = vis_name+'.jpg', format='jpg')
#         elif '4' in output_format:
#             pio.write_image(fig, file = vis_name+'.svg', format='svg')
#         elif '5' in output_format:
#             pio.write_image(fig, file = vis_name+'.pdf', format='pdf')
#         elif '6' in output_format:
#             pio.write_json(fig, file = vis_name)


if __name__ == "__main__":
    main()
    