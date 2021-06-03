import threading as t
import functions as f


settings_dict = {
    "dl_loc": "",
    "rename": "OW_replay",
    "stop_label": False,
    "browser_dl": False,
    "rename_dl": False,
    "auto_dl": True,
    "delete_after": True,
    "add_to_db": True
}
RANK_TRANSLATE_IMG = None
RANK_TRANSLATE_WL = None
RANK_TRANSLATE_TEXT = {
    0: "N/A",
    1: "S1",
    2: "S2",
    3: "S3",
    4: "S4",
    5: "SE",
    6: "SEM",
    7: "GN1",
    8: "GN2",
    9: "GN3",
    10: "GNM",
    11: "MG1",
    12: "MG2",
    13: "MGE",
    14: "DMG",
    15: "LE",
    16: "LEM",
    17: "SMFC",
    18: "Global",
}
# RANK_TRANSLATE_2 = {
#     0: "⚠",
#     1: ">",
#     2: ">>",
#     3: ">>>",
#     4: ">>>>",
#     5: "(>>>>",
#     6: "(*>>>>",
#     7: "(*)",
#     8: "(**)",
#     9: "(***)",
#     10: "(****)",
#     11: "︻╦╤─",
#     12: "(︻╦╤─)",
#     13: "*︻╦╤─*",
#     14: "🌟",
#     15: "*🦅*",
#     16: "(*🦅*)",
#     17: "*⚞◯⚟*",
#     18: "(*☢*)",
# }
MODE_TRANSLATE = {
    0: "Unknown",
    6: "Competitive",
    7: "Wingman"
}
WEAPON_TRANSLATE = {
    "c4": "c4",
    "planted_c4": "c4",
    "knife": "knife",
    "trigger_hurt": "world",
    "taser": "zeus",
    "decoy": "decoy",
    "flashbang": "flash",
    "hegrenade": "he",
    "incgrenade": "molotov",
    "molotov": "molotov",
    "smokegrenade": "smoke",
    "m249": "m249",
    "mag7": "mag7",
    "negev": "negev",
    "nova": "nova",
    "sawedoff": "sawdoff",
    "xm1014": "xm1014",
    "cz75a": "cz75a",
    "deagle": "deagle",
    "elite": "dualies",
    "fiveseven": "5-7",
    "glock": "glock",
    "hkp2000": "p2000",
    "p250": "p250",
    "revolver": "r8",
    "tec9": "tec9",
    "usp_silencer": "usp",
    "usp_silencer_off": "usp",
    "ak47": "ak47",
    "aug": "aug",
    "awp": "awp",
    "famas": "famas",
    "g3sg1": "g3sg1",
    "galilar": "galil",
    "m4a1": "m4a4",
    "m4a1_silencer": "m4a1",
    "m4a1_silencer_off": "m4a1",
    "scar20": "scar20",
    "sg556": "sg556",
    "ssg08": "scout",
    "bizon": "ppbizon",
    "mac10": "mac10",
    "mp5sd": "mp5",
    "mp7": "mp7",
    "mp9": "mp9",
    "p90": "p90",
    "ump45": "ump45",
    "world": "world",
    "inferno": "fire"
}

NAME_CUTOUT_MAIN = 16
NAME_CUTOUT_WATCHLIST = 22
NAME_CUTOUT_KILLS = 16
TEXT_CUTOUT_MAPSERV = 18

VERSION = "4.3"
PROJECT_LINK = "https://github.com/ZaharX97/OWReveal"
PROJECT_LINK_LATEST = PROJECT_LINK + "/releases/latest"
SITE_OWREV = "https://zahar.one/owrev"

list_links = list()
list_add_db = list()
profile_links = dict()
stats_active = True
browser_path = None
path_exec_folder = None
path_resources = None
last_server = None
demo_stats = None
demo_nrplayers = 0
# expected_players = 10
demo_mode = 0
demo_ranks = None
ranks_done = False
npcap_link = "https://nmap.org/npcap/"
found_time = None
thread_sniff = t.Thread()
thread_download = t.Thread()
thread_analyze = t.Thread()
thread_check_vac = t.Thread()
thread_add_to_db = t.Thread(target=f.add_to_db, daemon=True)
event_pkt_found = t.Event()
event_check_vac = t.Event()
app = None

dbconfig = {
    "CENSORED"
}
