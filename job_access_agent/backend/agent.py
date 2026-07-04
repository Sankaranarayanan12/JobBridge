import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from google.adk.agents import Agent
from google.adk.models import Gemini

from tools.job_search import (
    search_jobs,
    assess_communication_requirements,

)
from tools.pdf_export import save_as_pdf

model = Gemini(model="gemini-3.5-flash")

root_agent = Agent(
    name="JobAccessAgent",
    model=model,
    instruction="""
You help deaf/mute users find compatible jobs. Complete all steps below in one pass.

STEP 1 — Search:
Call search_jobs with the user's role query and location.

STEP 2 — Filter:
For each listing call assess_communication_requirements with the job title and description combined as one string:
"[title]. [description]"
- likely_incompatible: skip it.
- likely_compatible: keep it.
- ambiguous: keep it, add flag "Verify communication requirements before applying."

STEP 3 — Draft:
For each kept listing write a unique email mentioning the exact job title.
Never reuse the same draft for two different listings:
- State interest in the role and company using the user's name and skills.
- Request written-only accommodation under RPWD Act 2016.
- Add: "I would welcome the opportunity to discuss accommodation specifics with your HR team."
- End with: [DRAFT — Review before sending.]

STEP 4 — Save:
Call save_as_pdf with this JSON:
{
  "viable_jobs": [
    {
      "title": "...",
      "company": "...",
      "location": "...",
      "url": "...",
      "flag": null,
      "application_draft": "...",
      "inquiry_draft": "..."
    }
  ],
  "total_viable": 0,
  "generated_at": "ISO timestamp"
}

After the tool returns successfully, copy its local file information into the final response.
""",
    tools=[
        search_jobs,
        assess_communication_requirements,
        save_as_pdf,
    ],
)