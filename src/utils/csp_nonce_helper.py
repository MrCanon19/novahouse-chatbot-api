"""
CSP Nonce Helper for Strict Content Security Policy
===================================================

When ENABLE_STRICT_CSP=true is enabled, the application generates a unique
nonce for each response and includes it in the CSP header.

To use in templates:
1. Access the nonce from response headers: X-Content-Security-Policy-Nonce
2. Add nonce attribute to all inline <script> tags:
   <script nonce="{{ csp_nonce }}">...</script>

Migration Plan:
--------------
Phase 1: Preparation (Dev/Staging)
- Set ENABLE_STRICT_CSP=false (default)
- Audit all templates for inline scripts
- Move inline scripts to external .js files where possible
- For unavoidable inline scripts, add nonce attribute placeholders

Phase 2: Template Updates
- Update Flask template rendering to pass nonce:
  @app.context_processor
  def inject_csp_nonce():
      return {'csp_nonce': g.get('csp_nonce', '')}

- Modify after_request to store nonce in g:
  if os.getenv("ENABLE_STRICT_CSP") == "true":
      nonce = secrets.token_urlsafe(16)
      g.csp_nonce = nonce
      response.headers["X-Content-Security-Policy-Nonce"] = nonce

- Update templates:
  <script nonce="{{ csp_nonce }}">
      // Your inline JavaScript
  </script>

Phase 3: Testing
- Enable ENABLE_STRICT_CSP=true in staging
- Test all pages for CSP violations in browser console
- Fix any remaining inline scripts or styles

Phase 4: Production Rollout
- Set ENABLE_STRICT_CSP=true in production environment
- Monitor error logs for CSP violations
- Have rollback plan ready (set ENABLE_STRICT_CSP=false)

Current Status:
--------------
✅ CSP nonce generation implemented in src/main.py
✅ Minimal CSP active by default (allows unsafe-inline for compatibility)
⚠️  Strict CSP disabled by default (requires template migration)
⏳ Template audit and nonce injection - PENDING

Estimated Effort: 4-8 hours for template migration + testing
Risk Level: Medium (can break UI if templates not properly updated)
Benefit: High (prevents XSS attacks via inline script injection)
"""


def get_csp_nonce_from_response(response):
    """Extract CSP nonce from response headers if available."""
    return response.headers.get("X-Content-Security-Policy-Nonce", "")


def add_nonce_to_script_tag(script_content, nonce):
    """Helper to add nonce attribute to script tag."""
    if "<script" in script_content and "nonce=" not in script_content:
        return script_content.replace("<script", f'<script nonce="{nonce}"', 1)
    return script_content
