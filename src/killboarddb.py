import sqlite3
from util import DIR_PATH
import os

class KillboardDB:
    def __init__(self, db_path=DIR_PATH + 'lib/db/kills.db', clean=False):
        if clean:
            try:
                os.remove(db_path)
            except:
                pass

        self.db_path = db_path
        self.conn = self.connection()

        self.schema = {
            'kills' : '''CREATE TABLE kills (
                            killmail_id INTEGER UNIQUE,
                            killmail_time DATETIME,
                            kill_value NUMERIC,
                            ship_value NUMERIC,
                            solo TEXT,
                            solar_system_id INTEGER,
                            awox TEXT,
                            locationID INTEGER,
                            npc TEXT,
                            zkb_points NUMERIC,
                            hash TEXT,
                            PRIMARY KEY(`killmail_id`)
                        )''',
            'kills_attackers' : '''CREATE TABLE kills_attackers (
                            killmail_id INTEGER,
                            attacker_alliance_id INTEGER,
                            attacker_character_id INTEGER,
                            attacker_corporation_id INTEGER,
                            attacker_damage_done INTEGER,
                            attacker_final_blow TEXT,
                            attacker_security_status NUMERIC,
                            attacker_ship_type_id INTEGER,
                            attacker_weapon_type_id INTEGER
                        )''',
            'kills_victim' : '''CREATE TABLE kills_victim (
                            killmail_id INTEGER UNIQUE,
                            victim_alliance_id INTEGER,
                            victim_character_id INTEGER,
                            victim_corporation_id INTEGER,
                            victim_damage_taken INTEGER,
                            victim_position_x NUMERIC,
                            victim_position_y NUMERIC,
                            victim_position_z NUMERIC,
                            victim_ship_type_id INTEGER
                        )''',
            'kills_items' : '''CREATE TABLE kills_items (
                            killmail_id INTEGER,
                            flag INTEGER,
                            item_type_id INTEGER,
                            quantity_destroyed INTEGER,
                            quantity_dropped INTEGER,
                            singleton INTEGER
                        )'''
        }

        if not self.isBuilt():
            self.build()

    def connection(self):
        return sqlite3.connect(self.db_path)

    def isBuilt(self):
        cursor = self.conn.cursor()
        result = cursor.execute('''SELECT tbl_name FROM sqlite_master WHERE type='table';''')
        result = [item for subset in result for item in subset]
        return set(self.schema.keys()).issubset(result)

    def build(self):
        for table_name, table_setup_query in self.schema.items():
            self.conn.execute(table_setup_query)
        self.conn.commit()

    def insert_kill(self, event):
        cursor = self.conn.cursor()

        # check pk existance
        if len(cursor.execute('''SELECT * FROM kills WHERE killmail_id = :killmail_id''', {'killmail_id' : event['killmail_id']}).fetchall()) != 0:
             return False

        # insert kill into killmail table
        cursor.execute(
            '''INSERT INTO kills VALUES (:killmail_id, :killmail_time, :kill_value, :ship_value, :solo, :solar_system_id, :awox, :locationID, :npc, :zkb_points, :hash)''',
                {
                    'killmail_id' : event['killmail_id'],
                    'killmail_time' : event['killmail_time'],
                    'kill_value' : event['zkb']['totalValue'],
                    'ship_value' : event['zkb']['fittedValue'],
                    'solo' : event['zkb']['solo'],
                    'solar_system_id' : event['solar_system_id'],
                    'awox' : event['zkb']['awox'],
                    'locationID' : event['zkb']['locationID'],
                    'npc' : event['zkb']['npc'],
                    'zkb_points' : event['zkb']['points'],
                    'hash' : event['zkb']['hash']
                })

        # insert victim data
        cursor.execute(
            '''INSERT INTO kills_victim VALUES (:killmail_id, :victim_alliance_id, :victim_character_id, :victim_corporation_id, :victim_damage_taken, :victim_position_x, :victim_position_y, :victim_position_z, :victim_ship_type_id)''',
                {
                    'killmail_id' : event['killmail_id'],
                    'victim_alliance_id' : event['victim']['alliance_id'] if 'alliance_id' in event['victim'] else None,
                    'victim_character_id' : event['victim']['character_id'] if 'character_id' in event['victim'] else None,
                    'victim_corporation_id' : event['victim']['corporation_id'],
                    'victim_damage_taken' : event['victim']['damage_taken'],
                    'victim_position_x' : event['victim']['position']['x'],
                    'victim_position_y' : event['victim']['position']['y'],
                    'victim_position_z' : event['victim']['position']['z'],
                    'victim_ship_type_id' : event['victim']['ship_type_id']
                })

        # insert attackers data
        for attacker in event['attackers']:
            cursor.execute(
                '''INSERT INTO kills_attackers VALUES (:killmail_id, :attacker_alliance_id, :attacker_character_id, :attacker_corporation_id, :attacker_damage_done, :attacker_final_blow, :attacker_security_status, :attacker_ship_type_id, :attacker_weapon_type_id)''',
                    {
                        'killmail_id' : event['killmail_id'],
                        'attacker_alliance_id' : attacker['alliance_id'] if 'alliance_id' in attacker else None,
                        'attacker_character_id' : attacker['character_id'] if 'character_id' in attacker else None,
                        'attacker_corporation_id' : attacker['corporation_id'] if 'corporation_id' in attacker else None,
                        'attacker_damage_done' : attacker['damage_done'],
                        'attacker_final_blow' : attacker['final_blow'],
                        'attacker_security_status' : attacker['security_status'],
                        'attacker_ship_type_id' : attacker['ship_type_id'] if 'ship_type_id' in attacker else None,
                        'attacker_weapon_type_id' : attacker['weapon_type_id'] if 'weapon_type_id' in attacker else None
                    })

        # insert victim item data
        for item in event['victim']['items']:
            cursor.execute(
                '''INSERT INTO kills_items VALUES (:killmail_id, :flag, :item_type_id, :quantity_destroyed, :quantity_dropped, :singleton)''',
                    {
                        'killmail_id' : event['killmail_id'],
                        'flag' : item['flag'],
                        'item_type_id' : item['item_type_id'],
                        'quantity_destroyed' : item['quantity_destroyed'] if 'quantity_destroyed' in item else None,
                        'quantity_dropped' : item['quantity_dropped'] if 'quantity_dropped' in item else None,
                        'singleton' : item['singleton']
                    })

        cursor.close()
        self.conn.commit()
        return True

    def get_solo_ship_kills(self):
        cursor = self.conn.cursor()
        result = cursor.execute('''
            select kills.killmail_id, kills_victim.victim_ship_type_id, kills_attackers.attacker_ship_type_id
            from kills
            join kills_victim on kills.killmail_id = kills_victim.killmail_id
            join kills_attackers on kills.killmail_id = kills_attackers.killmail_id
            where kills.solo = 1
            and kills_attackers.attacker_character_id not null
            and kills_attackers.attacker_ship_type_id not null
            and kills_victim.victim_ship_type_id not null''')
        return result.fetchall()

    # def execute(self, query, args=None):
    #     cursor = self.conn.
    #     result = self
