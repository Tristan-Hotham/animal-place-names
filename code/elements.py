"""The curated, conservative list of animal elements in place names.

Three kinds of rule:
  NAMED   English (Old English or Old Norse) settlement names whose etymology the standard dictionaries give as containing the
          animal: matched on the whole name (with Great, Little, Upper, Lower, North, ... before it and a short list of
          manorial or saint's additions after it), only for settlements (not farms or houses), and where the county of the
          dictionary's place is known, only there. Certainty 'certain' where the dictionaries agree and the place is the one
          they discuss; 'probable' where the name recurs and I have not checked every instance.
  WORD    Welsh, Scottish Gaelic and Irish words for the animal, in the name or in name:cy / name:gd / name:ga, inside the
          language's area. These words have no common homonyms in place names once the false friends below are excluded, so
          the reading is 'certain' unless marked.
  MODERN  English or Scots animal words used descriptively (Wolf Crag, Raven Scar, Eagle's Nest, Tod Law), only with a
          landscape word, never on farms or houses. These are mostly later medieval or modern names and may honour a
          surname, an inn sign or a story rather than the animal: 'probable' at best.

Authorities (short keys, full references in the paper and NOTES.md):
  MILLS  Mills, A. D. (2011) A Dictionary of British Place-Names. Oxford University Press.
  WATTS  Watts, V. (2004) The Cambridge Dictionary of English Place-Names. Cambridge University Press.
  EKWALL Ekwall, E. (1960) The Concise Oxford Dictionary of English Place-Names, 4th edn. Clarendon Press.
  OWEN   Owen, H. W. and Morgan, R. (2007) Dictionary of the Place-Names of Wales. Gomer.
  WATSON Watson, W. J. (1926) The History of the Celtic Place-Names of Scotland. Blackwood.
  DICT   the ordinary dictionary sense of the Welsh, Gaelic or Irish word (Geiriadur Prifysgol Cymru; Dwelly's Gaelic
         dictionary; Ó Dónaill's Foclóir Gaeilge-Béarla), stated as a word meaning, not as a checked etymology of each place.
Every individual etymology below is from memory of these works and is listed in NOTES.md for the reviewer to check.
"""

