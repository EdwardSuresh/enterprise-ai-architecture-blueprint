# Website

`index.html` is the public site, published to GitHub Pages by `.github/workflows/pages.yml` on every push to `main` that changes this folder. It is a single self-contained page; diagrams render with Mermaid from jsDelivr.

**First-time setup:** in the repository's Settings → Pages, set **Source** to **GitHub Actions**, otherwise the first deploy fails.

`social-preview.png` (1280×640) is the link-preview image used by LinkedIn and other sites (`og:image`) and by the repository's social preview. Its source is `docs/assets/social-preview-source.html`: open it in a browser at 1280×640 and take a screenshot to regenerate.
