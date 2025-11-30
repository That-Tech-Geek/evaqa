import json
from fpdf import FPDF

def generate_memo():
    with open("council_votes.json") as f:
        votes = json.load(f)
    with open("verdict.json") as f:
        verdict = json.load(f)["verdict"]

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200,10,"One-Page Truth Memo", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200,10,f"Verdict: {verdict}", ln=True)
    pdf.ln(5)
    for agent, vote in votes.items():
        pdf.cell(200,10,f"{agent.title()}: {vote[0]} | {vote[1]}", ln=True)

    pdf.output("One_Page_Truth.pdf")
    print("PDF generated")

if __name__ == "__main__":
    generate_memo()
