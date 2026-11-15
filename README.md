# Stjärnjakten — Public information

The English/Swedish website for Stjärnjakten (Star Hunt), an iPhone, iPad and Android app for families (unreleased: closed beta, not yet in the App Store or on Google Play). Plain HTML, shared CSS and a small language selector; no build step or external dependencies.

## Pages and languages

| Page | English | Swedish |
| --- | --- | --- |
| Home | `/en/` | `/sv/` |
| Privacy policy | `/en/privacy/` | `/sv/privacy/` |
| Support | `/en/support/` | `/sv/support/` |
| Delete account and data | `/en/delete-account/` | `/sv/delete-account/` |
| Page not found | `/404.html` (both languages, served by GitHub Pages for unknown addresses) | |

Each page contains one language, with localized navigation, title, description and alternate-language metadata. The native language dropdown opens the same page in the other language. Explicit language paths always take priority and work without JavaScript; no-JavaScript visitors get ordinary language links instead of the dropdown.

The existing `/`, `/privacy/`, `/support/` and `/delete-account/` URLs are language entry points. `language.js` redirects to the matching page using a legacy `?lang=en`/`?lang=sv` or `#english`/`#svenska` value, then the saved browser preference, then the browser language (English fallback). Without JavaScript, these entry points display links to both languages. Only explicit dropdown choices are saved in local storage; no cookies or tracking are added. `styles.css` holds the shared responsive styling.

Every localized page has Open Graph and Twitter summary tags, and declares `color-scheme` as `light` in a meta tag and in `styles.css` (the app is light only). Edit the eight localized HTML pages directly and update English and Swedish together. Do not add a framework or a build pipeline for these static pages. Keep support instructions aligned with the app and update the policy date when its content changes. Update the closed-beta availability text when the app launches, and keep the privacy policy and deletion page aligned with what the backend stores and deletes (`stjarnjakten-backend` `convex/family`).

**Pending until the apps are public:** no store buttons or links exist yet. When the App Store listing exists, add `<meta name="apple-itunes-app" content="app-id=<App Store id>">` to `/en/` and `/sv/` (never with a placeholder id) and the App Store button; add the Google Play button when the listing exists. Android App Links (`/.well-known/assetlinks.json`) are not needed yet because the app opens no web links; add the file, with the app's signing certificate fingerprint, together with QR join by URL (deep-links standard).

The header, home-page card, favicon and Apple touch icon use `assets/app-icon.png`, copied unchanged from the Apple repository’s production `Apps/Shared/Resources/AppIcon.icon/Assets/AppIcon.png`. Update this copy when the production app artwork changes; do not use the development icon.

## Checks

Check one page while editing, then everything before committing:

```sh
python3 scripts/check.py sv/privacy # one page (substring of its path)
node --check language.js && git diff --check
python3 scripts/check.py            # full gate: all static checks
```

`scripts/check.py` verifies the required pages in both languages, working internal links, one `h1`, `lang`, `hreflang`, Open Graph/Twitter and light-only colour-scheme tags, Android coverage, no third-party requests, no Smart App Banner before an App Store ID exists, and that the policy still discloses family sharing, push, reminders and export. It uses only the Python standard library.

## Hosting

Use the existing GitHub Pages site for `stay-sweet/stjarnjakten-web`, publishing the repository root on `main`. `CNAME` preserves `starhunt.staysweet.dev`; `.nojekyll` keeps the site static and serves `.well-known` when it is added. Keep the domain-verification TXT record and the `starhunt` DNS CNAME pointing to `stay-sweet.github.io`.

Preview with `python3 -m http.server 8000` from this directory, then open `http://localhost:8000/`. Check home, privacy, support and delete-account in both languages at desktop and mobile widths, the language dropdown, browser Back, navigation and email links. Check the existing entry URLs before publishing by pushing to the existing Pages source.

After publishing, App Store Connect can use the matching language-specific URLs:

| Field | English | Swedish |
| --- | --- | --- |
| Privacy Policy URL (including TestFlight) | `https://starhunt.staysweet.dev/en/privacy/` | `https://starhunt.staysweet.dev/sv/privacy/` |
| Support URL | `https://starhunt.staysweet.dev/en/support/` | `https://starhunt.staysweet.dev/sv/support/` |
| Marketing URL | `https://starhunt.staysweet.dev/en/` | `https://starhunt.staysweet.dev/sv/` |
| Google Play data deletion URL | `https://starhunt.staysweet.dev/en/delete-account/` | `https://starhunt.staysweet.dev/sv/delete-account/` |

Existing app and metadata links to `/privacy/` and `/support/` continue to work. No app binary change is required for this website update. App Store Connect metadata is managed separately; editing this repository does not change it.

## Contact

Stay Sweet

info@staysweet.dev

## Project knowledge and work

North Production is the source of truth for current work, decisions and verification evidence: **Stjärnjakten (STJ)**, the StaySweet workspace (Project ID `ede96f47-e12c-4253-9a87-1448f6ad7993`). Read its Project context and [AGENTS.md](AGENTS.md) before starting. Keep repository usage and technical operations here; product requirements, decisions, plans, status and evidence belong in North.
