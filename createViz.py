import argparse

import OmeWAS


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Produce OmeWAS Visualization.')

    parser.add_argument('--vis_type', help='The type of data association study you are trying to visualize.', type=str)

# import
    parser.add_argument('--input_path', help='The path to the file containing Summary data.', type=str)
    parser.add_argument('--separation_strategy', help='The symbol used in the data file to separate columns.', type=str)

# dataframe setup
    parser.add_argument('--x_axis', help='The name of the column containing the x-axis.', type=str)
    parser.add_argument('--y_axis', help='The name of the column containing the y-axis.', type=str)
    parser.add_argument('--group', help='The name of the column containing the grouping variable.', type=str)
    parser.add_argument('--association_var', help='The name of the column containing the variable determining direction of effect.', type=str)

# No longer used
    parser.add_argument('--pos', help='Significant -log10(p) for threshold line (positive).', type=float)
    parser.add_argument('--neg', action='store_true', help='Would you like to plot a threshold line for negative direction of effect.')

# hover data: col_name, col_title, sig_digs, scientific notation
    parser.add_argument('--hover_data', nargs='+', help='List of columns and options to be displayed when hovering over a data point.', type=str)

# figure setup
    parser.add_argument('--title', default='ViziOWAS Figure', help='Title of the figure being produced.', type=str)
    parser.add_argument('--x_title', help='Title of the x_axis.', type=str)
    parser.add_argument('--y_title', help='Title of the y_axis.', type=str)
    parser.add_argument('--width', default=900, help='Width of the figure.', type=int)
    parser.add_argument('--height', default=600, help='Height of the figure.', type=int)
    parser.add_argument('--marker_size', default=14, help='Size of data points on the figure (1-30).', type=int)
    parser.add_argument('--crowded_origin', action='store_true', help='Set flag to improve visualization of crowded origin.')
    parser.add_argument('--show_legend', action='store_true', help='Would you like to show the legend on the figure.')

# export
    parser.add_argument('--output_path', default='./viziowas_figure', help='Path for plot output. Include file name, but do NOT include the file extension. ', type=str)
    parser.add_argument('--output_formats', default='studio', nargs='+', help='Type of file to export the plot in.', type=str)

# annotations
    parser.add_argument('--ancol', help='Name of column used to determine if data point is annotated.', type=str)
    parser.add_argument('--anvar', help='Name of column used to annotate significant data points.', type=str)
    parser.add_argument('--anlim', help='Maximum number of annotations per figure.', type=int)


    args = parser.parse_args()
    
    if args.vis_type and args.input_path and args.separation_strategy and args.x_axis and args.y_axis and args.group:
        OmeWAS.run(args)
    else:
        print("Specify the required arguments:")
        print("vis_type, input_path, separation_strategy, x_axis, y_axis, group, ancol")
    