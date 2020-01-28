# ViziOWAS
ViziOWAS is a command line based tool for creating interactive and static visualizations of PheWAS, LabWAS summary statistics.

## Prerequisites
Tested in Mac and Linux environments.

Written for use with [Python 3.7](https://www.python.org/), and the following packages used:
* [pandas (>=0.24.2 recommended)](http://pandas.pydata.org/)
* [plotly (>=4.1.1 recommded)](https://plot.ly/python/)

## Usage

### Getting Started

1) Install all prerequisite packages.

2) Clone the repository
```bash
$ git clone https://github.com/daniil-belikau/ViziOWAS.git
```

3) Change working directory to ViziOWAS
```bash
$ cd ViziOWAS
```

4) Run script with appropriate options to produce visualization file(s).
```bash
$ python3 createViz.py \
--vis_type phenome \
--input_path '../codemin1_phewas/data/codemin1_control_exclusions_F_pre_2019-11-04_cov_min_case_25.txt' \
--separation_strategy '\t' \
--x_axis phecode \
--y_axis p \
--group group \
--association_var or \
--hover_data phecode 'Phecode' n n description 'Description' n n p 'P-value' 3 y lci "Lower Confidence Interval" 3 n uci "Upper Confidence Interval" 3 n or "Odds Ratio" 3 n \
--title 'codemin1_control_exclusions_F_pre_2019-11-04_cov_min_case_25 PheWAS' \
--width 900 \
--height 600 \
--marker_size 14 \
--show_legend \
--output_path '../codemin1_phewas/output/codemin1_control_exclusions_F_pre_2019-11-04_cov_min_case_25' \
--output_formats 'studio' \
--anvar 'description'
```

### Legal Arguments

The following is the list of available command line arguments (make sure to enclose multi-word arguments in quotation marks):
* **--vis_type** <type> Type of summary stats being visualized. Can be *lab* or *phenome*.
* **--input_path** <path> Path to file containing summary stat data (tested with .txt and .csv files).
* **--separation_strategy** <strat> Specify the delimiter used in the data file (*'\t'*, *'\s'*, *','*).
* **--x_axis** <name> Name of the x_axis, as it appears in the given file.
* **--y_axis** <name> Name of the y_axis, as it appears in the given file.
* **--group** <name> Name of the grouping column, as it appears in the given file.
* **--association_var** <name> Name of the column that determines direction of effect. Direction of effect not shown, if this arg is not specified.
* **--neg** Setting this flag plots a Bonferonni threshold line for negative direction of effect.
* **--hover_data** (<column_name> <displayed_name> <sig_figs> <scientific_notation>)+ Specify what is displayed when hovering over a datapoint in the interactive visualization. Takes a multiple of four arguments, in the order specified here. sig_figs are specified with an integer, or an *n* if you wish to not set them. Scientific notation is set with a *y* or *n*.
* **--title** <title> Title of the plot.
* **--width** <width> Width of the figure.
* **--height** <height> Height of the figure.
* **--marker_size** <size> Size of data point markers (1 - 30).
* **--crowded_origin** If the flag is set, the black border around data points is replaced with a grey one.
* **--show_legend** If the flag is set, the legend for the plot is added on the right side of the figure.
* **--output_path** <path> The path to the directory including the file name (without format extension), where the output file should be wrtitten.
* **--output_format** (<format>)+ All formats in which the figure should be saved. Allowed values are: *studio*, *html*, *png*, *jpg*, *svg*, *pdf*, *json*.
* **--ancol** <name> If the input file contains a column that determines whether a data point is significant, specify this argument. If not specified, Bonferonni significance test will be performed on the dataset.
* **--anvar** <name> Name of column used to annotate significant points.
* **--anlim** <limit> The maximum number of annotations per figure. If not specified, unlimited annotationspermitted.

