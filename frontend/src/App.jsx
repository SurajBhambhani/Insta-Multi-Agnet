import { useEffect, useMemo, useState } from "react";
import "./App.css";

const API_BASE = "http://localhost:8000";

const emptyTone = {
  cinematic: 70,
  luxury: 60,
  minimal: 40,
};

function App() {
  const [projects, setProjects] = useState([]);
  const [activeProject, setActiveProject] = useState("");
  const [projectName, setProjectName] = useState("");
  const [languages, setLanguages] = useState(["English", "German", "Hindi"]);
  const [toneProfile, setToneProfile] = useState(emptyTone);
  const [assets, setAssets] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [contentItems, setContentItems] = useState([]);
  const [selectedAssetId, setSelectedAssetId] = useState("");
  const [openAiKey, setOpenAiKey] = useState("");
  const [savingKey, setSavingKey] = useState(false);
  const [keyStatus, setKeyStatus] = useState("");
  const [igUserId, setIgUserId] = useState("");
  const [igAccessToken, setIgAccessToken] = useState("");
  const [igDryRun, setIgDryRun] = useState(true);
  const [igStatus, setIgStatus] = useState("");
  const [publishContentId, setPublishContentId] = useState("");
  const [publishMediaUrl, setPublishMediaUrl] = useState("");
  const [publishing, setPublishing] = useState(false);

  const selectedProject = useMemo(
    () => projects.find((p) => p.id === activeProject),
    [projects, activeProject]
  );

  const loadProjects = async () => {
    const res = await fetch(`${API_BASE}/projects`);
    if (!res.ok) return;
    const data = await res.json();
    setProjects(data);
    if (!activeProject && data.length) {
      setActiveProject(data[0].id);
    }
  };

  const loadAssets = async (projectId) => {
    if (!projectId) return;
    const res = await fetch(`${API_BASE}/assets?project_id=${projectId}`);
    if (!res.ok) return;
    const data = await res.json();
    setAssets(data);
  };

  const loadContentItems = async (projectId) => {
    if (!projectId) return;
    const res = await fetch(`${API_BASE}/content?project_id=${projectId}`);
    if (!res.ok) return;
    const data = await res.json();
    setContentItems(data);
  };

  useEffect(() => {
    loadProjects();
  }, []);

  useEffect(() => {
    if (!activeProject) return;
    loadAssets(activeProject);
    loadContentItems(activeProject);
  }, [activeProject]);

  const createProject = async () => {
    if (!projectName.trim()) return;
    const payload = {
      name: projectName.trim(),
      languages,
      tone_profile: toneProfile,
      privacy_settings: {
        blur_faces: true,
        blur_plates: true,
        hide_children: true,
        mask_location: false,
      },
    };
    const res = await fetch(`${API_BASE}/projects`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (res.ok) {
      setProjectName("");
      await loadProjects();
    }
  };

  const handleFiles = async (event) => {
    if (!activeProject) return;
    const files = Array.from(event.target.files || []);
    if (!files.length) return;
    const form = new FormData();
    form.append("project_id", activeProject);
    files.forEach((file) => form.append("files", file));
    setUploading(true);
    const res = await fetch(`${API_BASE}/assets/ingest`, {
      method: "POST",
      body: form,
    });
    setUploading(false);
    if (res.ok) {
      await loadAssets(activeProject);
      await loadContentItems(activeProject);
    }
  };

  const generateDraft = async () => {
    if (!activeProject || !selectedAssetId) return;
    const res = await fetch(`${API_BASE}/content/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        project_id: activeProject,
        asset_id: selectedAssetId,
      }),
    });
    if (res.ok) {
      await loadContentItems(activeProject);
    }
  };

  const toggleLanguage = (lang) => {
    setLanguages((prev) =>
      prev.includes(lang) ? prev.filter((l) => l !== lang) : [...prev, lang]
    );
  };

  const updateTone = (key, value) => {
    setToneProfile((prev) => ({ ...prev, [key]: Number(value) }));
  };

  const saveOpenAiKey = async () => {
    if (!openAiKey.trim()) return;
    setSavingKey(true);
    const res = await fetch(`${API_BASE}/settings/llm`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        provider: "openai",
        api_key: openAiKey.trim(),
        model: "gpt-4o-mini",
      }),
    });
    setSavingKey(false);
    if (res.ok) {
      setKeyStatus("Saved. Pipeline will use ChatGPT for content.");
      setOpenAiKey("");
    } else {
      setKeyStatus("Could not save key. Check backend logs.");
    }
  };

  const saveInstagramSettings = async () => {
    if (!igUserId.trim() || !igAccessToken.trim()) return;
    const res = await fetch(`${API_BASE}/instagram/settings`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        ig_user_id: igUserId.trim(),
        access_token: igAccessToken.trim(),
        dry_run: igDryRun,
      }),
    });
    if (res.ok) {
      setIgStatus("Instagram settings saved.");
      setIgAccessToken("");
    } else {
      setIgStatus("Could not save Instagram settings.");
    }
  };

  const publishToInstagram = async () => {
    if (!publishContentId || !publishMediaUrl.trim()) return;
    setPublishing(true);
    const res = await fetch(`${API_BASE}/instagram/publish`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        content_item_id: publishContentId,
        media_url: publishMediaUrl.trim(),
        dry_run: igDryRun,
      }),
    });
    setPublishing(false);
    if (res.ok) {
      const data = await res.json();
      setIgStatus(`Instagram: ${data.status} (${data.message})`);
    } else {
      setIgStatus("Instagram publish failed. Check settings or URL.");
    }
  };

  return (
    <div className="app">
      <header className="hero">
        <div>
          <p className="tag">Local Creator Studio</p>
          <h1>Multi-agent content engine for travel creators.</h1>
          <p className="sub">
            Ingest raw media, extract insights, and build multilingual Instagram
            packages in one local workspace.
          </p>
        </div>
        <div className="project-selector">
          <label>Active Project</label>
          <select
            value={activeProject}
            onChange={(event) => setActiveProject(event.target.value)}
          >
            <option value="">Select a project</option>
            {projects.map((project) => (
              <option key={project.id} value={project.id}>
                {project.name}
              </option>
            ))}
          </select>
        </div>
      </header>

      <section className="panel">
        <div className="panel-header">
          <h2>Setup & Preferences</h2>
          <button onClick={createProject}>Create Project</button>
        </div>
        <div className="panel-body split">
          <div>
            <label>Project name</label>
            <input
              value={projectName}
              onChange={(event) => setProjectName(event.target.value)}
              placeholder="Barcelona Summer 2025"
            />
            <label>Languages</label>
            <div className="chip-row">
              {["English", "German", "Hindi"].map((lang) => (
                <button
                  key={lang}
                  type="button"
                  className={languages.includes(lang) ? "chip active" : "chip"}
                  onClick={() => toggleLanguage(lang)}
                >
                  {lang}
                </button>
              ))}
            </div>
            <label>ChatGPT API key (optional)</label>
            <input
              type="password"
              value={openAiKey}
              onChange={(event) => setOpenAiKey(event.target.value)}
              placeholder="sk-..."
            />
            <button
              type="button"
              className="secondary"
              onClick={saveOpenAiKey}
              disabled={savingKey}
            >
              {savingKey ? "Saving..." : "Save key"}
            </button>
            {keyStatus && <p className="status">{keyStatus}</p>}
            <label>Instagram User ID</label>
            <input
              value={igUserId}
              onChange={(event) => setIgUserId(event.target.value)}
              placeholder="1789..."
            />
            <label>Instagram Access Token</label>
            <input
              type="password"
              value={igAccessToken}
              onChange={(event) => setIgAccessToken(event.target.value)}
              placeholder="EAAG..."
            />
            <label className="checkbox">
              <input
                type="checkbox"
                checked={igDryRun}
                onChange={(event) => setIgDryRun(event.target.checked)}
              />
              Dry run (no post)
            </label>
            <button type="button" className="secondary" onClick={saveInstagramSettings}>
              Save Instagram settings
            </button>
          </div>
          <div>
            <label>Tone profile</label>
            <div className="slider-group">
              <div>
                <span>Cinematic</span>
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={toneProfile.cinematic}
                  onChange={(event) => updateTone("cinematic", event.target.value)}
                />
              </div>
              <div>
                <span>Luxury</span>
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={toneProfile.luxury}
                  onChange={(event) => updateTone("luxury", event.target.value)}
                />
              </div>
              <div>
                <span>Minimal</span>
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={toneProfile.minimal}
                  onChange={(event) => updateTone("minimal", event.target.value)}
                />
              </div>
            </div>
          </div>
          <div>
            <label>Privacy defaults</label>
            <ul className="checklist">
              <li>Blur faces + plates</li>
              <li>Hide children</li>
              <li>Optional location masking</li>
            </ul>
          </div>
        </div>
      </section>

      <section className="panel">
        <div className="panel-header">
          <h2>Ingest & Library</h2>
          <div className="inline-actions">
            <label className="upload">
              <input
                type="file"
                multiple
                webkitdirectory="true"
                onChange={handleFiles}
              />
              Add folder
            </label>
            <label className="upload">
              <input type="file" multiple onChange={handleFiles} />
              Add files
            </label>
          </div>
        </div>
        <div className="panel-body">
          {uploading && <p className="status">Uploading...</p>}
          <div className="grid">
            {assets.map((asset) => (
              <div
                key={asset.id}
                className={asset.id === selectedAssetId ? "card selected" : "card"}
                onClick={() => setSelectedAssetId(asset.id)}
                role="button"
                tabIndex={0}
              >
                <h3>{asset.type.toUpperCase()}</h3>
                <p className="muted">{asset.path.split("/").slice(-1)}</p>
                <div className="meta">
                  <span>{asset.resolution || "--"}</span>
                  <span>{asset.duration ? `${asset.duration}s` : ""}</span>
                </div>
                <div className="tags">
                  {Object.entries(asset.quality_scores).map(([key, value]) => (
                    <span key={key}>{key}: {value}</span>
                  ))}
                </div>
              </div>
            ))}
            {!assets.length && (
              <div className="empty">No assets yet. Add a folder to begin.</div>
            )}
          </div>
        </div>
      </section>

      <section className="panel">
        <div className="panel-header">
          <h2>Content Builder</h2>
          <button onClick={generateDraft} disabled={!selectedAssetId}>
            Generate Instagram Draft
          </button>
        </div>
        <div className="panel-body">
          {!selectedAssetId && (
            <p className="status">Select one image to generate a draft.</p>
          )}
          <div className="content-list">
            {contentItems.map((item) => (
              <article key={item.id} className="content-card">
                <div>
                  <h3>{item.format.toUpperCase()}</h3>
                  <p className="muted">Status: {item.status}</p>
                </div>
                <div className="caption-block">
                  <p><strong>EN:</strong> {item.captions.en || ""}</p>
                  <p><strong>DE:</strong> {item.captions.de || ""}</p>
                  <p><strong>HI:</strong> {item.captions.hi || ""}</p>
                </div>
              </article>
            ))}
            {!contentItems.length && (
              <div className="empty">No drafts yet. Generate one to start.</div>
            )}
          </div>
        </div>
      </section>

      <section className="panel">
        <div className="panel-header">
          <h2>Posting Packages</h2>
          <p className="muted">Export-ready items will appear here.</p>
        </div>
        <div className="panel-body">
          {selectedProject ? (
            <div className="package">
              <h3>{selectedProject.name}</h3>
              <p className="muted">Assets: {assets.length}</p>
              <p className="muted">Drafts: {contentItems.length}</p>
            </div>
          ) : (
            <div className="empty">Select a project to see packages.</div>
          )}
        </div>
      </section>

      <section className="panel">
        <div className="panel-header">
          <h2>Instagram Publishing</h2>
          <button onClick={publishToInstagram} disabled={publishing}>
            {publishing ? "Publishing..." : "Publish Draft"}
          </button>
        </div>
        <div className="panel-body split">
          <div>
            <label>Draft to publish</label>
            <select
              value={publishContentId}
              onChange={(event) => setPublishContentId(event.target.value)}
            >
              <option value="">Select a draft</option>
              {contentItems.map((item) => (
                <option key={item.id} value={item.id}>
                  {item.format.toUpperCase()} · {item.id.slice(0, 8)}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label>Public media URL</label>
            <input
              value={publishMediaUrl}
              onChange={(event) => setPublishMediaUrl(event.target.value)}
              placeholder="https://public-url.com/image.jpg"
            />
            <p className="muted">
              Instagram Graph API requires a publicly accessible media URL.
            </p>
          </div>
          {igStatus && <p className="status">{igStatus}</p>}
        </div>
      </section>
    </div>
  );
}

export default App;
