from homebase.models import Employees
from sidekick.views import set_user_string


def get_access(netid, area):
    netid = set_user_string(netid)  # in case we're not in production

    # we have to do this to get the user object itself since the get call will return a QuerySet
    user = Employees.objects.get(netid=netid)
    pos = user.position

    pos_fns = {
        "lbt": get_lbt_access,
        "spt": get_spt_access,
        "sst": get_sst_access,
        "llt": get_llt_access,
        "mgr": get_mgr_access,
        "stt": get_stt_access,
        "stm": get_stm_access,
        "dev": get_dev_access,
    }

    return pos_fns[pos](area) if not user.developer else pos_fns[pos](area) or pos_fns["dev"](area)


# NOTE: if you're having a trouble with a specific access area but the system as a whole seems functional,
#       check for missing commas!
def get_lbt_access(area):
    access_list = [
        # Page access
        "homebase_access", "passwords_access", "shift_access", "roster_access", "quote_access", "printer_access",

        # Passwords page
        "passwords_lab",

        # Shift Covers page
        "shift_viewlabs",

        # Printer Status page
        "printer_labs", "printer_labs_edit",
    ]
    return area in access_list


def get_spt_access(area):
    access_list = [
        # Page access
        "homebase_access", "passwords_access", "shift_access", "roster_access", "quote_access", "printer_access",

        # Passwords page
        "passwords_lab", "passwords_support",
        
        # Shift Covers page
        "shift_viewlabs", "shift_viewsupport",

        # Printer Status page
        "printer_all", "printer_all_edit",

        # Roster page
        # "roster_prof_all",
    ]
    return area in access_list


def get_sst_access(area):
    access_list = [
        # Page access
        "homebase_access", "passwords_access", "shift_access", "roster_access", "quote_access", "printer_access",

        # Nav elements
        "nav_modtools",

        # Passwords page
        "passwords_lab", "passwords_support",
        
        # Shift Covers page
        "shift_viewall",

        # Printer Status page
        "printer_all", "printer_all_edit",

        # Roster page
        "roster_prof_all",
    ]
    return area in access_list


def get_llt_access(area):
    access_list = [
        # Page access
        "homebase_access", "passwords_access", "shift_access", "roster_access", "quote_access", "printer_access",

        # Passwords page
        "passwords_lab",

        # Shift Covers page
        "shift_viewlabs", "shift_postlab",

        # Roster page
        "roster_modfb_lab",

        # Printer Status page
        "printer_labs", "printer_labs_edit",
    ]
    return area in access_list


def get_mgr_access(area):
    access_list = [
        # Page Access
        "homebase_access", "passwords_access", "shift_access", "roster_access", "quote_access", "printer_access",

        # Nav elements
        "nav_modtools",

        # Homebase page
        "homingbeacon_checkin", "homingbeacon_requestpaper", "announcements_canedit", "homingbeacon_updatestatus",

        # Shift Covers Page
        "shift_modpanel", "shift_postall", "shift_viewall",

        # Roster page
        "roster_editemp", "roster_addremoveemp", "roster_modfb_all", "roster_prof_all", "roster_prof_all_edit",

        # Roster comment overview
        "roster_overview",

        # Printer page
        "printer_all", "printer_all_edit",

        # Passwords page
        "passwords_lab", "passwords_support", "passwords_manager",
    ]
    return area in access_list


def get_stt_access(area):
    access_list = [
        # Page Access
        "homebase_access", "passwords_access", "shift_access", "roster_access", "quote_access", "printer_access",

        # Nav elements
        "nav_modtools",

        # Homebase page
        "homingbeacon_checkin", "homingbeacon_requestpaper", "announcements_canedit", "homingbeacon_updatestatus",

        # Shift Covers Page
        "shift_modpanel", "shift_postall", "shift_viewall",

        # Roster page
        "roster_editemp", "roster_addremoveemp", "roster_modfb_all", "roster_prof_all", "roster_prof_all_edit",

        # Roster comment overview
        "roster_overview",

        # Printer page
        "printer_all", "printer_all_edit",

        # Passwords page
        "passwords_lab", "passwords_support", "passwords_manager",
    ]
    return area in access_list


