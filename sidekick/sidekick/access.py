from homebase.models import Employees


def has_access(netid, area):
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


def get_lbt_access(area):
    access_list = [
        # Page access
        "homebase_access", "passwords_access", "shift_access", "roster_access", "quote_access", "printer_access",

        # Passwords page
        "passwords_lab",
        # TODO: Finish filling in
    ]
    return area in access_list


def get_spt_access(area):
    access_list = [
        "homebase_access", "passwords_access", "shift_access", "roster_access", "quote_access", "printer_access",
        # TODO: Finish filling in
    ]
    return area in access_list


def get_sst_access(area):
    access_list = [
        "homebase_access", "passwords_access", "shift_access", "roster_access", "quote_access", "printer_access",
        # TODO: Finish filling in
    ]
    return area in access_list


def get_llt_access(area):
    access_list = [
        "homebase_access", "passwords_access", "shift_access", "roster_access", "quote_access", "printer_access",
        # TODO: Finish filling in
    ]
    return area in access_list


def get_mgr_access(area):
    access_list = [
        "homebase_access", "passwords_access", "shift_access", "roster_access", "quote_access", "printer_access",
        # TODO: Finish filling in
    ]
    return area in access_list


def get_stt_access(area):
    access_list = [
        "homebase_access", "passwords_access", "shift_access", "roster_access", "quote_access", "printer_access",
        # TODO: Finish filling in
    ]
    return area in access_list


def get_stm_access(area):
    access_list = [
        "homebase_access", "passwords_access", "shift_access", "roster_access", "quote_access", "printer_access",
        # TODO: Finish filling in
    ]
    return area in access_list


def get_dev_access(area):
    access_list = [
        "homebase_access", "passwords_access", "shift_access", "roster_access", "quote_access", "printer_access",
        # TODO: Finish filling in
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
    "shift_viewall",                        # View all open shifts


    # Roster Page
    "roster_access",                        # Access roster page
    "roster_editemp",                       # Modify employee metadata
    "roster_addremoveemp",                  # Add or remove employee
    "roster_modemp_all",                    # Modify comment, discipline, & trophy data
    "roster_modemp_lab",                    # View/modify comments & discipline
    "roster_prof_all",                      # Access & edit all proficiencies


    # Quote Page
    "quote_access",                         # Access quote tool


    # Printer Status Page
    "printer_access",                       # Access printer page
    "printer_labs",                         # View computer lab printers
    "printer_all",                          # View all printers
    "printer_labs_edit",                    # Edit lab printer statuses
    "printer_all_edit",                     # Edit all printer statuses
]