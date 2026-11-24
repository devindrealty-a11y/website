import {
  escapeHtml,
  displayValue,
  partyModel,
  conductedBy,
  formatRecordedDateTime,
  formatNowPacific,
  tableComment,
  maintenanceLists,
  maintenanceLine,
  counts,
  summaryAgrees,
  legalParagraph,
  conditionClass,
  photoCandidates,
  isBlank,
} from "./report-model.js";
import { buildConditionReportPdf } from "./report-pdf.js";

const FALLBACK_ENDPOINT = "https://formsubmit.co/ajax/devin@axfordrealestate.ca";
const reportRoot = document.getElementById("report");

function endpoint() {
  const forms = (window.SITE_CONFIG && window.SITE_CONFIG.forms) || {};
  return String(forms.chatLead || FALLBACK_ENDPOINT).trim();
}

function field(id, label, value, blank) {
  const shown = displayValue(value, blank);
  const cls = shown.blank ? "field-line blank" : "field-line";
  const attr = id ? ` id="${id}"` : "";
  return `<div class="field"><div class="field-label">${escapeHtml(label)}</div><div class="${cls}"${attr}>${escapeHtml(shown.text)}</div></div>`;
}

function render(data) {
  const blank = data.statements.blank;
  const party = partyModel(data);
  const tally = counts(data);
  const lists = maintenanceLists(data);
  const b = data.brokerage;
  const rooms = data.rooms.map((room) => {
    const rows = room.items.map((item) => {
      const comment = tableComment(item);
      return `<tr>
        <td class="item">${escapeHtml(item.item)}</td>
        <td class="cond ${conditionClass(item.condition)}">${escapeHtml(item.condition)}</td>
        <td class="comment">${comment ? escapeHtml(comment) : ""}</td>
      </tr>`;
    }).join("");
    return `<h3 class="room-name">${escapeHtml(room.room)}</h3>
      <table class="room">
        <thead><tr><th>Item</th><th>Condition</th><th>Comments</th></tr></thead>
        <tbody>${rows}</tbody>
      </table>`;
  }).join("");

  const listHtml = (rows) => `<ol class="maint">${rows.map((row) => `<li>${escapeHtml(maintenanceLine(row))}</li>`).join("")}</ol>`;
  const fairBlock = lists.ratedWithoutComment.length
    ? `<h3>Rated Fair or Poor, with no comment recorded</h3>${listHtml(lists.ratedWithoutComment)}`
    : "";
  const match = summaryAgrees(data, tally)
    ? "The room, item, and condition counts below are taken from the items in this report. They match the counts in the inspection record."
    : "The room, item, and condition counts below are taken from the items in this report. They do not match summary_as_recorded in the data file.";
  const summaryRows = [
    ["Rooms inspected", tally.rooms],
    ["Items recorded", tally.items],
    ["Good", tally.conditions.Good],
    ["Fair", tally.conditions.Fair],
    ["Poor", tally.conditions.Poor],
    ["Not applicable", tally.conditions["Not applicable"]],
    ["Photographs in the inspection record", data.summary_as_recorded.photos_in_record],
    ["Photographs attached on this page", "0"],
    ["Maintenance or repair items stated in the record", data.summary_as_recorded.maintenance_repair_count],
    ["Tenant disagreements recorded", data.summary_as_recorded.tenant_disagreements],
  ].map(([label, value], index) => {
    const id = index === 7 ? ` id="photo-count"` : "";
    return `<div><dt>${escapeHtml(label)}</dt><dd${id}>${escapeHtml(value)}</dd></div>`;
  }).join("");

  const photos = data.photos.map((photo) => `<figure class="photo" data-photo="${photo.n}">
      <div class="frame">
        <img alt="" hidden>
        <div class="ph"><strong>Photograph ${photo.n}</strong><span>Not yet attached</span></div>
      </div>
      <figcaption>
        <p>${escapeHtml(photo.caption)}</p>
        <p class="file-hint">Add photos/${escapeHtml(photo.file)} (jpg or png also accepted)</p>
      </figcaption>
    </figure>`).join("");

  reportRoot.innerHTML = `
    <header class="letterhead">
      <div class="letterhead-top"><strong>${escapeHtml(b.name.toUpperCase())}</strong><span>${escapeHtml(b.phone)}</span></div>
      <p>${escapeHtml(b.address)}</p>
    </header>
    <h1>Condition inspection report</h1>
    <p class="sub">Move-in inspection at the start of the tenancy</p>
    <p class="sub">${escapeHtml(party.inspectionDate)}</p>
    <p class="record">Inspection record ${escapeHtml(data.record_id)}</p>
    <p>${escapeHtml(data.statements.prepared_by)}</p>
    <p class="note">${escapeHtml(data.statements.form_note)}</p>
    <p class="note">${escapeHtml(data.statements.move_in_only)}</p>
    <p class="note">${escapeHtml(data.statements.missing_fields)}</p>

    <h2>Parties and rental unit</h2>
    ${field("mirror-landlord-name", "A. Landlord's legal name", party.landlordName, blank)}
    ${field("mirror-landlord-address", "B. Landlord's address for service", party.landlordAddress, blank)}
    ${field("", "C. Tenant's legal name", party.tenantName, blank)}
    ${field("", "D. Rental unit street address", party.street, blank)}
    ${field("", "Unit", party.unit, blank)}
    ${field("", "City", party.city, blank)}
    ${field("", "Postal code", party.postal, blank)}
    ${field("", "E. Date the tenant is entitled to possession", party.possessionDate, blank)}
    ${field("", "F. Move-in inspection date", party.inspectionDate, blank)}
    ${field("", "Inspection start time", party.inspectionStart, blank)}
    <p class="group-label">Tenancy amounts — not recorded in the inspection</p>
    ${field("", "Monthly rent", party.rent, blank)}
    ${field("", "Security deposit", party.securityDeposit, blank)}
    ${field("", "Pet damage deposit", party.petDeposit, blank)}
    <p>${escapeHtml(conductedBy(data))}</p>

    <h2>Condition legend</h2>
    <ul class="legend">
      <li class="cond-good"><span class="swatch cond-good"></span>Good</li>
      <li class="cond-fair"><span class="swatch cond-fair"></span>Fair</li>
      <li class="cond-poor"><span class="swatch cond-poor"></span>Poor</li>
      <li class="cond-na"><span class="swatch cond-na"></span>Not applicable</li>
    </ul>
    <p class="note">${escapeHtml(data.statements.legend_note)}</p>

    <h2>Condition of the rental unit</h2>
    <p class="note">${escapeHtml(data.statements.rooms_note)}</p>
    ${rooms}

    <h2>Damage and items in need of maintenance or repair</h2>
    <p class="note">${escapeHtml(data.statements.maintenance_intro)}</p>
    <h3>Items with a comment</h3>
    ${listHtml(lists.withComment)}
    ${fairBlock}

    <h2>Keys and fobs issued to the tenant</h2>
    <p>${escapeHtml(data.keys.as_written)}</p>
    <dl class="summary"><div><dt>Unit keys</dt><dd>${escapeHtml(data.keys.unit_keys)}</dd></div><div><dt>Fobs</dt><dd>${escapeHtml(data.keys.fobs)}</dd></div></dl>
    <p>Photograph ${escapeHtml(data.keys.photo)} was recorded with the keys.</p>

    <h2>Photographs</h2>
    <p class="note">Four photographs are in the inspection record. Each one appears here when its image file is in the photos folder.</p>
    <div class="photos">${photos}</div>

    <h2>Summary</h2>
    <dl class="summary">${summaryRows}</dl>
    <p class="note">${escapeHtml(match)}</p>

    <h2>Tenant's statement</h2>
    <p>I, ${escapeHtml(data.tenant.name)},</p>
    <div class="check"><span class="box" aria-hidden="true"></span><span>agree that this report fairly represents the condition of the rental unit.</span></div>
    <div class="check"><span class="box" aria-hidden="true"></span><span>do not agree that this report fairly represents the condition of the rental unit, for the following reasons:</span></div>
    ${field("", "Reasons, if the tenant does not agree", null, blank)}
    <p class="note">${escapeHtml(data.statements.tenant_statement_note)}</p>

    <h2>Signatures</h2>
    <section class="card">
      <h3>Tenant</h3>
      <p><strong>${escapeHtml(data.signatures.tenant.name)}</strong></p>
      <p>Tenant</p>
      <p>Signed electronically</p>
      <p>${escapeHtml(formatRecordedDateTime(data.signatures.tenant.signed_at))}</p>
      <p>Recorded in the inspection (Rocket Inspection App).</p>
      <p>${escapeHtml(data.statements.timezone_note)}</p>
    </section>
    <section class="card">
      <h3>Landlord's authorized representative</h3>
      <p><strong>${escapeHtml(data.representative.name)}</strong></p>
      <p>${escapeHtml(data.representative.role)}</p>
      <p>${escapeHtml(data.representative.title)}, ${escapeHtml(b.name)}</p>
      <p><a href="mailto:${escapeHtml(b.email)}">${escapeHtml(b.email)}</a></p>
      <p>Signed electronically</p>
      <p>${escapeHtml(formatRecordedDateTime(data.representative.signed_at))}</p>
      <p>Recorded in the inspection (Rocket Inspection App).</p>
      <p>${escapeHtml(data.statements.representative_disclaimer)}</p>
      <p>${escapeHtml(data.statements.timezone_note)}</p>
    </section>

    <section class="card" id="landlord-sign">
      <h3>Landlord</h3>
      <p class="sign-help">${escapeHtml(data.statements.signing_help)}</p>
      <form id="sign-form" action="#" method="post" novalidate>
        <div class="hp" aria-hidden="true">
          <label>Leave this field empty <input type="text" name="_honey" tabindex="-1" autocomplete="off"></label>
        </div>
        <label class="stack">Landlord's legal name
          <input id="landlord-name" name="landlord_name" type="text" required autocomplete="name" spellcheck="false">
        </label>
        <label class="stack">Address for service
          <textarea id="landlord-address" name="address_for_service" required rows="3" autocomplete="street-address"></textarea>
        </label>
        <div class="sig-label" id="sig-label">Signature</div>
        <canvas id="sig" aria-labelledby="sig-label" tabindex="0"></canvas>
        <div class="row-actions"><button type="button" class="ghost" id="sig-clear">Clear signature</button></div>
        <label class="consent"><input type="checkbox" name="confirm_review" value="yes" required> <span>I have reviewed this report. The name and address above are the landlord's legal name and address for service, and the signature is mine.</span></label>
        <div id="form-status" class="form-status" role="status" aria-live="polite"></div>
        <div class="actions">
          <button type="button" class="secondary" id="download">Download signed PDF</button>
          <button type="submit" class="primary" id="submit-sign">Submit signature</button>
        </div>
      </form>
      <div id="confirmation" class="confirm" hidden tabindex="-1"></div>
    </section>

    <h2>Note — Residential Tenancy Act, s. 23, and Regulation, ss. 18 to 20</h2>
    <p class="note">${escapeHtml(legalParagraph(data))}</p>
  `;
}

