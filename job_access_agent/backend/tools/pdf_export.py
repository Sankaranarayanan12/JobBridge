import json
import os
import subprocess
import platform
from datetime import datetime
from xml.sax.saxutils import escape


def save_as_pdf(results_json: str, filename: str = "job_results.pdf") -> dict:
    """
    Saves job search results as a formatted PDF on the local system
    and tries to open it automatically.
    """
    try:
        data = json.loads(results_json)
    except json.JSONDecodeError as e:
        return {"status": "error", "message": f"Invalid JSON: {str(e)}"}

    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable

      
        if os.name == "nt":
            desktop = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
            if not os.path.exists(desktop):
                desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        else:
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")

        output_dir = desktop if os.path.exists(desktop) else os.path.dirname(os.path.abspath(__file__))
        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name, ext = os.path.splitext(filename)
        ext = ext if ext.lower() == ".pdf" else ".pdf"
        pdf_filename = f"{base_name}_{timestamp}{ext}"
        pdf_path = os.path.join(output_dir, pdf_filename)

        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=A4,
            leftMargin=2 * cm,
            rightMargin=2 * cm,
            topMargin=2 * cm,
            bottomMargin=2 * cm,
        )

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "Title", parent=styles["Heading1"],
            fontSize=20, textColor=colors.HexColor("#0F172A"), spaceAfter=4,
        )
        subtitle_style = ParagraphStyle(
            "Subtitle", parent=styles["Normal"],
            fontSize=10, textColor=colors.HexColor("#64748B"), spaceAfter=16,
        )
        job_title_style = ParagraphStyle(
            "JobTitle", parent=styles["Heading2"],
            fontSize=14, textColor=colors.HexColor("#0F172A"), spaceBefore=16, spaceAfter=2,
        )
        company_style = ParagraphStyle(
            "Company", parent=styles["Normal"],
            fontSize=10, textColor=colors.HexColor("#475569"), spaceAfter=6,
        )
        note_style = ParagraphStyle(
            "Note", parent=styles["Normal"],
            fontSize=9, textColor=colors.HexColor("#B45309"), leftIndent=8, spaceAfter=8,
        )
        flag_style = ParagraphStyle(
            "Flag", parent=styles["Normal"],
            fontSize=9, textColor=colors.HexColor("#0369A1"), leftIndent=8, spaceAfter=8,
        )
        section_label_style = ParagraphStyle(
            "SectionLabel", parent=styles["Normal"],
            fontSize=8, textColor=colors.HexColor("#94A3B8"),
            spaceBefore=10, spaceAfter=4, fontName="Helvetica-Bold",
        )
        draft_style = ParagraphStyle(
            "Draft", parent=styles["Normal"],
            fontSize=9, textColor=colors.HexColor("#1E293B"),
            backColor=colors.HexColor("#F8FAFC"), borderPadding=(8, 8, 8, 8),
            leftIndent=8, rightIndent=8, leading=14, spaceAfter=8,
        )
        footer_style = ParagraphStyle(
            "Footer", parent=styles["Normal"],
            fontSize=8, textColor=colors.HexColor("#94A3B8"), spaceAfter=0,
        )

        story = []
        jobs = data.get("viable_jobs", [])
        

        story.append(Paragraph("JobBridge", title_style))
        story.append(Paragraph(
    f"Accessible Job Matches &amp; Application Drafts &nbsp;·&nbsp; {len(jobs)} viable listings",
    subtitle_style
))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#E2E8F0")))

        if not jobs:
            story.append(Spacer(1, 24))
            story.append(Paragraph("No compatible listings found for this search.", styles["Normal"]))
        else:
            for i, job in enumerate(jobs):
                story.append(Spacer(1, 8))
                story.append(Paragraph(escape(job.get("title", "Untitled Role")), job_title_style))

                company  = escape(job.get("company", "Unknown Company"))
                location = escape(job.get("location", ""))
                company_line = company if not location else f"{company} &nbsp;·&nbsp; {location}"
                story.append(Paragraph(company_line, company_style))
                
                if job.get("flag"):
                    story.append(Paragraph(f"◎  {escape(job['flag'])}", flag_style))

                if job.get("url"):
                    safe_url = escape(job["url"])
                    story.append(Paragraph(
                        f'<a href="{safe_url}" color="#2563EB">{safe_url}</a>',
                        company_style
                    ))

                story.append(Paragraph("DRAFT APPLICATION EMAIL", section_label_style))
                raw_draft = job.get("application_draft", "")
                raw_draft = raw_draft.replace("\\n", "\n")
                draft_text = escape(raw_draft).replace("\n", "<br/>")
                story.append(Paragraph(draft_text, draft_style))

                if i < len(jobs) - 1:
                    story.append(Spacer(1, 8))
                    story.append(HRFlowable(
                        width="100%", thickness=0.5,
                        color=colors.HexColor("#E2E8F0"), dash=(3, 3)
                    ))

        story.append(Spacer(1, 24))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#E2E8F0")))
        story.append(Spacer(1, 6))
        story.append(Paragraph(
            "Generated by JobBridge · All application emails are drafts for review before sending.",
            footer_style
        ))

        doc.build(story)

        try:
            if platform.system() == "Windows":
                os.startfile(pdf_path)
            elif platform.system() == "Darwin":
                subprocess.run(["open", pdf_path], check=False)
            else:
                subprocess.run(["xdg-open", pdf_path], check=False)
        except Exception:
            pass

        return {
            "status": "success",
            "filename": pdf_filename,
            "records_saved": len(jobs),
            "pdf_url": f"file:///{pdf_path.replace(os.sep, '/')}",
            "local_path": pdf_path,
            "note": f"PDF saved to {pdf_path}",
        }

    except ImportError:
        return {"status": "error", "message": "reportlab not installed. Run: pip install reportlab"}
    except Exception as e:
        return {"status": "error", "message": str(e)}