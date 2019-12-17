import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import os

from . import util


# can export html with toImageButton toggled to produce static plots after adjusting annotations
def output_plot_file(figure, path, output_format, width=900, height=600):
    # file_name = util.get_text_input('Enter a name for the file that will be exported:', util.Format.free_text.value)
    # output_format = util.get_text_input('Enter the number corresponding to the output file format you prefer (interactive features only available with html):', util.Format.column_name.value, '\n 1. html file \n 2. png (small file, but lower image quality) \n 3. jpg (small file, but lower image quality) \n 4. svg \n 5. pdf \n 6. JSON', ['1', '2', '3', '4', '5', '6'])
    if 'studio' in output_format:
        pio.write_html(figure, file = path+'.html', config={
            'editable':True, 
            'displaylogo' : False, 
            'showSendToCloud' : True,
            'toImageButtonOptions': {
                'format' : 'png',
                'width'  : 900,
                'height' : 600,
                'scale'  : 6
            }})
    elif 'html' in output_format:
        pio.write_html(figure, file = path+'.html')
    elif 'png' in output_format:
        pio.write_image(figure, file = path+'.png', format='png', width=width, height=height, scale=6)
    elif 'jpg' in output_format:
        pio.write_image(figure, file = path+'.jpg', format='jpg', width=width, height=height, scale=6)
    elif 'svg' in output_format:
        pio.write_image(figure, file = path+'.svg', format='svg', width=width, height=height)
    elif 'pdf' in output_format:
        pio.write_image(figure, file = path+'.pdf', format='pdf', width=width, height=height)
    elif 'json' in output_format:
        pio.write_json(figure, file = path)

    # pio.write_html(figure, file = file_name+'.html', config={'editable':True, 'displaylogo' : False, 'responsive' : True,
    #                     'toImageButtonOptions': {
    #         'format' : 'svg',
    # #       'format' : 'pgn',
    # #       'format' : 'jpeg',
    # #       'format' : 'pdf',
    #         'width'  : 2000,
    #         'height' : 1200
    #     }, 'showSendToCloud' : True})


def assemble_hover_data(hover_pref):
    # columns.append('done')
    hover_cols = [hover_pref[i] for i in range(0, len(hover_pref), 4)]
    # hover_cols_titles = [hover_pref[i] for i in range(1, len(hover_pref), 4)]

    # Make sure that the check catches all cases
    hover_cols_transformations = [(hover_pref[i], int(hover_pref[i+2]), hover_pref[i+3]=='y') for i in range(0, len(hover_pref), 4) if not hover_pref[i+2] == 'n']
    # while True:
    #     col_name = util.get_text_input('Enter the next column or "done" if you are finished:', util.Format.column_name.value, validation=columns)
    #     if col_name == 'done': break
    #     col_title = util.get_text_input('Enter the name that this column will be displayed under:', util.Format.free_text.value)
    #     transform = util.get_text_input('Do you want to specify a number of signigicant digits or scientific notation for this column (yes/no):', util.Format.yes_no.value)
    #     if transform:
    #         sig_digs = util.get_text_input('Would you like to set a number of significant digits (yes/no):', util.Format.yes_no.value)
    #         if sig_digs:
    #             sig_digs = util.get_text_input('How many significant digits would you like to show for this column:', util.Format.numeric.value)
    #         scientific_notation = util.get_text_input('Would you like to show this column using scientific notation (yes/no):', util.Format.yes_no.value)
    #         hover_cols_transformations.append((col_name, sig_digs, scientific_notation))
    #     hover_cols.append(col_name)
    #     hover_cols_titles.append(col_title)
    # columns.remove('done')
    list_length = len(hover_pref)/4
    hover_template = [f'{hover_pref[i]}=%{{customdata[{index}]}}<br>' if index != list_length - 1 else f'{hover_pref[i]}=%{{customdata[{index}]}}' for index, i in enumerate(range(1, len(hover_pref), 4))]
    hover_str = ''.join(hover_template)

    return hover_cols, hover_str, hover_cols_transformations


def produce_figure(df, x_axis, group, hover_cols):
    return px.scatter(df, x=x_axis, y='y', color=group, hover_data=hover_cols, template='plotly_white')


def customize_markers(fig, unique_groups, group, hover_template, marker_size, crowded_origin):
    for gr in unique_groups:
        trace = fig.select_traces(selector={'legendgroup' : f'{group}={gr}'})
        color_hex = next(trace).marker.color.lstrip('#')
        color_rgba = tuple([int(color_hex[i:i+2], 16) if i != 1 else 0.5 for i in (0,2,4,1)])
        if crowded_origin:
            color = {'color' : f'rgba{color_rgba}', 'line' : {'color' : 'lightgrey', 'width' : 1}, 'size' : marker_size}
        else:
            color = {'color' : f'rgba{color_rgba}', 'line' : {'color' : 'black', 'width' : 2}, 'size' : marker_size}
        fig.update_traces(patch={
            'hovertemplate' : hover_template,
            'legendgroup' : gr,
            'name' : gr,
            'marker' : color
        }, selector={
            'legendgroup' : f'{group}={gr}'
        })
    return fig


def customize_layout(fig, title, annotations, x_axis, show_legend, x_max, lines=[], corr_dir=True):
    layout = {
        'title_text' : title,
        'yaxis' : go.layout.YAxis(showgrid=False, zeroline=False, title='-log10(p) x Direction of Effect'),
        'xaxis' : go.layout.XAxis(automargin=True, showgrid=False, title=x_axis, showticklabels=False),
        'showlegend' : show_legend,
        'legend' : go.layout.Legend(font = {'size' : 10}, itemclick='toggleothers', itemdoubleclick='toggle', tracegroupgap=1, orientation='h'),
        'annotations' : annotations
    }
    layout['shapes'] = [go.layout.Shape(type='line', x0=0, x1=x_max, y0=l[0], y1=l[0], line={'color':l[1], 'width':2}, layer='below') for l in lines]
    fig.update_layout(layout)
    return fig


def preview_figure(fig):
    fig.show(config={
        'editable':True, 
        'displaylogo' : False, 
        'responsive' : True,
        'toImageButtonOptions': {'format' : 'pdf', 'width'  : 2000, 'height' : 1200}, 
        'showSendToCloud' : True})


# if no directory specified, add default directory
def export_plot(fig, path, formats, width, height):
    # os.mkdir('plot_output')
    for f in formats:
        output_plot_file(fig, path, f, width, height)
    # export_file = util.get_text_input('Would you like to export this plot to another file (yes/no):', util.Format.yes_no.value)
