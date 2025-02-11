

import os
import requests
import svgwrite
from datetime import datetime
import random

GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"


def get_contributions():
    token = os.getenv("GITHUB_TOKEN") 
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



def generate_constellation():
    contributions = get_contributions()
    dwg = svgwrite.Drawing('assets/constellation.svg', size=('795px', '115px'))
    
    # Cosmic background with stars
    dwg.add(dwg.rect(insert=(0,0), size=('100%','100%'), fill='#000B1A'))
    _add_starry_background(dwg)  # Pass dwg to helper
    
    # Constellation lines
    points = _calculate_constellation_points(contributions)
    dwg.add(dwg.polyline(
        points=points,
        stroke='#6CF',
        fill='none',
        stroke_width=2,
        stroke_opacity=0.7,
        stroke_dasharray='5,3'
    ))
    
    # Animated stars
    for x, y in points:
        dwg.add(_create_pulsar_star(dwg, x, y, contributions))  # Pass dwg
    
    # Spaceship
    dwg.add(_create_spaceship(dwg, points[-1][0], points[-1][1]))  # Pass dwg
    
    # Contribution counter
    dwg.add(dwg.text(
        f"Cosmic Contributions: {contributions}",
        insert=(20, 100),
        fill='#FFF',
        font_size=14,
        font_family='monospace'
    ))
    
    dwg.save()

def _add_starry_background(dwg): 
    """Add random twinkling stars background"""
    for _ in range(50):
        dwg.add(dwg.circle(
            center=(random.randint(0, 795), random.randint(0, 115)),
            r=random.uniform(0.3, 0.8),
            fill='white',
            opacity=0.3,
            style="animation: twinkle 3s infinite"
        ))

def _create_pulsar_star(dwg, x, y, contributions):  # Accept dwg as first parameter
    """Create animated contribution star"""
    return dwg.circle(
        center=(x, y),
        r=3 + (contributions % 5),
        fill='#FFD700',
        stroke='#FFA500',
        stroke_width=1,
        style="""
        animation: pulse 2s infinite;
        @keyframes pulse {
            0% { r: 3; opacity: 0.8; }
            50% { r: 5; opacity: 1; }
            100% { r: 3; opacity: 0.8; }
        }
        """
    )

def _create_spaceship(dwg, x, y):
    """Animated pixel spaceship"""
    spaceship = dwg.g(
        transform=f"translate({x},{y})",
        style="animation: float 4s ease-in-out infinite"
    )
    
    # Add spaceship components separately
    spaceship.add(dwg.rect(insert=(-4, -4), size=(8, 8), fill='#00FFAA'))
    spaceship.add(dwg.polygon([(-6, 0), (6, 0), (0, -8)], fill='#FF4444'))

    return spaceship

def _calculate_constellation_points(contributions):
    """Generate constellation points based on contribution pattern"""
    # Sample pattern - implement your own logic here
    return [(100 + contributions, 50), 
            (300, 30 + contributions%50), 
            (500, 70), 
            (700, 40)]

if __name__ == "__main__":
    generate_constellation()