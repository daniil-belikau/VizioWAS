import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

from . import util


# can export html with toImageButton toggled to produce static plots after adjusting annotations
def output_plot_file(figure):
    file_name = util.get_text_input('Enter a name for the file that will be exported:', util.Format.free_text.value)
    output_format = util.get_text_input('Enter the number corresponding to the output file format you prefer (interactive features only available with html):', util.Format.column_name.value, '\n 1. html file \n 2. png (small file, but lower image quality) \n 3. jpg (small file, but lower image quality) \n 4. svg \n 5. pdf \n 6. JSON', ['1', '2', '3', '4', '5', '6'])
    if '1' in output_format:
        pio.write_html(figure, file = file_name+'.html')
    elif '2' in output_format:
        pio.write_image(figure, file = file_name+'.png', format='png')
    elif '3' in output_format:
        pio.write_image(figure, file = file_name+'.jpg', format='jpg')
    elif '4' in output_format:
        pio.write_image(figure, file = file_name+'.svg', format='svg')
    elif '5' in output_format:
        pio.write_image(figure, file = file_name+'.pdf', format='pdf')
    elif '6' in output_format:
        pio.write_json(figure, file = file_name)

    # pio.write_html(figure, file = file_name+'.html', config={'editable':True, 'displaylogo' : False, 'responsive' : True,
    #                     'toImageButtonOptions': {
    #         'format' : 'svg',
    # #       'format' : 'pgn',
    # #       'format' : 'jpeg',
    # #       'format' : 'pdf',
    #         'width'  : 2000,
    #         'height' : 1200
    #     }, 'showSendToCloud' : True})


def assemble_hover_data(columns):
    columns.append('done')
    hover_cols = []
    hover_cols_titles = []
    hover_cols_transformations = []
    while True:
        col_name = util.get_text_input('Enter the next column or "done" if you are finished:', util.Format.column_name.value, validation=columns)
        if col_name == 'done': break
        col_title = util.get_text_input('Enter the name that this column will be displayed under:', util.Format.free_text.value)
        transform = util.get_text_input('Do you want to specify a number of signigicant digits or scientific notation for this column (yes/no):', util.Format.yes_no.value)
        if transform:
            sig_digs = util.get_text_input('Would you like to set a number of significant digits (yes/no):', util.Format.yes_no.value)
            if sig_digs:
                sig_digs = util.get_text_input('How many significant digits would you like to show for this column:', util.Format.numeric.value)
            scientific_notation = util.get_text_input('Would you like to show this column using scientific notation (yes/no):', util.Format.yes_no.value)
            hover_cols_transformations.append((col_name, sig_digs, scientific_notation))
        hover_cols.append(col_name)
        hover_cols_titles.append(col_title)
    columns.remove('done')
    list_length = len(hover_cols_titles)
    hover_template = [f'{col}=%{{customdata[{i}]}}<br>' if i != list_length - 1 else f'{col}=%{{customdata[{i}]}}' for i, col in enumerate(hover_cols_titles)]
    hover_str = ''.join(hover_template)

    return hover_cols, hover_str, hover_cols_transformations


def produce_figure(df, x_axis, group, hover_cols):
    return px.scatter(df, x=x_axis, y='y', color=group, hover_data=hover_cols, template='plotly_white')


def customize_markers(fig, unique_groups, group, hover_template, marker_size):
    for gr in unique_groups:
        trace = fig.select_traces(selector={'legendgroup' : f'{group}={gr}'})
        color_hex = next(trace).marker.color.lstrip('#')
        color_rgba = tuple([int(color_hex[i:i+2], 16) if i != 1 else 0.5 for i in (0,2,4,1)])
        fig.update_traces(patch={
            'hovertemplate' : hover_template,
            'legendgroup' : gr,
            'name' : gr,
            'marker' : {'color' : f'rgba{color_rgba}', 'line' : {'color' : 'black', 'width' : 2}, 'size' : marker_size}
        }, selector={
            'legendgroup' : f'{group}={gr}'
        })
    return fig


def customize_layout(fig, title, annotations, x_axis, show_legend, x_max, auto_size=True, width=1600, height=1200, lines=[], corr_dir=True):
    layout = {
        'title_text' : title,
        'yaxis' : go.layout.YAxis(title='-log10(p)'),
        'xaxis' : go.layout.XAxis(automargin=True, showgrid=False, title=x_axis, showticklabels=False),
        'showlegend' : show_legend,
        'legend' : go.layout.Legend(font = {'size' : 10}, itemclick='toggleothers', itemdoubleclick='toggle', tracegroupgap=1),
        'annotations' : annotations
    }
    if not auto_size:
        layout['width'] = width
        layout['height'] = height
    if corr_dir:
        layout['shapes'] = [go.layout.Shape(type='line', x0=0, x1=x_max, y0=l[0], y1=l[0], line={'color':l[1], 'width':1}) for l in lines]
    fig.update_layout(layout)
    return fig


def preview_figure(fig):
    fig.show(config={
        'editable':True, 
        'displaylogo' : False, 
        'responsive' : True,
        'toImageButtonOptions': {'format' : 'pdf', 'width'  : 2000, 'height' : 1200}, 
        'showSendToCloud' : True})


def export_plot(fig):
    export_file = True
    while export_file:
        output_plot_file(fig)
        export_file = util.get_text_input('Would you like to export this plot to another file (yes/no):', util.Format.yes_no.value)
