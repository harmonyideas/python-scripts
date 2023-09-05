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

# Extract relevant columns and clean data
df = df[["Year", "Violent\ncrime"]]
df = df.rename(columns={"Violent\ncrime": "Violent Crime"})
df["Year"] = pd.to_datetime(df["Year"], format="%Y")
df["Violent Crime"] = df["Violent Crime"].astype(float)


# Plot data using pandas built-in functions
plt.style.use(["ggplot"])
df.plot(x="Year", y="Violent Crime", color="r")
plt.title("FBI Violent Crime Statistics")
plt.ylabel("Volume")
plt.xlabel("Year")
plt.show()
