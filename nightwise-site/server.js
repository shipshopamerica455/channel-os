// NightWise site: serves the static quiz page and proxies signups to MailerLite.
// Zero npm dependencies — plain Node 18+.
const http = require("http");
const fs = require("fs");
const path = require("path");

const PORT = process.env.PORT || 10000;
const TOKEN = process.env.MAILERLITE_TOKEN || (() => {
  try { return fs.readFileSync(path.join(require("os").homedir(), ".nightwise-mailerlite-token"), "utf8").trim(); }
  catch { return undefined; }
})();
const GROUP_ID = "192788827764426311"; // NightWise Quiz group

const PUBLIC_DIR = path.join(__dirname, "public");
const MIME = { ".html": "text/html", ".css": "text/css", ".js": "text/javascript", ".png": "image/png", ".svg": "image/svg+xml", ".ico": "image/x-icon" };

const ALLOWED_FIELDS = ["sleep_problem", "bedroom_issue", "mattress_age", "screens_in_bed", "caffeine_after_2pm", "wake_style"];

async function subscribe(body) {
  const email = String(body.email || "").trim().toLowerCase();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return { status: 400, json: { error: "Please enter a valid email address." } };
  if (body.website) return { status: 200, json: { ok: true } }; // honeypot

  const fields = { name: String(body.name || "").trim().slice(0, 80) };
  for (const key of ALLOWED_FIELDS) {
    if (body[key]) fields[key] = String(body[key]).slice(0, 120);
  }

  const res = await fetch("https://connect.mailerlite.com/api/subscribers", {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${TOKEN}` },
    body: JSON.stringify({ email, fields, groups: [GROUP_ID] }),
  });
  if (res.ok || res.status === 409) return { status: 200, json: { ok: true } };
  const detail = await res.text().catch(() => "");
  console.error("MailerLite error", res.status, detail.slice(0, 300));
  return { status: 502, json: { error: "Something went wrong — please try again in a minute." } };
}

const server = http.createServer((req, res) => {
  if (req.method === "POST" && req.url === "/api/subscribe") {
    let raw = "";
    req.on("data", (c) => { raw += c; if (raw.length > 10_000) req.destroy(); });
    req.on("end", async () => {
      try {
        const out = await subscribe(JSON.parse(raw));
        res.writeHead(out.status, { "Content-Type": "application/json" });
        res.end(JSON.stringify(out.json));
      } catch {
        res.writeHead(400, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ error: "Bad request" }));
      }
    });
    return;
  }

  let file = req.url.split("?")[0];
  if (file === "/" || file === "/quiz") file = "/index.html";
  const full = path.join(PUBLIC_DIR, path.normalize(file));
  if (!full.startsWith(PUBLIC_DIR)) { res.writeHead(403); return res.end(); }
  fs.readFile(full, (err, data) => {
    if (err) { res.writeHead(404, { "Content-Type": "text/plain" }); return res.end("Not found"); }
    res.writeHead(200, { "Content-Type": MIME[path.extname(full)] || "application/octet-stream" });
    res.end(data);
  });
});

server.listen(PORT, () => console.log(`NightWise site on :${PORT}`));