function setMirror(id, value, blank) {
  const el = document.getElementById(id);
  const shown = displayValue(value, blank);
  el.textContent = shown.text;
  el.classList.toggle("blank", shown.blank);
}

function showStatus(cls, text) {
  const status = document.getElementById("form-status");
  status.className = "form-status show " + cls;
  status.textContent = text;
}

let libsPromise = null;
function loadScript(src) {
  return new Promise((resolve, reject) => {
    const existing = document.querySelector(`script[data-src="${src}"]`);
    if (existing) {
      if (existing.dataset.loaded === "1") resolve();
      else existing.addEventListener("load", () => resolve(), { once: true });
      return;
    }
    const script = document.createElement("script");
    script.src = src;
    script.dataset.src = src;
    script.onload = () => { script.dataset.loaded = "1"; resolve(); };
    script.onerror = () => reject(new Error(src));
    document.head.appendChild(script);
  });
}
function loadLibs() {
  if (window.PDFLib && window.fontkit) return Promise.resolve();
  if (!libsPromise) {
    libsPromise = loadScript("vendor/pdf-lib.min.js").then(() => loadScript("vendor/fontkit.umd.min.js"));
  }
  return libsPromise;
}

async function fetchBytes(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(url);
  return new Uint8Array(await res.arrayBuffer());
}