# ---------- NAMED: whole settlement names from the dictionaries
# (head name, animal, layer, element, gloss, certainty, counties or None)
NAMED = [
    # wolf
    ("Woolpit", "wolf", "english", "OE wulf-pytt", "pit for trapping wolves", "certain", ["Suffolk"]),
    ("Woolley", "wolf", "english", "OE wulf + lēah", "wood or clearing frequented by wolves", "certain", ["West Yorkshire"]),
    ("Woolley", "wolf", "english", "OE wulf + lēah", "wood or clearing frequented by wolves (as the Yorkshire Woolley; not checked for this one)", "probable", None),
    ("Ulpha", "wolf", "norse", "ON ulfr + haugr", "hill frequented by wolves", "certain", ["Cumbria"]),
    ("Wolf's Castle", "wolf", "welsh", "Welsh Casblaidd, blaidd", "the wolf's castle (Welsh Casblaidd)", "probable", ["Dyfed"]),
    # beaver
    ("Beverley", "beaver", "english", "OE beofor + a stream name", "beaver stream or beaver lodge", "certain", ["East Riding of Yorkshire"]),
    ("Bevercotes", "beaver", "english", "OE beofor + cot", "beavers' lodges, shelters for beavers", "certain", ["Nottinghamshire"]),
    ("Beversbrook", "beaver", "english", "OE beofor + brōc", "beavers' brook", "probable", ["Wiltshire"]),
    # crane (the dictionaries often say 'cranes or herons')
    ("Cranfield", "crane", "english", "OE cran + feld", "open land frequented by cranes or herons", "certain", ["Bedfordshire"]),
    ("Cranbrook", "crane", "english", "OE cran + brōc", "brook frequented by cranes or herons", "certain", ["Kent"]),
    ("Cranborne", "crane", "english", "OE cran + burna", "stream frequented by cranes or herons", "certain", ["Dorset"]),
    ("Cranbourne", "crane", "english", "OE cran + burna", "stream frequented by cranes or herons", "probable", ["Berkshire"]),
    ("Cranford", "crane", "english", "OE cran + ford", "ford frequented by cranes or herons", "certain", ["Greater London", "Northamptonshire"]),
    ("Cranmore", "crane", "english", "OE cran + mere", "pool frequented by cranes or herons", "certain", ["Somerset"]),
    ("Cranwell", "crane", "english", "OE cran + wella", "spring or stream frequented by cranes or herons", "certain", ["Lincolnshire"]),
    ("Cranleigh", "crane", "english", "OE cran + lēah", "clearing frequented by cranes or herons", "certain", ["Surrey"]),
    ("Cransley", "crane", "english", "OE cran + lēah", "clearing frequented by cranes or herons", "probable", ["Northamptonshire"]),
    ("Tranmere", "crane", "norse", "ON trani + melr", "sandbank frequented by cranes", "certain", ["Merseyside"]),
    ("Cranshaws", "crane", "english", "OE cran + sceaga", "wood frequented by cranes or herons", "probable", ["Scottish Borders"]),
    # eagle
    ("Arncliffe", "eagle", "english", "OE earn + clif", "cliff frequented by eagles", "certain", ["North Yorkshire"]),
    ("Earnley", "eagle", "english", "OE earn + lēah", "wood or clearing frequented by eagles", "certain", ["West Sussex"]),
    ("Arnold", "eagle", "english", "OE earn + halh", "nook of land frequented by eagles", "certain", ["Nottinghamshire"]),
    ("Arnold", "eagle", "english", "OE earn + halh", "nook of land frequented by eagles", "probable", ["East Riding of Yorkshire"]),
    ("Yarnscombe", "eagle", "english", "OE earn + cumb", "valley of the eagles", "probable", ["Devon"]),
    ("Ernesettle", "eagle", "english", "OE earn + setl", "eagle's seat or eyrie", "probable", ["Devon"]),
    # wild boar
    ("Everley", "boar", "english", "OE eofor + lēah", "wood or clearing frequented by wild boar", "certain", ["Wiltshire", "North Yorkshire"]),
    ("Eversley", "boar", "english", "OE eofor + lēah", "wood or clearing of the wild boar", "certain", ["Hampshire"]),
    ("Evershot", "boar", "english", "OE eofor + scēat", "corner of land frequented by wild boar", "probable", ["Dorset"]),
    ("Eversholt", "boar", "english", "OE eofor + holt", "wood frequented by wild boar", "probable", ["Bedfordshire"]),
    ("Everdon", "boar", "english", "OE eofor + dūn", "hill frequented by wild boar", "probable", ["Northamptonshire"]),
    ("Wildboarclough", "boar", "english", "ME wilde bor + OE clōh", "ravine frequented by wild boar", "certain", ["Cheshire"]),
    # deer
    ("Hertford", "deer", "english", "OE heorot + ford", "ford frequented by harts", "certain", ["Hertfordshire"]),
    ("Hartlepool", "deer", "english", "OE heorot + ēg + pōl", "pool by the hart island (Heruteu)", "certain", ["Durham"]),
    ("Hartfield", "deer", "english", "OE heorot + feld", "open land frequented by harts", "certain", ["East Sussex"]),
    ("Hartley", "deer", "english", "OE heorot + lēah", "wood or clearing frequented by harts", "probable", None),
    ("Hartley Wintney", "deer", "english", "OE heorot + lēah", "wood or clearing frequented by harts", "certain", ["Hampshire"]),
    ("Hartford", "deer", "english", "OE heorot + ford", "ford frequented by harts", "probable", ["Cheshire", "Cambridgeshire", "Northumberland"]),
    ("Harthill", "deer", "english", "OE heorot + hyll", "hill frequented by harts", "probable", ["South Yorkshire", "Cheshire", "North Lanarkshire"]),
    ("Hartshead", "deer", "english", "OE heorot + hēafod", "the hart's headland or hill", "probable", ["West Yorkshire"]),
    ("Hartsop", "deer", "english", "OE heorot + hop", "valley of the hart", "certain", ["Cumbria"]),
    ("Hartshorne", "deer", "english", "OE heorot + horn", "hart's horn, a hill shaped like one", "probable", ["Derbyshire"]),
    ("Hartwell", "deer", "english", "OE heorot + wella", "spring frequented by harts", "probable", ["Buckinghamshire", "Northamptonshire"]),
    ("Hartburn", "deer", "english", "OE heorot + burna", "stream frequented by harts", "probable", ["Northumberland", "Durham"]),
    ("Hindhead", "deer", "english", "OE hind + hēafod", "hill frequented by hinds", "certain", ["Surrey"]),
    ("Hindley", "deer", "english", "OE hind + lēah", "wood or clearing frequented by hinds", "certain", ["Greater Manchester"]),
    ("Darley", "deer", "english", "OE dēor + lēah", "wood or clearing frequented by deer", "probable", ["Derbyshire", "North Yorkshire"]),
    ("Durley", "deer", "english", "OE dēor + lēah", "wood or clearing frequented by deer", "certain", ["Hampshire"]),
    ("Deerhurst", "deer", "english", "OE dēor + hyrst", "wooded hill frequented by deer", "certain", ["Gloucestershire"]),
    ("Dyrham", "deer", "english", "OE dēor + hamm", "enclosed valley or deer enclosure", "certain", ["Gloucestershire"]),
    ("Dearham", "deer", "english", "OE dēor + hām or hamm", "homestead or enclosure where deer are kept", "probable", ["Cumbria"]),
    # badger
    ("Brockhall", "badger", "english", "OE brocc + hol", "badger holes (setts)", "certain", ["Northamptonshire"]),
    ("Brockholes", "badger", "english", "OE brocc + hol", "badger holes (setts)", "certain", ["West Yorkshire", "Lancashire"]),
    # fox
    ("Foxley", "fox", "english", "OE fox + lēah", "wood or clearing frequented by foxes", "certain", "ENGLAND"),
    ("Foxholes", "fox", "english", "OE fox + hol", "fox holes, earths", "certain", ["North Yorkshire"]),
    ("Foxearth", "fox", "english", "OE fox + eorth", "fox's earth", "certain", ["Essex"]),
    ("Foxcote", "fox", "english", "OE fox + cot", "fox's earth or den", "probable", None),
    ("Foxhall", "fox", "english", "OE fox + hol", "fox hole", "probable", ["Suffolk"]),
    ("Foxton", "fox", "english", "OE fox + denu or tūn", "valley or farm frequented by foxes", "probable", ["Leicestershire", "Cambridgeshire", "Durham", "North Yorkshire"]),
    # wildcat
    ("Catford", "wildcat", "english", "OE catt + ford", "ford frequented by (wild) cats", "certain", ["Greater London"]),
    ("Catcleugh", "wildcat", "english", "OE catt + clōh", "ravine of the (wild) cats", "probable", ["Northumberland", "Scottish Borders"]),
    ("Catshill", "wildcat", "english", "OE catt + hyll", "hill frequented by (wild) cats", "probable", ["Worcestershire"]),
    # otter
    ("Otterburn", "otter", "english", "OE otor + burna", "otter stream", "certain", ["Northumberland", "North Yorkshire"]),
    ("Otterbourne", "otter", "english", "OE otor + burna", "otter stream", "certain", ["Hampshire"]),
    ("Ottery St Mary", "otter", "english", "OE otor + ēa (River Otter)", "on the River Otter, 'otter stream'", "certain", ["Devon"]),
    ("Otterton", "otter", "english", "OE otor + ēa + tūn (River Otter)", "farm on the River Otter, 'otter stream'", "certain", ["Devon"]),
    # salmon
    ("Leixlip", "salmon", "norse", "ON lax + hlaup", "salmon leap", "certain", None),
    # swan
    ("Swanmore", "swan", "english", "OE swan + mere", "pool frequented by swans", "probable", ["Hampshire"]),
    ("Swanbourne", "swan", "english", "OE swan + burna", "stream frequented by swans", "probable", ["Buckinghamshire"]),
    # kite
    ("Gledhow", "kite", "english", "OE gleoda + hōh", "hill spur frequented by kites", "probable", ["West Yorkshire"]),
]
# words allowed before and after a NAMED head name
PRE = r"(?:(?:great|little|upper|lower|nether|over|north|south|east|west|high|old|new|long|church|kings|king's|monks?)\s+)*"
POST = r"(?:\s+(?:st\.?|saint)\s+\w+|\s+(?:abbey|dale|wintney|mauditt|wespall|village|common|green|heath|moor|end))?"

