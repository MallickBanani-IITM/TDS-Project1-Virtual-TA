import json
import os

RAW_PATH = "data/discourse_raw.json"
OUTPUT_PATH = "data/cleaned_discourse.json"

def preprocess():
    with open(RAW_PATH, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    topics = raw_data.get("topic_list", {}).get("topics", [])
    if not topics:
        print("No topics found in raw data.")
        return

    cleaned = []

    for topic in topics:
        cleaned.append({
            "id": topic["id"],
            "title": topic["title"],
            "url": f"https://discourse.onlinedegree.iitm.ac.in/t/{topic['slug']}/{topic['id']}",
            "excerpt": topic.get("excerpt", ""),
        })

    # Save to cleaned JSON
    os.makedirs("data", exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2)

    print(f"✅ Preprocessed {len(cleaned)} topics. Saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    preprocess()

