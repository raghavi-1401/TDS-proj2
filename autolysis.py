import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import httpx
import chardet

# Ensure environment variable for API token is set
API_TOKEN = os.environ.get("AIPROXY_TOKEN")
if not API_TOKEN:
    print("Error: AIPROXY_TOKEN environment variable is not set.")
    sys.exit(1)

# Ensure the correct usage
if len(sys.argv) != 2:
    print("Usage: python autolysis.py <dataset.csv>")
    sys.exit(1)

# Get the dataset file path from command-line argument
file_path = sys.argv[1]
if not os.path.isfile(file_path):
    print(f"Error: File '{file_path}' not found.")
    sys.exit(1)

# Detect encoding of the file
with open(file_path, "rb") as f:
    result = chardet.detect(f.read())
encoding = result["encoding"]

# Load the dataset
try:
    df = pd.read_csv(file_path, encoding=encoding)
except Exception as e:
    print(f"Error loading file: {e}")
    sys.exit(1)

# Initial inspection of the dataset
print("Dataset loaded successfully!")
print("First 5 rows of the dataset:")
print(df.head())

# Save the analysis to a README.md
readme_content = []

readme_content.append(f"# Analysis of {os.path.basename(file_path)}\n\n")
readme_content.append("## Dataset Overview\n")
readme_content.append(f"- Number of rows: {df.shape[0]}\n")
readme_content.append(f"- Number of columns: {df.shape[1]}\n\n")
readme_content.append("### Column Names:\n")
readme_content.append("\n")
readme_content.append(", ".join(df.columns) + "\n")
readme_content.append("\n\n")
readme_content.append("### Data Types:\n")
readme_content.append("\n")
readme_content.append(df.dtypes.to_string() + "\n")
readme_content.append("\n\n")

# Basic data description
readme_content.append("### Summary Statistics:\n")
readme_content.append("\n")
readme_content.append(df.describe(include="all").to_string() + "\n")
readme_content.append("\n\n")

# Plot generation
output_plots = []
for column in df.select_dtypes(include=["number"]).columns:
    plt.figure(figsize=(10, 6))
    sns.histplot(df[column].dropna(), kde=True)
    plt.title(f"Distribution of {column}")
    plt.xlabel(column)
    plt.ylabel("Frequency")
    plot_file = f"{column}_distribution.png"
    plt.savefig(plot_file)
    plt.close()
    output_plots.append(plot_file)
    readme_content.append(f"![{column} Distribution]({plot_file})\n\n")

# Save README.md
with open("README.md", "w") as f:
    f.writelines(readme_content)

print("Analysis complete!")
print("- Summary written to README.md")
print(f"- Plots saved: {', '.join(output_plots)}")