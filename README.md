# DSCI510_Final
# Dependencies
Required libararies:

pandas, pgeocode, requests, time, urllib, urlopen, json, plotly.express, urlopen, numpy, matplotlib, seaborn, statsmodels

# Running the project
Below are detailed steps on how to run the code:
1) Threr are 3 code files: “get_the_data.py”, “visualization_and_analysis.py”, and “main.ipynb”. Under the “data” folder, there are 4 CSV files: “pop-by-zip-code.csv”, “population_zipcode_lat_lon.csv”, “climate.csv”, and “air_quality.csv”.
2) The “get_the_data.py” is for data collection. Data collection needs the “pop-by-zip-code.csv” as an input. If run, make sure the “pop-by-zip-code.csv” is under the same directory of “get_the_data.py” (move to the “code” folder). After running, the output (web scrapped data) will be three csv fiels: “population_zipcode_lat_lon.csv”(population data), “climate.csv”(climate data), and “air_quality.csv”(air quality data). 
Note: The data collected is real-time data. If run, the data will be different from the sample data. Subsequent visualization and analysis are based on the collected data in the “data” folder.
3) The “visualization_and_analysis.py” contains the functions for data visualization and analysis. The “main.ipynb” is the main code of this project. Running this file will automatically call the functions in the “visualization_and_analysis.py”. The main code needs 3 input CSV data files. Make sure  “population_zipcode_lat_lon.csv”(population data), “climate.csv”(climate data), and “air_quality.csv”(air quality data), “visualization_and_analysis.py”, and “main.ipynb” are under the same directory. The outputs are visualized figures and analysis results.
4) Visualized figures are saved under the “visualization images” folder.


# Methodology
# Visualization
Air quality index histogram with different categories

Air quality level distribution pie chart

Air polutant concentrations box plot

Air pollutants correlation heatmap

# Future Work
