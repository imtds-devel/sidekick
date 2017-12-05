from homebase.models import Employees

def has_access(netid, access_area):
    # we have to do this to get the user object itself since the get call will return a QuerySet
    user = None
    for u in Employees.objects.get(netid=netid):
        user = u

    return Employee_Access.get_access(user.position, access_area, user.developer)

class Employee_Access():
    def get_access(self, pos, area, is_dev):
        pos_dict = {
            "lbt": self.get_lbt_access,
            "spt": self.get_spt_access,
            "sst": self.get_sst_access,
            "llt": self.get_llt_access,
            "mgr": self.get_mgr_access,
            "stt": self.get_stt_access,
            "stm": self.get_stm_access,
            "dev": self.get_dev_access
        }

        return pos_dict[pos](area) or pos_dict["dev"](area) if is_dev else pos_dict[pos](area)


    def get_lbt_access(self, area):
        return True

    def get_spt_access(self, area):
        return True

    def get_sst_access(self, area):
        return True

    def get_llt_access(self, area):
        return True

    def get_mgr_access(self, area):
        return True

    def get_stt_access(self, area):
        return True

    def get_stm_access(self, area):
        return True

    def get_dev_access(self, area):
        return True

MASTER_ACCESS_TEMPLATE = {
    "homebase_"
}