function sniff(bytes) {
  if (bytes.length > 3 && bytes[0] === 0xff && bytes[1] === 0xd8) return "jpg";
  if (bytes.length > 4 && bytes[0] === 0x89 && bytes[1] === 0x50 && bytes[2] === 0x4e && bytes[3] === 0x47) return "png";
  return null;
}

async function loadPhotos(data) {
  const photos = [];
  for (const photo of data.photos) {
    let found = null;
    for (const name of photoCandidates(photo)) {
      try {
        const res = await fetch(`photos/${name}`);
        if (!res.ok) continue;
        const bytes = new Uint8Array(await res.arrayBuffer());
        const format = sniff(bytes);
        if (!format) continue;
        found = { n: photo.n, bytes, format };
        break;
      } catch (err) {
        found = null;
      }
    }
    photos.push(found || { n: photo.n, bytes: null, format: null });
  }
  return photos;
}

function attachPhotos(data) {
  const figures = reportRoot.querySelectorAll("figure.photo");
  let pending = figures.length;
  let found = 0;
  const countEl = document.getElementById("photo-count");
  const finish = (ok) => {
    if (ok) found += 1;
    pending -= 1;
    if (pending === 0 && countEl) countEl.textContent = String(found);
  };
  figures.forEach((figure) => {
    const n = Number(figure.getAttribute("data-photo"));
    const photo = data.photos.find((item) => item.n === n);
    const img = figure.querySelector("img");
    const placeholder = figure.querySelector(".ph");
    const hint = figure.querySelector(".file-hint");
    const names = photoCandidates(photo);
    let index = 0;
    const tryNext = () => {
      if (index >= names.length) {
        img.hidden = true;
        placeholder.hidden = false;
        finish(false);
        return;
      }
      img.src = `photos/${names[index]}`;
      index += 1;
    };
    img.addEventListener("load", () => {
      img.hidden = false;
      placeholder.hidden = true;
      if (hint) hint.hidden = true;
      finish(true);
    });
    img.addEventListener("error", tryNext);
    tryNext();
  });
}

