// Generate the contribution-snake SVGs locally, without depending on any
// third-party GitHub Action.
//
// This script:
//   1. Pulls the public contribution graph for the requested user from a
//      public, unauthenticated API (so no GITHUB_TOKEN is required).
//   2. Reuses the Platane/snk packages (cloned on demand into ./.snk-vendor)
//      to compute the snake route and render the SVGs.
//
// Usage:
//     node .scripts/generate-snake-svgs.mjs [github_user_name]
//
// Outputs (relative to the repo root):
//     dist/github-contribution-grid-snake.svg
//     dist/github-contribution-grid-snake-dark.svg
import { execSync } from "node:child_process";
import * as fs from "node:fs";
import * as path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const REPO_ROOT = path.resolve(path.dirname(__filename), "..");
const SNK_VERSION = "v3.4.0";
const SNK_DIR = path.join(REPO_ROOT, ".snk-vendor");
const DIST_DIR = path.join(REPO_ROOT, "dist");

const userName =
  process.argv[2] ||
  process.env.GITHUB_USER ||
  process.env.GITHUB_REPOSITORY_OWNER ||
  "hazemelerefey";

function ensureSnk() {
  if (fs.existsSync(path.join(SNK_DIR, "packages", "svg-creator"))) return;
  console.log(`cloning Platane/snk@${SNK_VERSION} into ${SNK_DIR}`);
  fs.rmSync(SNK_DIR, { recursive: true, force: true });
  execSync(
    `git clone --depth 1 --branch ${SNK_VERSION} https://github.com/Platane/snk.git "${SNK_DIR}"`,
    { stdio: "inherit" },
  );
  console.log("installing snk dependencies");
  execSync("npm install --silent --no-audit --no-fund", {
    cwd: SNK_DIR,
    stdio: "inherit",
  });
}

async function fetchContributions(user) {
  const url = `https://github-contributions-api.jogruber.de/v4/${encodeURIComponent(user)}?y=last`;
  console.log(`fetching contributions for ${user}`);
  const res = await fetch(url, { headers: { "User-Agent": "snake-svg-gen" } });
  if (!res.ok) {
    throw new Error(`contributions API returned ${res.status} ${res.statusText}`);
  }
  const data = await res.json();

  const days = data.contributions.map((d) => ({
    date: d.date,
    count: d.count,
    level: d.level,
    weekday: new Date(d.date + "T00:00:00Z").getUTCDay(),
  }));

  // Align to the first Sunday so the grid is exactly 7 rows tall.
  let firstIdx = days.findIndex((d) => d.weekday === 0);
  if (firstIdx < 0) firstIdx = 0;

  return days.slice(firstIdx).map((d, i) => ({
    x: Math.floor(i / 7),
    y: i % 7,
    date: d.date,
    count: d.count,
    level: d.level,
  }));
}

async function main() {
  ensureSnk();

  const importTs = async (relPath) => {
    const abs = path.join(SNK_DIR, relPath);
    return import(pathToFileURL(abs).href);
  };

  const [
    { userContributionToGrid },
    { parseOutputsOption },
    { getBestRoute },
    { getPathToPose },
    { snake4 },
    { createSvg },
  ] = await Promise.all([
    importTs("packages/action/userContributionToGrid.ts"),
    importTs("packages/action/outputsOptions.ts"),
    importTs("packages/solver/getBestRoute.ts"),
    importTs("packages/solver/getPathToPose.ts"),
    importTs("packages/types/__fixtures__/snake.ts"),
    importTs("packages/svg-creator/index.ts"),
  ]);

  const cells = await fetchContributions(userName);
  console.log(`fetched ${cells.length} cells`);

  const grid = userContributionToGrid(cells);
  const chain = getBestRoute(grid, snake4);
  if (!chain) throw new Error("snk solver could not find a route");
  chain.push(...getPathToPose(chain[chain.length - 1], snake4));

  const outputs = parseOutputsOption([
    "github-contribution-grid-snake.svg",
    "github-contribution-grid-snake-dark.svg?palette=github-dark",
  ]);

  fs.mkdirSync(DIST_DIR, { recursive: true });
  for (const out of outputs) {
    if (!out || out.format !== "svg") continue;
    const svg = createSvg(grid, cells, chain, out.drawOptions, out.animationOptions);
    const target = path.join(DIST_DIR, out.filename);
    fs.writeFileSync(target, svg);
    console.log(`wrote ${target} (${svg.length} bytes)`);
  }
}

main().catch((err) => {
  console.error("snake-svg generation failed:", err);
  process.exit(1);
});
