import os
import requests
import svgwrite
from datetime import datetime
import random

GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

def get_contributions():
    token = os.getenv("GITHUB_TOKEN")  # Must be stored in GitHub Secrets
    if not token:
        raise ValueError("GITHUB_TOKEN environment variable is missing!")

    headers = {"Authorization": f"Bearer {token}"}

    query = """
    {
      viewer {
        contributionsCollection {
          contributionCalendar {
            totalContributions
          }
        }
      }
    }
    """

    response = requests.post(GITHUB_GRAPHQL_URL, headers=headers, json={"query": query})
    data = response.json()

    if "errors" in data:
        raise Exception(f"GraphQL Error: {data['errors']}")

    return data["data"]["viewer"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]

def generate_river():
    contributions = get_contributions()
    dwg = svgwrite.Drawing('assets/code-river.svg', size=('800px', '120px'))

    # Background gradient
    gradient = dwg.defs.add(dwg.linearGradient(id="bgGradient", gradientTransform="rotate(90)"))
    gradient.add_stop_color(0, "#0A0F1F")
    gradient.add_stop_color(1, "#1A2B4C")
    dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill="url(#bgGradient)"))

    # Define animation for flowing effect
    dwg.defs.add(dwg.style("""
    @keyframes flow {
        0% { transform: translateX(0); }
        100% { transform: translateX(-800px); }
    }
    """))

    # Create moving contribution blocks
    for i in range(40):  # Number of blocks
        x = random.randint(0, 800)
        y = random.randint(20, 80)
        color = random.choice(["#00FF88", "#FF0088", "#FFA500", "#00A3FF"])
        
        rect = dwg.rect(
            insert=(x, y),
            size=(10, 10),
            fill=color,
            opacity=0.8,
            style="animation: flow 5s linear infinite;"
        )
        dwg.add(rect)

    # Add contribution stats
    dwg.add(dwg.text(
        f"Contributions: {contributions}",
        insert=(20, 100),
        fill='#FFFFFF',
        font_size=14,
        font_weight='bold'
    ))

    dwg.save()

if __name__ == "__main__":
    generate_river()













