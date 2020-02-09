import argparse

import LabWAS
import PheWAS


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Produce OmeWAS Visualization.')

    # vis type
    # implement mutually exclusive argument group ?
    parser.add_argument('--vis_type', help='The type of data association study you are trying to visualize.', type=str)
    
    # data impot
    parser.add_argument('--input_path', help='The path to the file containing Summary data.', type=str)
    parser.add_argument('--separation_strategy', help='The symbol used in the data file to separate columns.', type=str)

    # basic df info
    parser.add_argument('--x_axis', help='The name of the column containing the x-axis.', type=str)
    parser.add_argument('--y_axis', help='The name of the column containing the y-axis.', type=str)
    parser.add_argument('--group', help='The name of the column containing the grouping variable.', type=str)
    
    # association_direction is now "'association_var' in args"
    parser.add_argument('--association_var', help='The name of the column containing the variable determining direction of effect.', type=str)
    
    # significance threshold line
    # need only pos if no direction of effect

    # No longer used
    parser.add_argument('--pos', help='Significant -log10(p) for threshold line (positive).', type=float)
    # Used now to determine if negative threshold line should plotted
    parser.add_argument('--neg', help='Significant -log10(p) for threshold line (negative).', type=float)

    # hover data: col_name, col_title, sig_digs, scientific notation
    # column_transformations = (col_name, sigdigs, scienotation)
    # get rid of transform var
    # list comprehension to separate into 3 lists ?
    parser.add_argument('--hover_data', nargs='+', help='List of columns and options to be displayed when hovering over a data point.', type=str)

    # figure setup
    # use some args as flags instead of expectign a value
    parser.add_argument('--title', help='Title of the figure being produced.', type=str)
    parser.add_argument('--x_title', help='Title of the x_axis.', type=str)
    parser.add_argument('--y_title', help='Title of the y_axis.', type=str)
    parser.add_argument('--width', help='Width of the figure.', type=int)
    parser.add_argument('--height', help='Height of the figure.', type=int)
    parser.add_argument('--marker_size', help='Size of data points on the figure (1-20).', type=int)
    parser.add_argument('--crowded_origin', action='store_true', help='Set flag to improve visualization of crowded origin.')
    parser.add_argument('--show_legend', action='store_true', help='Would you like to show the legend on the figure.')

    # export
    # if output_path not set, create default output directory and output there
    # if editable, don't output anything else
    parser.add_argument('--output_path', help='Path for plot output. Include file name, but do NOT include the file extension. ', type=str)
    parser.add_argument('--output_formats', nargs='+', help='Type of file to export the plot in.', type=str)

    # annotations
    # check if annotation limit exists
    # put anthr and ancol in mutually exclusive group
    parser.add_argument('--ancol', help='Name of column used to determine if data point is annotated.', type=str)
    parser.add_argument('--anvar', help='Name of column used to annotate significant data points.', type=str)
    parser.add_argument('--anlim', help='Maximum number of annotations per figure.', type=int)


    args = parser.parse_args()
    
    if args.vis_type == 'lab':
        LabWAS.run(args)

    elif args.vis_type == 'phenome':
        PheWAS.run(args)
    