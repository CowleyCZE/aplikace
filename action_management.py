import json
import os
import logging
from datetime import datetime
from action_info_manager import ActionInfoManager

class ActionManagement:
    def __init__(self, excel_path):
        self.actions = []
        self.selected_action = None
        self.config_file = 'action_config.json'
        self.action_info_manager = ActionInfoManager(excel_path)
        self.load_config()
        logging.info("Inicializována třída ActionManagement")

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.actions = config.get('actions', [])
                self.selected_action = config.get('selected_action', None)
            logging.info(f"Načtena konfigurace: {len(self.actions)} akcí, vybraná akce: {self.selected_action}")
        else:
            logging.warning(f"Konfigurační soubor {self.config_file} nenalezen")

    def save_config(self):
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'actions': self.actions,
                    'selected_action': self.selected_action
                }, f, ensure_ascii=False, indent=2)
            logging.info(f"Konfigurace uložena do souboru: {self.config_file}")
        except Exception as e:
            logging.error(f"Chyba při ukládání konfigurace: {str(e)}")

    def add_action(self, name, start_date, end_date):
        logging.info(f"Pokus o přidání akce: {name}")
        if name and not any(action['name'] == name for action in self.actions):
            self.actions.append({
                'name': name,
                'start_date': start_date,
                'end_date': end_date
            })
            self.save_config()
            logging.info(f"Přidána nová akce: {name}")
            return True
        logging.warning(f"Nepodařilo se přidat akci: {name}")
        return False

    def update_action(self, index, new_name, new_start_date, new_end_date):
        if 0 <= index < len(self.actions):
            self.actions[index] = {
                'name': new_name,
                'start_date': new_start_date,
                'end_date': new_end_date
            }
            self.save_config()
            if self.selected_action == self.actions[index]['name']:
                self.action_info_manager.write_action_info(new_name, new_start_date, new_end_date)
            logging.info(f"Aktualizována akce: {new_name}")
            return True
        logging.warning(f"Nepodařilo se aktualizovat akci s indexem: {index}")
        return False

    def delete_action(self, index):
        if 0 <= index < len(self.actions):
            deleted_action = self.actions.pop(index)
            if self.selected_action == deleted_action['name']:
                self.selected_action = None
                self.action_info_manager.clear_action_info()
            self.save_config()
            logging.info(f"Smazána akce: {deleted_action['name']}")
            return deleted_action['name']
        logging.warning(f"Nepodařilo se smazat akci s indexem: {index}")
        return None

    def select_action(self, index):
        if 0 <= index < len(self.actions):
            selected_action = self.actions[index]
            self.selected_action = selected_action['name']
            self.action_info_manager.write_action_info(
                selected_action['name'],
                selected_action['start_date'],
                selected_action['end_date']
            )
            self.save_config()
            logging.info(f"Vybrána akce: {self.selected_action}")
            return True
        logging.warning(f"Nepodařilo se vybrat akci s indexem: {index}")
        return False

    def deselect_action(self):
        self.selected_action = None
        self.action_info_manager.clear_action_info()
        self.save_config()
        logging.info("Zrušen výběr akce")

    def get_actions(self):
        return self.actions

    def get_selected_action(self):
        return self.selected_action

    def get_action_date_range(self):
        if self.selected_action:
            action = next((a for a in self.actions if a['name'] == self.selected_action), None)
            if action:
                return f"{action['start_date']} - {action['end_date']}"
        return None