# ---------- WORD: Welsh, Gaelic and Irish words (regex on accent-stripped lower case)
# (id, animal, layer, regex, nations, fields, gloss, certainty, authority)
B = r"(?<![a-z])"     # word start (letters only, so h-iolaire and a' mhadaidh work)
E = r"(?![a-z])"      # word end
WORD = [
    ("cy_blaidd", "wolf", "welsh", B + r"(blaidd|bleiddiaid|bleiddiau)" + E, ["Wales"], "n cy", "blaidd, wolf (plural bleiddiaid)", "certain", "DICT"),
    ("gd_madadh_allaidh", "wolf", "gaelic", B + r"(madadh|mhadaidh|madaidh)[ -]allaidh" + E, ["Scotland"], "n gd", "madadh-allaidh, wolf ('wild dog')", "certain", "DICT"),
    ("ga_mactire", "wolf", "irish", B + r"mh?ac tire" + E, ["Ireland", "Northern Ireland"], "ga", "mac tíre, wolf", "certain", "DICT"),
    ("cy_afanc", "beaver", "welsh", B + r"(afanc|afangc)" + E, ["Wales"], "n cy", "afanc, beaver (also a water monster of legend)", "probable", "DICT"),
    ("cy_garan", "crane", "welsh", B + r"(garan|ngaran)" + E, ["Wales"], "n cy", "garan, crane or heron", "probable", "DICT"),
    ("cy_eryr", "eagle", "welsh", B + r"(eryr|eryrod)" + E, ["Wales"], "n cy", "eryr, eagle", "certain", "DICT"),
    ("gd_iolair", "eagle", "gaelic", B + r"(iolair|iolaire|h-iolaire|iolairean)" + E, ["Scotland"], "n gd", "iolair, eagle", "certain", "DICT"),
    ("ga_iolar", "eagle", "irish", B + r"(iolar|iolair|h-iolar|iolrach)" + E, ["Ireland", "Northern Ireland"], "ga", "iolar, eagle", "certain", "DICT"),
    ("cy_baedd", "boar", "welsh", B + r"(baedd|baeddod)" + E, ["Wales"], "n cy", "baedd, boar", "certain", "DICT"),
    ("gd_torc", "boar", "gaelic", B + r"(torc|tuirc|thuirc)" + E, ["Scotland"], "n gd", "torc, boar (genitive tuirc)", "certain", "DICT"),
    ("ga_torc", "boar", "irish", B + r"(torc|tuirc|dtorc|thorc)" + E, ["Ireland", "Northern Ireland"], "n ga", "torc, boar", "certain", "DICT"),
    ("cy_cigfran", "raven", "welsh", B + r"(cigfran|gigfran)" + E, ["Wales"], "n cy", "cigfran, raven", "certain", "DICT"),
    ("gd_fitheach", "raven", "gaelic", B + r"(fitheach|fhitheach|fithich|fhithich)" + E, ["Scotland"], "n gd", "fitheach, raven (genitive fithich)", "certain", "DICT"),
    ("cy_carw", "deer", "welsh", B + r"(carw|ceirw|hydd|ewig|hyddod)" + E, ["Wales"], "n cy", "carw, stag or deer (plural ceirw); hydd, stag; ewig, hind", "certain", "DICT"),
    ("gd_fiadh", "deer", "gaelic", B + r"(fiadh|fhiadh|feidh|fheidh|eilid|eilde|h-eilde|eildeig)" + E, ["Scotland"], "n gd", "fiadh, deer (genitive fèidh); eilid, hind (genitive eilde)", "certain", "DICT"),
    ("ga_fia", "deer", "irish", B + r"(fia|fiadh|fhia|bhfia|fiaigh)" + E, ["Ireland", "Northern Ireland"], "ga", "fia, deer", "certain", "DICT"),
    ("cy_broch", "badger", "welsh", B + r"(broch|mochyn daear|moch daear)" + E, ["Wales"], "n cy", "broch or mochyn daear, badger", "probable", "DICT"),
    ("gd_broc", "badger", "gaelic", B + r"(broc|bruic|bhruic|bhroc)" + E, ["Scotland"], "n gd", "broc, badger (genitive bruic)", "certain", "DICT"),
    ("ga_broc", "badger", "irish", B + r"(broc|mbroc|bruic|bhruic|brocach|brocaigh)" + E, ["Ireland", "Northern Ireland"], "ga", "broc, badger; brocach, badger sett", "certain", "DICT"),
    ("ie_brockagh", "badger", "irish", B + r"(brockagh|brackagh|brocka)" + E, ["Ireland", "Northern Ireland"], "n", "anglicised Irish brocach, badger sett", "probable", "DICT"),
    ("ie_nabrock", "badger", "irish", r"nabrock" + E, ["Ireland", "Northern Ireland"], "n", "anglicised Irish na mbroc, of the badgers", "probable", "DICT"),
    ("cy_llwynog", "fox", "welsh", B + r"(llwynog|llwynogod|cadno|gadno|chadno|nghadno)" + E, ["Wales"], "n cy", "llwynog or cadno, fox", "certain", "DICT"),
    ("gd_sionnach", "fox", "gaelic", B + r"(sionnach|shionnach|sionnaich|shionnaich|t-sionnaich|(madadh|mhadaidh|madaidh)[ -]ruaidh)" + E, ["Scotland"], "n gd", "sionnach or madadh-ruadh, fox", "certain", "DICT"),
    ("ga_sionnach", "fox", "irish", B + r"(sionnach|tsionnaigh|shionnaigh|sionnaigh|mhadra rua|madra rua)" + E, ["Ireland", "Northern Ireland"], "ga", "sionnach or madra rua, fox", "certain", "DICT"),
    ("cy_cath", "wildcat", "welsh", B + r"(cath|gath|nghath|cathod)" + E, ["Wales"], "n cy", "cath, cat (wild cat in hill names)", "probable", "DICT"),
    ("gd_cat", "wildcat", "gaelic", B + r"(chait|nan cat|cat fiadhaich)" + E, ["Scotland"], "n gd", "cat, cat (wild cat in hill names)", "probable", "DICT"),
    ("ga_cat", "wildcat", "irish", B + r"(chait|gcat)" + E, ["Ireland", "Northern Ireland"], "ga", "cat, cat (wild cat in hill names)", "probable", "DICT"),
    ("cy_dyfrgi", "otter", "welsh", B + r"(dyfrgi|dwrgi|dyfrgwn)" + E, ["Wales"], "n cy", "dyfrgi, otter", "certain", "DICT"),
    ("gd_dobhran", "otter", "gaelic", B + r"(dobhran|dhobhrain|dobhrain|dobharchu)" + E, ["Scotland"], "n gd", "dòbhran, otter", "certain", "DICT"),
    ("ga_dobharchu", "otter", "irish", B + r"(dobharchu|madra uisce|mhadra uisce)" + E, ["Ireland", "Northern Ireland"], "ga", "dobharchú or madra uisce, otter", "certain", "DICT"),
    ("cy_eog", "salmon", "welsh", B + r"(eog|eogiaid|samwn)" + E, ["Wales"], "n cy", "eog, salmon", "certain", "DICT"),
    ("gd_bradan", "salmon", "gaelic", B + r"(bradan|bhradan|bradain|bhradain)" + E, ["Scotland"], "n gd", "bradan, salmon", "certain", "DICT"),
    ("ga_bradan", "salmon", "irish", B + r"(bradan|bhradain|mbradan)" + E, ["Ireland", "Northern Ireland"], "ga", "bradán, salmon", "certain", "DICT"),
    ("cy_alarch", "swan", "welsh", B + r"(alarch|elyrch|alarchod)" + E, ["Wales"], "n cy", "alarch, swan", "certain", "DICT"),
    ("gd_eala", "swan", "gaelic", B + r"(h-eala|eala|ealachan)" + E, ["Scotland"], "n gd", "eala, swan", "certain", "DICT"),
    ("ga_eala", "swan", "irish", B + r"(h-eala|eala|ealai)" + E, ["Ireland", "Northern Ireland"], "ga", "eala, swan", "certain", "DICT"),
    ("cy_barcud", "kite", "welsh", B + r"(barcud|farcud|barcutiaid)" + E, ["Wales"], "n cy", "barcud, kite", "certain", "DICT"),
]
# madadh on its own means dog, fox or wolf: counted separately as 'uncertain' and kept out of every total
MADADH = B + r"(madadh|mhadaidh|madaidh|mhadadh|madaidhean)" + E

