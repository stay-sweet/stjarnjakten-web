# Stjärnjakten — Public information

The English/Swedish website for Stjärnjakten (Star Hunt), an iPhone and iPad app for families. Plain HTML, shared CSS and a small language selector; no build step or external dependencies.

## Pages and languages

| Page | English | Swedish |
| --- | --- | --- |
| Home | `/en/` | `/sv/` |
| Privacy policy | `/en/privacy/` | `/sv/privacy/` |
| Support | `/en/support/` | `/sv/support/` |

Each page contains one language, with localized navigation, title, description and alternate-language metadata. The native language dropdown opens the same page in the other language. Explicit language paths always take priority and work without JavaScript; no-JavaScript visitors get ordinary language links instead of the dropdown.

The existing `/`, `/privacy/` and `/support/` URLs are language entry points. `language.js` redirects to the matching page using a legacy `?lang=en`/`?lang=sv` or `#english`/`#svenska` value, then the saved browser preference, then the browser language (English fallback). Without JavaScript, these entry points display links to both languages. Only explicit dropdown choices are saved in local storage; no cookies or tracking are added. `styles.css` holds the shared responsive styling.

Edit the six localized HTML pages directly and update English and Swedish together. Keep support instructions aligned with the app and update the policy date when its content changes. Update the closed-beta availability text when the app launches. Do not add a framework or a build pipeline for these static pages.

The header, home-page card, favicon and Apple touch icon use `assets/app-icon.png`, copied unchanged from the Apple repository’s production `Apps/Shared/Resources/AppIcon.icon/Assets/AppIcon.png`. Update this copy when the production app artwork changes; do not use the development icon.

## Hosting

Use the existing GitHub Pages site for `stay-sweet/stjarnjakten-web`, publishing the repository root on `main`. `CNAME` preserves `starhunt.staysweet.dev`. Keep the domain-verification TXT record and the `starhunt` DNS CNAME pointing to `stay-sweet.github.io`.

Preview with `python3 -m http.server 8000` from this directory, then open `http://localhost:8000/`. Check home, privacy and support in both languages at desktop and mobile widths, the language dropdown, browser Back, navigation and email links. Check the existing entry URLs before publishing by pushing to the existing Pages source.

After publishing, App Store Connect can use the matching language-specific URLs:

| Field | English | Swedish |
| --- | --- | --- |
| Privacy Policy URL (including TestFlight) | `https://starhunt.staysweet.dev/en/privacy/` | `https://starhunt.staysweet.dev/sv/privacy/` |
| Support URL | `https://starhunt.staysweet.dev/en/support/` | `https://starhunt.staysweet.dev/sv/support/` |
| Marketing URL | `https://starhunt.staysweet.dev/en/` | `https://starhunt.staysweet.dev/sv/` |

Existing app and metadata links to `/privacy/` and `/support/` continue to work. No app binary change is required for this website update. App Store Connect metadata is managed separately; editing this repository does not change it.

## Contact

Stay Sweet

info@staysweet.dev
