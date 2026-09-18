# Score career posts against three content pillars from a CSV of texts.
import argparse
import csv
import re

PILLARS = {
    "past_achievement": [
        "published", "shipped", "delivered", "led", "awarded", "completed",
        "achieved", "launched", "built", "solved", "paper", "grant"
    ],
    "current_work": [
        "learning", "building", "working", "exploring", "prototyping",
        "studying", "experimenting", "currently", "today", "developing"
    ],
    "industry_commentary": [
        "industry", "trend", "future", "ai", "regulatory", "strategy",
        "market", "opinion", "think", "perspective", "landscape", "impact"
    ],
}


def score_text(text):
    tokens = re.findall(r"[a-z]+", text.lower())
    counts = {}
    for pillar, words in PILLARS.items():
        counts[pillar] = sum(tokens.count(w) for w in words)
    total = sum(counts.values())
    if total == 0:
        return {p: 0.0 for p in PILLARS}, "none"
    norm = {p: counts[p] / total for p in PILLARS}
    dominant = max(norm, key=norm.get)
    return norm, dominant


def main():
    parser = argparse.ArgumentParser(description="Classify posts into career pillars.")
    parser.add_argument("--input", required=True, help="CSV with a 'text' column.")
    args = parser.parse_args()

    with open(args.input, newline="") as fh:
        reader = csv.DictReader(fh)
        for i, row in enumerate(reader):
            norm, dominant = score_text(row.get("text", ""))
            summary = ", ".join(p + "=" + format(norm[p], ".2f") for p in PILLARS)
            print("post " + str(i) + ": dominant=" + dominant + " | " + summary)


if __name__ == "__main__":
    main()