# ---------- MODERN: English and Scots animal words with a landscape word
LANDWORD = (r"(crags?|craig|scar|scars|nest|rock|rocks|cliff|clough|cleugh|hill|hills|knowe|knot|nab|gill|ghyll|holes?|howe?|tor|"
            r"stones?|law|pike|fell|moss|wood|dale|den|dean|dene|heugh|hope|pits?|slack|side|edge|top|head|bank|cove|island|"
            r"moor|pool|loch|lough|well|bog|bottom|burn|beck|brook|leap|seat|play|lea|lee|ley|haugh|mere|rigg|ridge|end)")
MODERN = [
    # (id, animal, regex on the name, certainty)
    ("en_wolf", "wolf", B + r"wolf(e|s|'s)?\s*" + LANDWORD + E, "probable"),
    ("en_wolf2", "wolf", B + r"wolf(hole|pit|pits|cleugh|crag|crags|hill|hope|lee|elee|sdale|stone|stones)" + E, "probable"),
    ("en_eagle", "eagle", B + r"eagle(s|'s)?\s*" + LANDWORD + E, "probable"),
    ("en_raven", "raven", B + r"raven(s|'s)?\s*" + LANDWORD + E, "probable"),
    ("en_raven2", "raven", B + r"raven(scar|scliffe|stones?|crag|scleugh|shaw|hill|scrag|snest|stonedale)" + E, "probable"),
    ("en_crane", "crane", B + r"crane(s|'s)?\s*" + LANDWORD + E, "probable"),
    ("en_hart", "deer", B + r"(hart|harts|hart's|hind|hinds|deer|stag|stags)\s*" + LANDWORD + E, "probable"),
    ("en_harter", "deer", B + r"(harter fell|hartsop|hart side|hart crag)" + E, "probable"),
    ("en_brock", "badger", B + r"(brock|brocks|brock's|badger|badgers|badger's)\s*" + LANDWORD + E, "probable"),
    ("en_brock2", "badger", B + r"brock(holes?|hole|crag|stones?)" + E, "probable"),
    ("en_fox", "fox", B + r"(fox|foxes|fox's|tod|tods|tod's)\s*" + LANDWORD + E, "probable"),
    ("en_fox2", "fox", B + r"(fox|tod)(holes?|hills?|hall|crags?|knowe|law|cleugh|stones?|dens?)" + E, "probable"),
    ("en_cat", "wildcat", B + r"(cat|cats|cat's)\s*" + LANDWORD + E, "probable"),
    ("en_cat2", "wildcat", B + r"(cat bells|catbells|catstycam|catstye cam|catcleugh|catcrag|catstones?|cat ?gill)" + E, "probable"),
    ("en_otter", "otter", B + r"(otter|otters|otter's)\s*" + LANDWORD + E, "probable"),
    ("en_otter2", "otter", B + r"otter(swick|spool|hole|stone|shaw)" + E, "probable"),
    ("en_swan", "swan", B + r"(swan|swans|swan's)\s*" + LANDWORD + E, "probable"),
    ("en_kite", "kite", B + r"(kite|kites|kite's|glede)\s*" + LANDWORD + E, "probable"),
    ("en_kite2", "kite", B + r"kite(snest|brook)" + E, "probable"),
    ("en_boar", "boar", B + r"(wild boar|boar|boars|boar's)\s*" + LANDWORD + E, "probable"),
    ("en_beaver", "beaver", B + r"(beaver|beavers)\s*" + LANDWORD + E, "probable"),
    ("en_salmon", "salmon", B + r"(salmon)\s*(leap|pool|rock)" + E, "probable"),
]
# false friends, matched on the accent-stripped lower-case name; any match removes the candidate (all rules)
EXCLUDE = [
    (r"wolverhampton|wolverton|wolvercote|wolverley|wolsingham|wolstanton|wolston|woolston|woolaston|wollaton|woolfardisworthy|"
     r"wolferton|wolfreton|wolfhampcote|wolviston|woolsington|wolsty|wulf halh", "Old English personal names (Wulfrun, Wulfhere, Wulfstan...)"),
    (r"^(the )?wolf( rock)?$", "Wolf Rock, off Land's End, named for the noise of the sea"),
    (r"eaglesfield|eaglesham|eaglescliffe|egglescliffe|gleneagles|glen eagles|dalleagles|mounteagle|^eagle$|^eagle barnsdale|eagle moor|eaglehall|eagle hall",
     "OE eclēs, Gaelic eaglais 'church', or Eagle in Lincolnshire, OE āc-lēah 'oak wood', and their offshoots"),
    (r"barnoldswick|arnold's|arnold ings|arnside|arnesby", "personal names (Beornwulf, Arnold)"),
    (r"beverston|beverstone|beveridge|beverkae|beveree|beverley (farm|spring)", "personal or transferred names"),
    (r"boarhunt|boarstall|boarden|boardmills|boardwalk|boards|wild boar enclosure|boars hill", "OE burh 'fort', bord 'board', or modern"),
    (r"swanage|swanscombe|swanton|swanley|swanwick|swannington|swansea|swang|aswanley", "OE swān 'herdsman', Old Norse Sveinn, dialect swang 'bog'"),
    (r"catherine|cathedral|catton|caton|catchwater|cattle|catterick|catterall|cathedine|catthaw|catmose|catsfield", "St Catherine, personal names, cattle"),
    (r"potter|totter|dotter|gotter|snotter|wotter|hotter|cotter|lotter|rotter", "not otter"),
    (r"hartlebury|hartington|hartpury|hartshill|harton|hartest", "personal names or other words"),
    (r"hinton|hindon|hinderwell|hinderclay|hindlip", "OE hīwan 'household, monks' or St Hild"),
    (r"deer park|deerpark|old deer park", "a medieval deer park: hunting, not the wild animal (counted apart)"),
    (r"brockhampton|brockton|brockwell|brockley|brockhurst|brockham|brockenhurst|brockdish|brockworth|brocklesby|brockweir|brocton", "OE brōc 'brook' or personal names"),
    (r"toddington|todmorden|todd\b|todds\b|todd's", "personal names, Todmorden"),
    (r"craven|ravensworth|ravensthorpe|raventhorpe|ravenstone$|ravenscar$|ravenglass|ravensdale|ravenseat|ravenspark|ravenswood|ravenhill|ravenfield|ravensfleet",
     "Old Norse personal name Hrafn, or Brittonic, or modern estate names"),
    (r"cranhill|crannagh|cranagh|crannich|cranaig|crannach|cranny|cranham|cranwich|cranmere", "Gaelic or Irish crann 'tree', or uncertain"),
    (r"limavady|polmaddy|portavadie|glenamaddy", "anglicised madadh in Ireland and Galloway: dog, not wolf"),
    (r"otterswick", "Old Norse vik, a bay, with a first element read as a personal or god name (Groome gives Odinswic for the Sanday bay), not secure for the otter"),
    (r"salmonby|burton salmon|salmond|culsalmond", "personal or family names"),
    (r"kites hardwick|kitebrook", "manorial or uncertain"),
    (r"badger$|badgers mount|badgers glory|badgers dene", "Badger in Shropshire (personal name) and modern house names"),
    (r"foxton locks|foxhunters|fox covert", "fox coverts are planted for hunting, not evidence of wild foxes"),
    (r"fox and hounds|fox & hounds", "inn signs"),
]
