import winreg


class RegistryLoader:

    def __init__(self, reg_path):
        self.reg_path = reg_path

    def get_registry(self, reg_name):
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, self.reg_path, 0, winreg.KEY_READ)
            reg_value, reg_type = winreg.QueryValueEx(reg_key, reg_name)
            winreg.CloseKey(reg_key)
            return reg_value
        except WindowsError:
            return None
