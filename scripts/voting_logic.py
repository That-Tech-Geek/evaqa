import json

def tally_votes():
    with open("council_votes.json") as f:
        votes = json.load(f)

    if any(v[0]=="BLOCK" for v in votes.values()):
        verdict = "CONDITIONAL / BLOCK"
    elif all(v[0]=="APPROVE" for v in votes.values()):
        verdict = "AUTO-WIRE"
    else:
        verdict = "HUMAN INTERVENTION"

    with open("verdict.json", "w") as f:
        json.dump({"verdict": verdict}, f)
    print("Verdict:", verdict)

if __name__ == "__main__":
    tally_votes()
