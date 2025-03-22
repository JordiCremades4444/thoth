## =====================================
## Pivot
## =====================================

pivot_params = {
    "df": df,
    "t": "X",
    "dimensions": ["X", "X"],
    "measures": ["X", "X"],
    "aggfuncs": ["X", "X"],
}

p = dataframe_tools.Pivot(df, pivot_params).run_pivot()

## =====================================
## Plotter
## =====================================

dataframe_tools.Plotter(
    dfp, plot_params=plot_params, figure_params=figure_params
).run_plotter()

figure_params = {
    "n_plots": 1,
    "fig_length": 10,
    "fig_height": 6,
    "x_rotation": 45,
    "share_x": False,
    "share_y": False,
    "x_limits": None,  # [(X, X)]
    "y_limits": None,  # [(X, X)]
    "log_axis": None,  # ['x', 'y', 'both']
    "title": None,
}

# Lineplot
plot_params = [
    {
        "plot_type": "lineplot",
        "x_column": [1],
        "y_columns": [2, 3],
        "colors": ["b", "o"],  # ['o','g','r','pu','br','pi','gr','ol','cy']
        "styles": ["-", "-"],  # ['--'. '-', ':']
        "legend": True,
    },
]

# Scatterplot
plot_params = [
    {
        "plot_type": "scatterplot",
        "x_column": [1],
        "y_columns": [2, 3],
        "colors": ["b", "o"],  # ['o','g','r','pu','br','pi','gr','ol','cy']
        "legend": True,
    },
]

# Histogram
plot_params = [
    {
        "plot_type": "histogram",
        "y_columns": [2, 3],
        "colors": ["b", "o"],  # ['o','g','r','pu','br','pi','gr','ol','cy']
        "legend": True,
        "bins": 10,
    },
]

# Histogram Accumulated
plot_params = [
    {
        "plot_type": "histogram_accumulated",
        "y_columns": [2, 3],
        "colors": ["b", "o"],  # ['o','g','r','pu','br','pi','gr','ol','cy']
        "legend": True,
        "bins": 10,
    },
]
