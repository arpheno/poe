CHROMATIC = "Chromatic Orb"
ALCHEMY = "Orb of Alchemy"
ALTERATION = "Orb of Alteration"
DIVINE = "Divine Orb"
REGRET = "Orb of Regret"
PRISM = "Gemcutter's Prism"
ORB_OF_SCOURING = "Orb of Scouring"
CHAOS = "Chaos Orb"
VAAL_ORB = "Vaal Orb"
EXALTED_ORB = "Exalted Orb"
CHISEL = "Cartographer's Chisel"
FUSING = "Orb of Fusing"
TRANSMUTE = "Orb of Transmutation"
AUGMENT = "Orb of Augmentation"
CHANCE = "Orb of Chance"
JEWELLERS = "Jeweller's Orb"
SCOUR = "Orb of Scouring"
BAUBLE = "Glassblower's Bauble"
WHETSTONE = "Blacksmith's Whetstone"
UNMAKING = "Orb of Unmaking"
try:
    from poe.secrets import ssid as real_ssid

    ssid = real_ssid
except ImportError as e:
    print(e)
    print("Please set ssid in secrets.py")
    with open("poe/secrets.py", "w") as f:
        f.write("ssid=")
    ssid = ""
HARD_CURRENCY = [
    ALTERATION,
    # ALCHEMY,
    'Greater Eldritch Ichor',
    'Greater Eldritch Ember',
    "Chaos Orb",
    "Vaal Orb",
    "Warlord's Exalted Orb",
    DIVINE,
    "Exalted Orb",
    "Exalted Shard",
    # FUSING,
    "Ancient Orb",
    # "Jeweller's Orb",
    "Awakened Sextant",
    PRISM,
    # "Regal Orb",
    "Mirror Shard",
    "Stacked Deck",
    "Mirror of Kalandra",
    "Orb of Annulment",
    # CHISEL,
    UNMAKING,
    "Awakener's Orb",
    "Crescent Splinter",
]
price_in = [
    # "Orb of Alteration",
    # "Orb of Alchemy",
    "Chaos Orb",
    # "Vaal Orb",
    # "Divine Orb",
    # "Exalted Orb",
    # "Mirror Shard",
    # "Mirror of Kalandra",
]

blacklist = [
    "The One With All",
    "A Mother's Parting Gift",
    "The Brittle Emperor",
    "The Master Artisan",
    "Tranquillity",
    "Amber Oil",
    "The Opulent",
    "The Mind's Eyes",
    "Divine Justice",
    "Anarchy's Price",
    "Assassin's Favour",
    "Boundless Realms",
    "Cartographer's Delight",
    "Clear Oil",
    "Cursed Words",
    "Death",
    "Doedre's Madness",
    "Friendship",
    "Gift of the Gemling Queen",#191+109

    "Her Mask",
    "Hunter's Resolve",
    "Imperial Legacy",
    "Lantador's Lost Love",
    "Light and Truth",
    "Lingering Remnants",
    "Might is Right",
    "Prosperity",
    "Rain Tempter",
    "Rats",
    "Scholar of the Seas",
    "Sepia Oil",
    "Struck by Lightning",
    "The Jeweller's Boon",
    "The Archmage's Right Hand",
    "The Arena Champion",
    "The Battle Born",
    "The Bear Woman",
    "The Beast",
    "The Body",
    "The Calling",
    "The Easy Stroll",
    "The Endurance",
    "The Eye of the Dragon",
    "The Flora's Gift",
    "The Gambler",
    "The Penitent",
    "The Garish Power",
    "The Gentleman",
    "The Gladiator",
    "The Hermit",
    "The Incantation",
    "The Inoculated",
    "The Journalist",
    "The Sword King's Salute",
    "The King's Blade",
    "The Long Watch",
    "The Lover",
    "The Lord of Celebration",
    "The Lion",
    "The Lich",
    "The Last Supper",
    "The Last One Standing",
    "The Journey",
    "The Jester",
    "The Hunger",
    "The Lunaris Priestess",
    "The Metalsmith's Gift",
    "The Mountain",
    "The Oath",
    "The Scarred Meadow",
    "The Sigil",
    "The Siren",
    "The Stormcaller",
    "The Summoner",
    "The Surgeon",
    "The Tower",
    "The Traitor",
    "The Tumbleweed",
    "The Twins",
    "The Warden",
    "The Watcher",
    "The Web",
    "The Witch",
    "The Wolf's Legacy",
    "The Wolf's Shadow",
    "The Wolverine",
    "Thirst for Knowledge",
    "Thunderous Skies",
    "Turn the Other Cheek",
    "Volatile Power",
    "Audacity",
    "Blind Venture",
    "Destined to Crumble",
    "Dialla's Subjugation",
    "Earth Drinker",
    "Glimmer of Hope",
    "Grave Knowledge",
    "Heterochromia",
    "Hope",
    "Hubris",
    "Jack in the Box",
    "Lost Worlds",
    "Lysah's Respite",
    "Shard of Fate",
    "The Aesthete",
    "The Carrion Crow",
    "The Cataclysm",
    "The Conduit",
    "The Cursed King",
    "The Demoness",
    "The Doppelganger",
    "The Dragon",
    "The Drunken Aristocrat",
    "The Encroaching Darkness",
    "The Explorer",
    "The Feast",
    "The Fletcher",
    "The Formless Sea",
    "The Fox",
    "The Pack Leader",
    "The Rabid Rhoa",
    "The Scavenger",
    "The Scholar",
    "The Sun",
    "The Surveyor",
    "The Visionary",
    "The Wolf",
    "Treasure Hunter",
    "Turn the Other Cheek",
    "Mitts",
    "Call to the First Ones",
    "The Coming Storm",
    "The Standoff",
    "The Forsaken",
    "Atziri's Arsenal",
    "The Blazing Fire",
    "The Ruthless Ceinture",
    "The Deceiver",
    "Forbidden Power",
    "The Breach",
    "Three Voices",
    "The Army of Blood",
    "The Sword King's Salute",
    "The Fathomless Depths",
    "The Rite of Elements",
    "The Dreamland",
    "The Admirer",
    "The Twilight Moon",
    "The Price of Protection",
    "A Dab of Ink",
    "The Mad King",
    "Alone in the Darkness",
    "Dark Temptation",
    "The Messenger",
    "Echoes of Love",
    "The Deep Ones",
    "Buried Treasure",
    "Vile Power",
    "The Skeleton",
    "Akil's Prophecy",
    "The Deal",
    "Cameria's Cut",
    "The Cache",
    "Prejudice",
    "The Adventuring Spirit",
    "The Blessing of Moosh",
    "The Fox in the Brambles",
    "The Unexpected Prize",
    "The Side Quest",
    "Boon of the First Ones",
    "Boon of Justice",
]
# LEAGUE = "Standard"
LEAGUE = "Archnemesis"
