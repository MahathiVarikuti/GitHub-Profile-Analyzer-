# GitHub Profile Analyzer

**An Interactive Web Dashboard for Data-Driven GitHub Profile Analysis**

GitHub Profile Analyzer automatically fetches and analyzes any public GitHub user's profile, surfacing their top languages, most popular repositories, and key project themes using NLP.

---

## Problem Statement

A GitHub profile acts as a developer's living portfolio, but interpreting it quickly and objectively is tedious. Developers, recruiters, and managers face the same challenge: manually browsing through repositories to piece together a coherent picture of someone's skills and focus areas is slow and subjective. There's no simple tool to aggregate this into a clear, visual summary.

---

## Solution

1. User enters any public GitHub username
2. App fetches profile and repository data via the GitHub REST API
3. Programming languages are aggregated across all repositories
4. Repositories are ranked by star count
5. README files are cleaned and analyzed using TF-IDF keyword extraction
6. All insights are rendered in a clean, interactive Streamlit dashboard
7. Report can be downloaded as a `.txt` file

---

## Tech Stack

- **Language:** Python
- **Web Framework:** Streamlit
- **API:** GitHub REST API
- **NLP:** Scikit-learn (`TfidfVectorizer`)
- **Data Handling:** Pandas
- **Visualization:** Matplotlib
- **HTTP Requests:** Requests

---

## Features

* **User Stats Overview**
  Displays avatar, name, public repo count, follower count, and account creation date.

* **Language Breakdown Chart**
  Bar chart of the top 5 programming languages used across all public repositories.

* **Top Repositories Table**
  Lists the top 5 repositories ranked by star count with direct links.

* **Project Keyword Extraction**
  Applies TF-IDF on repository README files (after cleaning URLs, HTML tags, and noise) to extract the top 15 most relevant project keywords.

* **Download Report**
  Exports the full analysis as a `.txt` file.

---

## Architecture

```
User enters GitHub username
        ↓
GitHub API → fetch user data, repos, README files
        ↓
Data Processing:
  - Aggregate language usage
  - Sort repos by star count
  - Clean README text → TF-IDF keyword extraction
        ↓
Visualization:
  - Matplotlib bar chart (languages)
  - Pandas DataFrame (repos)
  - Keyword tags
        ↓
Streamlit Dashboard → Download Report (.txt)
```

---

## Installation & Usage

### 1. Install Dependencies

```bash
pip install streamlit requests pandas scikit-learn matplotlib
```

### 2. Set Up GitHub API Token

Create a `.env` file or set your token directly in `app.py` to avoid GitHub API rate limits:

```python
GITHUB_TOKEN = "your_github_token_here"
```

### 3. Run the App

```bash
streamlit run app.py
```

### 4. Analyze a Profile

Enter any public GitHub username in the input field and click **Analyze**.

---

## Limitations

- Only public repositories and profiles are analyzed, private repos and org data are out of scope.
- Keyword extraction quality depends on how well-maintained the README files are. Sparse or empty READMEs yield less useful results.
- Commit history and contribution frequency are not analyzed.

---

## Future Improvements

- **Commit Activity Analysis:** Visualize contribution frequency and patterns over time.
- **Contribution Graph:** Recreate the GitHub contribution heatmap with detailed stats.
- **User Comparison:** Analyze two profiles side-by-side.
- **Cloud Deployment:** Deploy to Streamlit Community Cloud for public access.

---

## References

- Streamlit Inc., *Streamlit Documentation*, https://docs.streamlit.io/
- GitHub Inc., *GitHub REST API Documentation*, https://docs.github.com/en/rest
- Pedregosa *et al.*, "Scikit-learn: Machine Learning in Python," *JMLR*, vol. 12, 2011.
- Hunter, J. D., "Matplotlib: A 2D graphics environment," *Computing in Science & Engineering*, 2007.
- The pandas development team, *pandas*, Zenodo, 2023.
