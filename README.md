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

The following is the list of available command line arguments:
* **--vis_type** type of summary stats being visualized. Can be *lab* or *phenome*
* **--input_path** path to file containing summary stat data (tested with .txt and .csv files)
* **--separation_strategy** specify the delimiter used in the data file (*'\t'*, *'\s'*, *','*)
* **--x_axis** name of the x_axis, as it appears in the given file
* **--y_axis** name of the y_axis, as it appears in the given file
* **--group** name of the grouping column, as it appears in the given file