function setupSignature(canvas) {
  const ctx = canvas.getContext("2d");
  let drawing = false;
  let ratio = 1;

  function style() {
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
    ctx.lineWidth = 2.4;
    ctx.lineCap = "round";
    ctx.lineJoin = "round";
    ctx.strokeStyle = "#132639";
  }

  function size() {
    const next = Math.min(window.devicePixelRatio || 1, 2);
    const w = Math.max(1, canvas.clientWidth);
    const h = Math.max(1, canvas.clientHeight);
    const bw = Math.round(w * next);
    const bh = Math.round(h * next);
    if (canvas.width === bw && canvas.height === bh) return;
    const keep = hasInk() ? canvas.toDataURL("image/png") : null;
    ratio = next;
    canvas.width = bw;
    canvas.height = bh;
    style();
    if (keep) {
      const image = new Image();
      image.onload = () => ctx.drawImage(image, 0, 0, w, h);
      image.src = keep;
    }
  }

  function point(event) {
    const rect = canvas.getBoundingClientRect();
    return { x: event.clientX - rect.left, y: event.clientY - rect.top };
  }

  function hasInk() {
    if (!canvas.width || !canvas.height) return false;
    const pixels = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
    for (let i = 3; i < pixels.length; i += 4) if (pixels[i] > 8) return true;
    return false;
  }

  function clear() {
    ctx.save();
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.restore();
    style();
  }

  function exportPng() {
    const w = canvas.width;
    const h = canvas.height;
    const pixels = ctx.getImageData(0, 0, w, h);
    let minX = w;
    let minY = h;
    let maxX = 0;
    let maxY = 0;
    let ink = false;
    for (let y = 0; y < h; y += 1) {
      for (let x = 0; x < w; x += 1) {
        if (pixels.data[(y * w + x) * 4 + 3] <= 8) continue;
        ink = true;
        if (x < minX) minX = x;
        if (x > maxX) maxX = x;
        if (y < minY) minY = y;
        if (y > maxY) maxY = y;
      }
    }
    if (!ink) return null;
    const pad = Math.round(8 * ratio);
    minX = Math.max(0, minX - pad);
    minY = Math.max(0, minY - pad);
    maxX = Math.min(w - 1, maxX + pad);
    maxY = Math.min(h - 1, maxY + pad);
    const cw = maxX - minX + 1;
    const ch = maxY - minY + 1;
    const scale = Math.min(1, 800 / cw);
    const out = document.createElement("canvas");
    out.width = Math.max(1, Math.round(cw * scale));
    out.height = Math.max(1, Math.round(ch * scale));
    out.getContext("2d").drawImage(canvas, minX, minY, cw, ch, 0, 0, out.width, out.height);
    return out.toDataURL("image/png");
  }

  canvas.addEventListener("pointerdown", (event) => {
    if (canvas.dataset.locked === "1") return;
    event.preventDefault();
    canvas.setPointerCapture(event.pointerId);
    drawing = true;
    const p = point(event);
    ctx.beginPath();
    ctx.moveTo(p.x, p.y);
    ctx.lineTo(p.x + 0.2, p.y + 0.2);
    ctx.stroke();
  });
  canvas.addEventListener("pointermove", (event) => {
    if (!drawing) return;
    const p = point(event);
    ctx.lineTo(p.x, p.y);
    ctx.stroke();
  });
  const stop = () => { drawing = false; };
  canvas.addEventListener("pointerup", stop);
  canvas.addEventListener("pointercancel", stop);
  window.addEventListener("resize", size);
  requestAnimationFrame(size);
  return { clear, hasInk, exportPng, size };
}

