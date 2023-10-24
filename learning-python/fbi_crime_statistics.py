import pandas as pd
import matplotlib.pyplot as plt

# Read CSV file into a DataFrame
df = pd.read_csv(
"static/fbi-stats.csv", 
delimiter=",", 
quotechar='"', 
thousands=",", 
dtype={"Year": int, "Violent\ncrime": float},
)

# Select relevant columns and clean data
df = df[["Year", "Violent\ncrime"]]
df.columns = ["Year", "Violent\ncrime"]
df["Year"] = pd.to_datetime(df["Year"], format="%Y")
df["Violent Crime"] = df["Violent\ncrime"].astype(float)

# Plot data using Pandas built-in functions
plt.figure(figsize=(10, 6))
plt.style.use(["ggplot"])
df.plot(x="Year", y="Violent\ncrime", color="r", linestyle="-", marker="o")

# Customize plot
plt.title("FBI Violent Crime Statistics")
plt.ylabel("Volume")
plt.xlabel("Year")
plt.xticks(rotation=45)
plt.grid(True)

# Display plot
plt.show()

