import os
import httpx


VERBAL_SIGNALS = [
    "verbal communication", "standup", "stand-up", "client calls",
    "phone calls", "presentations", "voice", "spoken", "oral",
    "meetings", "conference calls", "customer facing", "client-facing"
]

ASYNC_SIGNALS = [
    "written communication", "email", "slack", "async", "asynchronous",
    "documentation", "remote", "text-based", "chat"
]


def search_jobs(query: str, location: str) -> dict:
    """
    Searches for jobs using Adzuna API.
 
    """
    app_id = os.getenv("ADZUNA_APP_ID")
    api_key = os.getenv("ADZUNA_API_KEY")

    if not app_id or not api_key:
        return {
            "status": "error",
            "message": (
                "Adzuna API keys not set. "
                "Add ADZUNA_APP_ID and ADZUNA_API_KEY to your .env file. "
                "Register free at https://developer.adzuna.com"
            )
        }

    try:
        url = (
            f"https://api.adzuna.com/v1/api/jobs/in/search/1"
            f"?app_id={app_id}&app_key={api_key}"
            f"&results_per_page=3"
            f"&what={query}"
            f"&where={location}"
            f"&content-type=application/json"
        )
        response = httpx.get(url, timeout=10.0)

        if response.status_code == 200:
            data = response.json()
            listings = []
            for result in data.get("results", []):
                listings.append({
                    "id": result.get("id"),
                    "title": result.get("title"),
                    "company": result.get("company", {}).get("display_name"),
                    "location": result.get("location", {}).get("display_name"),
                    "description": result.get("description", ""),
                    "url": result.get("redirect_url")
                })

            if not listings:
                return {
                    "status": "error",
                    "message": f"No listings found for '{query}' in '{location}'. Try broader terms."
                }

            return {"status": "success", "listings": listings}

        return {
            "status": "error",
            "message": f"Adzuna returned status {response.status_code}: {response.text[:200]}"
        }

    except httpx.TimeoutException:
        return {"status": "error", "message": "Adzuna API timed out. Try again."}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def assess_communication_requirements(job_description: str) -> dict:
    """
    Deterministic keyword filter.
    Checks verbal vs async communication signals in a job description.
    """
    desc_lower = job_description.lower()

    verbal_hits = [s for s in VERBAL_SIGNALS if s in desc_lower]
    async_hits = [s for s in ASYNC_SIGNALS if s in desc_lower]

    if verbal_hits and not async_hits:
        verdict = "likely_incompatible"
    elif async_hits and not verbal_hits:
        verdict = "likely_compatible"
    else:
        verdict = "ambiguous"

    return {
        "verdict": verdict,
        "verbal_signals_found": verbal_hits,
        "async_signals_found": async_hits,
        "requires_agent_judgment": verdict == "ambiguous"
    }


