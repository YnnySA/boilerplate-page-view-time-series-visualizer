import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib.ticker import ScalarFormatter
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)

df = pd.read_csv("fcc-forum-pageviews.csv", 
                 parse_dates=["date"], 
                 index_col="date")


# Clean data
df = df[
    (df["value"] >= df["value"].quantile(0.025))&
    (df["value"] <= df["value"].quantile(0.975))
]


def draw_line_plot():
   
    # Draw line plot
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    sns.lineplot(data=df, palette=["red"], legend=False)
       
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    allData = df_bar.groupby([df_bar.index.year, df_bar.index.month])['value'].agg(['sum', 'count'])
    allData['average'] = allData['sum'] / allData['count']
    fullData = [0,0,0,0] + allData["average"].tolist()
    sliced = []
    for n in range(4):
        sliced += [fullData[0:12]]
        fullData = fullData[12:]
    
    columns=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    
    # Draw bar plot
    data = {
        "x": sliced,
        "xlabels" : [2016, 2017, 2018, 2019],
    }
    frame = pd.DataFrame(data["x"], index=data["xlabels"])
    fig, ax = plt.subplots()
    frame.plot(kind="bar", ax=ax)
    ax.set_ylabel("Average Page Views")
    ax.set_xlabel("Years")
    ax.legend(columns).set_title("Months")
    
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    # Year-wise Box Plot (Trend)
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    axes[0].yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
    
    # Month-wise Box Plot (Seasonality)
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1],
                order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')
    axes[1].yaxis.set_major_formatter(ScalarFormatter(useOffset=False))


    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
