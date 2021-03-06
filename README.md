# VizioWAS
ViziOWAS is a command line-based tool for creating interactive and static visualizations of your -omics association scan results (e.g., results from your phenome-wide association scan (PheWAS) or lab-wide association scan (LabWAS)).

## Sample Output On A PheWAS Dataset
![Sample Output Image](https://github.com/daniil-belikau/VizioWAS/blob/sample_image/codemin1_control_exclusions_F_pre_2019-11-04_cov_min_case_25.png?raw=true)
[Click here for an interactive version of the plot.](https://dennislabvisualizations.github.io/codemin1_control_exclusions_F_pre_2019-11-04_cov_min_case_25/)

## Prerequisites
Tested in Mac and Linux environments.

Developed for use with [Python 3.7](https://www.python.org/), and the following packages used:
* [pandas (*>*=0.24.2 recommended)](http://pandas.pydata.org/)
* [plotly (*>*=4.6.0 recommded)](https://plot.ly/python/)

## Using VizioWAS

### Getting Started

1) Install all prerequisite packages.

2) Clone the repository.
```bash
$ git clone https://github.com/daniil-belikau/VizioWAS.git
```

3) Change working directory to VizioWAS.
```bash
$ cd VizioWAS
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

### Argument Specification

The following is the list of available command line arguments (make sure to enclose multi-word arguments in quotation marks):
* **--vis_type** *<*type*>* Type of summary stats being visualized. Can be *lab* or *phenome*.
* **--input_path** *<*path*>* Path to file containing summary stat data (tested with .txt and .csv files). *Note: the file should not contain any pvalues that will be imported into python as 0.*
* **--separation_strategy** *<*strat*>* Specify the delimiter used in the data file ('\t', '\s', ',').
* **--x_axis** *<*name*>* Name of the x_axis, as it appears in the given file.
* **--y_axis** *<*name*>* Name of the y_axis, as it appears in the given file.
* **--group** *<*name*>* Name of the grouping column, as it appears in the given file.
* **--association_var** *<*name*>* Name of the column that determines direction of effect. Direction of effect not shown, if this arg is not specified.
* **--neg** Setting this flag plots a Bonferonni threshold line for negative direction of effect.
* **--hover_data** (*<*column_name*>* *<*displayed_name*>* *<*sig_figs*>* *<*scientific_notation*>*)+ Specify what is displayed when hovering over a datapoint in the interactive visualization. Takes a multiple of four arguments, in the order specified here. sig_figs are specified with an integer, or an *n* if you wish to not set them. Scientific notation is set with a *y* or *n*.
* **--title** *<*title*>* Title of the plot.
* **--x_title** *<*title*>* Title of the x_axis.
* **--y_title** *<*title*>* Title of the y_axis.
* **--width** *<*width*>* Width of the figure.
* **--height** *<*height*>* Height of the figure.
* **--marker_size** *<*size*>* Size of data point markers (1 - 30).
* **--crowded_origin** If the flag is set, the black border around data points is replaced with a grey one.
* **--show_legend** If the flag is set, the legend for the plot is added on the right side of the figure.
* **--output_path** *<*path*>* The path to the directory including the file name (without format extension), where the output file should be wrtitten.
* **--output_format** (*<*format*>*)+ All formats in which the figure should be saved. Allowed values are: *studio*, *html*, *png*, *jpg*, *svg*, *pdf*, *json*.
* **--ancol** *<*name*>* If the input file contains a column that determines whether a data point is significant, specify this argument. If not specified, Bonferonni corrected p-values will be used.
* **--anvar** *<*name*>* Name of column used to annotate significant points.
* **--anlim** *<*limit*>* The maximum number of annotations per figure. If not specified, unlimited annotationspermitted.

#### Required Arguments:

* **--vis_type**
* **--input_path**
* **--separation_strategy**
* **--x_axis**
* **--y_axis**
* **--group**

### Editing figures

If the automatically generated figures are not satisfactory (e.g. overlapping annotations), they can be edited manually. Note however, that this requires **making your figure public**. To edit figures manually:

1) Specify **--output_format** to be *studio*.

2) Locate the html file generated from that script call and open it.
   
   *If you only need a static image of the plot, once the file is opened, adjust the plot using the mouse. Then click the camera button on the upper right hand corner of the figure to get the modified plot image. Skip the rest of the instructions.*

3) On the upper right hand corner of the figure, find and press the *edit in chart studio* button (icon showing a floppy disk).

4) A new tab with an online editing studio will be opened, containing the figure. Most aspects of the figure can be edited here in a visual and interactive way, inlcuding annotation placement.

5) Once all the edits are done, the figure needs to be saved. Click the blue *Save* button on the left sidebar.

6) Name the plot, and set the privacy selector to **Public**, then press *Save*.

7) To export the edited figure, click *Export* on the left sidebar, and choose *Image* for static plot or *HTML* for an interactive plot. When creating a static plot, to ensure that it is high quality, adjust the scale factor to *2x* or *3x*.

### Example

You can try using VizioWAS with the sample data and arguments provided in the *Example* directory:

1) Open a command-line window and navigate to the VizioWAS directory.

2) Open the *test_args.txt* file inside the *Example* directory and copy one of the two sample calls (starting with python3 and ending with an empty line).

3) Paste the text into your command-line window and run.

4) You can find the output figures in the *Example/Output* directory. The input data can be found in the *Example/Data* directory.

## Hosting

If you plan to host your interactive visualizations, [here](https://github.com/daniil-belikau/VizioWAS/blob/master/GHP%20Visualization%20Hosting%20Tutorial.pdf) is a guide to do it for free with GitHub Pages.

