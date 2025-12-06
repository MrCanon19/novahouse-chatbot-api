import matplotlib.pyplot as plt
import pandas as pd

from src.models.leads import Lead

# Eksport danych do CSV


def export_leads_to_csv(filepath="leads_export.csv"):
    leads = Lead.query.all()
    data = [
        {
            "id": lead.id,
            "name": lead.name,
            "email": lead.email,
            "score": lead.lead_score,
            "package": lead.interested_package,
            "location": lead.location,
            "created": lead.last_interaction,
        }
        for lead in leads
    ]
    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False)
    print(f"Eksportowano {len(df)} leadów do {filepath}")


# Wykresy analityczne


def plot_lead_score_histogram():
    leads = Lead.query.all()
    scores = [lead.lead_score for lead in leads if lead.lead_score is not None]
    plt.hist(scores, bins=10, color="skyblue")
    plt.title("Lead Score Distribution")
    plt.xlabel("Score")
    plt.ylabel("Count")
    plt.show()


def plot_leads_by_package():
    leads = Lead.query.all()
    packages = [lead.interested_package for lead in leads if lead.interested_package]
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
    for lead in leads:
        if lead.lead_score is None:
            continue
        if lead.lead_score < 40:
            segments["low"] += 1
        elif lead.lead_score < 70:
            segments["medium"] += 1
        else:
            segments["high"] += 1
    print("Segmentacja leadów:", segments)
    return segments
