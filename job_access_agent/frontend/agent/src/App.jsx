import { useEffect, useRef, useState } from "react"

const STEPS = [
  {
    key: "JobAccessAgent",
    label: "Searching, Filtering & Drafting",
    desc: "Finding listings, removing voice-based roles, writing emails",
  },
  {
    key: "saving",
    label: "Saving PDF",
    desc: "Exporting results to your Desktop",
  },
]

const COMM_OPTIONS = [
  "Figma comments", "Slack", "Email", "Jira",
  "GitHub", "Confluence", "WhatsApp", "Notion",
]

function Tag({ children, color = "slate" }) {
  const map = {
    cyan:    "bg-cyan-400/10 text-cyan-400 border-cyan-400/20",
    emerald: "bg-emerald-400/10 text-emerald-400 border-emerald-400/20",
    amber:   "bg-amber-400/10 text-amber-400 border-amber-400/20",
    slate:   "bg-slate-700/40 text-slate-400 border-slate-700",
  }
  return (
    <span className={`text-[10px] font-mono px-2 py-0.5 rounded-full border ${map[color]}`}>
      {children}
    </span>
  )
}

function Divider() {
  return <div className="border-t border-[#1F2937] my-6" />
}

// ─── Screen 1: User Profile ───────────────────────────────────────────────────
function ProfileScreen({ onNext }) {
  const [form, setForm] = useState({
    name: "", role: "", location: "", skills: "", commTools: [], extra: "",
  })

  const set = (k, v) => setForm(prev => ({ ...prev, [k]: v }))

  const toggleTool = (tool) => {
    set("commTools",
      form.commTools.includes(tool)
        ? form.commTools.filter(x => x !== tool)
        : [...form.commTools, tool]
    )
  }

  const valid = form.name.trim() && form.role.trim() && form.location.trim()

  return (
    <div className="max-w-xl mx-auto fade-up">
      <div className="mb-8">
        <p className="text-xs font-mono text-cyan-400 mb-2 tracking-widest">STEP 1 OF 2</p>
        <h2 className="text-2xl font-display font-bold text-white">Tell us about yourself</h2>
        <p className="text-slate-400 text-sm mt-1">
          Your details personalise every application email we draft for you.
        </p>
      </div>

      <div className="space-y-4">
        <div>
          <label className="block text-xs text-slate-400 mb-1.5">
            Full name <span className="text-cyan-400">*</span>
          </label>
          <input
            value={form.name}
            onChange={e => set("name", e.target.value)}
            placeholder="e.g. Narayanan V"
            className="w-full bg-[#111827] border border-[#1F2937] rounded-xl px-4 py-3 text-sm text-white placeholder-slate-600 focus:outline-none focus:border-cyan-500 transition-colors"
          />
        </div>

        <div className="flex gap-3">
          <div className="flex-1">
            <label className="block text-xs text-slate-400 mb-1.5">
              Job role you want <span className="text-cyan-400">*</span>
            </label>
            <input
              value={form.role}
              onChange={e => set("role", e.target.value)}
              placeholder="e.g. UI Designer, Data Entry, QA Engineer"
              className="w-full bg-[#111827] border border-[#1F2937] rounded-xl px-4 py-3 text-sm text-white placeholder-slate-600 focus:outline-none focus:border-cyan-500 transition-colors"
            />
          </div>
          <div className="w-40">
            <label className="block text-xs text-slate-400 mb-1.5">
              Location <span className="text-cyan-400">*</span>
            </label>
            <input
              value={form.location}
              onChange={e => set("location", e.target.value)}
              placeholder="e.g. Chennai"
              className="w-full bg-[#111827] border border-[#1F2937] rounded-xl px-4 py-3 text-sm text-white placeholder-slate-600 focus:outline-none focus:border-cyan-500 transition-colors"
            />
          </div>
        </div>

        <div>
          <label className="block text-xs text-slate-400 mb-1.5">Your key skills</label>
          <input
            value={form.skills}
            onChange={e => set("skills", e.target.value)}
            placeholder="e.g. React, Jira, QA, Excel, Figma"
            className="w-full bg-[#111827] border border-[#1F2937] rounded-xl px-4 py-3 text-sm text-white placeholder-slate-600 focus:outline-none focus:border-cyan-500 transition-colors"
          />
        </div>

        <div>
          <label className="block text-xs text-slate-400 mb-2">Communication tools you use</label>
          <div className="flex flex-wrap gap-2">
            {COMM_OPTIONS.map(tool => (
              <button
                key={tool}
                type="button"
                onClick={() => toggleTool(tool)}
                className={`text-xs px-3 py-1.5 rounded-full border transition-all ${
                  form.commTools.includes(tool)
                    ? "bg-cyan-400/10 border-cyan-400/40 text-cyan-300"
                    : "bg-[#111827] border-[#1F2937] text-slate-400 hover:border-slate-500"
                }`}
              >
                {tool}
              </button>
            ))}
          </div>
        </div>

        <div>
          <label className="block text-xs text-slate-400 mb-1.5">
            Anything else to mention? <span className="text-slate-600">(optional)</span>
          </label>
          <textarea
            value={form.extra}
            onChange={e => set("extra", e.target.value)}
            rows={2}
            placeholder="e.g. Open to remote, available immediately, comfortable with async collaboration"
            className="w-full bg-[#111827] border border-[#1F2937] rounded-xl px-4 py-3 text-sm text-white placeholder-slate-600 focus:outline-none focus:border-cyan-500 transition-colors resize-none"
          />
        </div>

        <button
          type="button"
          onClick={() => valid && onNext(form)}
          disabled={!valid}
          className="w-full py-3.5 rounded-xl bg-cyan-400 hover:bg-cyan-300 disabled:bg-[#1F2937] disabled:text-slate-600 disabled:cursor-not-allowed text-[#0A0E1A] font-bold text-sm transition-all duration-200 mt-2"
        >
          Find my jobs →
        </button>
      </div>
    </div>
  )
}

