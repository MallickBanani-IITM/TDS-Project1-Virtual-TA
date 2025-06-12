import json
import os
from difflib import SequenceMatcher
from typing import Tuple, List

DATA_PATH = "data/cleaned_discourse.json"

def load_discourse_data():
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def find_best_matches(question, top_n=2):
    data = load_discourse_data()
    scored = []

    for post in data:
        text = post["title"] + " " + post.get("excerpt", "")
        score = SequenceMatcher(None, question.lower(), text.lower()).ratio()
        scored.append((score, post))

    scored.sort(reverse=True, key=lambda x: x[0])
    best_matches = [item[1] for item in scored[:top_n]]
    return best_matches

# ✅ This replaces the dummy placeholder function
def get_answer_from_knowledge_base(question: str, image_b64: str = None) -> Tuple[str, List[dict]]:
    matches = find_best_matches(question)
    if not matches:
        return "Sorry, I couldn't find a relevant answer.", []

    answer = "Based on similar questions, here’s what I found:"
    links = []
    for m in matches:
        links.append({
            "url": m["url"],
            "text": m["title"]
        })

    return answer, links
