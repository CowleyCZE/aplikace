import json
import os
import logging
from dropbox_manager import DropboxManager

class EmployeeManagement:
    def __init__(self, dropbox_manager):
        self.zamestnanci = []
        self.vybrani_zamestnanci = []
        self.config_file = 'employee_config.json'
        self.dropbox_manager = dropbox_manager
        self.dropbox_path = '/employee_config.json'
        self.load_config()
        logging.info("Inicializována třída EmployeeManagement")

    def load_config(self):
        try:
            json_content = self.dropbox_manager.read_json(self.dropbox_path)
            if json_content:
                config = json.loads(json_content)
                self.zamestnanci = config.get('zamestnanci', [])
                self.vybrani_zamestnanci = config.get('vybrani_zamestnanci', [])
                logging.info(f"Načtena konfigurace z Dropboxu: {len(self.zamestnanci)} zaměstnanců, {len(self.vybrani_zamestnanci)} vybraných")
            else:
                logging.warning(f"Konfigurační soubor na Dropboxu nenalezen")
        except Exception as e:
            logging.error(f"Chyba při načítání konfigurace z Dropboxu: {str(e)}")

    def save_config(self):
        try:
            config = {
                'zamestnanci': self.zamestnanci,
                'vybrani_zamestnanci': self.vybrani_zamestnanci
            }
            json_content = json.dumps(config, ensure_ascii=False, indent=2)
            self.dropbox_manager.write_json(self.dropbox_path, json_content)
            logging.info(f"Konfigurace uložena na Dropbox: {self.dropbox_path}")
        except Exception as e:
            logging.error(f"Chyba při ukládání konfigurace na Dropbox: {str(e)}")

    def pridat_vybraneho_zamestnance(self, zamestnanec):
        if zamestnanec in self.zamestnanci and zamestnanec not in self.vybrani_zamestnanci:
            self.vybrani_zamestnanci.append(zamestnanec)
            self.save_config()
            logging.info(f"Přidán vybraný zaměstnanec: {zamestnanec}")
            return True
        logging.warning(f"Nepodařilo se přidat vybraného zaměstnance: {zamestnanec}")
        return False

    def odebrat_vybraneho_zamestnance(self, zamestnanec):
        if zamestnanec in self.vybrani_zamestnanci:
            self.vybrani_zamestnanci.remove(zamestnanec)
            self.save_config()
            logging.info(f"Odebrán vybraný zaměstnanec: {zamestnanec}")
            return True
        logging.warning(f"Nepodařilo se odebrat vybraného zaměstnance: {zamestnanec}")
        return False

    def oznacit_zamestnance(self, cislo):
        if 1 <= cislo <= len(self.zamestnanci):
            zamestnanec = self.zamestnanci[cislo - 1]
            if zamestnanec in self.vybrani_zamestnanci:
                return self.odebrat_vybraneho_zamestnance(zamestnanec)
            else:
                return self.pridat_vybraneho_zamestnance(zamestnanec)
        logging.error(f"Pokus o označení/odznačení zaměstnance s neplatným číslem: {cislo}")
        return False

    def get_vybrani_zamestnanci(self):
        logging.info(f"Vrácen seznam vybraných zaměstnanců: {len(self.vybrani_zamestnanci)} položek")
        return self.vybrani_zamestnanci