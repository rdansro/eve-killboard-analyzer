import sqlite3
from util import DIR_PATH
import os

class KillboardDB:
    def __init__(self, db_path=DIR_PATH + 'lib/db/kills.db', clean=False):
        if clean:
            os.remove(db_path)

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
                            killmail_id INTEGER UNIQUE,
                            attacker_alliance_id INTEGER,
                            attacker_character_id INTEGER,
                            attacker_corporation_id INTEGER,
                            attacker_damage_done INTEGER,
                            attacker_final_blow TEXT,
                            attacker_security_status NUMERIC,
                            attacker_ship_type_id INTEGER,
                            attacker_weapon_type_id INTEGER,
                            PRIMARY KEY(`killmail_id`)
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
                            victim_ship_type_id INTEGER,
                            PRIMARY KEY(`killmail_id`)
                        )''',
            'kills_items' : '''CREATE TABLE kills_items (
                            killmail_id INTEGER UNIQUE,
                            flag INTEGER,
                            item_type_id INTEGER,
                            quantity_destroyed INTEGER,
                            quantity_dropped INTEGER,
                            singleton INTEGER,
                            PRIMARY KEY(`killmail_id`)
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

        cursor.execute('''INSERT INTO kills VALUES (:killmail_id, :killmail_time, :kill_value, :ship_value, :solo, :solar_system_id, :awox, :locationID, :npc, :zkb_points, :hash)''',
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

        cursor.close()

        self.conn.commit()