// ─── Pipeline Step Node ───────────────────────────────────────────────────────
function StepNode({ step, state, tools, isLast }) {
  const active  = state === "active"
  const done    = state === "complete"
  const pending = state === "pending"

  return (
    <div className="flex gap-4">
      <div className="flex flex-col items-center">
        <div className={`w-9 h-9 rounded-full border-2 flex items-center justify-center text-sm shrink-0 transition-all duration-500
          ${active  ? "border-cyan-400 bg-cyan-400/10 text-cyan-400 pulse-cyan" : ""}
          ${done    ? "border-emerald-400 bg-emerald-400/10 text-emerald-400"   : ""}
          ${pending ? "border-[#1F2937] bg-[#111827] text-slate-700"            : ""}`}
        >
          {done ? "✓" : active ? "◉" : "○"}
        </div>
        {!isLast && (
          <div className={`w-px flex-1 min-h-8 mt-1 transition-all duration-700 ${done ? "bg-emerald-400/30" : "bg-[#1F2937]"}`} />
        )}
      </div>

      <div className="pb-7 flex-1 min-w-0">
        <div className="flex items-center gap-2 mb-0.5">
          <span className={`text-sm font-semibold transition-colors ${
            active ? "text-cyan-300" : done ? "text-emerald-300" : "text-slate-600"
          }`}>
            {step.label}
          </span>
          {active && (
            <span className="flex gap-0.5">
              {[0, 1, 2].map(i => (
                <span key={i} className="w-1 h-1 rounded-full bg-cyan-400 animate-bounce"
                  style={{ animationDelay: `${i * 0.15}s` }} />
              ))}
            </span>
          )}
        </div>
        <p className={`text-xs ${pending ? "text-slate-700" : "text-slate-500"}`}>
          {step.desc}
        </p>
        {tools?.length > 0 && (
          <div className="flex flex-wrap gap-1.5 mt-2">
            {tools.map((tool, i) => <Tag key={i} color="cyan">{tool}()</Tag>)}
          </div>
        )}
      </div>
    </div>
  )
}


