/**
 * Letter-size condition inspection report.
 * Verdana is not licensed for embedding. DejaVu Sans is the embedded fallback.
 * The same function builds the file Devin prints and the PDF the landlord downloads.
 */
import {
  isBlank,
  formatIsoDate,
  formatRecordedDateTime,
  partyModel,
  conductedBy,
  tableComment,
  maintenanceLists,
  maintenanceLine,
  legalParagraph,
  counts,
  summaryAgrees,
} from "./report-model.js";

const PAGE_W = 612;
const PAGE_H = 792;
const ML = 50;
const MR = 50;
const CW = PAGE_W - ML - MR;
const CONTENT_TOP = 706;
const CONTENT_BOTTOM = 56;
const ITEM_W = 166;
const COND_W = 98;
const COMM_W = CW - ITEM_W - COND_W;

function wrap(text, font, size, maxWidth) {
  const clean = String(text == null ? "" : text).replace(/\s+/g, " ").trim();
  if (!clean) return [];
  const words = clean.split(" ");
  const lines = [];
  let line = "";
  const pushLong = (word) => {
    if (font.widthOfTextAtSize(word, size) <= maxWidth) return [word];
    const parts = [];
    let cur = "";
    for (const ch of word) {
      const trial = cur + ch;
      if (font.widthOfTextAtSize(trial, size) <= maxWidth) cur = trial;
      else {
        if (cur) parts.push(cur);
        cur = ch;
      }
    }
    if (cur) parts.push(cur);
    return parts;
  };
  for (const word of words) {
    for (const part of pushLong(word)) {
      const trial = line ? `${line} ${part}` : part;
      if (font.widthOfTextAtSize(trial, size) <= maxWidth) line = trial;
      else {
        if (line) lines.push(line);
        line = part;
      }
    }
  }
  if (line) lines.push(line);
  return lines;
}

function wrapBlock(text, font, size, maxWidth) {
  const paras = String(text == null ? "" : text).replace(/\r\n/g, "\n").split("\n");
  const lines = [];
  for (const para of paras) {
    const wrapped = wrap(para, font, size, maxWidth);
    lines.push(...(wrapped.length ? wrapped : [""]));
  }
  return lines;
}

