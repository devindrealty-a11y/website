/**
 * Checks the condition inspection report: counts, required words, letter size,
 * margins, and that the private page stays unlisted.
 */
import fs from "fs";
import path from "path";
import { spawnSync } from "child_process";
import { fileURLToPath } from "url";
import { PDFDocument } from "pdf-lib";
import { buildReport, findReports } from "./build_condition_report.mjs";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const failures = [];
function assert(cond, message) {
  if (!cond) failures.push(message);
}

const reports = findReports(root);
assert(reports.length === 1, `expected one report, found ${reports.length}`);
const reportPath = reports[0];
const dir = path.dirname(reportPath);
const data = JSON.parse(fs.readFileSync(reportPath, "utf8"));
const { counts, summaryAgrees, maintenanceLists, isBlank } = await import(pathToFile(dir, "report-model.js"));

function pathToFile(folder, name) {
  return new URL(`file://${path.join(folder, name)}`);
}

const tally = counts(data);
assert(summaryAgrees(data, tally), "summary counts do not match the items");
assert(tally.items === 66, `expected 66 items, got ${tally.items}`);
assert(tally.rooms === 8, `expected 8 rooms, got ${tally.rooms}`);
const lists = maintenanceLists(data);
assert(lists.withComment.length === 15, `expected 15 commented items, got ${lists.withComment.length}`);
assert(lists.ratedWithoutComment.length === 5, `expected 5 fair/poor items without comments, got ${lists.ratedWithoutComment.length}`);
const printed = data.rooms.flatMap((room) => room.items.map((item) => item.comment || "")).join("\n");
assert(!printed.includes("[Light?]"), "uncertain [Light?] marker left in a printed comment");
assert(!printed.includes("foot fan"), "voice-to-text 'foot fan' left in a printed comment");
for (const key of ["street_address", "unit", "city", "postal_code"]) {
  assert(isBlank(data.property[key]), `property.${key} should stay blank`);
}
assert(isBlank(data.landlord.name) && isBlank(data.landlord.address_for_service), "landlord fields should stay blank");
assert(isBlank(data.tenancy.start_date) && isBlank(data.tenancy.rent), "tenancy start and rent should stay blank");
assert(isBlank(data.inspection_time_start), "inspection start time should stay blank");

const { outPath, bytes } = await buildReport(reportPath);
const doc = await PDFDocument.load(bytes);
assert(doc.getPageCount() >= 4, `expected several pages, got ${doc.getPageCount()}`);
for (const page of doc.getPages()) {
  const { width, height } = page.getSize();
  assert(Math.abs(width - 612) < 0.1 && Math.abs(height - 792) < 0.1, `page is ${width}x${height}, expected letter`);
}

const text = spawnSync("pdftotext", ["-layout", outPath, "-"], { encoding: "utf8" });
assert(text.status === 0, "pdftotext failed");
const body = text.stdout.replace(/\s+/g, " ");
const required = [
  "AXFORD REAL ESTATE",
  "2326 Clarke St., Port Moody, BC V3H 1Y8",
  "778-355-0116",
  "CONDITION INSPECTION REPORT",
  "Victoria Longbourne",
  "Devin Desaulniers",
  "777262eb-8e67-4a10-b54e-4c92030607f0",
  "Blank — to be completed.",
  "Holes in screens.",
  "Marks on the closet door.",
  "Dark areas along the edges throughout.",
  "Wear and tear in cabinet drawers.",
  "Electrical outlets punched in.",
  "Light under the hood fan is not turning on.",
  "Front left stove-top burner is not working.",
  "Damaged floorboards and chips in flooring.",
  "Three unit keys and one fob key.",
  "10:49 a.m.",
  "11:38 a.m.",
  "within 7 days",
  "s. 23",
  "SS. 18 TO 20",
  "Authorized representative",
  "Not yet attached",
  "Does not mean the landlord was present",
  "The time zone was not stated",
  "0 disagreements",
];
for (const phrase of required) {
  assert(body.includes(phrase), `PDF missing: ${phrase}`);
}
const banned = ["[Light?]", "foot fan", " null", "null", "$1,500", "1,500", "1500", "service fee", "GST", "assumed Pacific"];
for (const phrase of banned) {
  if (phrase === "null") {
    assert(!/\bnull\b/i.test(body), "PDF contains null");
  } else {
    assert(!body.includes(phrase), `PDF contains banned text: ${phrase}`);
  }
}
assert((body.match(/\bGood\b/g) || []).length >= 48, "expected the word Good at least 48 times");
assert((body.match(/\bPoor\b/g) || []).length >= 1, "expected Poor");

const bbox = spawnSync("pdftotext", ["-bbox", outPath, "-"], { encoding: "utf8" });
assert(bbox.status === 0, "pdftotext -bbox failed");
const pages = [...bbox.stdout.matchAll(/<page width="([\d.]+)" height="([\d.]+)">([\s\S]*?)<\/page>/g)];
assert(pages.length === doc.getPageCount(), "bbox page count mismatch");
for (const page of pages) {
  const width = Number(page[1]);
  const height = Number(page[2]);
  const words = [...page[3].matchAll(/<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)"/g)];
  for (const word of words) {
    const xMin = Number(word[1]);
    const yMin = Number(word[2]);
    const xMax = Number(word[3]);
    const yMax = Number(word[4]);
    if (xMin < 36 || xMax > width - 36 || yMin < 20 || yMax > height - 20) {
      failures.push(`text outside margin: x ${xMin}-${xMax} y ${yMin}-${yMax} on a ${width}x${height} page`);
      break;
    }
  }
}

const token = path.basename(dir);
const sitemap = fs.readFileSync(path.join(root, "sitemap.xml"), "utf8");
const robots = fs.readFileSync(path.join(root, "robots.txt"), "utf8");
const home = fs.readFileSync(path.join(root, "index.html"), "utf8");
assert(!sitemap.includes(token), "signing page is in the sitemap");
assert(!robots.includes(token), "signing path is in robots.txt");
assert(!home.includes(token), "signing page is linked from the home page");
const pageHtml = fs.readFileSync(path.join(dir, "index.html"), "utf8");
assert(pageHtml.includes("noindex, nofollow"), "signing page missing noindex");
assert(!pageHtml.includes("nav-links"), "signing page should not use the site nav");

const pageJs = fs.readFileSync(path.join(dir, "page.js"), "utf8");
assert(pageJs.includes("formsubmit.co/ajax/devin@axfordrealestate.ca"), "FormSubmit endpoint missing");
assert(pageJs.includes("SITE_CONFIG"), "page should follow the site FormSubmit config");
assert(pageJs.includes('"_template"') || pageJs.includes("_template"), "FormSubmit table template missing");
assert(pageJs.includes("_honey"), "honeypot missing");

if (failures.length) {
  console.error(failures.join("\n"));
  process.exit(1);
}
console.log(`OK ${doc.getPageCount()} letter pages, ${body.length} chars of text, unlisted path ${token}`);