function dataUrlToBytes(url) {
  const b64 = url.split(",")[1];
  const bin = atob(b64);
  const bytes = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i += 1) bytes[i] = bin.charCodeAt(i);
  return bytes;
}

function wire(data) {
  const blank = data.statements.blank;
  const form = document.getElementById("sign-form");
  const nameInput = document.getElementById("landlord-name");
  const addressInput = document.getElementById("landlord-address");
  const canvas = document.getElementById("sig");
  const pad = setupSignature(canvas);
  const downloadBtn = document.getElementById("download");
  const submitBtn = document.getElementById("submit-sign");

  const sync = () => {
    setMirror("mirror-landlord-name", nameInput.value.trim(), blank);
    setMirror("mirror-landlord-address", addressInput.value.trim(), blank);
  };
  nameInput.addEventListener("input", sync);
  addressInput.addEventListener("input", sync);

  document.getElementById("sig-clear").addEventListener("click", () => {
    if (canvas.dataset.locked === "1") return;
    pad.clear();
  });

  function missingPieces() {
    const missing = [];
    if (isBlank(nameInput.value)) missing.push("the landlord's legal name");
    if (isBlank(addressInput.value)) missing.push("the address for service");
    if (!pad.hasInk()) missing.push("a signature");
    return missing;
  }

  async function makePdf() {
    const missing = missingPieces();
    if (missing.length) {
      showStatus("error", `Add ${missing.join(", ")} before downloading the signed PDF.`);
      if (isBlank(nameInput.value)) nameInput.focus();
      else if (isBlank(addressInput.value)) addressInput.focus();
      else canvas.focus();
      return null;
    }
    showStatus("success", "Preparing the PDF…");
    await loadLibs();
    const [regular, bold, photos] = await Promise.all([
      fetchBytes("fonts/DejaVuSans.ttf"),
      fetchBytes("fonts/DejaVuSans-Bold.ttf"),
      loadPhotos(data),
    ]);
    const stamp = formatNowPacific(new Date());
    const png = pad.exportPng();
    const bytes = await buildConditionReportPdf(window.PDFLib, window.fontkit, data, {
      regular, bold, photos,
    }, {
      landlordName: nameInput.value.trim(),
      landlordAddress: addressInput.value.trim(),
      signaturePng: dataUrlToBytes(png),
      signedAtLabel: stamp.label,
    });
    return { bytes, stamp, png };
  }

  downloadBtn.addEventListener("click", async () => {
    downloadBtn.disabled = true;
    try {
      const made = await makePdf();
      if (!made) return;
      const blob = new Blob([made.bytes], { type: "application/pdf" });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = "condition-inspection-report-signed.pdf";
      document.body.appendChild(link);
      link.click();
      link.remove();
      setTimeout(() => URL.revokeObjectURL(url), 2000);
      showStatus("success", "The signed PDF downloaded. The landlord's name, address for service, signature, and the time are in that file.");
    } catch (err) {
      showStatus("error", "The PDF could not be prepared. Refresh the page and try again.");
    } finally {
      downloadBtn.disabled = false;
    }
  });

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    nameInput.setCustomValidity(isBlank(nameInput.value) ? "Enter the landlord's legal name." : "");
    addressInput.setCustomValidity(isBlank(addressInput.value) ? "Enter the address for service." : "");
    if (!form.reportValidity()) return;
    if (!pad.hasInk()) {
      showStatus("error", "Sign in the box before submitting.");
      canvas.focus();
      return;
    }
    const honey = new FormData(form).get("_honey");
    const stamp = formatNowPacific(new Date());
    const png = pad.exportPng();
    if (honey) {
      showSent(data, nameInput.value.trim(), stamp);
      return;
    }
    const url = endpoint();
    if (!url) {
      showStatus("error", "This form is not connected right now, so nothing was sent. Email devin@axfordrealestate.ca.");
      return;
    }
    const payload = {
      _subject: `Condition inspection signed: ${data.tenant.name}`,
      _template: "table",
      form: "Condition inspection report",
      page: window.location.href,
      landlord_name: nameInput.value.trim(),
      address_for_service: addressInput.value.trim(),
      signed_at: `${stamp.label} (${stamp.iso})`,
      record_id: data.record_id,
      tenant_name: data.tenant.name,
      confirm_review: "yes",
      signature: png,
    };
    submitBtn.disabled = true;
    const previous = submitBtn.textContent;
    submitBtn.textContent = "Sending…";
    showStatus("success", "Sending…");
    try {
      const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(payload),
      });
      const body = await res.json().catch(() => ({}));
      const ok = res.ok && String(body.success) !== "false";
      if (!ok) throw new Error("rejected");
      showSent(data, payload.landlord_name, stamp);
    } catch (err) {
      showStatus("error", "Sorry, something went wrong and the signature may not have been sent. Email devin@axfordrealestate.ca or call 778-355-0116.");
      submitBtn.disabled = false;
      submitBtn.textContent = previous;
    }
  });
}

