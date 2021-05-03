"""
This script will generate the
race char for the specified 
fields and customize the chart
based on the input given
"""

import pandas as pd
import bar_chart_race as bcr


class BarRaceChart:
    def __init__(self):
        self.n_bars = 0
        self.colors = []
        self.required_columns = []
        self.chart_title = ""
        self.steps_per_period = 50
        self.period_length = 2500
        self.dpi = 300
        self.sheet_data = ""
        self.data_frame = ""
        self.sort_direction = "desc"
        self.sheet_path = ""
        self.sheet_name = ""
        self.final_sheet_path_with_name = ""
        self.final_video_name = ""
        self.counter_label = ""

    """
    Definition to get all the parameters
    required for creating the race graph
    """

    def get_default_values(self):
        self.sheet_path = input("Enter the file path of excel sheet: ")
        self.sheet_path = self.sheet_path.replace("\\", "/")

        self.sheet_name = input("Enter the sheet name without any extension: ")
        self.final_sheet_path_with_name = (
            self.sheet_path + "/" + self.sheet_name + ".csv"
        )

        column_names = input(
            "Enter the column names as comma separated value with no spaces in between: "
        )
        self.required_columns = column_names.split(",")

        colors_scheme = input(
            "Enter the color scheme value as comma separated if applicable, else press enter: "
        )
        if len(colors_scheme) == 0:
            self.colors = "dark12"
        else:
            self.colors = colors_scheme.split(",")

        self.n_bars = int(input("Enter the number of bars you require: "))

        self.chart_title = input("Enter the Chart title: ")

        self.counter_label = input("Enter the counter field label: ")

        output_video_path = input("Enter the file path to save the final video: ")
        output_video_path = output_video_path.replace("\\", "/")
        output_video_name = input("Enter the output video name without any extension: ")

        if output_video_path[-1] == "/":
            self.final_video_name = output_video_path + output_video_name + ".mp4"
        else:
            self.final_video_name = output_video_path + "/" + output_video_name + ".mp4"

    """
    Definition to pre process the data
    and convert it into the proper 
    format required by the bar_chart_graph module
    """

    def pre_process_data(self):
        self.sheet_data = pd.read_csv(self.final_sheet_path_with_name)

        self.sheet_data = self.sheet_data[self.required_columns]

        self.data_frame = self.sheet_data.pivot_table(
            values=self.required_columns[2],
            index=[self.required_columns[0]],
            columns=self.required_columns[1],
        )

        self.data_frame.fillna(0, inplace=True)
        self.data_frame.sort_values(list(self.data_frame.columns), inplace=True)
        self.data_frame = self.data_frame.sort_index()

        self.data_frame.iloc[:, 0:-1] = self.data_frame.iloc[:, 0:-1].cumsum()

    """
    This method will retrieve the
    top n number of items from the 
    entire data
    """

    def retrieve_top_list(self):
        top_of_the_list = set()

        for index, row in self.data_frame.iterrows():
            top_of_the_list |= set(
                row[row > 0].sort_values(ascending=False).head(self.n_bars).index
            )

        self.data_frame = self.data_frame[top_of_the_list]

    """
    Definition to create the
    race chart
    """

    def create_bar_race_graph(self):
        bcr.bar_chart_race(
            df=self.data_frame,
            n_bars=self.n_bars,
            sort=self.sort_direction,
            filename=self.final_video_name,
            title=self.chart_title,
            period_length=self.period_length,
            dpi=self.dpi,
            cmap=self.colors,
            period_label={"x": 0.99, "y": 0.25, "ha": "right", "va": "center"},
            period_summary_func=lambda v, r: {
                "x": 0.99,
                "y": 0.18,
                "s": f"{self.counter_label}: {v.nlargest(self.n_bars).sum():,.0f}",
                "ha": "right",
                "size": 12,
            },
        )


if __name__ == "__main__":
    race_chart_object = BarRaceChart()
    race_chart_object.get_default_values()
    race_chart_object.pre_process_data()
    race_chart_object.retrieve_top_list()
    race_chart_object.create_bar_race_graph()
