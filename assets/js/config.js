/*
 * ===================== FORM CONFIGURATION (one spot) =====================
 * GitHub Pages cannot process form submissions by itself.
 * Until an endpoint is set below, forms will NOT send anything — visitors
 * see a "forms not yet connected" placeholder message instead.
 *
 * To go live, paste the endpoint URL(s) from your chosen service, e.g.:
 *   Formspree:   "https://formspree.io/f/abcdwxyz"
 *   FormSubmit:  "https://formsubmit.co/your-random-alias"
 *   Getform/Basin etc. work the same way.
 * You can use one endpoint for both forms, or one per form.
 * ========================================================================
 */
window.SITE_CONFIG = {
  forms: {
    buyerListings: "",   // "Send me listings" form on buyers.html
    tenantIntake: ""     // Relocation rental intake form on tenants.html
  }
};
