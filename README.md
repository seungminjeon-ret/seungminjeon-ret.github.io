# Seungmin Jeon

Research homepage: https://seungminjeon-ret.github.io/

This repository contains the public static website only. GitHub Actions deploys
the four allowlisted files in `site/` to GitHub Pages from `main`.

- `site/index.html`: biography, publications, education, and profile links
- `site/assets/style.css`: responsive layout and typography
- `site/assets/favicon.svg`: site icon
- `site/assets/social.png`: sharing image

Edit the HTML and CSS to update the site. Run `python3 scripts/check_site.py`
before committing, and check the result at mobile and desktop widths.

No JavaScript, runtime dependencies, server, analytics, or external API is needed.
