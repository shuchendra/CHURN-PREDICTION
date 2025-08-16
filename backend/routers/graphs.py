import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def bar_chart_single_column(df: pd.DataFrame, col: str):
    plt.figure(figsize=(8, 6))
    sns.countplot(x=col, data=df, palette="viridis")
    plt.title(f"Bar Chart of {col}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"graphs/{col}_bar_chart.png")
    plt.close()

def pie_chart_single_column(df: pd.DataFrame, col: str):
    plt.figure(figsize=(8, 6))
    df[col].value_counts().plot.pie(autopct="%1.1f%%", startangle=90, cmap="viridis")
    plt.title(f"Pie Chart of {col}")
    plt.ylabel("")
    plt.savefig(f"graphs/{col}_pie_chart.png")
    plt.close()

def histogram_single_column(df: pd.DataFrame, col: str):
    plt.figure(figsize=(8, 6))
    sns.histplot(df[col], bins=30, kde=True, color="blue")
    plt.title(f"Histogram of {col}")
    plt.xlabel(col)
    plt.ylabel("Frequency")
    plt.savefig(f"graphs/{col}_histogram.png")
    plt.close()

def box_plot_single_column(df: pd.DataFrame, col: str):
    plt.figure(figsize=(8, 6))
    sns.boxplot(y=df[col], color="blue")
    plt.title(f"Box Plot of {col}")
    plt.ylabel(col)
    plt.savefig(f"graphs/{col}_box_plot.png")
    plt.close()

def density_plot_single_column(df: pd.DataFrame, col: str):
    plt.figure(figsize=(8, 6))
    sns.kdeplot(df[col], fill=True, color="blue")
    plt.title(f"Density Plot of {col}")
    plt.xlabel(col)
    plt.ylabel("Density")
    plt.savefig(f"graphs/{col}_density_plot.png")
    plt.close()

def mosaic_plot_relationship(df: pd.DataFrame, col1: str, col2: str):
    from statsmodels.graphics.mosaicplot import mosaic
    plt.figure(figsize=(10, 6))
    mosaic(df, [col1, col2])
    plt.title(f"Mosaic Plot of {col1} vs {col2}")
    plt.savefig(f"graphs/{col1}_{col2}_mosaic_plot.png")
    plt.close()

def stacked_bar_chart_relationship(df: pd.DataFrame, col1: str, col2: str):
    crosstab = pd.crosstab(df[col1], df[col2])
    crosstab.plot(kind="bar", stacked=True, colormap="viridis", figsize=(10, 6))
    plt.title(f"Stacked Bar Chart of {col1} vs {col2}")
    plt.xlabel(col1)
    plt.ylabel("Count")
    plt.savefig(f"graphs/{col1}_{col2}_stacked_bar_chart.png")
    plt.close()

def box_plot_relationship(df: pd.DataFrame, col1: str, col2: str):
    plt.figure(figsize=(8, 6))
    sns.boxplot(x=df[col1], y=df[col2], palette="coolwarm")
    plt.title(f"Box Plot of {col1} vs {col2}")
    plt.savefig(f"graphs/{col1}_{col2}_box_plot.png")
    plt.close()

def violin_plot_relationship(df: pd.DataFrame, col1: str, col2: str):
    plt.figure(figsize=(8, 6))
    sns.violinplot(x=df[col1], y=df[col2], palette="coolwarm")
    plt.title(f"Violin Plot of {col1} vs {col2}")
    plt.savefig(f"graphs/{col1}_{col2}_violin_plot.png")
    plt.close()

def bar_chart_relationship(df: pd.DataFrame, col1: str, col2: str):
    plt.figure(figsize=(8, 6))
    sns.barplot(x=df[col1], y=df[col2], palette="viridis")
    plt.title(f"Bar Chart of {col1} vs {col2}")
    plt.savefig(f"graphs/{col1}_{col2}_bar_chart.png")
    plt.close()

def scatter_plot_relationship(df: pd.DataFrame, col1: str, col2: str):
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=df[col1], y=df[col2], alpha=0.6, color="blue")
    plt.title(f"Scatter Plot of {col1} vs {col2}")
    plt.savefig(f"graphs/{col1}_{col2}_scatter_plot.png")
    plt.close()

def line_plot_relationship(df: pd.DataFrame, col1: str, col2: str):
    plt.figure(figsize=(8, 6))
    sns.lineplot(x=df[col1], y=df[col2], color="red")
    plt.title(f"Line Plot of {col1} vs {col2}")
    plt.savefig(f"graphs/{col1}_{col2}_line_plot.png")
    plt.close()

def heatmap_relationship(df: pd.DataFrame, col1: str, col2: str):
    plt.figure(figsize=(8, 6))
    pivot_table = df.pivot_table(values=col2, index=col1, aggfunc="mean")
    sns.heatmap(pivot_table, cmap="coolwarm", annot=True)
    plt.title(f"Heatmap of {col1} vs {col2}")
    plt.savefig(f"graphs/{col1}_{col2}_heatmap.png")
    plt.close()
