import os, sys, json, uuid, asyncio, re

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def sse(event, data):
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


async def real_pipeline(prompt, query, location):
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.genai import types as genai_types
    from agent import root_agent

    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent,
        app_name="job_access_agent",
        session_service=session_service,
    )

    session_id, user_id = str(uuid.uuid4()), "user"
    await session_service.create_session(
        app_name="job_access_agent",
        user_id=user_id,
        session_id=session_id,
    )

    content = genai_types.Content(
        role="user",
        parts=[genai_types.Part(text=prompt)],
    )

    current_agent = None

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content,
    ):
        author = getattr(event, "author", None)

        if author and author != current_agent:
            if current_agent:
                yield sse("agent_complete", {"agent": current_agent})
            current_agent = author
            yield sse("agent_start", {"agent": author})
            await asyncio.sleep(0)

        if event.content and event.content.parts:
            for part in event.content.parts:
                fc = getattr(part, "function_call", None)
                if fc:
                    yield sse("tool_call", {"agent": author, "tool": fc.name})
                    await asyncio.sleep(0)

        if event.is_final_response():
            # Read text from event content directly
            raw = ""
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, "text") and part.text:
                        raw += part.text

            # Fallback to session state
            if not raw:
                session = await session_service.get_session(
                    app_name="job_access_agent",
                    user_id=user_id,
                    session_id=session_id,
                )
                raw = session.state.get("final_output", "") if session else ""

            # Extract JSON from response
            try:
                match = re.search(r'\{.*\}', raw, re.DOTALL)
                clean = match.group(0) if match else raw
                data = json.loads(clean)
            except Exception:
                data = {"viable_jobs": []}

            if current_agent:
                yield sse("agent_complete", {"agent": current_agent})

            yield sse("agent_start",    {"agent": "saving"})
            yield sse("agent_complete", {"agent": "saving"})
            yield sse("pipeline_complete", {
                "jobs":       data.get("viable_jobs", []),
                "pdf_url":    data.get("pdf_url"),
                "local_path": data.get("local_path"),
            })


@app.get("/api/stream")
async def stream(
    query:    str = Query(...),
    location: str = Query(...),
    prompt:   str = Query(""),
):
    async def generate():
        try:
            p = prompt or (
                f"I am deaf and mute. Find me {query} jobs in {location}. "
                f"I cannot attend voice calls or verbal meetings."
            )
            async for chunk in real_pipeline(p, query, location):
                yield chunk
        except Exception as e:
            yield sse("server_error", {"message": str(e)})

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control":    "no-cache",
            "Connection":       "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@app.get("/api/health")
async def health():
    return {"status": "ok"}