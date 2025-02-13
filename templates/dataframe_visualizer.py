v = dataframe_visualizer.DataFrameVisualizer(df)

plot_params = [
    {
        "plot_type": "lineplot",
        "x_column": "XXX",
        "y_columns": ["XXX", "XXX"],
        "colors": ["orange","blue",],  # blue, orange, green, red, purple, brown, pink, gray, olive, cyan
        "styles": ["-", "-"],  # -, --, :
        "legend": True,
        },
        {
        "plot_type": "scatterplot",
        "x_column": "XXX",
        "y_columns": ["XXX", "XXX"],
        "colors": ["orange","blue",],  # blue, orange, green, red, purple, brown, pink, gray, olive, cyan
        "legend": True,
        },
        {
        "plot_type": "barplot",
        "x_column": "XXX",
        "y_columns": ["XXX", "XXX"],
        "colors": ["orange","blue",],  # blue, orange, green, red, purple, brown, pink, gray, olive, cyan
        "legend": True,
        "bar_width": 0.8,
        },
        {
        "plot_type": "histogram",
        "y_columns": ["XXX", "XXX"],
        "colors": ["orange","blue",],  # blue, orange, green, red, purple, brown, pink, gray, olive, cyan
        "legend": True,
        "bins": 10,
        },
        {
        "plot_type": "histogram_acummulated",
        "y_columns": ["XXX", "XXX"],
        "colors": ["orange","blue",],  # blue, orange, green, red, purple, brown, pink, gray, olive, cyan
        "legend": True,
        "bins": 10,
        },
        {
        # default LB = Q1 - 1.5*IQR, UB = Q3 + 1.5*IQR
        # IQR = Q3 - Q1, Q1 = 25th percentile, Q3 = 75th percentile
        "plot_type": "boxplot_and_whiskers",
        "y_columns": ["XXX", "XXX"],
        "colors": ["orange","blue",],  # blue, orange, green, red, purple, brown, pink, gray, olive, cyan
        "legend": True,
        },
]

figure_params = {
    'n_plots': 1,
    'fig_length': 10,
    'fig_height': 6,
    'x_rotation': 45,
    'share_x': False,
    'share_y': False,
    'x_limits': None, # [(0,100),(0,1000)]
    'y_limits': None, # [(0,100),(0,1000)]
    'log_axis': None, # 'x', 'y', 'both'
    'title': 'XXX'
}

# Call the plot method to handle the entire flow
v.plot(
    figure_params=figure_params,
    plot_params=plot_params
)