def get_stm_access(area):
    access_list = [
        # Page Access
        "homebase_access", "passwords_access", "shift_access", "roster_access", "quote_access", "printer_access",

        # Nav elements
        "nav_modtools",

        # Homebase page
        "homingbeacon_checkin", "homingbeacon_requestpaper", "announcements_canedit", "homingbeacon_updatestatus",

        # Shift Covers Page
        "shift_modpanel", "shift_postall", "shift_viewall",

        # Roster page
        "roster_editemp", "roster_addremoveemp", "roster_modfb_all", "roster_prof_all", "roster_prof_all_edit",

        # Roster comment overview
        "roster_overview",

        # Printer page
        "printer_all", "printer_all_edit",

        # Passwords page
        "passwords_lab", "passwords_support", "passwords_manager",
    ]
    return area in access_list


def get_dev_access(area):
    access_list = [
        # Page Access
        "homebase_access", "passwords_access", "shift_access", "roster_access", "quote_access", "printer_access",

        # Nav elements
        "nav_modtools",

        # Homebase page
        "homingbeacon_checkin", "homingbeacon_requestpaper", "announcements_canedit",

        # Shift Covers Page
        "shift_modpanel", "shift_postall", "shift_viewall",

        # Roster page
        "roster_editemp", "roster_addremoveemp", "roster_modfb_all", "roster_prof_all", "roster_prof_all_edit",

        # Printer page
        "printer_all", "printer_all_edit",

        # Passwords page
        "passwords_all",
    ]
    return area in access_list


MASTER_ACCESS_TEMPLATE = [
    # Nav access
    "nav_modtools",                         # MoD tools in the navbar


    # Homebase Page
    "homebase_access",                      # May access homebase page
    #   Homing Beacon
    "homingbeacon_checkin",                 # Can check employees in
    "homingbeacon_requestpaper",            # Can request a paper count
    #   Announcements/Events
    "announcements_canedit",                # Can post, modify, or delete announcements/events


    # Passwords Page
    "passwords_access",                     # Access passwords page
    "passwords_lab",                        # Access lab passwords
    "passwords_support",                    # Access support passwords
    "passwords_manager",                    # Access manager passwords
    "passwords_dev",                        # Access dev passwords
    "passwords_all",                        # Access all passwords


    # Shift Covers Page
    "shift_access",                         # Access shift covers page
    "shift_modpanel",                       # View MOD Panel for shift
    "shift_postlab",                        # Post any lab tech's covers
    "shift_postall",                        # Post anyone's covers!
    "shift_viewlabs",                       # View open lab shifts
    "shift_viewsupport",                    # View open sd & rc shifts
    "shift_viewsenior",                     # View sst shifts
    "shift_viewall",                        # View all open shifts


    # Roster Page
    "roster_access",                        # Access roster page
    "roster_editemp",                       # Modify employee metadata
    "roster_addremoveemp",                  # Add or remove employee
    "roster_modfb_all",                     # Modify comment, discipline, & trophy data
    "roster_modfb_lab",                     # View/modify comments & discipline for lab techs
    "roster_prof_all",                      # Access all proficiencies
    "roster_prof_all_edit",                 # Edit all proficiencies
    "roster_overview",                      # Access the overview page to see all comments


    # Quote Page
    "quote_access",                         # Access quote tool


    # Printer Status Page
    "printer_access",                       # Access printer page
    "printer_labs",                         # View computer lab printers
    "printer_all",                          # View all printers
    "printer_labs_edit",                    # Edit lab printer statuses
    "printer_all_edit",                     # Edit all printer statuses
]