// ─── Screen 2: Search + Results ───────────────────────────────────────────────
function SearchScreen({ profile, onBack }) {
  const [status, setStatus]       = useState("idle")
  const [stepStates, setStepStates] = useState({})
  const [toolMap, setToolMap]     = useState({})
  const [jobs, setJobs]           = useState([])
  const [error, setError]         = useState("")
  const esRef = useRef(null)

  const setStep = (key, value) => setStepStates(prev => ({ ...prev, [key]: value }))
  const addTool = (agent, tool)  => setToolMap(prev => {
    const existing = prev[agent] || []
    if (existing.includes(tool)) return prev
    return { ...prev, [agent]: [...existing, tool] }
  })

  const closeStream = () => {
    if (esRef.current) { esRef.current.close(); esRef.current = null }
  }

  useEffect(() => () => closeStream(), [])

  const run = () => {
    closeStream()
    setStatus("running")
    setStepStates({})
    setToolMap({})
    setJobs([])
    setError("")

    const tools = profile.commTools?.join(", ") || ""
    const prompt = [
      `I am deaf and mute. My name is ${profile.name}.`,
      `Find me ${profile.role} jobs in ${profile.location}.`,
      `I cannot attend voice calls, phone interviews, or verbal meetings.`,
      tools ? `I communicate well via ${tools}.` : "",
      profile.skills ? `My skills include: ${profile.skills}.` : "",
      profile.extra || "",
    ].filter(Boolean).join(" ")

    const params = new URLSearchParams({ query: profile.role, location: profile.location, prompt })
    const es = new EventSource(`/api/stream?${params.toString()}`)
    esRef.current = es

    es.addEventListener("agent_start",       e => { const { agent } = JSON.parse(e.data); setStep(agent, "active") })
    es.addEventListener("agent_complete",    e => { const { agent } = JSON.parse(e.data); setStep(agent, "complete") })
    es.addEventListener("tool_call",         e => { const { agent, tool } = JSON.parse(e.data); addTool(agent, tool) })
    es.addEventListener("pipeline_complete", e => {
      const { jobs: resultJobs = [] } = JSON.parse(e.data)
      setJobs(resultJobs)
      setStatus("complete")
      closeStream()
    })
    es.addEventListener("server_error", e => {
      try { setError(JSON.parse(e.data).message || "Something went wrong.") }
      catch { setError("Something went wrong.") }
      setStatus("error")
      closeStream()
    })
    es.onerror = () => {
      if (es.readyState === EventSource.CLOSED) return
      setError("Connection lost.")
      setStatus("error")
      closeStream()
    }
  }

  const reset = () => {
    closeStream()
    setStatus("idle")
    setStepStates({})
    setToolMap({})
    setJobs([])
    setError("")
  }

  return (
    <div className="max-w-2xl mx-auto">
      <div className="flex items-center justify-between mb-8 px-4 py-3 rounded-xl bg-[#111827] border border-[#1F2937]">
        <div className="text-sm">
          <span className="text-white font-medium">{profile.name}</span>
          <span className="text-slate-500 mx-2">·</span>
          <span className="text-slate-400">{profile.role} in {profile.location}</span>
        </div>
        <button type="button" onClick={onBack}
          className="text-xs text-slate-500 hover:text-slate-300 transition-colors">
          Edit profile
        </button>
      </div>

      {status === "idle" && (
        <div className="text-center fade-up">
          <h2 className="text-xl font-display font-bold text-white mb-2">Ready to find your jobs</h2>
          <p className="text-slate-400 text-sm mb-6">
            We'll search listings, filter out voice-based roles, and draft two emails per job —
            an application and an accommodation inquiry.
          </p>
          <button type="button" onClick={run}
            className="px-8 py-3.5 rounded-xl bg-cyan-400 hover:bg-cyan-300 text-[#0A0E1A] font-bold text-sm transition-all">
            Start job search →
          </button>
        </div>
      )}

      {(status === "running" || status === "complete" || status === "error") && (
        <div className="mb-8">
          <p className="text-[10px] font-mono text-slate-500 uppercase tracking-widest mb-5">Agent Pipeline</p>
          {STEPS.map((step, index) => (
            <StepNode
              key={step.key}
              step={step}
              state={stepStates[step.key] || "pending"}
              tools={toolMap[step.key] || []}
              isLast={index === STEPS.length - 1}
            />
          ))}
        </div>
      )}

      {status === "error" && (
        <div className="px-4 py-3 rounded-xl border border-red-400/20 bg-red-400/5 text-red-300 text-sm mb-6">
          {error}
          <button type="button" onClick={reset} className="ml-3 text-red-400 underline text-xs">
            Try again
          </button>
        </div>
      )}

      {status === "complete" && (
        <div className="fade-up">
          <Divider />
          <div className="flex items-center justify-between mb-4">
            <button type="button" onClick={reset}
              className="text-xs text-slate-500 hover:text-slate-300 transition-colors">
              New search
            </button>
          </div>

        </div>
      )}
    </div>
  )
}

// ─── Root App ─────────────────────────────────────────────────────────────────
export default function App() {
  const [screen, setScreen]   = useState("profile")
  const [profile, setProfile] = useState(null)

  return (
    <div className="min-h-screen bg-[#0A0E1A]">
      <header className="border-b border-[#1F2937] px-6 py-4 mb-10">
        <div className="max-w-2xl mx-auto flex items-center gap-3">
          <div className="w-7 h-7 rounded-lg bg-cyan-400/10 border border-cyan-400/30 flex items-center justify-center">
            <span className="text-cyan-400 text-xs">JB</span>
          </div>
          <div>
            <span className="font-display font-bold text-white text-base">JobBridge</span>
            <span className="text-slate-600 text-xs ml-2">
              Accessible job matching for deaf & mute professionals
            </span>
          </div>
        </div>
      </header>

      <main className="px-6 pb-16">
        {screen === "profile" && (
          <ProfileScreen onNext={profileData => { setProfile(profileData); setScreen("search") }} />
        )}
        {screen === "search" && profile && (
          <SearchScreen profile={profile} onBack={() => setScreen("profile")} />
        )}
      </main>
    </div>
  )
}