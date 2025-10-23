import streamlit as st
import requests
from collections import Counter
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import re # Import the regular expressions library

# Import your token from config.py
from config import GITHUB_TOKEN

# --- GitHub API Helper Functions (No changes from original) ---
def get_user_data(username):
    """Fetches basic user data."""
    url = f"https://api.github.com/users/{username}"
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def get_repos(username):
    """Fetches all public repositories for a user."""
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{username}/repos?per_page=100&page={page}"
        headers = {'Authorization': f'token {GITHUB_TOKEN}'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if not data:
                break
            repos.extend(data)
            page += 1
        else:
            return None
    return repos

def get_readme_content(repo_full_name):
    """Fetches the README content for a single repository."""
    url = f"https://api.github.com/repos/{repo_full_name}/readme"
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3.raw'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return ""

# --- Analysis Functions ---
def analyze_languages(repos):
    """Counts the primary language for each repo."""
    if not repos:
        return None
    lang_counter = Counter(repo['language'] for repo in repos if repo['language'])
    return lang_counter.most_common(5)

def get_top_repos(repos):
    """Finds the top 5 repos by star count."""
    if not repos:
        return []
    sorted_repos = sorted(repos, key=lambda x: x['stargazers_count'], reverse=True)
    return sorted_repos[:5]

def extract_keywords(repos):
    """Cleans README text and extracts top keywords using TF-IDF."""
    readmes = [get_readme_content(repo['full_name']) for repo in repos if not repo['fork']]
    if not any(readmes):
        return []

    cleaned_readmes = []
    for text in readmes:
        # 1. Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        # 2. Remove image tags and markdown image links
        text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
        # 3. Remove HTML tags
        text = re.sub(r'<.*?>', '', text)
        # 4. Remove non-alphabetic characters (but keep spaces)
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        # 5. Convert to lowercase
        text = text.lower()
        cleaned_readmes.append(text)

    if not any(cleaned_readmes):
        return []
    
    vectorizer = TfidfVectorizer(stop_words='english', max_features=15)
    try:
        vectorizer.fit_transform(cleaned_readmes)
        return vectorizer.get_feature_names_out().tolist()
    except ValueError:
        # This can happen if all text is filtered out
        return []


# --- Visualization Function (Modified for Streamlit) ---
def create_language_chart(lang_data, username):
    """Creates a bar chart and returns the Matplotlib figure."""
    if not lang_data:
        return None
    
    languages, counts = zip(*lang_data)
    
    plt.style.use('seaborn-v0_8-paper')
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.bar(languages, counts, color='#3498DB')
    ax.set_title(f"Top Languages for {username}", fontsize=12)
    ax.set_ylabel("Repo Count", fontsize=9)
    plt.xticks(rotation=45, ha="right", fontsize=9)
    plt.yticks(fontsize=9)
    plt.tight_layout()
    return fig

# --- Report Generation Function ---
def generate_report_text(user_data, repos, lang_data, top_repos, keywords):
    report = f"GitHub Profile Analysis Report for {user_data.get('name', user_data['login'])}\n"
    report += "="*40 + "\n\n"
    report += "--- User Stats ---\n"
    report += f"Public Repos: {user_data.get('public_repos', 'N/A')}\n"
    report += f"Followers: {user_data.get('followers', 'N/A')}\n"
    report += f"Member Since: {user_data.get('created_at', '').split('T')[0]}\n\n"
    report += "--- Top 5 Repositories by Stars ---\n"
    for repo in top_repos:
        report += f"- {repo['name']} ({repo['stargazers_count']} ★)\n"
    report += "\n"
    report += "--- Top 5 Programming Languages ---\n"
    if lang_data:
        for lang, count in lang_data:
            report += f"- {lang}: {count} repos\n"
    else:
        report += "No language data found.\n"
    report += "\n"
    report += "--- Top Project Keywords ---\n"
    report += ", ".join(keywords) + "\n"
    return report

# --- Streamlit UI ---
st.set_page_config(layout="wide")
st.title(" GitHub Profile Analyzer")

username = st.text_input("Enter a GitHub Username:", "")

if st.button("Analyze"):
    if not username:
        st.warning("Please enter a username.")
    else:
        with st.spinner("Fetching and analyzing data..."):
            user_data = get_user_data(username)
            if not user_data:
                st.error("Could not find GitHub user. Please check the username.")
            else:
                repos = get_repos(username)
                
                # Perform all analyses
                lang_data = analyze_languages(repos)
                top_repos = get_top_repos(repos)
                keywords = extract_keywords(repos)
                
                # --- Build the Dashboard ---
                col1, col2 = st.columns([1, 1.5])

                with col1:
                    st.image(user_data['avatar_url'], width=140)
                    st.header(f"[{user_data.get('name', username)}]({user_data['html_url']})")
                    
                    st.subheader("User Stats")
                    st.text(f"Public Repos: {user_data['public_repos']}")
                    st.text(f"Followers: {user_data['followers']}")
                    st.text(f"Member Since: {user_data['created_at'].split('T')[0]}")
                    
                    # Download Button
                    report_text = generate_report_text(user_data, repos, lang_data, top_repos, keywords)
                    st.download_button(
                        label="Download Report",
                        data=report_text,
                        file_name=f"{username}_report.txt",
                        mime="text/plain"
                    )

                with col2:
                    st.subheader("Language Breakdown")
                    chart_fig = create_language_chart(lang_data, username)
                    if chart_fig:
                        st.pyplot(chart_fig)
                    else:
                        st.write("Not enough language data to generate a chart.")

                st.subheader("Top Repositories & Project Keywords")
                col_details1, col_details2 = st.columns(2)
                
                with col_details1:
                    st.markdown("**Top Repositories by Stars**")
                    if top_repos:
                        # Use st.dataframe for a cleaner, error-free table
                        repo_display_df = pd.DataFrame({
                            "Repository": [repo['name'] for repo in top_repos],
                            "Stars ★": [repo['stargazers_count'] for repo in top_repos],
                            "URL": [repo['html_url'] for repo in top_repos]
                        })
                        st.dataframe(
                            repo_display_df,
                            column_config={
                                "URL": st.column_config.LinkColumn("Link to Repo")
                            },
                            hide_index=True,
                            use_container_width=True
                        )
                    else:
                        st.write("No public repositories found.")

                with col_details2:
                    st.markdown("**Project Keywords**")
                    if keywords:
                        # FIXED: Added a dark text color to the span style
                        keywords_html = "".join(f'<span style="background-color: #ECF0F1; color: #2C3E50; border-radius: 12px; padding: 4px 8px; margin: 2px; display: inline-block; font-size: 0.8rem;">{kw}</span>' for kw in keywords)
                        st.markdown(keywords_html, unsafe_allow_html=True)
                    else:
                        st.write("No keywords found in READMEs.")

