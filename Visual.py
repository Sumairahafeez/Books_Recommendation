import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Load the data
df = pd.read_csv('F:/4th semeter/AILAB/Books/books.csv', encoding='utf-8', on_bad_lines='skip')

# Clean and preprocess the data
df = df.dropna(subset=['publisher', 'ratings_count'])  # Drop rows where publisher or ratings are NaN

# Aggregate the total ratings by publisher
publisher_ratings = df.groupby('publisher')['ratings_count'].sum().reset_index(name='ratings_count')

# Sort by total ratings for better visualization
publisher_ratings = publisher_ratings.sort_values(by='ratings_count', ascending=False).head(20)

# Create a Pie Chart
plt.figure(figsize=(10, 8))
plt.pie(publisher_ratings['ratings_count'], labels=publisher_ratings['publisher'], autopct='%1.1f%%', colors=sns.color_palette("pastel", len(publisher_ratings)))

# Set plot title
plt.title('Total Ratings of Each Publisher', fontsize=16)
plt.tight_layout()
plt.show()





