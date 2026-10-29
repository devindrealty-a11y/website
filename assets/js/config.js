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
    chatLead: "https://formsubmit.co/ajax/devin@axfordrealestate.ca", // chat widget message (not test-submitted)
    qualifiedLead: "https://formsubmit.co/ajax/devin@axfordrealestate.ca", // home + contact qualifying form (not test-submitted)
    // True-cost guide sign-up. Emails Devin only. Not test-submitted.
    // Subject is set in assets/js/true-cost.js: "True cost guide sign-up: <name>".
    trueCostSignup: "https://formsubmit.co/ajax/devin@axfordrealestate.ca",
    marketReport: "https://formsubmit.co/ajax/devin@axfordrealestate.ca", // market-report PDF gate (not test-submitted)
    // Mortgage rates page. Subject is "Mortgage intro request". Not test-submitted.
    // Devin introduces the client to a licensed mortgage professional. He does not underwrite.
    mortgageIntro: "https://formsubmit.co/ajax/devin@axfordrealestate.ca"
  }
};
