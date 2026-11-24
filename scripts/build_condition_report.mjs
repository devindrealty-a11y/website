/**
 * Build the condition inspection PDF from inspections/<id>/report.json.
 *
 *   npm install
 *   node scripts/build_condition_report.mjs
 *   node scripts/build_condition_report.mjs inspections/<id>/report.json
 *
 * Verdana is not licensed for embedding. The PDF uses DejaVu Sans, a wide sans
 * with a large x-height, as the close fallback. The signing page asks the
 * browser for Verdana first.
 */
import fs from "fs";
import path from "path";
import { fileURLToPath, pathToFileURL } from "url";
import fontkit from "@pdf-lib/fontkit";
import * as pdfLib from "pdf-lib";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");

export function findReports(start = root) {
  const dir = path.join(start, "inspections");
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir)
    .map((name) => path.join(dir, name, "report.json"))
    .filter((file) => fs.existsSync(file));
}

function loadPhoto(photosDir, photo, candidates) {
  if (!fs.existsSync(photosDir)) {
    console.warn(`Photograph ${photo.n} not attached. Folder missing: ${photosDir}`);
    return { n: photo.n, bytes: null, format: null };
  }
  for (const name of candidates) {
    const full = path.join(photosDir, name);
    if (!fs.existsSync(full)) continue;
    const ext = path.extname(name).toLowerCase();
    if (ext === ".webp") {
      console.warn(`Skipping ${name}: save a jpg or png for the PDF.`);
      continue;
    }
    if (ext !== ".jpg" && ext !== ".jpeg" && ext !== ".png") continue;
    console.log(`Photograph ${photo.n}: ${name}`);
    return {
      n: photo.n,
      bytes: new Uint8Array(fs.readFileSync(full)),
      format: ext === ".png" ? "png" : "jpg",
    };
  }
  console.warn(`Photograph ${photo.n} not attached. Add ${photo.file} to ${photosDir}`);
  return { n: photo.n, bytes: null, format: null };
}

export async function buildReport(reportPath) {
  const dir = path.dirname(reportPath);
  const data = JSON.parse(fs.readFileSync(reportPath, "utf8"));
  const modelUrl = pathToFileURL(path.join(dir, "report-model.js")).href;
  const pdfUrl = pathToFileURL(path.join(dir, "report-pdf.js")).href;
  const model = await import(modelUrl);
  const { buildConditionReportPdf } = await import(pdfUrl);
  const photosDir = path.join(dir, data.photos_dir || "photos");
  const photos = data.photos.map((photo) => loadPhoto(photosDir, photo, model.photoCandidates(photo)));
  const bytes = await buildConditionReportPdf(pdfLib, fontkit, data, {
    regular: new Uint8Array(fs.readFileSync(path.join(dir, "fonts", "DejaVuSans.ttf"))),
    bold: new Uint8Array(fs.readFileSync(path.join(dir, "fonts", "DejaVuSans-Bold.ttf"))),
    photos,
  });
  const outName = data.output_pdf || "condition-inspection-report.pdf";
  const outPath = path.join(dir, outName);
  fs.writeFileSync(outPath, bytes);
  return { outPath, bytes, data };
}

async function main() {
  const arg = process.argv[2];
  const reports = arg ? [path.resolve(arg)] : findReports();
  if (!reports.length) {
    console.error("No inspections/*/report.json found.");
    process.exit(1);
  }
  if (!arg && reports.length > 1) {
    console.error("More than one report. Pass the report.json path.");
    reports.forEach((file) => console.error(file));
    process.exit(1);
  }
  const { outPath, bytes } = await buildReport(reports[0]);
  console.log(`Wrote ${outPath} (${bytes.length} bytes)`);
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  main().catch((err) => {
    console.error(err);
    process.exit(1);
  });
}
