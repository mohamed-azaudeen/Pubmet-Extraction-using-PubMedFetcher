import pandas as pd
from metapub import PubMedFetcher
from functools import reduce
import streamlit as st
from PIL import Image

st.set_page_config(layout="wide", page_title="PubMed Article Finder", page_icon="🔍")

col1, col2, col3 = st.columns([1, 2, 1])
         
with col2:
    st.title(":blue[PubMed Article Finder]")
st.subheader(":red[Enter a keyword to search for articles :]")

keyword = st.text_input("Enter your text here:")
if st.button(":green[Search]"):
    num_of_articles = 20

    fetch = PubMedFetcher()
    pmids = fetch.pmids_for_query(keyword,retmax=num_of_articles)

    titles = {}
    abstracts = {}
    authors = {}
    years = {}
    journals = {}
    citations = {}
    links = {}

    for pmid in pmids:
        article = fetch.article_by_pmid(pmid)
        titles[pmid] = article.title
        authors[pmid] = ', '.join(article.authors)
        years[pmid] = article.year
        journals[pmid] = article.journal
        citations[pmid] = article.citation
        links[pmid] = article.url

    Title = pd.DataFrame(list(titles.items()), columns=['pmid', 'Title'])
    Author = pd.DataFrame(list(authors.items()), columns=['pmid', 'Author'])
    Year = pd.DataFrame(list(years.items()), columns=['pmid', 'Year'])
    Journal = pd.DataFrame(list(journals.items()), columns=['pmid', 'Journal'])
    Citation = pd.DataFrame(list(citations.items()), columns=['pmid', 'Citation'])
    Link = pd.DataFrame(list(links.items()), columns=['pmid', 'Link'])

    Link['Link'] = Link['Link'].apply(lambda x: f'<a href="{x}" target="_blank">PubMed Link</a>')

    data_frames = [Title,Author,Year,Journal,Citation,Link]

    df_merged = reduce(lambda left,right: pd.merge(left, right, on=['pmid'], how='outer'), data_frames)

    st.write(df_merged.to_html(escape=False, index=False), unsafe_allow_html=True)