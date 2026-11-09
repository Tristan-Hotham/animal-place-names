# animal-place-names: working notes

Brief: /home/claude/work/new9/BRIEFS.md (study 1) + shared rules in /home/claude/work/new8/BRIEFS.md and /home/claude/newdata/BRIEF.md.
Format refs: studies/church-orientation, studies/sunless-valleys (page engine: Inked World from ../ink-map/, like sunless-valleys).
Work files: /home/claude/scratch/animal-place-names (delete at the end).

## Pipeline
01_gazetteer.py (UK places + UK natural features + Irish places, county/nation from ONS counties, ground height from
raw_new8 terrain tiles) -> 02_match.py (elements.py rules, EXCLUDE false friends, overrides.csv hand review, repeats
within 3 km merged into one place) -> 03_analysis.py (results.json + data files) -> 04_export.py (page data) ->
05_figures.py -> 06_build_site.py -> 07_paper.py -> reddit/collage.py -> 09_readme.py -> 08_release.py -> qa.js

## Review (whole set, not a sample)
- Every one of the ~900 candidate rows was read by eye (WORK/review.txt, now data/candidates_review.csv).
- Rule changes after review: 'buck' and 'roe' removed (bucc can be a he-goat; Roedean is 'rough valley'); modern
  descriptive rules no longer apply to suburb/neighbourhood/quarter (modern estate names: Ravenhead, Badger Hill, Swanpool...);
  Foxley limited to England; Darley Abbey/Dale folded into Darley; Wolf's Castle county = Dyfed (preserved county).
- overrides.csv: 28 hand decisions (25 at build, 3 added in independent review) (Donnybrook = St Broc; Brackagh = breacach 'speckled'; Colmonell = St Colman Ela;
  Arbirlot = Elliot Water; inn signs Stags Head, Black Swan Hill, Boarshead...).
- madadh alone (dog/fox/wolf) kept apart as 'uncertain' (23 rows), never counted.

## References to verify (all cited from memory; reviewer please check title, venue, year)
- Mills, A. D. (2011) A Dictionary of British Place-Names, rev. edn. Oxford University Press. (first edn 2003)
- Watts, V. (ed.) (2004) The Cambridge Dictionary of English Place-Names. Cambridge University Press.
- Ekwall, E. (1960) The Concise Oxford Dictionary of English Place-Names, 4th edn. Oxford: Clarendon Press.
- Gelling, M. and Cole, A. (2000) The Landscape of Place-Names. Stamford: Shaun Tyas.
- Owen, H. W. and Morgan, R. (2007) Dictionary of the Place-Names of Wales. Llandysul: Gomer.
- Watson, W. J. (1926) The History of the Celtic Place-Names of Scotland. Edinburgh: Blackwood.
- Aybes, C. and Yalden, D. W. (1995) Place-name evidence for the former distribution and status of wolves and beavers in
  Britain. Mammal Review 25(4), 201 to 227.
- Boisseau, S. and Yalden, D. W. (1998) The former status of the Crane Grus grus in Britain. Ibis 140(3), 482 to 500.
- Yalden, D. (1999) The History of British Mammals. London: T. and A. D. Poyser.
- Coles, B. (2006) Beavers in Britain's Past. Oxford: Oxbow Books (WARP Occasional Paper 19).
- Pluskowski, A. (2006) Wolves and the Wilderness in the Middle Ages. Woodbridge: Boydell Press.
- Hickey, K. (2000) A geographical perspective on the decline and extermination of the Irish wolf Canis lupus: an initial
  assessment. Irish Geography 33(2), 185 to 198.
- Love, J. A. (1983) The Return of the Sea Eagle. Cambridge University Press.
- Vrandečić and Krötzsch not used. OpenStreetMap: ODbL; QLever (Bast and Buchhold 2017, CIKM) as in sibling studies.
- Individual etymologies in code/elements.py (NAMED list) are from memory of Mills/Watts/Ekwall and should be spot-checked;
  each is marked certain or probable. Loss dates: wolf England c. 1500, Scotland late 17th/18th c., Ireland 1786; beaver
  16th c.; crane as breeder c. 1600; boar 13th c. in the wild; white-tailed eagle 1918, reintroduced to Rum from 1975.

## Log
- 01, 02, 03 done. 800 candidates, 51 corrected (6.4%), 749 names kept, 673 places, 190 certain.
- 04 to 09, collage, header, QA done (0 console errors at 1280 and 390; QA screenshots as jpg). Scratch folder deleted
  (rerun 01 to regenerate the gazetteer, ~20 s). Paper PDF shows https://doi.org/10.5281/zenodo.24075293: publisher reruns
  `DOI=10.5281/zenodo.N python3 code/07_paper.py` then `python3 code/08_release.py`.
- Bast, H. and Buchhold, B. (2017) QLever, CIKM 2017, 647 to 656: also to verify.
- Page text claims Woolpit 'green children' legend (blog only) and reintroductions (cranes in the Broads and Levels, beavers):
  general knowledge, not cited; check wording.

## Independent review (2026)
- Rerun from raw reproduced every shipped number exactly; then fixed:
- Data: repeats merged with spaces ignored (Wolf Hope + Wolfhope Head/Bush 0.3 km apart, Crane Dale + Cranedale Spout, Hart Fell + Hartfell Spa, etc.);
  Otterswick (Orkney, Shetland) excluded (Norse vik with a personal or god name, Groome gives Odinswic); Otterburn Camp dropped
  (named after the village); St Raven's Edge dropped; farm 'Blaidd' set probable. Now 800 candidates, 30 false friends,
  26 dropped (7.0%), 744 names, 662 places, 189 certain. Wolf 33 (4 certain), 256 m vs 103 m, 0/20,000; crane 23, 91% England.
- New stricter height test (elev_test_other: against other animals' names of same kind and rule family): wolf p = 0.003.
  Fox no longer significant (p = 0.10); otter 36 m vs 73 m, p = 0.05 (15 places): texts softened.
- References checked online: Hickey issue number dropped (journal page ambiguous), Aybes issue dropped, Bast CIKM title fixed,
  Coles series added. Beaver loss softened (date debated); reintroduction lines softened (only Rum 1975 kept, cited Love 1983).
