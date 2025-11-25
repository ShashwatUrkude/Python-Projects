# SocialGraph Analyzer

A simple Python-based social network data processor that:
- Cleans raw user and page data
- Displays user relationships and page listings
- Recommends new friends based on mutual connections
- Suggests pages users might like using shared page interests

This project demonstrates how recommendation logic can be built without machine learning, using graph and similarity-based ranking.

---

## 🚀 Features
✔ Remove invalid or duplicate data  
✔ Show users with friends and liked pages  
✔ Recommend **People You May Know** based on mutual friends  
✔ Recommend **Pages You Might Like** based on shared interests  
✔ Save cleaned data into a new JSON file

---

## 🧠 How It Works
The script loads raw JSON, cleans it, then calculates:
- **Mutual friend counts** → friend suggestions
- **Shared page likes** → page recommendations

Recommendations are ranked in descending order based on relevance.

---

## 📂 Project Structure
