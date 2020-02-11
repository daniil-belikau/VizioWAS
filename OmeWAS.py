from vizutil import data, plot


def run(args):
    shuffle = True if args.vis_type == 'lab' else False
    df = data.data_import(args.input_path, args.separation_strategy, shuffle)
    df = data.data_clean(df, [args.x_axis, args.y_axis, args.group], args.y_axis)
    df = data.format_yaxis(df, args.y_axis, args.association_var)

    hover_data = plot.assemble_hover_data(args.hover_data) if args.hover_data else None

    bonferroni_threshold = data.bonferroni(df, args.y_axis)
        
    if args.ancol:
        manual = False
        threshold = args.ancol
    else: 
        manual = True
        threshold = bonferroni_threshold
    
    if args.neg:
        lines = [(bonferroni_threshold, 'red'), (-bonferroni_threshold, 'red'), (0, 'lightgrey')]
    else:
        lines = [(bonferroni_threshold, 'red'), (0, 'lightgrey')]
        
    annotations = data.create_annotations(df, args.x_axis, args.y_axis, args.anvar, threshold, args.anlim, manual)
    
    if hover_data:
        df = data.transform_hover_data(df, hover_data[2])

    x_title = args.x_title if args.x_title else args.x_axis
    y_title = args.y_title if args.y_title else '-log10(p) x Direction of Effect'

    
    fig = plot.produce_figure(df, args.x_axis, args.group, hover_data)
    fig = plot.customize_markers(fig, df[args.group].unique(), args.group, hover_data, args.marker_size, args.crowded_origin)

    spec = (len(df.index), False) if args.vis_type == 'lab' else (df[args.x_axis].max(), True)
    fig = plot.customize_layout(fig, args.title, annotations, args.x_axis, args.show_legend, spec[0], x_title, y_title, lines, spec[1])
    
    plot.export_plot(fig, args.output_path, args.output_formats, args.width, args.height)
