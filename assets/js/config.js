/*
 * ===================== FORM CONFIGURATION (one spot) =====================
 * Both forms post via AJAX to FormSubmit (https://formsubmit.co), which emails
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
 * ========================================================================
 */
window.SITE_CONFIG = {
  forms: {
    buyerListings: "https://formsubmit.co/ajax/devin@axfordrealestate.ca", // buyers.html "Send me listings"
    tenantIntake:  "https://formsubmit.co/ajax/devin@axfordrealestate.ca", // tenants.html relocation intake
    listingInquiry: "https://formsubmit.co/ajax/devin@axfordrealestate.ca", // listings.html detail-page inquiry (not test-submitted)
    rentalInquiry: "https://formsubmit.co/ajax/devin@axfordrealestate.ca" // rentals.html detail-page inquiry (not test-submitted)
  }
};
