import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class Pivot:
    """
    A class to pivot and aggregate a DataFrame.
    """

    def __init__(self, df, pivot_params):
        self.df = df
        self.index = pivot_params["index"]
        self.columns = pivot_params["columns"]
        self.values = pivot_params["values"]
        self.aggfuncs = pivot_params["aggfuncs"]

    def __try_datetime_conversion(self, index):
        try:
            self.df[index] = pd.to_datetime(self.df[index])
        except (ValueError, TypeError, KeyError):
            pass

    def __flatten_multi_index_columns(self, pivot_table):
        pivot_table.columns = [
            "__".join(map(str, col)).strip() for col in pivot_table.columns.values
        ]

        return pivot_table

    def __resolve_column_names(self, column_references):
        resolved_columns = []

        for column_reference in column_references:
            if isinstance(column_reference, int):  # If it's an index
                resolved_columns.append(
                    self.df.columns[column_reference - 1]
                )  # Convert 1-based index to 0-based
            else:
                resolved_columns.append(
                    column_reference
                )  # If it's already a column name

        return resolved_columns

    def __validate_columns(self, columns):
        missing_cols = [col for col in columns if col not in self.df.columns]
        if missing_cols:
            raise ValueError(f"Columns {missing_cols} not found in the dataframe.")

    def __validate_aggfuncs(self):
        for func in self.aggfuncs:
            if func not in ["sum", "mean", "median", "min", "max"]:
                raise ValueError(
                    f"Invalid aggregation function '{func}'. Valid options are: ['sum', 'mean', 'median', 'min', 'max']"
                )

    def run_pivot(self):
        self.index = self.__resolve_column_names(self.index)
        self.index = self.index[0]
        self.columns = self.__resolve_column_names(self.columns)
        self.values = self.__resolve_column_names(self.values)

        self.__validate_columns([self.index] + self.columns + self.values)

        self.__validate_aggfuncs()

        self.__try_datetime_conversion(self.index)

        pivot_table = pd.pivot_table(
            self.df,
            values=self.values,
            index=self.index,
            columns=self.columns,
            aggfunc=self.aggfuncs,
        )

        df_pivoted = self.__flatten_multi_index_columns(pivot_table)

        df_pivoted.reset_index(inplace=True)

        df_pivoted.sort_values(by=self.index, inplace=True)

        return df_pivoted


