import matplotlib.pyplot as plt
import pandas as pd

from src.models.leads import Lead

# Eksport danych do CSV


def export_leads_to_csv(filepath="leads_export.csv"):
    leads = Lead.query.all()
    data = [
        {
            "id": l.id,
            "name": l.name,
            "email": l.email,
            "score": l.lead_score,
            "package": l.interested_package,
            "location": l.location,
            "created": l.last_interaction,
        }
        for l in leads
    ]
    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False)
    print(f"Eksportowano {len(df)} leadów do {filepath}")


# Wykresy analityczne


def plot_lead_score_histogram():
    leads = Lead.query.all()
    scores = [l.lead_score for l in leads if l.lead_score is not None]
    plt.hist(scores, bins=10, color="skyblue")
    plt.title("Lead Score Distribution")
    plt.xlabel("Score")
    plt.ylabel("Count")
    plt.show()


def plot_leads_by_package():
    leads = Lead.query.all()
    packages = [l.interested_package for l in leads if l.interested_package]
    df = pd.DataFrame(packages, columns=["package"])
    df["package"].value_counts().plot(kind="bar", color="orange")
    plt.title("Leads by Package")
    plt.xlabel("Package")
    plt.ylabel("Count")
    plt.show()


# Segmentacja leadów


def segment_leads_by_score():
    leads = Lead.query.all()
    segments = {"low": 0, "medium": 0, "high": 0}
    for l in leads:
        if l.lead_score is None:
            continue
        if l.lead_score < 40:
            segments["low"] += 1
        elif l.lead_score < 70:
            segments["medium"] += 1
        else:
            segments["high"] += 1
    print("Segmentacja leadów:", segments)
    return segments
