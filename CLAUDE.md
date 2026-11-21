# Life list of Roshni — how to update this site

This repo is Roshni's bird life-list website, served by GitHub Pages from `main` at
https://roshnisubudhi6.github.io/life-list-of-roshni/. Roshni logs birds in Notion; this repo is
updated from Notion by a scheduled sync. Photos live only in Notion and in `photos/` here. Never
upload them to Claude storage.

## Files
- `index.html` — the whole site. Bird data sits in `<script id="data" type="application/json">`.
  Read and write it only with `tools/birds.py` (`dump` / `load`); don't hand-edit the JSON.
- `photos/` — site photos, JPEG, longest side 1400px, quality ~78, named `<bird-id>-<n>.jpg`.
- `sync/notion_map.json` — Notion page id → bird id, plus the Notion file names already imported
  per page. Pages marked `"skipped"` are not birds; leave them out.
- Google Analytics (ID `G-THEQJ9VJYJ`): the gtag tags in `<head>` and the
  `<script id="analytics">` click tracking before `</body>`. Keep both as they are.

## Notion source
- Data source: `collection://214f1a93-912c-80a2-aae6-000b48b907df` (database inside the
  "🦜 Birding" page `214f1a93912c80f3b31ed87b37ad78d9`). Each row is one bird; properties are
  `Name`, `Created`, `Place of the photo taken`; the page body holds Roshni's notes and photos.
- Notes often say "Spotted on 27 June 2026 in Dandeli" — each such line is a sighting.
- Get photos with the Notion tools (fetch the page with `include_file_urls`, or
  `get_file_download_urls`), download right away (signed URLs expire), resize, save to `photos/`.

## Bird record
```json
{"id":"indian-roller","name":"Indian Roller","sci":"Coracias benghalensis",
 "art":{"t":"roller","c":{"b":"#7E7A5A","u":"#A88A86","h":"#6E9AB8","w":"#4FA8C0","k":"#1E1E1E","t":"#3E80B0"},"x":{"band":"#264F9A"}},
 "desc":"One or two sentences: what the bird is and one memorable trait.",
 "notes":"Roshni's own notes from Notion, tidied, without the sighting-date lines.",
 "sightings":[{"date":"2025-12-28","place":"Anandam World City"}],
 "photos":[{"id":"photos/indian-roller-1.jpg"}]}
```
- `id`: lowercase name with hyphens, unique. `name`: proper common name (fix spelling).
- `sightings`: `date` is `YYYY-MM-DD`, `YYYY` when Roshni only knows the year (e.g. "late 2025"), or `""`. Add `"country"` only for a country other than
  India, New Zealand or Singapore (those are inferred from the place). If no date is in the notes,
  use the Notion `Created` date. Keep sightings unique (same date + place = duplicate).
- `art.t` shape (pick the closest): perch, sunbird, swallow, beeeater, kingfisher, roller, barbet,
  woodpecker, cuckoo, parrot, pigeon, hornbill, owl, raptor, wader, nightheron, stork, ibis, shore,
  duck, goose, swan, rail, grebe, cormorant, pelican, gull, albatross, quail, kiwi.
- `art.c` colours: b back, u underparts, h head, w wing, k bill, l legs, t tail (hex, muted, true to
  the species).
- `art.x` optional extras: mask, brow, cap, cheek, throat, face, crest (+crestC), patch, band, vent,
  rump, spots, bars, scales, streak, stripe, tailTip, eye (iris), ring (eye ring), hook, fork, fan,
  streamers, casque, shield, tipC, wattle, collar, nape, sheen; size/pose: bl, bh, tail, ta, leg,
  bill, bt, tilt, perch (branch, wire, trunk, ground, rock, grass, flower, shallow, water, lily).
  Look at similar birds already in the data and copy their style.

## Sync steps
1. Query the Notion data source for all rows. Compare against `sync/notion_map.json`.
2. New row (page id not in the map) that is a bird → add a bird record (description, art, notes,
   sightings, photos) and add it to the map. Not a bird → add with `"skipped"`.
3. Known row → add any new sighting dates/places from its notes and any photos whose Notion file
   name isn't in `photos_imported`. Update notes if Roshni added text. Never remove existing data,
   and never overwrite fields that differ only because they were tidied.
   Placeholder dates: when a bird's notes had no date, its sighting was set to the Notion
   `Created` date. If the notes now contain real dates and none of them is that `Created` date,
   replace the placeholder sighting with the dates from the notes — don't keep it as an extra.
4. If a Notion row was deleted, leave the bird on the site and mention it in the summary.
5. Only change bird data, `photos/` and `sync/notion_map.json`. Don't change the page's design,
   code, icons or other files unless Roshni asks in the run's instructions.
6. Check: `python3 tools/birds.py dump` parses, every photo path exists, open `index.html` in a
   headless browser and confirm no script errors.
7. Commit with a message listing what changed (e.g. "Add Indian Pitta; 2 sightings, 3 photos")
   and push to `main`. If nothing changed, don't commit.