function showSent(data, name, stamp) {
  const box = document.getElementById("confirmation");
  box.hidden = false;
  box.replaceChildren();
  const title = document.createElement("h2");
  title.textContent = "Sent";
  const p1 = document.createElement("p");
  p1.textContent = `Devin Desaulniers was emailed the signature, legal name, address for service, time, and record ID ${data.record_id}.`;
  const p2 = document.createElement("p");
  p2.textContent = `Signed by ${name} at ${stamp.label}. You can still download the signed PDF.`;
  box.append(title, p1, p2);
  const status = document.getElementById("form-status");
  status.className = "form-status";
  status.textContent = "";
  document.getElementById("submit-sign").disabled = true;
  document.getElementById("submit-sign").textContent = "Sent";
  document.getElementById("landlord-name").disabled = true;
  document.getElementById("landlord-address").disabled = true;
  document.getElementById("sig").dataset.locked = "1";
  document.getElementById("sig-clear").disabled = true;
  formCheckbox().disabled = true;
  box.focus();
}

function formCheckbox() {
  return document.querySelector('#sign-form input[name="confirm_review"]');
}

async function main() {
  let data;
  try {
    const res = await fetch("report.json");
    if (!res.ok) throw new Error(String(res.status));
    data = await res.json();
  } catch (err) {
    reportRoot.textContent = "The report did not load. Refresh the page. If it still fails, email devin@axfordrealestate.ca.";
    return;
  }
  document.title = `Condition inspection report — ${data.tenant.name}`;
  render(data);
  attachPhotos(data);
  wire(data);
}

main();
