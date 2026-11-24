/** Shared inspection-report values for the PDF and the signing page. */

const MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

export function isBlank(value) {
  return value == null || String(value).trim() === "";
}

export function formatIsoDate(iso) {
  if (isBlank(iso)) return "";
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(iso).trim());
  if (!m) return String(iso);
  return `${Number(m[3])} ${MONTHS[Number(m[2]) - 1]} ${m[1]}`;
}

export function formatRecordedDateTime(value) {
  if (isBlank(value)) return "";
  const m = /^(\d{4})-(\d{2})-(\d{2})\s+(\d{1,2}):(\d{2})\s*(AM|PM)$/i.exec(String(value).trim());
  if (!m) return String(value);
  const ampm = m[6].toLowerCase() === "am" ? "a.m." : "p.m.";
  return `${Number(m[3])} ${MONTHS[Number(m[2]) - 1]} ${m[1]}, ${Number(m[4])}:${m[5]} ${ampm}`;
}

export function formatNowPacific(date = new Date()) {
  const parts = new Intl.DateTimeFormat("en-GB", {
    timeZone: "America/Vancouver",
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
    hour12: true,
  }).formatToParts(date);
  const get = (type) => parts.find((p) => p.type === type)?.value || "";
  const period = get("dayPeriod").toLowerCase().replace(/\./g, "").replace("am", "a.m.").replace("pm", "p.m.");
  const label = `${Number(get("day"))} ${get("month")} ${get("year")}, ${get("hour")}:${get("minute")} ${period} Pacific Time`;
  return { label, iso: date.toISOString() };
}

export function counts(data) {
  const conditions = { Good: 0, Fair: 0, Poor: 0, "Not applicable": 0 };
  let items = 0;
  let other = 0;
  for (const room of data.rooms) {
    for (const item of room.items) {
      items += 1;
      if (conditions[item.condition] != null) conditions[item.condition] += 1;
      else other += 1;
    }
  }
  return { rooms: data.rooms.length, items, conditions, other };
}

export function summaryAgrees(data, tally) {
  const s = data.summary_as_recorded;
  return s.rooms_inspected === tally.rooms
    && s.items_recorded === tally.items
    && s.good === tally.conditions.Good
    && s.fair === tally.conditions.Fair
    && s.poor === tally.conditions.Poor
    && s.not_applicable === tally.conditions["Not applicable"]
    && tally.other === 0;
}

export function partyModel(data, overrides = {}) {
  return {
    landlordName: overrides.landlordName != null ? overrides.landlordName : data.landlord.name,
    landlordAddress: overrides.landlordAddress != null ? overrides.landlordAddress : data.landlord.address_for_service,
    tenantName: data.tenant.name,
    street: data.property.street_address,
    unit: data.property.unit,
    city: data.property.city,
    postal: data.property.postal_code,
    possessionDate: data.tenancy.start_date,
    inspectionDate: formatIsoDate(data.inspection_date),
    inspectionStart: data.inspection_time_start,
    rent: data.tenancy.rent,
    securityDeposit: data.tenancy.security_deposit,
    petDeposit: data.tenancy.pet_deposit,
  };
}

export function conductedBy(data) {
  const r = data.representative;
  const b = data.brokerage;
  return `Inspection conducted for the landlord by ${r.name}, ${r.title}, ${b.name}, ${b.address}. Office phone ${b.phone}.`;
}

export function tableComment(item) {
  const parts = [];
  if (item.comment && String(item.comment).trim()) parts.push(String(item.comment).trim());
  if (item.photo) parts.push(`Photograph ${item.photo} was recorded with this item.`);
  return parts.join(" ");
}

export function maintenanceLists(data) {
  const withComment = [];
  const ratedWithoutComment = [];
  for (const room of data.rooms) {
    for (const item of room.items) {
      const row = {
        room: room.room,
        item: item.item,
        condition: item.condition,
        comment: item.comment ? String(item.comment).trim() : "",
        photo: item.photo || null,
      };
      if (row.comment) withComment.push(row);
      else if (row.condition === "Fair" || row.condition === "Poor") ratedWithoutComment.push(row);
    }
  }
  return { withComment, ratedWithoutComment };
}

export function maintenanceLine(row) {
  const parts = [`${row.room} — ${row.item} — ${row.condition}.`];
  parts.push(row.comment || "No comment was recorded.");
  if (row.photo) parts.push(`Photograph ${row.photo} was recorded with this item.`);
  return parts.join(" ");
}

export function legalParagraph(data) {
  return `${data.statements.legal_note} Lines marked "${data.statements.blank}" were not in the inspection record and are to be filled in before that copy is given to the tenant.`;
}

export function photoCandidates(photo) {
  const stem = String(photo.file).replace(/\.[^.]+$/, "");
  return ["jpg", "jpeg", "png"].map((ext) => `${stem}.${ext}`);
}

export function conditionClass(condition) {
  if (condition === "Good") return "cond-good";
  if (condition === "Fair") return "cond-fair";
  if (condition === "Poor") return "cond-poor";
  return "cond-na";
}

export function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (ch) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  }[ch]));
}

export function displayValue(value, blankLabel) {
  if (isBlank(value)) return { blank: true, text: blankLabel };
  return { blank: false, text: String(value) };
}