class Plotter:
    """
    Class to plot dataframes.
    """

    def __init__(self, df, plot_params=None, figure_params=None):
        self.df = df

        # --------------------------------#
        # - Plot parameters               #
        # --------------------------------#

        self.colors = {
            "b": "#1f77b4",
            "o": "#ff7f0e",
            "g": "#2ca02c",
            "r": "#d62728",
            "pu": "#9467bd",
            "br": "#8c564b",
            "pi": "#e377c2",
            "gr": "#7f7f7f",
            "ol": "#bcbd22",
            "cy": "#17becf",
        }
        self.styles = {"-": "-", "--": "--", ":": ":"}

        self.default_plot_params = {
            "plot_type": "lineplot",
            "x_column": [1],  # Default to the first column
            "y_columns": [2],  # Default to the second column
            "legend": True,
        }

        # Merge default parameters with provided ones
        if plot_params is None:
            plot_params = [{}]
        self.plot_params = [
            {**self.default_plot_params, **params} for params in plot_params
        ]  # figure_params will overwrite default_params

        # --------------------------------#
        # - Fig Axs parameters            #
        # --------------------------------#

        default_fig_axs_params = {
            "n_plots": 1,
            "fig_length": 10,
            "fig_height": 6,
            "x_rotation": 45,
            "share_x": False,
            "share_y": False,
            "x_limits": None,
            "y_limits": None,
            "log_axis": None,
            "title": None,
        }

        # Merge default parameters with provided ones
        if figure_params is None:
            figure_params = {}
        self.figure_params = {
            **default_fig_axs_params,
            **figure_params,
        }  # figure_params will overwrite default_params

    def __resolve_column_names(self, column_references):
        """
        Resolves a list of column references (by name or index) to actual column names.
        """
        resolved_columns = []
        for column_reference in column_references:
            if isinstance(column_reference, int):  # If it's an index
                resolved_columns.append(
                    self.df.columns[column_reference - 1]
                )  # Convert 1-based index to 0-based
            else:
                resolved_columns.append(
                    column_reference
                )  # If it's already a column name
        return resolved_columns

    def __validate_columns(self, columns):
        missing_cols = [col for col in columns if col not in self.df.columns]
        if missing_cols:
            raise ValueError(f"Columns {missing_cols} not found in the dataframe.")

    def __validate_plot_type(self, plot_type):
        valid_plot_types = [
            "lineplot",
            "scatterplot",
            "histogram",
            "histogram_accumulated",
        ]
        if plot_type not in valid_plot_types:
            raise ValueError(
                f"Invalid plot type '{plot}'. Valid options are: {valid_plot_types}"
            )

    def __validate_legend(self, legend):
        if not isinstance(legend, bool):
            raise ValueError("legend must be a boolean.")

    def __get_bins(self, bins):
        if bins is None:
            return 10
        if not isinstance(bins, (int)):
            raise ValueError("bins must be an int.")
        if bins <= 0:
            raise ValueError("bins must be greater than 0.")
        return bins

    def __get_colors(self, colors, n):
        """
        Validates and retrieves colors for plotting.

        Parameters:
            colors (list of str or None): A list of color names or None. If None, default colors are used.
            n (int): The number of colors required.

        Returns:
            list of str: List of color hex codes.
        """
        if colors is None:
            return list(np.random.choice(list(self.colors.values()), n, replace=False))
        if len(colors) != n:
            raise ValueError(
                "The number of colors provided does not match the number of columns."
            )
        for color in colors:
            if color not in self.colors:
                raise ValueError(
                    f"Color '{color}' is not a valid color. Available colors are: {list(self.colors.keys())}"
                )
        return [self.colors.get(color) for color in colors]

    def __get_styles(self, styles, n):
        if styles is None:
            return [self.styles["-"]] * n
        if len(styles) != n:
            raise ValueError(
                "The number of styles provided does not match the number of columns."
            )
        for style in styles:
            if style not in self.styles:
                raise ValueError(
                    f"Style '{style}' is not a valid style. Available styles are: {list(self.styles.keys())}"
                )
        return [self.styles.get(style) for style in styles]

    def __unpack_plot_params(self, config):
        plot_type = config.get("plot_type")
        self.__validate_plot_type(plot_type)

        x_column = config.get("x_column")
        x_column = self.__resolve_column_names(x_column)
        self.__validate_columns(x_column)

        y_columns = config.get("y_columns")
        y_columns = self.__resolve_column_names(y_columns)
        self.__validate_columns(y_columns)

        colors = config.get("colors", None)
        colors = self.__get_colors(colors, len(y_columns))

        styles = config.get("styles", None)
        styles = self.__get_styles(styles, len(y_columns))

        legend = config.get("legend")
        self.__validate_legend(legend)

        bins = config.get("bins", None)
        bins = self.__get_bins(bins)

        unpacked_config_dict = {
            "plot_type": plot_type,
            "x_column": x_column,
            "y_columns": y_columns,
            "colors": colors,
            "styles": styles,
            "legend": legend,
            "bins": bins,
        }

        return unpacked_config_dict

    def __try_datetime_conversion(self, column):
        try:
            self.df[column] = pd.to_datetime(self.df[column])
        except (ValueError, TypeError, KeyError):
            pass

    def __set_limits(self, ax, i):
        if self.x_limits is not None:
            ax.set_xlim(left=self.x_limits[i][0], right=self.x_limits[i][1])

        if self.y_limits is not None:
            ax.set_ylim(bottom=self.y_limits[i][0], top=self.y_limits[i][1])

        return ax

    def __set_log_axis(self, ax, i):
        if self.log_axis is not None:
            if self.log_axis[i] == "x":
                ax.set_xscale("log")
            elif self.log_axis[i] == "y":
                ax.set_yscale("log")
            elif self.log_axis[i] == "both":
                ax.set_xscale("log")
                ax.set_yscale("log")

        return ax

    def __set_title(self, fig):
        if self.title:
            fig.text(0.5, 0.95, self.title, ha="center", fontsize=16)

        return fig

    def run_canvas(self):
        self.n_plots = self.figure_params["n_plots"]
        self.size = (self.figure_params["fig_length"], self.figure_params["fig_height"])
        self.x_rotation = self.figure_params["x_rotation"]
        self.share_x = self.figure_params["share_x"]
        self.share_y = self.figure_params["share_y"]
        self.x_limits = self.figure_params["x_limits"]
        self.y_limits = self.figure_params["y_limits"]
        self.title = self.figure_params["title"]
        self.log_axis = self.figure_params["log_axis"]

        fig, axs = plt.subplots(
            self.n_plots, figsize=self.size, sharex=self.share_x, sharey=self.share_y
        )

        if self.n_plots == 1:
            axs = [
                axs
            ]  # Ensure axs is always a list. Otherwise, enumerate(axs) will fail

        for i, ax in enumerate(axs):
            ax.tick_params(axis="x", rotation=self.x_rotation)  # Set x-axis rotation

            ax = self.__set_limits(ax, i)  # Set axis limits

            ax = self.__set_log_axis(ax, i)  # Set logarithmic scale

            fig = self.__set_title(fig)  # Set title

        return fig, axs

    def multiple_variable_lineplot(self, unpacked_config, ax):
        """
        Creates a line plot for multiple y variables against an x variable.
        If the x_column is a pd.datetime, then the x-axis will not be too crowded.
        """

        self.__try_datetime_conversion(unpacked_config["x_column"])

        for y_column, color, style in zip(
            unpacked_config["y_columns"],
            unpacked_config["colors"],
            unpacked_config["styles"],
        ):
            ax.plot(
                self.df[unpacked_config["x_column"]],
                self.df[y_column],
                color=color,
                linestyle=style,
                label=y_column,
            )

        if unpacked_config["legend"]:
            ax.legend(loc="best")

    def multiple_variable_scatterplot(self, unpacked_config, ax):
        """
        Creates a scatter plot for multiple y variables against an x variable.
        """

        for y_column, color in zip(
            unpacked_config["y_columns"], unpacked_config["colors"]
        ):
            ax.scatter(
                self.df[unpacked_config["x_column"]],
                self.df[y_column],
                color=color,
                label=y_column,
            )

        if unpacked_config["legend"]:
            ax.legend(loc="best")

    def multiple_variable_histogram(self, unpacked_config, ax):
        """
        Creates normalized histograms for the specified columns.
        """

        for y_column, color in zip(
            unpacked_config["y_columns"], unpacked_config["colors"]
        ):
            # Drop null values before plotting
            self.df[y_column].dropna().plot.hist(
                bins=unpacked_config["bins"],
                alpha=0.5,
                color=color,
                ax=ax,
                density=True,
                label=y_column,
                edgecolor="black",
            )

        if unpacked_config["legend"]:
            ax.legend(loc="best")

    def multiple_variable_histogram_accumulated(self, unpacked_config, ax):
        """
        Creates normalized histograms for the specified columns.
        """

        for y_column, color in zip(
            unpacked_config["y_columns"], unpacked_config["colors"]
        ):
            # Drop null values before plotting
            data = self.df[y_column].dropna()
            hist, bin_edges = np.histogram(
                data, bins=unpacked_config["bins"], density=True
            )
            cdf = np.cumsum(hist * np.diff(bin_edges))
            ax.plot(bin_edges[1:], cdf, color=color, label=y_column)

        ax.axhline(y=0.25, color="gray", linestyle="--", linewidth=0.7)
        ax.axhline(y=0.5, color="gray", linestyle="--", linewidth=0.7)
        ax.axhline(y=0.75, color="gray", linestyle="--", linewidth=0.7)

        if unpacked_config["legend"]:
            ax.legend(loc="best")

    def run_plotter(self):
        """
        Iteratively plots each configuration in plot_params, using the provided df and canvas.
        """

        fig, axs = self.run_canvas()

        for idx, config in enumerate(self.plot_params):
            unpacked_config = self.__unpack_plot_params(
                config
            )  # We pick one configuration at a time

            if unpacked_config["plot_type"] == "lineplot":
                self.multiple_variable_lineplot(unpacked_config, axs[idx])

            if unpacked_config["plot_type"] == "scatterplot":
                self.multiple_variable_scatterplot(unpacked_config, axs[idx])

            if unpacked_config["plot_type"] == "histogram":
                self.multiple_variable_histogram(unpacked_config, axs[idx])

            if unpacked_config["plot_type"] == "histogram_accumulated":
                self.multiple_variable_histogram_accumulated(unpacked_config, axs[idx])
