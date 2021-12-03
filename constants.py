CHROMATIC = "Chromatic Orb"
ALCHEMY = "Orb of Alchemy"
ALTERATION = "Orb of Alteration"
DIVINE = "Divine Orb"
REGRET = "Orb of Regret"
PRISM = "Gemcutter's Prism"
ORB_OF_SCOURING = 'Orb of Scouring'
CHAOS = 'Chaos Orb'
VAAL_ORB = 'Vaal Orb'
EXALTED_ORB = 'Exalted Orb'
CHISEL = "Cartographer's Chisel"
ORB_OF_FUSING = "Orb of Fusing"
try:
    from secrets import ssid as real_ssid
    ssid = real_ssid
except ImportError as e:
    print(e)
    print("Please set ssid in secrets.py")
    with open('secrets.py','w') as f:
        f.write('ssid=')
    ssid = ''
hard_currency = [
    ALTERATION,
    ALCHEMY,
    "Chaos Orb",
    "Vaal Orb",
    "Warlord's Exalted Orb",
    DIVINE,
    "Exalted Orb",
    "Exalted Shard",
    ORB_OF_FUSING,
    "Jeweller's Orb",
    "Awakened Sextant",
    "Prime Sextant",
    PRISM,
    "Regal Orb",
    "Mirror Shard",
    "Stacked Deck",
    "Mirror of Kalandra",
    CHISEL,
    "Orb of Unmaking",
    "Awakener's Orb",
    "Crescent Splinter"

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

currency_shards={
    'Seven Years Bad Luck':(1/13,'Mirror Shard'),
    'The Sephirot':(11/10,'Divine Orb'),
    "The Saint's Treasure":(2 / 10, EXALTED_ORB),
    "The Inventor":(10 / 6, VAAL_ORB),
    "The Innocent":(40/10,'Orb of Regret'),
    "The Immortal":(1/90,'Mirror of Kalandra'),
    "The Hoarder":(1 / 12, EXALTED_ORB),
    "No Traces":(30 / 9, ORB_OF_SCOURING),
    "Lucky Deck":(10/9,'Stacked Deck'),
    "Alluring Bounty":(10 / 7, EXALTED_ORB),
    'Abandoned Wealth':(3 / 5, EXALTED_ORB),
    'Underground Forest':(10/4,'Awakened Sextant'),
    'Three Faces in the Dark':(3 / 7, CHAOS),
    'The Scholar':(40/3,'Scroll of Wisdom'),
    'The Catalyst':(3 / 4, VAAL_ORB),
    "Lucky Connections":(20 / 7, ORB_OF_FUSING),
    "Loyalty":(3 / 5, ORB_OF_FUSING),
    "Boon of Justice":(1/6, "Offering to the Goddess"),
    "Sambodhi's Wisdom":(1/3, "A Master Seeks Help, Jun"),
    "The Cartographer":(10 / 1, CHISEL),
    "Gemcutter's Promise":(1 / 3, PRISM),
    "Coveted Possession":(5/9,"Regal Orb"),
"Vile Power":(1/5,"Ancient Doom"),
    "The Union":(10/7,PRISM),
    "The Gemcutter":(1/3,PRISM),
    "Grave Knowledge":(1/6,PRISM),
    "Vinia's Token":(10 / 5, REGRET),
"The Mad King":(1/7, "The King's Path"),
    "Dark Temptation":(1/5,"Obliteration"),
    "The Chains that Bind":(1/11),
    "Vanity":(1 / 9, DIVINE),
    "Humility":(1 / 9, DIVINE),
    "The Wrath":(10 / 8, CHAOS),
    "A Dab of Ink":(1/9,"The Poet's Pen"),
    "The Sun":(1/7,"Rise of the Phoenix"),
    "The Realm":(1/5,"Portal"),
    "The Blazing Fire":(1/8,"Chin Sol"),
    "The Jeweller's Boon":(1/5,"The Jeweller's Touch"),
    "The Valley of Steel Boxes":(1/9,'Monstrous Treasure'),
    "The Porcupine":(1/6,DIVINE),
    "The Betrayal":(1/9,"Maligaro's Virtuosity"),

    'The Swordking\'s Salute':(1/7,"Daresso's Salute"),
    "The Dark Mage":(1/6,DIVINE),
    "Acclimatisation":(20 / 2, ALTERATION),
    "The Polymath":(1/3,"Astramentis"),
    "The Offering":(1/6,"Shavronne's Wrappings"),
    "The Survalist":(7 / 3, ALCHEMY),
    "Demigod's Wager":(1/7, "Orb of Annulment"),
    "Societie's Remorse":(10/1,ALTERATION),
    "Brush, Paint and Palette":(1/5,"The Artist"),
    "Chaotic Disposition":(5/1,CHAOS),
    "The Heroic Shot":(17, CHROMATIC),


}
blacklist = [
    'Clear Oil',
    'Amber Oil',
    'Sepia Oil',
    'Turn the Other Cheeck',
    'Thunderous Skies',
    'Volatile Power',
    'The Hermit',
    "The Wolf's Shadow",
    "Thirst for Knowledge",
    "The Wolverine",
    "The Witch",
    "The Web",
    "The Twins",
    "The Twighlight Moon",
    "The Tower",
    "The Surgeon",
    "The Summoner",
    "The Mountain",
    "The Lover",
    "The Long Watch",
    "The Journalist",
    "The King's Blade",
    "The Inoculated",
    "The Incantation",
    "The Gladiator",
    "The Flora's Gift",
    "The Endurance",
    "Her Mask",
    "The Gentleman",
    "The Garish Power",
    "The Gambler",
    "The Carrior Crow",
    "The Beast",
    "The Battle Born",
    "The Archmage's Right Hand",
    "Struck by Lightning",
    "Scholar of the Seas",
    "Might is Right",
    "Lingering Remnants",
    "Light and Truth",
    "Lantador's Lost Love",
    "Imperial Legacy",
    "Gift of the Gemling Queen",
    "Friendship",
    "Doedre's Madness",
    "Death",
    "Cursed Words",
    "Assassin's Favour",
    "A Mother's Parting Gift",
    "The Arena Champion",
    "The Scarred Meadow",
    "The Lunaris Priestess",
    "The Oath",
    "The Eye of the Dragon",
    "The Body",
    "The Warden",
    "Cartographer's Delight",

    "The Traitor",
"Prosperity",
    "Anarchy's Price",
    "The Easy Stroll",
    "Rain Tempter",
    "Rats",
    "The Watcher",

    "Hunter's Resolve",
    "The Metalsmith's Gift",
"The Bear Woman",
"The Calling",
    "Boundless Realms",
'The Siren',
    "The Sigil",
    "The Wolf's Legacy",
    "The Tumbleweed",
    'The Stormcaller'

]
