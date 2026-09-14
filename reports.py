from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import pandas as pd


def generate_entries_pdf(df) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Energy Cost Report", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Total Cost: ${df['cost_usd'].sum():,.2f}", styles["Normal"]))
    story.append(Paragraph(f"Entries: {len(df)}", styles["Normal"]))
    story.append(Spacer(1, 20))

    table_data = [["Date", "Source", "Currency", "Cost", "Cost (USD)", "kWh", "Notes"]]
    for _, row in df.iterrows():
        table_data.append([
            str(row["date"]), row["source"], row["currency"],
            f"{row['cost']:.2f}", f"{row['cost_usd']:.2f}",
            str(row["units_kwh"]) if not pd.isna(row["units_kwh"]) else "-",
            str(row["notes"]) if row["notes"] else "",
        ])

    table = Table(table_data, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a2b4a")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(table)

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()