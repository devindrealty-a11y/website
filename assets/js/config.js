/*
 * ===================== FORM CONFIGURATION (one spot) =====================
 * The contact forms post via AJAX to FormSubmit (https://formsubmit.co), which emails
 * each submission to the address in the URL. No account needed.
 *
 * IMPORTANT: the very first real submission triggers a one-time activation
 * email from FormSubmit to devin@axfordrealestate.ca. Devin must click
 * "Activate Form" in that email; submissions are only delivered after that.
 * After activation, FormSubmit provides a random alias string — you can swap
 * the email in these URLs for that alias to hide the address from spam bots,
 * e.g. "https://formsubmit.co/ajax/abc123randomalias".
 *
 * Set a value to "" to disconnect a form (it will then show a notice instead).
 *
 * Chat switch (one line):
 *   chat: "lead"     free step-by-step chat box (default). This replaces Elfsight.
 *   chat: "elfsight" Elfsight AI chatbot (app id below). The free chat box stays off.
 *
 * The chat box emails a copy through leadChat (FormSubmit). That address has not
 * been test-submitted. It also adds the lead through the Supabase function named
 * below. The anon key is the public Desk key. Visitors can only add a lead.
 * ========================================================================
 */
window.SITE_CONFIG = {
  forms: {
    buyerListings: "https://formsubmit.co/ajax/devin@axfordrealestate.ca", // buyers.html "Send me listings"
    tenantIntake:  "https://formsubmit.co/ajax/devin@axfordrealestate.ca", // tenants.html relocation intake
    listingInquiry: "https://formsubmit.co/ajax/devin@axfordrealestate.ca", // listings.html detail inquiry (not test-submitted)
    rentalInquiry: "https://formsubmit.co/ajax/devin@axfordrealestate.ca", // rentals.html detail inquiry (not test-submitted)
    homeEvaluation: "https://formsubmit.co/ajax/devin@axfordrealestate.ca", // home-evaluation.html (not test-submitted)
    buyerOpinion: "https://formsubmit.co/ajax/devin@axfordrealestate.ca", // buyer-opinion.html (not test-submitted)
    leadChat: "https://formsubmit.co/ajax/devin@axfordrealestate.ca" // chat box backup email (not test-submitted)
  },
  chat: "lead",
  elfsightAppId: "a317cda7-7d35-4984-bea6-2d5efb757691",
  supabase: {
    url: "https://gwmfrxnoxoknzfuzktqi.supabase.co",
    anonKey: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd3bWZyeG5veG9rbnpmdXprdHFpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTE0NzQ2MzMsImV4cCI6MjEwNzA1MDYzM30.7w5rC_2y0DEap7MtmCVwsGxlQPMRgrMjWRbj1jR3DZw",
    leadFunction: "submit_website_chat_lead"
  }
};