export async function buildConditionReportPdf(pdfLib, fontkit, data, assets, options = {}) {
  const { PDFDocument, rgb } = pdfLib;
  const NAVY = rgb(0.09, 0.227, 0.369);
  const INK = rgb(0.075, 0.149, 0.224);
  const MUTED = rgb(0.29, 0.33, 0.36);
  const LINE = rgb(0.62, 0.68, 0.74);
  const HEAD_BG = rgb(0.9, 0.929, 0.953);
  const WHITE = rgb(1, 1, 1);
  const PLACE = rgb(0.945, 0.953, 0.961);
  const GOOD = rgb(0.08, 0.322, 0.176);
  const FAIR = rgb(0.42, 0.28, 0.02);
  const POOR = rgb(0.55, 0.11, 0.11);

  const doc = await PDFDocument.create();
  doc.registerFontkit(fontkit);
  const regular = await doc.embedFont(assets.regular, { subset: true });
  const bold = await doc.embedFont(assets.bold, { subset: true });
  const fonts = { regular, bold };

  const colorFor = (condition) => {
    if (condition === "Good") return GOOD;
    if (condition === "Fair") return FAIR;
    if (condition === "Poor") return POOR;
    return MUTED;
  };

  let page = null;
  let y = CONTENT_TOP;

  const drawHeader = (pg) => {
    pg.drawText(data.brokerage.name.toUpperCase(), {
      x: ML, y: 748, size: 10, font: bold, color: NAVY,
    });
    const phone = data.brokerage.phone;
    const phoneW = bold.widthOfTextAtSize(phone, 10);
    pg.drawText(phone, { x: PAGE_W - MR - phoneW, y: 748, size: 10, font: bold, color: NAVY });
    pg.drawText(data.brokerage.address, { x: ML, y: 734, size: 8.5, font: regular, color: INK });
    pg.drawLine({
      start: { x: ML, y: 724 }, end: { x: PAGE_W - MR, y: 724 }, thickness: 1.75, color: NAVY,
    });
  };

  const newPage = () => {
    page = doc.addPage([PAGE_W, PAGE_H]);
    drawHeader(page);
    y = CONTENT_TOP;
  };

  const ensure = (h) => {
    if (y - h >= CONTENT_BOTTOM) return;
    if (h >= CONTENT_TOP - CONTENT_BOTTOM) return;
    newPage();
  };

  const gap = (n) => { y -= n; };

  const drawWrapped = (text, font, size, color, leading) => {
    const lead = leading || size + 3;
    const lines = wrapBlock(text, font, size, CW);
    const h = lines.length * lead;
    ensure(h);
    lines.forEach((line, i) => {
      if (!line) return;
      page.drawText(line, { x: ML, y: y - size - i * lead, size, font, color });
    });
    y -= h;
  };

  const heading = (text) => {
    ensure(46);
    y -= 11;
    page.drawText(text, { x: ML, y: y - 11, size: 11, font: bold, color: NAVY });
    y -= 16;
    page.drawLine({ start: { x: ML, y }, end: { x: ML + CW, y }, thickness: 1, color: NAVY });
    y -= 8;
  };

  const drawBlankLines = (count) => {
    const hint = data.statements.blank;
    const hintW = regular.widthOfTextAtSize(hint, 8.5);
    for (let i = 0; i < count; i += 1) {
      ensure(16);
      let xLine = ML;
      if (i === 0) {
        page.drawText(hint, { x: ML, y: y - 10, size: 8.5, font: regular, color: MUTED });
        xLine = ML + hintW + 8;
      }
      page.drawLine({
        start: { x: xLine, y: y - 12 },
        end: { x: ML + CW, y: y - 12 },
        thickness: 0.75,
        color: NAVY,
      });
      y -= 16;
    }
  };

  const drawField = (label, value, blankCount = 1) => {
    const labelLines = wrap(label, bold, 9, CW);
    const filled = !isBlank(value);
    const valueLines = filled ? wrapBlock(String(value).trim(), regular, 10, CW) : [];
    const labelH = labelLines.length * 12;
    const valueH = filled ? valueLines.length * 13 : blankCount * 16;
    ensure(labelH + valueH + 4);
    labelLines.forEach((line, i) => {
      page.drawText(line, { x: ML, y: y - 9 - i * 12, size: 9, font: bold, color: INK });
    });
    y -= labelH;
    if (!filled) {
      drawBlankLines(blankCount);
    } else {
      valueLines.forEach((line, i) => {
        if (!line) return;
        page.drawText(line, { x: ML, y: y - 11 - i * 13, size: 10, font: regular, color: INK });
      });
      y -= valueLines.length * 13;
    }
    y -= 3;
  };

  const drawColHeader = () => {
    const h = 16;
    ensure(h);
    page.drawRectangle({ x: ML, y: y - h, width: CW, height: h, color: HEAD_BG });
    const baseline = y - 11.5;
    page.drawText("Item", { x: ML + 4, y: baseline, size: 8.5, font: bold, color: INK });
    page.drawText("Condition", { x: ML + ITEM_W + 4, y: baseline, size: 8.5, font: bold, color: INK });
    page.drawText("Comments", { x: ML + ITEM_W + COND_W + 4, y: baseline, size: 8.5, font: bold, color: INK });
    page.drawLine({ start: { x: ML, y: y - h }, end: { x: ML + CW, y: y - h }, thickness: 0.6, color: NAVY });
    y -= h;
  };

  const drawRoomHeader = (name) => {
    const h = 18;
    ensure(h);
    page.drawRectangle({ x: ML, y: y - h, width: CW, height: h, color: NAVY });
    page.drawText(name, { x: ML + 6, y: y - 12.5, size: 9, font: bold, color: WHITE });
    y -= h;
  };

  const drawRow = (item, condition, comment) => {
    const leading = 11;
    const itemLines = wrap(item, regular, 8.5, ITEM_W - 8);
    const condLines = wrap(condition, bold, 8.5, COND_W - 8);
    const commentLines = comment ? wrap(comment, regular, 8.5, COMM_W - 8) : [];
    const n = Math.max(itemLines.length, condLines.length, commentLines.length, 1);
    const h = n * leading + 6;
    const top = y;
    const paint = (lines, x, font, color) => {
      lines.forEach((line, i) => {
        page.drawText(line, {
          x: x + 4,
          y: top - 4 - 8.5 - i * leading,
          size: 8.5,
          font,
          color,
        });
      });
    };
    paint(itemLines, ML, regular, INK);
    paint(condLines, ML + ITEM_W, bold, colorFor(condition));
    paint(commentLines, ML + ITEM_W + COND_W, regular, INK);
    page.drawLine({
      start: { x: ML + ITEM_W, y: top }, end: { x: ML + ITEM_W, y: top - h }, thickness: 0.35, color: LINE,
    });
    page.drawLine({
      start: { x: ML + ITEM_W + COND_W, y: top }, end: { x: ML + ITEM_W + COND_W, y: top - h }, thickness: 0.35, color: LINE,
    });
    y = top - h;
    page.drawLine({ start: { x: ML, y }, end: { x: ML + CW, y }, thickness: 0.4, color: LINE });
  };

  const rowHeight = (item) => {
    const comment = tableComment(item);
    const probeLines = Math.max(
      wrap(item.item, regular, 8.5, ITEM_W - 8).length,
      wrap(item.condition, bold, 8.5, COND_W - 8).length,
      comment ? wrap(comment, regular, 8.5, COMM_W - 8).length : 1,
    );
    return probeLines * 11 + 6;
  };

  const drawRooms = () => {
    data.rooms.forEach((room) => {
      let started = false;
      let continued = false;
      room.items.forEach((item, index) => {
        const rowH = rowHeight(item);
        let need = rowH + (started ? 0 : 34);
        if (!started && room.items[index + 1]) need += rowHeight(room.items[index + 1]);
        if (y - need < CONTENT_BOTTOM) {
          newPage();
          continued = started;
          started = false;
        }
        if (!started) {
          drawRoomHeader(continued ? `${room.room} (continued)` : room.room);
          drawColHeader();
          started = true;
          continued = true;
        }
        drawRow(item.item, item.condition, tableComment(item));
      });
      gap(8);
    });
  };

  const drawNumbered = (rows) => {
    rows.forEach((row, index) => {
      const text = maintenanceLine(row);
      const lines = wrap(text, regular, 9, CW - 22);
      const h = lines.length * 12;
      ensure(h + 2);
      page.drawText(`${index + 1}.`, { x: ML, y: y - 9, size: 9, font: bold, color: INK });
      lines.forEach((line, i) => {
        page.drawText(line, { x: ML + 20, y: y - 9 - i * 12, size: 9, font: regular, color: INK });
      });
      y -= h + 3;
    });
  };

  const drawSummaryRow = (label, value) => {
    ensure(16);
    page.drawText(label, { x: ML, y: y - 10, size: 9, font: regular, color: INK });
    const s = String(value);
    const w = bold.widthOfTextAtSize(s, 9);
    page.drawText(s, { x: ML + CW - w, y: y - 10, size: 9, font: bold, color: INK });
    y -= 13;
    page.drawLine({ start: { x: ML, y }, end: { x: ML + CW, y }, thickness: 0.35, color: LINE });
    y -= 3;
  };

  const drawInfoCard = (title, rows) => {
    const innerW = CW - 16;
    const prepared = rows.map((row) => {
      const lead = row.size + 3;
      return { ...row, lines: wrapBlock(row.text, row.font, row.size, innerW), lead };
    });
    let inner = 12 + 16;
    for (const row of prepared) inner += Math.max(row.lines.length, 1) * row.lead;
    inner += 6;
    ensure(inner);
    const top = y;
    page.drawRectangle({
      x: ML, y: top - inner, width: CW, height: inner, borderColor: NAVY, borderWidth: 0.9,
    });
    page.drawText(title, { x: ML + 8, y: top - 18, size: 9.5, font: bold, color: NAVY });
    let cursor = top - 22;
    for (const row of prepared) {
      row.lines.forEach((line, i) => {
        if (!line) return;
        page.drawText(line, {
          x: ML + 8,
          y: cursor - row.size - i * row.lead,
          size: row.size,
          font: row.font,
          color: row.color || INK,
        });
      });
      cursor -= Math.max(row.lines.length, 1) * row.lead;
    }
    y = top - inner - 8;
  };

  const party = partyModel(data, options);

  const drawLandlordCard = async () => {
    const name = isBlank(party.landlordName) ? "" : String(party.landlordName).trim();
    const when = options.signedAtLabel ? String(options.signedAtLabel).trim() : "";
    let image = null;
    let iw = 0;
    let ih = 0;
    if (options.signaturePng && options.signaturePng.length) {
      image = await doc.embedPng(options.signaturePng);
      const sc = Math.min((CW - 16) / image.width, 58 / image.height);
      iw = image.width * sc;
      ih = image.height * sc;
    }
    const signed = Boolean(image && name && when);
    const innerW = CW - 16;
    const nameLines = signed ? wrap(`Legal name: ${name}`, regular, 9.5, innerW) : [];
    const whenLines = signed ? wrap(`Signed ${when}`, regular, 9, innerW) : [];
    let inner = 12 + 16;
    if (signed) {
      inner += nameLines.length * 13 + 6 + ih + 6 + whenLines.length * 12;
    } else {
      inner += 3 * 32;
    }
    inner += 8;
    ensure(inner);
    const top = y;
    page.drawRectangle({
      x: ML, y: top - inner, width: CW, height: inner, borderColor: NAVY, borderWidth: 0.9,
    });
    page.drawText("LANDLORD", { x: ML + 8, y: top - 18, size: 9.5, font: bold, color: NAVY });
    let cursor = top - 28;
    if (signed) {
      nameLines.forEach((line, i) => {
        page.drawText(line, { x: ML + 8, y: cursor - i * 13, size: 9.5, font: regular, color: INK });
      });
      cursor -= nameLines.length * 13 + 4;
      page.drawImage(image, { x: ML + 8, y: cursor - ih, width: iw, height: ih });
      cursor -= ih + 8;
      whenLines.forEach((line, i) => {
        page.drawText(line, { x: ML + 8, y: cursor - i * 12, size: 9, font: regular, color: INK });
      });
    } else {
      const hint = data.statements.blank;
      const hintW = regular.widthOfTextAtSize(hint, 8.5);
      ["Legal name", "Signature", "Date"].forEach((label) => {
        page.drawText(label, { x: ML + 8, y: cursor, size: 9, font: bold, color: INK });
        cursor -= 12;
        page.drawText(hint, { x: ML + 8, y: cursor, size: 8.5, font: regular, color: MUTED });
        page.drawLine({
          start: { x: ML + 8 + hintW + 8, y: cursor - 1 },
          end: { x: ML + CW - 8, y: cursor - 1 },
          thickness: 0.75,
          color: NAVY,
        });
        cursor -= 18;
      });
    }
    y = top - inner - 8;
  };

  const embeddedPhotos = [];
  for (const photo of data.photos) {
    const found = (assets.photos || []).find((p) => p.n === photo.n && p.bytes && p.bytes.length);
    let image = null;
    if (found) {
      image = found.format === "png" ? await doc.embedPng(found.bytes) : await doc.embedJpg(found.bytes);
    }
    embeddedPhotos.push({ ...photo, image });
  }

  newPage();

  page.drawText("CONDITION INSPECTION REPORT", {
    x: ML, y: y - 16, size: 15, font: bold, color: NAVY,
  });
  y -= 24;
  drawWrapped("Move-in inspection at the start of the tenancy", regular, 10.5, INK, 13);
  gap(1);
  drawWrapped(formatIsoDate(data.inspection_date), regular, 10.5, INK, 13);
  gap(1);
  drawWrapped(`Inspection record ${data.record_id}`, regular, 8.5, INK, 11);
  gap(8);
  drawWrapped(data.statements.prepared_by, regular, 9, INK, 12);
  gap(4);
  drawWrapped(data.statements.form_note, regular, 8.5, INK, 11.5);
  gap(3);
  drawWrapped(data.statements.move_in_only, regular, 8.5, INK, 11.5);
  gap(3);
  drawWrapped(data.statements.missing_fields, regular, 8.5, INK, 11.5);

  heading("PARTIES AND RENTAL UNIT");
  drawField("A. Landlord's legal name", party.landlordName, 1);
  drawField("B. Landlord's address for service", party.landlordAddress, isBlank(party.landlordAddress) ? 2 : 1);
  drawField("C. Tenant's legal name", party.tenantName, 1);
  drawField("D. Rental unit street address", party.street, 1);
  drawField("Unit", party.unit, 1);
  drawField("City", party.city, 1);
  drawField("Postal code", party.postal, 1);
  drawField("E. Date the tenant is entitled to possession", party.possessionDate, 1);
  drawField("F. Move-in inspection date", party.inspectionDate, 1);
  drawField("Inspection start time", party.inspectionStart, 1);
  ensure(16);
  page.drawText("Tenancy amounts — not recorded in the inspection", {
    x: ML, y: y - 9, size: 8.5, font: bold, color: INK,
  });
  y -= 14;
  drawField("Monthly rent", party.rent, 1);
  drawField("Security deposit", party.securityDeposit, 1);
  drawField("Pet damage deposit", party.petDeposit, 1);
  drawWrapped(conductedBy(data), regular, 9, INK, 12);

  heading("CONDITION LEGEND");
  {
    const labels = ["Good", "Fair", "Poor", "Not applicable"];
    const col = CW / 4;
    ensure(18);
    labels.forEach((name, i) => {
      const x = ML + i * col;
      page.drawRectangle({ x, y: y - 11, width: 8, height: 8, color: colorFor(name) });
      page.drawText(name, { x: x + 12, y: y - 10, size: 8.5, font: bold, color: INK });
    });
    y -= 16;
  }
  drawWrapped(data.statements.legend_note, regular, 8.5, INK, 11.5);

  heading("CONDITION OF THE RENTAL UNIT");
  drawWrapped(data.statements.rooms_note, regular, 8.5, INK, 11.5);
  gap(6);
  drawRooms();

  heading("DAMAGE AND ITEMS IN NEED OF MAINTENANCE OR REPAIR");
  drawWrapped(data.statements.maintenance_intro, regular, 8.5, INK, 11.5);
  gap(6);
  const lists = maintenanceLists(data);
  ensure(16);
  page.drawText("Items with a comment", { x: ML, y: y - 10, size: 9.5, font: bold, color: INK });
  y -= 16;
  drawNumbered(lists.withComment);
  if (lists.ratedWithoutComment.length) {
    gap(6);
    ensure(16);
    page.drawText("Rated Fair or Poor, with no comment recorded", {
      x: ML, y: y - 10, size: 9.5, font: bold, color: INK,
    });
    y -= 16;
    drawNumbered(lists.ratedWithoutComment);
  }

  heading("KEYS AND FOBS ISSUED TO THE TENANT");
  drawWrapped(data.keys.as_written, regular, 10, INK, 13);
  gap(4);
  drawSummaryRow("Unit keys", data.keys.unit_keys);
  drawSummaryRow("Fobs", data.keys.fobs);
  gap(4);
  drawWrapped(`Photograph ${data.keys.photo} was recorded with the keys.`, regular, 9, INK, 12);

  heading("PHOTOGRAPHS");
  drawWrapped("Four photographs are in the inspection record. A photograph appears below when its image file is in the photos folder.", regular, 8.5, INK, 11.5);
  gap(6);
  {
    const gapX = 12;
    const boxW = (CW - gapX) / 2;
    const boxH = 132;
    for (let i = 0; i < embeddedPhotos.length; i += 2) {
      const pair = [embeddedPhotos[i], embeddedPhotos[i + 1]].filter(Boolean);
      const captions = pair.map((photo) => wrap(photo.caption, regular, 8.5, boxW));
      const capLines = Math.max(...captions.map((lines) => lines.length), 1);
      const rowH = boxH + 6 + capLines * 11;
      ensure(rowH + 8);
      pair.forEach((photo, col) => {
        const x = ML + col * (boxW + gapX);
        const bottom = y - boxH;
        page.drawRectangle({
          x, y: bottom, width: boxW, height: boxH,
          color: photo.image ? WHITE : PLACE,
          borderColor: LINE,
          borderWidth: 0.8,
        });
        if (photo.image) {
          const sc = Math.min((boxW - 8) / photo.image.width, (boxH - 8) / photo.image.height);
          const dw = photo.image.width * sc;
          const dh = photo.image.height * sc;
          page.drawImage(photo.image, {
            x: x + (boxW - dw) / 2,
            y: bottom + (boxH - dh) / 2,
            width: dw,
            height: dh,
          });
        } else {
          const t1 = `Photograph ${photo.n}`;
          const t2 = "Not yet attached";
          const w1 = bold.widthOfTextAtSize(t1, 9);
          const w2 = regular.widthOfTextAtSize(t2, 8.5);
          page.drawText(t1, { x: x + (boxW - w1) / 2, y: bottom + boxH / 2 + 4, size: 9, font: bold, color: INK });
          page.drawText(t2, { x: x + (boxW - w2) / 2, y: bottom + boxH / 2 - 12, size: 8.5, font: regular, color: MUTED });
        }
        captions[col].forEach((line, li) => {
          page.drawText(line, {
            x, y: bottom - 14 - li * 11, size: 8.5, font: regular, color: INK,
          });
        });
      });
      y -= rowH + 10;
    }
  }

  heading("SUMMARY");
  const tally = counts(data);
  const attached = embeddedPhotos.filter((photo) => photo.image).length;
  drawSummaryRow("Rooms inspected", tally.rooms);
  drawSummaryRow("Items recorded", tally.items);
  drawSummaryRow("Good", tally.conditions.Good);
  drawSummaryRow("Fair", tally.conditions.Fair);
  drawSummaryRow("Poor", tally.conditions.Poor);
  drawSummaryRow("Not applicable", tally.conditions["Not applicable"]);
  drawSummaryRow("Photographs in the inspection record", data.summary_as_recorded.photos_in_record);
  drawSummaryRow("Photographs attached to this copy", attached);
  drawSummaryRow("Maintenance or repair items stated in the record", data.summary_as_recorded.maintenance_repair_count);
  drawSummaryRow("Tenant disagreements recorded", data.summary_as_recorded.tenant_disagreements);
  gap(6);
  const match = summaryAgrees(data, tally)
    ? "The room, item, and condition counts above are taken from the items in this report. They match the counts in the inspection record."
    : "The room, item, and condition counts above are taken from the items in this report. They do not match summary_as_recorded in the data file.";
  drawWrapped(match, regular, 8.5, INK, 11.5);

  heading("TENANT'S STATEMENT");
  drawWrapped(`I, ${data.tenant.name},`, regular, 10, INK, 13);
  gap(4);
  const drawCheck = (text) => {
    const lines = wrap(text, regular, 9.5, CW - 22);
    const h = Math.max(12, lines.length * 12);
    ensure(h + 2);
    page.drawRectangle({
      x: ML, y: y - 11, width: 9, height: 9, borderColor: NAVY, borderWidth: 0.9,
    });
    lines.forEach((line, i) => {
      page.drawText(line, { x: ML + 16, y: y - 10 - i * 12, size: 9.5, font: regular, color: INK });
    });
    y -= h + 3;
  };
  drawCheck("agree that this report fairly represents the condition of the rental unit.");
  drawCheck("do not agree that this report fairly represents the condition of the rental unit, for the following reasons:");
  gap(2);
  drawField("Reasons, if the tenant does not agree", null, 2);
  drawWrapped(data.statements.tenant_statement_note, regular, 8.5, INK, 11.5);

  ensure(220);
  heading("SIGNATURES");
  drawInfoCard("TENANT", [
    { text: data.signatures.tenant.name, font: bold, size: 10.5 },
    { text: "Tenant", font: regular, size: 9.5 },
    { text: "Signed electronically", font: regular, size: 9.5 },
    { text: formatRecordedDateTime(data.signatures.tenant.signed_at), font: regular, size: 9.5 },
    { text: "Recorded in the inspection (Rocket Inspection App).", font: regular, size: 8.5 },
    { text: data.statements.timezone_note, font: regular, size: 8.5 },
  ]);
  drawInfoCard("LANDLORD'S AUTHORIZED REPRESENTATIVE", [
    { text: data.representative.name, font: bold, size: 10.5 },
    { text: data.representative.role, font: regular, size: 9.5 },
    { text: `${data.representative.title}, ${data.brokerage.name}`, font: regular, size: 9.5 },
    { text: data.brokerage.email, font: regular, size: 9 },
    { text: "Signed electronically", font: regular, size: 9.5 },
    { text: formatRecordedDateTime(data.representative.signed_at), font: regular, size: 9.5 },
    { text: "Recorded in the inspection (Rocket Inspection App).", font: regular, size: 8.5 },
    { text: data.statements.representative_disclaimer, font: regular, size: 8.5 },
    { text: data.statements.timezone_note, font: regular, size: 8.5 },
  ]);
  await drawLandlordCard();

  heading("NOTE — RESIDENTIAL TENANCY ACT, S. 23, AND REGULATION, SS. 18 TO 20");
  drawWrapped(legalParagraph(data), regular, 8.5, INK, 11.5);

  const total = doc.getPageCount();
  doc.getPages().forEach((pg, index) => {
    pg.drawLine({
      start: { x: ML, y: 46 }, end: { x: PAGE_W - MR, y: 46 }, thickness: 0.6, color: NAVY,
    });
    const label = `Page ${index + 1} of ${total}`;
    const lw = regular.widthOfTextAtSize(label, 8.5);
    pg.drawText(label, { x: (PAGE_W - lw) / 2, y: 32, size: 8.5, font: regular, color: INK });
    pg.drawText(data.tenant.name, { x: ML, y: 32, size: 8.5, font: regular, color: INK });
    const right = "Move-in condition inspection";
    const rw = regular.widthOfTextAtSize(right, 8.5);
    pg.drawText(right, { x: PAGE_W - MR - rw, y: 32, size: 8.5, font: regular, color: INK });
  });

  doc.setTitle(`Condition Inspection Report — ${data.tenant.name}`);
  doc.setAuthor(data.brokerage.name);
  doc.setSubject("Move-in condition inspection at the start of the tenancy");
  doc.setCreator(`${data.brokerage.name} condition inspection report`);
  doc.setProducer(data.brokerage.name);
  return doc.save();
}
