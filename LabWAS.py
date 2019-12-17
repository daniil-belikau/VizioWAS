import vizutil 
from vizutil import plot
from vizutil import data 
from vizutil import util


def run(args):
    # path = util.get_text_input('Enter the path to the file containing the data to be visualized:', util.Format.free_text.value)
    # separation_strategy = util.get_text_input('\n 1. Commas \n 2. Tabs \n 3. Pipe \n 4. Other', util.Format.item_in_list.value, 
    #                                     'Enter the number corresponding to the separation strategy of your file:', 
    #                                     { '1': ',', '2': '\t', '3': '|', '4': 'other' })
    # if separation_strategy == 'other':
    #     separation_strategy = util.get_text_input('Specify the separation strategy:', util.Format.free_text.value)
    
    df = data.data_import(args.input_path, args.separation_strategy, True)

    # available_cols = list(df.columns)
    # x_axis = util.get_text_input('Which column contains the values for the x axis:', util.Format.column_name.value, 
    #                         message=f'This is the list of available columns: \n {available_cols}', validation=available_cols)
    # y_axis = util.get_text_input('Which column contains the values for the y axis:', util.Format.column_name.value, 
    #                         validation=available_cols)
    # group = util.get_text_input('Based on which column should the data points be grouped:', util.Format.column_name.value, 
    #                         validation=available_cols)
    # association_direction = util.get_text_input('Would you like to show the association direction in your figure (yes/no):', util.Format.yes_no.value)

    df = data.data_clean(df, [args.x_axis, args.y_axis, args.group], args.y_axis)

    # available_cols = list(df.columns)
    # association_var=''
    # if args.association_var:
    #     association_var = util.get_text_input('Which column determines the direction of association:', util.Format.column_name.value, validation=available_cols)
    df = data.format_yaxis(df, args.y_axis, args.association_var)

    # print('\nNow choose what information you would like to be displayed when hovering over a data point. Press enter after each column name. Enter "done" if you are done specifying the columns.')
    hover_data = plot.assemble_hover_data(args.hover_data)

    if args.neg:
        # pos = util.get_text_input('Enter the -log10(p) for significant positive correlation:', util.Format.numeric.value)
        # neg = util.get_text_input('Enter the -log10(p) for significant negative correlation:', util.Format.numeric.value)
        lines = [(args.pos, 'red'), (-int(args.neg), 'red'), (0, 'lightgrey')]
    else:
        # pos = util.get_text_input('Enter the -log10(p) for significant correlation:', util.Format.numeric.value)
        lines = [(args.pos, 'red'), (0, 'lightgrey')]
    # annotation_threshold_column = util.get_text_input('Do you have a column that determines if a data point should be annotated (yes/no):', util.Format.yes_no.value)
    # if not annotation_threshold_column:
    #     annotation_threshold = util.get_text_input('Enter the -log10(p) threshold for annotating values on the figure:', util.Format.numeric.value)
    # else: 
    #     annotation_threshold = util.get_text_input('Which column column would you like to use for that:', util.Format.column_name.value, validation=available_cols)
    # annotation_var = util.get_text_input('Which column would you like to use to annotate significant points:', util.Format.column_name.value, validation=available_cols)
    # annotation_limit_change = util.get_text_input('The 10 most significant points will be annotated to prevent crowdedness. Would you like to change this limit (yes/no):', util.Format.yes_no.value)
    # annotation_limit = 10
    # if annotation_limit_change:
    #     annotation_limit = int(util.get_text_input('What is the maximum number of annotations you would like on your figure:', util.Format.numeric.value, validation=available_cols))
    # lim = 10 if not args.anlim else args.anlim
    if args.ancol:
        manual = False
        threshold = args.ancol
    else: 
        manual = True
        threshold = args.anthr 
        
    annotations = data.create_annotations(df, args.x_axis, args.y_axis, args.anvar, threshold, args.anlim, manual)

    # title = util.get_text_input('Enter figure title:', util.Format.free_text.value)
    # marker_size = util.get_text_input('Choose the corresponding number:', util.Format.item_in_list.value, '\nHow big would you like the data point markers to be? \n 1. Small \n 2. Medium \n 3. Large', 
    #                             { '1':8, '2':12, '3':16 })
    # show_legend = util.get_text_input('Would you like to include a legend in your visualization (yes/no):', util.Format.yes_no.value)
    # width = util.get_text_input('The width in pixels:', util.Format.numeric.value, '\nEnter the dimensions for the figure.')
    # height = util.get_text_input('The height in pixels:', util.Format.numeric.value)

    df = data.transform_hover_data(df, hover_data[2])

    fig = plot.produce_figure(df, args.x_axis, args.group, hover_data[0])
    fig = plot.customize_markers(fig, df[args.group].unique(), args.group, hover_data[1], args.marker_size, args.crowded_origin)
    fig = plot.customize_layout(fig, args.title, annotations, args.x_axis, args.show_legend, len(df.index), lines, args.association_var)
    
    # util.get_text_input('Press Enter to review the plot:', util.Format.press_enter.value)
    # plot.preview_figure(fig)
    # print('You can output this plot in multiple files and formats.')
    plot.export_plot(fig, args.output_path, args.output_formats, args.width, args.height)
