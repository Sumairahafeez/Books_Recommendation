import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
# Streamlit page setup
st.set_page_config(page_title="Books Dashboard", layout="wide")
st.title("📚 Book Insights Dashboard")
st.markdown("Upload a dataset of books and explore various visualizations using the sidebar.")

uploaded_file = st.file_uploader("📂 Upload your `books.csv` file", type="csv")
def download_plot(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png")
    st.download_button(
        label="📥 Download Report as PNG",
        data=buf.getvalue(),
        file_name="visualization_report.png",
        mime="image/png"
    )
# if uploaded_file:
def load_data():
    try:
        df = pd.read_csv('books.csv', encoding='utf-8', on_bad_lines='skip')
        df.drop_duplicates(inplace=True)
        df.reset_index(drop=True, inplace=True)
        df['publication_date'] = pd.to_datetime(df['publication_date'], errors='coerce')
        df = df.drop_duplicates(subset=['title'])
        df = df[df['publication_date'].notna()]
        df['title'] = df['title'].apply(lambda x: x.split('/')[0])
        df['publication_year'] = df['publication_date'].dt.year

        st.success("File uploaded and loaded successfully!")
        # Sidebar controls
        st.sidebar.header("📊 Visualization Options")

        viz_option = st.sidebar.radio(
            "Choose Visualization Type",
            [
                "Top Rated Books",
                "Books by Page Count",
                "Books by Ratings Count",
                "Scatter Plot: Pages vs Rating",
                "Histogram: Average Rating",
                "Top Rated Books by Author",
                "Most Recent Books",
                "Revisions by Publisher",
                "Ratings by Publisher",
                "Number of Books per year",
                "Average Ratings per Year",
                "Books vs number of pages",
            ]
        )

        # Common filters
        st.sidebar.markdown("### Filters")
        slider_val = st.sidebar.slider("Select Number of Records", 5, 50, 10)
        fig, ax = plt.subplots(figsize=(16, 12))

        if viz_option == "Top Rated Books":
            top_books = df.sort_values(by='average_rating', ascending=False).head(slider_val)
            top_books['authors'] = top_books['authors'].apply(lambda x: x.split('/')[0])
            with st.expander("🔍 Preview Data"):
                st.dataframe(top_books.head(10))
            sns.barplot(x='average_rating', y='title',hue='  num_pages', data=top_books,palette='pastel', ax=ax, dodge=False
            )
            ax.set_title("Top Rated Books", fontdict={'fontsize': 18, 'fontweight': 'bold', 'fontname': 'Arial'})
            ax.set_xlabel("Average Rating", fontdict={'fontsize': 18, 'fontweight': 'bold', 'fontname': 'Arial'})
            ax.set_ylabel("Book Title", fontdict={'fontsize': 18, 'fontweight': 'bold', 'fontname': 'Arial'})
            ax.tick_params(axis='y', labelsize=12)
            ax.tick_params(axis='x', labelsize=12)
            st.pyplot(fig)

        elif viz_option == "Books by Page Count":
            top_books = df.sort_values(by='  num_pages', ascending=False).head(slider_val)
            with st.expander("🔍 Preview Data"):
                st.dataframe(top_books.head(10))
            sns.barplot(
                x='  num_pages', y='title',
                data=top_books, palette='pastel', ax=ax)
            ax.set_title("Books with Most Pages", fontdict={'fontsize': 18, 'fontweight': 'bold', 'fontname': 'Arial'})
            ax.set_xlabel("Number of Pages", fontdict={'fontsize': 18, 'fontweight': 'bold', 'fontname': 'Arial'})
            ax.tick_params(axis='y', labelsize=12)
            ax.set_ylabel("Book Title", fontdict={'fontsize': 18, 'fontweight': 'bold', 'fontname': 'Arial'})
            ax.tick_params(axis='x', labelsize=12)
            st.pyplot(fig)

        elif viz_option == "Books by Ratings Count":
            top_books = df.sort_values(by='ratings_count', ascending=False).head(slider_val)
            with st.expander("🔍 Preview Data"):
                st.dataframe(top_books.head(10))
            sns.barplot(
                x='ratings_count', y='title',data=top_books, palette='pastel', ax=ax)
            ax.set_title("Books with Most Ratings", fontdict={'fontsize': 18, 'fontweight': 'bold', 'fontname': 'Arial'})
            ax.tick_params(axis='y', labelsize=12)
            ax.set_xlabel("Ratings Count", fontdict={'fontsize': 18, 'fontweight': 'bold', 'fontname': 'Arial'})
            ax.set_ylabel("Book Title", fontdict={'fontsize': 18, 'fontweight': 'bold', 'fontname': 'Arial'})
            ax.tick_params(axis='x', labelsize=12)
            st.pyplot(fig)

        elif viz_option == "Scatter Plot: Pages vs Rating":
            with st.expander("🔍 Preview Data"):
                st.dataframe(df.head(10))
            sns.scatterplot(
                data=df,x='  num_pages', y='average_rating',size='ratings_count', hue='average_rating',palette='pastel', ax=ax)
            ax.set_title("Pages vs Rating (Size = Ratings Count)", fontdict={'fontsize': 18, 'fontweight': 'bold', 'fontname': 'Arial'})
            ax.tick_params(axis='y', labelsize=12)
            ax.set_xlabel("Number of Pages", fontdict={'fontsize': 18, 'fontweight': 'bold', 'fontname': 'Arial'})
            ax.set_ylabel("Average Rating", fontdict={'fontsize': 18, 'fontweight': 'bold', 'fontname': 'Arial'})
            ax.tick_params(axis='x', labelsize=12)
            st.pyplot(fig)

        elif viz_option == "Histogram: Average Rating":
            with st.expander("🔍 Preview Data"):
                st.dataframe(df.head(10))
            sns.histplot(data=df,x='average_rating', bins=20,kde=True, color='teal', ax=ax)
            ax.set_title("Distribution of Average Ratings", fontdict={'fontsize': 18, 'fontweight': 'bold', 'fontname': 'Arial'})
            ax.set_xlabel("Average Rating", fontdict={'fontsize': 18, 'fontweight': 'bold', 'fontname': 'Arial'})
            ax.tick_params(axis='y', labelsize=12)
            ax.set_ylabel("Frequency", fontdict={'fontsize': 18, 'fontweight': 'bold', 'fontname': 'Arial'})
            ax.tick_params(axis='x', labelsize=12)
            st.pyplot(fig)
        elif viz_option == "Top Rated Books by Author":
            top_books = df.sort_values(by='average_rating', ascending=False).dropna(subset=['authors', 'average_rating'])
            top_books['authors'] = top_books['authors'].apply(lambda x: x.split('/')[0])
            top_unique = top_books.drop_duplicates(subset='authors', keep='first')
            top_n = top_unique.head(slider_val)
            with st.expander("🔍 Preview Data"):
                st.dataframe(top_n.head(top_n.shape[0]))
            fig, ax = plt.subplots(figsize=(20, 15))
            sns.barplot(data=top_n, x='authors', y='average_rating', hue='title', dodge=False, palette='pastel', width=0.3, ax=ax)
            ax.set_title('Top Authors with Their Highest Rated Book', fontdict={'fontsize': 18, 'fontweight': 'bold', 'fontname': 'Arial'})
            ax.tick_params(axis='y', labelsize=12)
            ax.set_xlabel('Author',     fontdict={'fontsize': 18, 'fontweight': 'bold', 'fontname': 'Arial'})
            ax.tick_params(axis='x', labelsize=12)
            ax.set_ylabel('Average Ratings', fontdict={'fontsize': 18, 'fontweight': 'bold', 'fontname': 'Arial'})
            ax.legend(title='Book Title', bbox_to_anchor=(1.15, 1), loc='upper left')
            st.pyplot(fig)
            download_plot(fig)

        elif viz_option == "Most Recent Books":
            df['publication_date'] = pd.to_datetime(df['publication_date'], errors='coerce')
            df = df.drop_duplicates(subset=['title'])
            df = df[df['publication_date'].notna()]
            df['title'] = df['title'].apply(lambda x: x.split('/')[0])
            df['publication_year'] = df['publication_date'].dt.year
            recent_books = df.sort_values(by='publication_year', ascending=False).head(slider_val)
            with st.expander("🔍 Preview Data"):
                st.dataframe(recent_books.head(slider_val))
            fig, ax = plt.subplots(figsize=(15, 8))
            sns.barplot(data=recent_books, y='title', x='  num_pages', hue='publication_date', palette='pastel', width=0.5, ax=ax)
            ax.set_title('Most Recent Books by Publication Year', fontsize=16)
            ax.set_xlabel('Number of Pages', fontsize=12)
            ax.set_ylabel('Book Title', fontsize=12)
            ax.tick_params(axis='x', rotation=45)
            st.pyplot(fig)
            download_plot(fig)

        elif viz_option == "Revisions by Publisher":
            rev_df = df.dropna(subset=['publisher'])
            rev_summary = rev_df.groupby('publisher').size().reset_index(name='revision_count')
            rev_summary = rev_summary.sort_values(by='revision_count', ascending=False).head(slider_val)
            with st.expander("🔍 Preview Data"):
                st.dataframe(rev_summary.head(slider_val))
            fig, ax = plt.subplots(figsize=(15, 10))
            sns.scatterplot(data=rev_summary, x='publisher', y='revision_count', hue='publisher', palette='pastel', s=100, ax=ax)
            ax.set_title('Text Revisions by Each Publisher', fontsize=16)
            ax.set_xlabel('Publisher', fontsize=12)
            ax.set_ylabel('Number of Revisions', fontsize=12)
            ax.tick_params(axis='x', rotation=45)
            st.pyplot(fig)
            download_plot(fig)

        elif viz_option == "Ratings by Publisher":
            ratings_df = df.dropna(subset=['publisher', 'ratings_count'])
            ratings_summary = ratings_df.groupby('publisher')['ratings_count'].sum().reset_index(name='ratings_count')
            ratings_summary = ratings_summary.sort_values(by='ratings_count', ascending=False).head(slider_val)
            with st.expander("🔍 Preview Data"):
                st.dataframe(ratings_summary.head(slider_val))
            fig, ax = plt.subplots(figsize=(10, 8))
            ax.pie(ratings_summary['ratings_count'], labels=ratings_summary['publisher'], autopct='%1.1f%%', colors=sns.color_palette("pastel", len(ratings_summary)))
            ax.set_title('Total Ratings of Each Publisher', fontsize=16)
            st.pyplot(fig)
            download_plot(fig)
        elif viz_option == "Number of Books per year":
            books_per_year = df['publication_year'].value_counts().reset_index()
            books_per_year.columns = ['Publication Year', 'Number of Books']
            books_per_year = books_per_year.sort_values(by='Publication Year')
            with st.expander("🔍 Preview Data"):
                st.dataframe(books_per_year.head(slider_val))
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.lineplot(data=books_per_year, x='Publication Year', y='Number of Books', marker='o')
            ax.set_title('Number of Books Published per Year', fontsize=16)
            ax.set_xlabel('Publication Year', fontsize=12)
            ax.set_ylabel('Number of Books', fontsize=12)
            st.pyplot(fig)
            download_plot(fig)
        elif viz_option == "Average Ratings per Year":
            df = pd.read_csv("books.csv", encoding='utf-8', on_bad_lines='skip')
            df['publication_date'] = pd.to_datetime(df['publication_date'], errors='coerce')
            df = df[df['publication_date'].notna()]
            df['publication_year'] = df['publication_date'].dt.year
            ratings_per_year = df.groupby('publication_year')['average_rating'].mean().reset_index()
            ratings_per_year = ratings_per_year.sort_values(by='publication_year')
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.lineplot(data=ratings_per_year, x='publication_year', y='average_rating', marker='o', ax=ax)
            ax.set_title('Average Ratings per Year')
            ax.set_xlabel('Publication Year')
            ax.set_ylabel('Average Rating')
            download_plot(fig)
            st.pyplot(fig)
            
        elif viz_option == "Books vs number of pages":
            df.reset_index(drop=True, inplace=True)
            top_books = df[df['ratings_count'] > 1000].sort_values(by='average_rating', ascending=False).head(slider_val)
            with st.expander("🔍 Preview Data"):
                st.dataframe(top_books.head(slider_val))
            # st.title(f'Top {slider_val} Books by Average Rating')
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x='average_rating', y='title', hue='  num_pages', data=top_books, palette='pastel', ax=ax)
            ax.set_title(f'Top {slider_val} Books by Average Rating', fontsize=16)
            ax.set_xlabel('Average Rating', fontsize=12)
            ax.set_ylabel('Book Title', fontsize=12)
            download_plot(fig)
            st.pyplot(fig)


    except Exception as e:
        st.error(f"⚠️ Error: {e}")

# else:
    # st.info("Please upload a CSV file to get started.")
load_data()