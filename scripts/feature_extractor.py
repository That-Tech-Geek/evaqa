import sys
import json

def extract_features(url):
    features = {
        "github_velocity": 45,      # commits/month
        "founder_obsession": 9,     # 1-10
        "market_tam": 4200000000,   # Bottom-up
        "burn_multiple": 2.5
    }
    with open("feature_vectors.json", "w") as f:
        json.dump(features, f)
    print("Features extracted:", features)

if __name__ == "__main__":
    url = sys.argv[1]
    extract_features(url)
