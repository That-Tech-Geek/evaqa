import json

def hawk_agent(features): return ("APPROVE", "TAM validated")
def accountant_agent(features): return ("WATCH", "Burn acceptable")
def wargamer_agent(features): return ("APPROVE", "PLG wedge validated")
def psychologist_agent(features): return ("APPROVE", "Founder obsession top 1%")
def gatekeeper_agent(features): return ("BLOCK", "Dead equity detected")

def run_council():
    with open("feature_vectors.json") as f:
        features = json.load(f)

    votes = {}
    votes["hawk"] = hawk_agent(features)
    votes["accountant"] = accountant_agent(features)
    votes["wargamer"] = wargamer_agent(features)
    votes["psychologist"] = psychologist_agent(features)
    votes["gatekeeper"] = gatekeeper_agent(features)

    with open("council_votes.json", "w") as f:
        json.dump(votes, f)
    print("Council votes generated:", votes)

if __name__ == "__main__":
    run_council()
