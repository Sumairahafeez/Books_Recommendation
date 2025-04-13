import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

# Page Configuration
st.set_page_config(page_title="Books Dataset Visualizations", layout="wide")
st.title("📚 Books Dataset - Visual Analytics Dashboard")

# Load and preprocess the data
@st.cache_data
def load_data():
    df = pd.read_csv("books.csv", encoding='utf-8', on_bad_lines='skip')
    df['publication_date'] = pd.to_datetime(df['publication_date'], errors='coerce')
    df = df.drop_duplicates(subset=['title'])
    df = df[df['publication_date'].notna()]
    df['title'] = df['title'].apply(lambda x: x.split('/')[0])
    df['publication_year'] = df['publication_date'].dt.year
    return df

df = load_data()

# Sidebar
st.sidebar.header("Visualization Controls")
chart_type = st.sidebar.radio("Select a Visualization", [
    "Top Rated Books by Author",
    "Most Recent Books",
    "Revisions by Publisher",
    "Ratings by Publisher",
    "Number of Books per year",
    "Average Ratings per Year",
    "Books vs number of pages"
])

slider_val = st.sidebar.slider("Select Number of Records", 5, 50, 10)

def download_plot(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png")
    st.download_button(
        label="📥 Download Report as PNG",
        data=buf.getvalue(),
        file_name="visualization_report.png",
        mime="image/png"
    )

# Visualizations
if chart_type == "Top Rated Books by Author":
    top_books = df.sort_values(by='average_rating', ascending=False).dropna(subset=['authors', 'average_rating'])
    top_books['authors'] = top_books['authors'].apply(lambda x: x.split('/')[0])
    top_unique = top_books.drop_duplicates(subset='authors', keep='first')
    top_n = top_unique.head(slider_val)

    fig, ax = plt.subplots(figsize=(25, 20))
    sns.barplot(data=top_n, x='authors', y='average_rating', hue='title', dodge=False, palette='pastel', width=0.3, ax=ax)
    ax.set_title('Top Authors with Their Highest Rated Book')
    ax.set_xlabel('Author')
    ax.set_ylabel('Average Ratings')
    ax.legend(title='Book Title', bbox_to_anchor=(1.15, 1), loc='upper left')
    st.pyplot(fig)
    download_plot(fig)

elif chart_type == "Most Recent Books":
    recent_books = df.sort_values(by='publication_year', ascending=False).head(slider_val)
    fig, ax = plt.subplots(figsize=(15, 8))
    sns.barplot(data=recent_books, y='title', x='  num_pages', hue='publication_date', palette='pastel', width=0.5, ax=ax)
    ax.set_title('Most Recent Books by Publication Year', fontsize=16)
    ax.set_xlabel('Number of Pages', fontsize=12)
    ax.set_ylabel('Book Title', fontsize=12)
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)
    download_plot(fig)

elif chart_type == "Revisions by Publisher":
    rev_df = df.dropna(subset=['publisher'])
    rev_summary = rev_df.groupby('publisher').size().reset_index(name='revision_count')
    rev_summary = rev_summary.sort_values(by='revision_count', ascending=False).head(slider_val)

    fig, ax = plt.subplots(figsize=(15, 10))
    sns.scatterplot(data=rev_summary, x='publisher', y='revision_count', hue='publisher', palette='pastel', s=100, ax=ax)
    ax.set_title('Text Revisions by Each Publisher', fontsize=16)
    ax.set_xlabel('Publisher', fontsize=12)
    ax.set_ylabel('Number of Revisions', fontsize=12)
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)
    download_plot(fig)

elif chart_type == "Ratings by Publisher":
    ratings_df = df.dropna(subset=['publisher', 'ratings_count'])
    ratings_summary = ratings_df.groupby('publisher')['ratings_count'].sum().reset_index(name='ratings_count')
    ratings_summary = ratings_summary.sort_values(by='ratings_count', ascending=False).head(slider_val)

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.pie(ratings_summary['ratings_count'], labels=ratings_summary['publisher'], autopct='%1.1f%%', colors=sns.color_palette("pastel", len(ratings_summary)))
    ax.set_title('Total Ratings of Each Publisher', fontsize=16)
    st.pyplot(fig)
    download_plot(fig)
elif chart_type == "Number of Books per year":
    books_per_year = df['publication_year'].value_counts().reset_index()
    books_per_year.columns = ['Publication Year', 'Number of Books']
    books_per_year = books_per_year.sort_values(by='Publication Year')

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=books_per_year, x='Publication Year', y='Number of Books', marker='o')
    ax.set_title('Number of Books Published per Year', fontsize=16)
    ax.set_xlabel('Publication Year', fontsize=12)
    ax.set_ylabel('Number of Books', fontsize=12)
    st.pyplot(fig)
    download_plot(fig)
elif chart_type == "Average Ratings per Year":
    ratings_per_year = df.groupby('publication_year')['average_rating'].mean().reset_index()
    ratings_per_year = ratings_per_year.sort_values(by='publication_year')

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=ratings_per_year, x='publication_year', y='average_rating', marker='o')
    ax.set_title('Average Ratings per Year', fontsize=16)
    ax.set_xlabel('Publication Year', fontsize=12)
    ax.set_ylabel('Average Rating', fontsize=12)
    st.pyplot(fig)
    download_plot(fig)
elif chart_type == "Books vs number of pages":
    df.reset_index(drop=True, inplace=True)
    top_books = df[df['ratings_count'] > 1000].sort_values(by='average_rating', ascending=False).head(slider_val)

    # Set up Streamlit app layout
    st.title(f'Top {slider_val} Books by Average Rating')

    # Create the plot using seaborn and matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='average_rating', y='title', hue='  num_pages', data=top_books, palette='pastel', ax=ax)
    ax.set_title(f'Top {slider_val} Books by Average Rating', fontsize=16)
    ax.set_xlabel('Average Rating', fontsize=12)
    ax.set_ylabel('Book Title', fontsize=12)

    # Display plot in the Streamlit app
    st.pyplot(fig)
# Footer
st.markdown("---")
st.caption("Crafted with ❤️ using Streamlit and Seaborn")
