import sys
import pandas as pd
import plotly.graph_objects as go
import math


def determine_offset(state, y_positive):
    if state == 0:
        return (-25, -4, 1) if y_positive else (-25, 4, 1)
    elif state == 1:
        return (0, -15, 2) if y_positive else (0, 15, 2)
    elif state == 2:
        return (25, -4, 0) if y_positive else (25, 4, 0)


def data_import(data_path, separation_strategy, shuffle=False):
    try:
        df = pd.read_csv(data_path, sep=separation_strategy)
        return df.sample(frac=1).reset_index(drop=True) if shuffle else df
    except:
        print('Unable to import data. Check that the file path and separation strategy are correct!')
        sys.exit()


def data_clean(df, mandatory, y_axis):
    df.dropna(axis=0, subset=mandatory, inplace=True)
    df.dropna(axis=1, how='all', inplace=True)
    if len(df[df[y_axis] == 0].index) > 0:
        print('Please make sure there are no P-values equal to 0 in your data.')
        sys.exit()
    return df

    # Possible mechanism to fix this
    # df[y_axis] = df[df[y_axis].isna() == False][y_axis].apply(lambda y: y if y != 0 else sys.float_info.min)


def format_yaxis(df, y_axis, association_var):
    if association_var:
        stat = 0 if 'beta' in association_var.lower() else 1
        df['y'] = df.apply(lambda x: -math.log10(x[y_axis]) if x[association_var] > stat else math.log10(x[y_axis]), axis=1)
    else:
        df['y'] = df[y_axis].apply(lambda x: -math.log(x, 10))
    return df


def place_x_ticks(df, group, numeric, x_axis=''):
    if numeric:
        tick_labels = []
        # return [(group, df[df[group] == group][x_axis].mean()) for group in df[group].unique()]
        for unique_group in df[group].unique():
            tick_labels.append(df[df[group] == unique_group][x_axis].mean())
    else:
        tick_labels = []
        tick_dict = dict.fromkeys(df['group'].unique(), 0)
        # for unique_group in df[group].unique():
        #     tick_dict[unique_group] = 0
        for row in df.iterrows():
            tick_dict[row[group]] += 1
        prev = 0
        for key in tick_dict.keys():
            tick_dict[key] += prev
            tick_labels.append((str(key), (prev + tick_dict[key])/2))
            prev = tick_dict[key]
    return tick_labels


def create_annotations(df, x_axis, y_axis, annotation_col, threshold, limit, manual=False):
    annotations = []
    above_thresh = df[(df['y'] >= threshold) | (df['y'] <= -threshold)] if manual else df[df[threshold] == True]
    above_sorted = above_thresh.sort_values(by=[y_axis], ascending=True)
    if limit: above_sorted = above_sorted.iloc[:limit]
    state = 0
    for index in range(len(above_sorted.index)):
        annot = above_sorted.iloc[index]
        offset = determine_offset(state, annot['y']>0)
        annotations.append(go.layout.Annotation(
                x=annot[x_axis],
                y=annot['y'],
                ayref='pixel',
                ay=offset[1],
                axref='pixel',
                ax=offset[0],
                text=annot[annotation_col],
                font=go.layout.annotation.Font(size=12)
        ))
        state = offset[2]
    return annotations


def bonferroni(df, y_axis):
    n = df.shape[0]
    correction = 0.05 / n
    threshold = -math.log10(correction)
    return threshold


def transform_hover_data(df, transformations):
    for tupl in transformations:
        if tupl[2]:
            temp = f'.{int(tupl[1])}e'
            df[tupl[0]] = df[tupl[0]].apply(lambda x: format(x, temp))
        else:
            df[tupl[0]] = df[tupl[0]].apply(lambda x: round(x, -int(math.floor(math.log10(abs(x)))-tupl[1] + 1) ))
    return df

