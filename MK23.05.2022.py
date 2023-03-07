import os
import re
import random
import keyboard
import requests
from mss import mss
import pyautogui
import numpy as np
import math
import time
import datetime
import cv2
import copy
import inspect
import json
import pytesseract

def load_profile():
    with open("Profile.json", "r", encoding="utf-8") as file_profile:
        file_user = json.load(file_profile)
        file_profile.close()
        if file_user["profile"] == "k":
            return file_user["k"]
        if file_user["profile"] == "m":
            return file_user["m"]

class Player:
    monitor1 = {  # Весь экран
            'left': 0,
            'top': 0,
            'width': 1920,
            'height': 1080,

    }
    monitorTESSERACKT = {
        'left': 50,
        'top': 1040,
        'width': 125,
        'height': 40,

    }

    def __init__(self, multiplier_location_x, multiplier_location_y, red, green, distance_map, distance_yard, scatter):

        self.multiplier_location_x = multiplier_location_x
        self.multiplier_location_y = multiplier_location_y

        self.list_coordinates = Player.target_coordinates('Coordinat_2.txt')

        self.original_elusive_rich_elethium_deposit = Player.target_coordinates('Resources\Elusive_Rich_Elethium_Deposit(197).txt')
        self.elusive_rich_elethium_deposit = copy.copy(self.original_elusive_rich_elethium_deposit)

        self.original_rich_elethium_deposit = Player.target_coordinates('Resources\Rich_Elethium_Deposit(137).txt')
        self.rich_elethium_deposit = copy.copy(self.original_rich_elethium_deposit)

        self.original_elethium_deposit = Player.target_coordinates('Resources\Elethium_Deposit(316).txt')
        self.elethium_deposit = copy.copy(self.original_elethium_deposit)

        self.original_elusive_rich_progenium_deposit = Player.target_coordinates('Resources\Elusive_Rich_Progenium_Deposit(197).txt')
        self.elusive_rich_progenium_deposit = copy.copy(self.original_elusive_rich_progenium_deposit)

        self.original_elusive_progenium_deposit = Player.target_coordinates('Resources\Elusive_Progenium_Deposit(247).txt')
        self.elusive_progenium_deposit = copy.copy(self.original_elusive_progenium_deposit)

        self.original_rich_progenium_deposit = Player.target_coordinates('Resources\Rich_Progenium_Deposit(88).txt')
        self.rich_progenium_deposit = copy.copy(self.original_rich_progenium_deposit)

        self.original_progenium_deposit = Player.target_coordinates('Resources\Progenium_Deposit(92).txt')
        self.progenium_deposit = copy.copy(self.original_progenium_deposit)

        self.original_forgotten_treasure_vault = Player.target_coordinates('Resources\Forgotten_Treasure_Vault(60).txt')
        self.forgotten_treasure_vault = copy.copy(self.original_forgotten_treasure_vault)

        self.original_discarded_automa_scrap = Player.target_coordinates('Resources\Discarded_Automa_Scrap(18).txt')
        self.discarded_automa_scrap = copy.copy(self.original_discarded_automa_scrap)

        self.original_cypher_bound_chest = Player.target_coordinates('Resources\Cypher_Bound_Chest(107).txt')
        self.cypher_bound_chest = copy.copy(self.original_cypher_bound_chest)

        self.original_tarachnid_eggs = Player.target_coordinates('Resources\Tarachnid_Eggs(5).txt')
        self.tarachnid_eggs = copy.copy(self.original_tarachnid_eggs)

        self.original_avian_nest = Player.target_coordinates('Resources\Avian_Nest(38).txt')
        self.avian_nest = copy.copy(self.original_avian_nest)

        self.original_mawsworn_supply_chest = Player.target_coordinates('Resources\Mawsworn_Supply_Chest(34).txt')
        self.mawsworn_supply_chest = copy.copy(self.original_mawsworn_supply_chest)

        self.near_res_50 = None

        self.player_coordinates_x2, self.player_coordinates_y2 = self.pytesseract_player_target(self.list_coordinates)

        self.player_coordinates_x0 = 0
        self.player_coordinates_y0 = 0
        self.player_coordinates_x1 = 0
        self.player_coordinates_y1 = 0
        self.need_check_minimap = 0
        self.find_res_minimap = None
        self.check_buff = None
        self.red_NPC = red#[45.37, 38.79]
        self.green_NPC = green#[44.88, 29.78]
        self.distanceAC = 0
        self.distanceAB = 0
        self.distanceBC = 0
        self.angle_degree = 0
        self.cosine_exterior_angle = 0
        self.left_or_right_angle = ''
        self.rotation_sec = ''
        self.note = ''
        self.target_sight_x = 0
        self.target_sight_y = 0

        self.distance_for_check_res_on_the_map = distance_map
        self.distance_for_check_res_in_yard = distance_yard
        self.scatter = scatter

        self.one_class = 0
        self.two_class = 0

    def __str__(self):
        print(self.multiplier_location_x)
        print(self.multiplier_location_y)
        print(self.list_coordinates)
        print(f'Точка назначения: {self.player_coordinates_x2}, {self.player_coordinates_y2}')
        print(f'Положение игрока: {self.player_coordinates_x0}, {self.player_coordinates_y0}')
        print(f'Положение взгляда: {self.player_coordinates_x1}, {self.player_coordinates_y1}')
        print(f'ДистанцияAC: {self.distanceAC}')
        print(f'ДистанцияAB: {self.distanceAB}')
        print(f'ДистанцияBC: {self.distanceBC}')
        print(f'Угол поворота: {self.angle_degree}')
        print(f'Внешний угол поворота: {self.cosine_exterior_angle}')
        print(f'Сторона поворота: {self.left_or_right_angle}')
        print(f'Длительность нажатия: {self.rotation_sec}')
        print(f'Клавиша поворота: {self.note}')
        print("======================================================================================")
        print('\n')

    @staticmethod
    def error(ex, write):
        time_error = datetime.datetime.now().strftime("%H:%M:%S")
        error = inspect.stack()
        line = re.findall("line \w+", str(error))
        all_error = f"{time_error}  {line[1]} >>> {ex}" + "\n"
        print(f"{time_error}  {line[1]} >>> {ex}")
        if write == "yes":
            with open("Error.txt", "a", encoding="utf-8") as error:
                error.write(all_error)

    def find_error(self):
        disconnect = monitor.construct_gui(time_active=5, img=monitor.disconnect,
                                           similarity=0.8, offset_x=0, offset_y=0,
                                           region=(1700, 990, 200, 60), grayscale=False)
        if disconnect: return "disconnect"

        m = mss()
        grab = m.grab({"left": user["scull_position"][0], "top": user["scull_position"][1], "width": 1, "height": 1})
        grab = np.array(grab)[0][0]
        if grab[0] == user["scull_color"][0] and grab[1] == user["scull_color"][1] and grab[2] == user["scull_color"][2]: return "dead"

        m = mss()
        grab = m.grab({"left": user["hp_position"][0], "top": user["hp_position"][1], "width": 1, "height": 1})
        full_screen_array = np.array(grab)
        hp = (full_screen_array == (user["hp_color"][0], user["hp_color"][1], user["hp_color"][2], 255))
        if False in hp:
            return "unknown_hp_off"
        else: return "unknown_hp_on"

    @staticmethod
    def str_magik(strings):
        strings = str(strings)
        if len(strings) < 5:
            return strings + "0"
        else:
            return strings

    @staticmethod
    def target_coordinates(name):
        """Загрузка координат точек назначения"""
        list_coordinates = []
        infile1 = str(name)
        file1 = open(infile1, mode='r', encoding='utf_8')
        for x in file1:
            x = x.strip()
            if len(x) > 11:
                x = x[:-1]
                list_coordinates.append(x)
            else:
                list_coordinates.append(x)
        file1.close()
        print(f"Имя документа: {name}, Длина документа: {len(list_coordinates)}")
        return list_coordinates

    #@staticmethod
    #def get_layout():
        #u = ctypes.windll.LoadLibrary("user32.dll")
        #pf = getattr(u, "GetKeyboardLayout")
        #print(pf)
        #if hex(pf(0)) == '0x4190419':
            #print("ru-change(english)")
            #window_handle = win32gui.GetForegroundWindow()

            #result = win32api.SendMessage(window_handle, 0x0050, 0, 0x04090409) # программная смена

            # keyboard.press_and_release('shift + alt') # смена клавиатурой

            # return 'ru'
        #if hex(pf(0)) == '0x4090409':
            #print("en-normal")
            # return 'en'

        # os.startfile("D:\Zagruzki\change_langue\change_langue.exe")

    @staticmethod
    def pytesseract_player_target(list_coordinates_player, num=0):
        """Получение первых координат из списка"""
        player_coordinates_x2 = list_coordinates_player[num][:5]
        player_coordinates_y2 = list_coordinates_player[num][6:]
        return player_coordinates_x2, player_coordinates_y2

    def pytesseract_player_xy0(self, how):
        """Считывание координат в цифровой формат"""
        if player.one_class == 0:
            value = 0
            error = 0
            while error != 1:
                try:
                    m = mss()
                    crop_img1 = m.grab(Player.monitorTESSERACKT)
                    img_arr = np.array(crop_img1)
                    player_coordinates = pytesseract.image_to_string(img_arr, config='outputbase digits')
                    player_coordinates = (player_coordinates.split())[0]
                    number = player_coordinates.replace(".", "")

                    x1 = number[:2]
                    x2 = number[2:4]
                    y1 = number[4:6]
                    y2 = number[6:8]
                    warning_x1 = float(x1)/2
                    warning_x2 = float(x2)/2
                    warning_y1 = float(y1)/2
                    warning_y2 = float(y2)/2
                    player_coordinates_x, player_coordinates_y = f"{x1}.{x2}", f"{y1}.{y2}"
                    if how == 0:
                        self.player_coordinates_x0 = player_coordinates_x
                        self.player_coordinates_y0 = player_coordinates_y
                    if how == 1:
                        self.player_coordinates_x1 = player_coordinates_x
                        self.player_coordinates_y1 = player_coordinates_y

                    return self.player_coordinates_x0, self.player_coordinates_y0

                except Exception as ex:
                    player.error(ex=ex, write="no")
                    value += 1
                    if value > 3:
                        keyboard.release("w")
                        time.sleep(0.1)
                        keyboard.press("w")
                        time.sleep(0.1 + random.uniform(0.1, 0.2))
                        keyboard.release("w")
                    print(value)
                    if value == 100:
                        player.error(ex=ex, write="yes")
                        combat.telegram(hp_ignore=True)

    def distance_to_target(self, how):
        """Расчет дистанции:треугольника ABC"""
        if player.one_class == 0:
            if how == 0: # Расстояние AС
                try:
                    x = [float(self.player_coordinates_x2), float(self.player_coordinates_x0)]
                    y = [float(self.player_coordinates_y2), float(self.player_coordinates_y0)]
                    xy = (np.max(x) - np.min(x)) * self.multiplier_location_x
                    yx = (np.max(y) - np.min(y)) * self.multiplier_location_y
                    distance = math.sqrt(math.pow(xy, 2) + math.pow(yx, 2))
                    self.distanceAC = distance
                except Exception as ex:
                    player.error(ex=ex, write="no")
            if how == 1: # Расстояние AB
                try:
                    x = [float(self.player_coordinates_x1), float(self.player_coordinates_x0)]
                    y = [float(self.player_coordinates_y1), float(self.player_coordinates_y0)]
                    xy = (np.max(x) - np.min(x)) * self.multiplier_location_x
                    yx = (np.max(y) - np.min(y)) * self.multiplier_location_y
                    distance = math.sqrt(math.pow(xy, 2) + math.pow(yx, 2))
                    self.distanceAB = distance
                except Exception as ex:
                    player.error(ex=ex, write="no")
            if how == 2: # Расстояние BC
                try:
                    x = [float(self.player_coordinates_x2), float(self.player_coordinates_x1)]
                    y = [float(self.player_coordinates_y2), float(self.player_coordinates_y1)]
                    xy = (np.max(x) - np.min(x)) * self.multiplier_location_x
                    yx = (np.max(y) - np.min(y)) * self.multiplier_location_y
                    distance = math.sqrt(math.pow(xy, 2) + math.pow(yx, 2))
                    self.distanceBC = distance
                except Exception as ex:
                    player.error(ex=ex, write="no")

    def cosine_angle(self):
        """Нахождение косинуса угла"""
        if player.one_class == 0:
            try:
                x1 = float(self.player_coordinates_x1) * float(self.multiplier_location_x) - float(self.player_coordinates_x0)\
                     * float(self.multiplier_location_x)
                y1 = float(self.player_coordinates_y1) * float(self.multiplier_location_y) - float(self.player_coordinates_y0)\
                     * float(self.multiplier_location_y)
                x2 = float(self.player_coordinates_x2) * float(self.multiplier_location_x) - float(self.player_coordinates_x0)\
                     * float(self.multiplier_location_x)
                y2 = float(self.player_coordinates_y2) * float(self.multiplier_location_y) - float(self.player_coordinates_y0)\
                     * float(self.multiplier_location_y)
            except Exception as ex:
                player.error(ex=ex, write="no")

            try:
                cosine = (x1 * x2 + y1 * y2) / (
                        math.sqrt(math.pow(x1, 2) + math.pow(y1, 2)) * math.sqrt(math.pow(x2, 2) + math.pow(y2, 2)))
                angle_cosine = (math.degrees(math.acos(cosine)))  # Переводит в градусы
                self.angle_degree = angle_cosine
            except Exception as ex:
                player.error(ex=ex, write="no")
                cosine = 450
                self.angle_degree = cosine

    def exterior_angle(self):
        if player.one_class == 0:
            try:
                cosine_exterior_angle = (math.pow(self.distanceAB, 2) + math.pow(self.distanceBC, 2) - math.pow(
                    self.distanceAC, 2)) / \
                                        (2 * self.distanceAB * self.distanceBC)
                try:
                    cosine_exterior_angle = (math.degrees(math.acos(cosine_exterior_angle)))
                    cosine_exterior_angle = 180 - cosine_exterior_angle
                    self.cosine_exterior_angle = cosine_exterior_angle
                except ValueError as ex:
                    player.error(ex=ex, write="no")

            except ZeroDivisionError as ex:
                player.error(ex=ex, write="no")
                cosine = 450
                self.cosine_exterior_angle = cosine

    def left_or_right(self):
        if player.one_class == 0:
            try:
                player_x0 = float(self.player_coordinates_x0)
                player_y0 = float(self.player_coordinates_y0)
                sight_x1 = float(self.player_coordinates_x1)
                sight_y1 = float(self.player_coordinates_y1)
                target_x2 = float(self.player_coordinates_x2)
                target_y2 = float(self.player_coordinates_y2)
                self.target_sight_x = sight_x1
                self.target_sight_y = sight_y1
                sight_x01 = np.abs(float(player_x0) - float(sight_x1))
                sight_y01 = np.abs(float(player_y0) - float(sight_y1))
                if player_x0 < target_x2 and player_y0 < target_y2:
                    if player_x0 == sight_x1 and player_y0 > sight_y1:
                        self.left_or_right_angle = str('Право')
                    if player_x0 == sight_x1 and player_y0 < sight_y1:
                        self.left_or_right_angle = str('Лево')
                    if player_y0 == sight_y1 and player_x0 > sight_x1:
                        self.left_or_right_angle = str('Лево')
                    if player_y0 == sight_y1 and player_x0 < sight_x1:
                        self.left_or_right_angle = str('Право')
                    if sight_x1 < player_x0 and sight_y1 < player_y0:
                        while self.target_sight_x < target_x2:
                            self.target_sight_x += sight_x01
                            self.target_sight_y += sight_y01
                        if self.target_sight_y < target_y2:
                            self.left_or_right_angle = str('Лево')
                        elif self.target_sight_y > target_y2:
                            self.left_or_right_angle = str('Право')
                            pass
                    if sight_x1 > player_x0 and sight_y1 < player_y0:
                        self.left_or_right_angle = str('Право')
                        pass
                    if sight_x1 < player_x0 and sight_y1 > player_y0:
                        self.left_or_right_angle = str('Лево')
                        pass
                    if sight_x1 > player_x0 and sight_y1 > player_y0:
                        while self.target_sight_x < target_x2:
                            self.target_sight_x += (sight_x1 + sight_x01)
                            self.target_sight_y += (sight_y1 + sight_y01)
                        if self.target_sight_y < target_y2:
                            self.left_or_right_angle = str('Право')
                            pass
                        elif self.target_sight_y > target_y2:
                            self.left_or_right_angle = str('Лево')
                            pass

                if player_x0 > target_x2 and player_y0 < target_y2:
                    if player_x0 == sight_x1 and player_y0 > sight_y1:
                        self.left_or_right_angle = str('Лево')
                    if player_x0 == sight_x1 and player_y0 < sight_y1:
                        self.left_or_right_angle = str('Право')
                    if player_y0 == sight_y1 and player_x0 > sight_x1:
                        self.left_or_right_angle = str('Лево')
                    if player_y0 == sight_y1 and player_x0 < sight_x1:
                        self.left_or_right_angle = str('Право')
                    if sight_x1 < player_x0 and sight_y1 < player_y0:
                        self.left_or_right_angle = str('Лево')
                        pass
                    if sight_x1 > player_x0 and sight_y1 < player_y0:
                        while self.target_sight_x > target_x2:
                            self.target_sight_x -= sight_x01
                            self.target_sight_y += sight_y01
                        if self.target_sight_y < target_y2:
                            self.left_or_right_angle = str('Право')
                            pass
                        elif self.target_sight_y > target_y2:
                            self.left_or_right_angle = str('Лево')
                            pass
                    if sight_x1 < player_x0 and sight_y1 > player_y0:
                        while self.target_sight_x > target_x2:
                            self.target_sight_x -= sight_x01
                            self.target_sight_y += sight_y01
                        if self.target_sight_y < target_y2:
                            self.left_or_right_angle = str('Лево')
                            pass
                        elif self.target_sight_y > target_y2:
                            self.left_or_right_angle = str('Право')
                            pass
                    if sight_x1 > player_x0 and sight_y1 > player_y0:
                        self.left_or_right_angle = str('Право')
                        pass

                if player_x0 < target_x2 and player_y0 > target_y2:
                    if player_x0 == sight_x1 and player_y0 > sight_y1:
                        self.left_or_right_angle = str('Право')
                    if player_x0 == sight_x1 and player_y0 < sight_y1:
                        self.left_or_right_angle = str('Лево')
                    if player_y0 == sight_y1 and player_x0 > sight_x1:
                        self.left_or_right_angle = str('Право')
                    if player_y0 == sight_y1 and player_x0 < sight_x1:
                        self.left_or_right_angle = str('Лево')
                    if sight_x1 < player_x0 and sight_y1 < player_y0:
                        self.left_or_right_angle = str('Право')
                        pass
                    if sight_x1 > player_x0 and sight_y1 < player_y0:
                        while self.target_sight_x < target_x2:
                            self.target_sight_x += sight_x01
                            self.target_sight_y -= sight_y01
                        if self.target_sight_y < target_y2:
                            self.left_or_right_angle = str('Право')
                            pass
                        elif self.target_sight_y > target_y2:
                            self.left_or_right_angle = str('Лево')
                            pass
                    if sight_x1 < player_x0 and sight_y1 > player_y0:
                        while self.target_sight_x < target_x2:
                            self.target_sight_x += sight_x01
                            self.target_sight_y -= sight_y01
                        if self.target_sight_y < target_y2:
                            self.left_or_right_angle = str('Лево')
                            pass
                        elif self.target_sight_y > target_y2:
                            self.left_or_right_angle = str('Право')
                            pass
                    if sight_x1 > player_x0 and sight_y1 > player_y0:
                        self.left_or_right_angle = str('Лево')
                        pass

                if player_x0 > target_x2 and player_y0 > target_y2:
                    if player_x0 == sight_x1 and player_y0 > sight_y1:
                        self.left_or_right_angle = str('Лево')
                    if player_x0 == sight_x1 and player_y0 < sight_y1:
                        self.left_or_right_angle = str('Право')
                    if player_y0 == sight_y1 and player_x0 > sight_x1:
                        self.left_or_right_angle = str('Право')
                    if player_y0 == sight_y1 and player_x0 < sight_x1:
                        self.left_or_right_angle = str('Лево')
                    if sight_x1 < player_x0 and sight_y1 < player_y0:
                        while self.target_sight_x > target_x2:
                            self.target_sight_x -= sight_x01
                            self.target_sight_y -= sight_y01
                        if self.target_sight_y < target_y2:
                            self.left_or_right_angle = str('Лево')
                            pass
                        elif self.target_sight_y > target_y2:
                            self.left_or_right_angle = str('Право')
                            pass
                    if sight_x1 > player_x0 and sight_y1 < player_y0:
                        self.left_or_right_angle = str('Лево')
                        pass
                    if sight_x1 < player_x0 and sight_y1 > player_y0:
                        self.left_or_right_angle = str('Право')
                        pass
                    if sight_x1 > player_x0 and sight_y1 > player_y0:
                        while self.target_sight_x > target_x2:
                            self.target_sight_x -= sight_x01
                            self.target_sight_y -= sight_y01
                        if self.target_sight_y < target_y2:
                            self.left_or_right_angle = str('Право')
                            pass
                        elif self.target_sight_y > target_y2:
                            self.left_or_right_angle = str('Лево')
                            pass

                if player_x0 == target_x2 or player_y0 == target_y2:
                    print("Игрок равен цели по x или y: "), print(player_x0, player_y0, target_x2, target_y2)
                    return 'Привет', float(0), float(0)
                if sight_x01 == 0 or sight_y01 == 0:
                    print('Взгляд игрока равен положению игрока по x или y: '), print(sight_x01, sight_y01, player_x0,
                                                                                      player_y0)
                    return 'Привет', float(0), float(0)
            except Exception as ex:
                player.error(ex=ex, write="no")

    def movement(self):
        if player.one_class == 0:
            note = 'non'
            if self.left_or_right_angle == 'Право':
                note = 'd'
            if self.left_or_right_angle == 'Лево':
                note = 'a'

            rotation_sec = 0.0055555555555556 * self.cosine_exterior_angle

            self.rotation_sec = rotation_sec
            self.note = note

    def move(self, how, distance):
        if player.one_class == 0:
            if self.angle_degree == 450 or self.cosine_exterior_angle == 450:
                pyautogui.keyUp('w')
                pyautogui.keyDown('s')
                time.sleep(2)
                pyautogui.keyUp('s')
                pyautogui.keyDown('a')
                time.sleep(0.9)
                pyautogui.keyUp('a')
                pyautogui.keyDown('w')
                pass

            elif self.distanceAC <= 50:
                if player.one_class == 0:
                    keyboard.release('w')
                    player.pytesseract_player_xy0(how=0)
                    player.distance_to_target(how=0)
                    keyboard.press(f'{self.note}')
                    time.sleep(float(self.rotation_sec))
                    keyboard.release(f'{self.note}')
                    tt = 0.0344827 * self.distanceAC
                    keyboard.press("w")
                    time.sleep(float(tt))
                    keyboard.release("w")
                    player.pytesseract_player_xy0(how=0)
                    player.distance_to_target(how=0)

                    if self.distanceAC < distance:
                        if player.one_class == 0:
                            if how == 1:
                                print(f"Расстояние до цели: {self.distanceAC}")
                                monitor.boarding_protocol(tactic="Not")
                                player.yard_5()
                            if how == 2:
                                print(f"Расстояние до цели: {self.distanceAC}")
                                monitor.find_res_on_screen(1, 960, 560, 10)
                                if monitor.tru_or_false:
                                    monitor.boarding_protocol(tactic="collection")
                                    player.yard_50()
                                player.yard_50()
                            if how == 3:
                                print(f"Расстояние до цели: {self.distanceAC}")
                                monitor.boarding_protocol(tactic="Not")
                                player.yard_50()

            elif self.distanceAC > 50:
                if player.one_class == 0:
                    keyboard.press(f'{self.note}')
                    time.sleep(float(self.rotation_sec))
                    keyboard.release(f'{self.note}')
                    pass

    def yard_5(self):
        if player.one_class == 0:
            player.find_res_minimap = None
            self.need_check_minimap = 0
            player.list_coordinates = list(player.list_coordinates)
            index = (player.list_coordinates.index(
                str(player.player_coordinates_x2) + " " + str(player.player_coordinates_y2))) + 1
            try:
                self.player_coordinates_x2, self.player_coordinates_y2 = self.pytesseract_player_target(
                    self.list_coordinates, num=index)
            except IndexError as ex:
                self.player_coordinates_x2, self.player_coordinates_y2 = self.pytesseract_player_target(
                    self.list_coordinates, num=0)
                player.error(ex=ex, write="no")

                self.elusive_rich_elethium_deposit = copy.copy(self.original_elusive_rich_elethium_deposit)
                self.rich_elethium_deposit = copy.copy(self.original_rich_elethium_deposit)
                self.elethium_deposit = copy.copy(self.original_elethium_deposit)

                self.elusive_rich_progenium_deposit = copy.copy(self.original_elusive_rich_progenium_deposit)
                self.elusive_progenium_deposit = copy.copy(self.original_elusive_progenium_deposit)
                self.rich_progenium_deposit = copy.copy(self.original_rich_progenium_deposit)
                self.progenium_deposit = copy.copy(self.original_progenium_deposit)


                self.forgotten_treasure_vault = copy.copy(self.original_forgotten_treasure_vault)
                self.discarded_automa_scrap = copy.copy(self.original_discarded_automa_scrap)
                self.cypher_bound_chest = copy.copy(self.original_cypher_bound_chest)
                self.tarachnid_eggs = copy.copy(self.original_tarachnid_eggs)
                self.avian_nest = copy.copy(self.original_avian_nest)
                self.mawsworn_supply_chest = copy.copy(self.original_mawsworn_supply_chest)
                print(f"Все координаты сброшены . . .")

    def yard_50(self):
        if player.one_class == 0:
            player.find_res_minimap = None
            self.need_check_minimap = 0
            player.near_res_50 = list(self.near_res_50)

            try:
                index = (player.near_res_50.index(
                    player.str_magik(player.player_coordinates_x2) + " " + player.str_magik(
                        player.player_coordinates_y2))) + 1
                self.player_coordinates_x2, self.player_coordinates_y2 = self.pytesseract_player_target(
                    self.near_res_50, num=index)
                print(f"Следующая координата руды: {self.player_coordinates_x2, self.player_coordinates_y2}")
            except IndexError as ex:
                player.error(ex=ex, write="no")
                self.two_class = 1

    @staticmethod
    def for_check_coordinates_res():
        player.pytesseract_player_xy0(how=0)
        monitor.check_minimap()
        player.distance_near(print_me="yes")

    def distance_near(self, print_me="no"):
        if player.one_class == 0:
            find_name=[]
            for item in monitor.all_info:
                if 'ERPD' in item: find_name.append('ERPD')
                if 'EPD' in item: find_name.append('EPD')
                if 'RPD' in item: find_name.append('RPD')
                if 'PD' in item: find_name.append('PD')
                if 'ERED' in item: find_name.append('ERED')
                if 'RED' in item: find_name.append('RED')
                if 'ED' in item: find_name.append('ED')
                if 'FTV' in item: find_name.append('FTV')
                if 'DAS' in item: find_name.append('DAS')
                if 'CBC' in item: find_name.append('CBC')
                if 'TE' in item: find_name.append('TE')
                if 'AN' in item: find_name.append('AN')
                if 'MSC' in item: find_name.append('MSC')
            list_name = set(find_name)

            elusive_rich_progenium_deposit_temporary_list = []
            elusive_progenium_deposit_temporary_list = []
            rich_progenium_deposit_temporary_list = []
            progenium_deposit_temporary_list = []

            elusive_rich_elethium_deposit_temporary_list = []
            rich_elethium_deposit_temporary_list = []
            elethium_deposit_temporary_list = []
            forgotten_treasure_vault_list = []
            discarded_automa_scrap_list = []
            cypher_bound_chest_list = []
            tarachnid_eggs_list = []
            avian_nest_list = []
            mawsworn_supply_chest = []

            def distance_for_res(list_coordinates, name):
                cup_square = []
                cup_coordinates = []
                pix_coordinates = []
                for item_0 in monitor.all_info:
                    if name in item_0:
                        cup_square.append(item_0[2])
                        pix_coordinates.append((item_0[0][0], item_0[0][1]))
                for item_1 in list_coordinates:
                    item_x = item_1[:5]
                    item_y = item_1[6:]
                    try:
                        x = [float(item_x), float(player.player_coordinates_x0)]
                        y = [float(item_y), float(player.player_coordinates_y0)]
                        xy = (np.max(x) - np.min(x)) * player.multiplier_location_x
                        yx = (np.max(y) - np.min(y)) * player.multiplier_location_y
                        distance = math.sqrt(math.pow(xy, 2) + math.pow(yx, 2))
                    except Exception as e:
                        player.error(ex=e, write="no")
                        distance = 1000

                    if distance <= self.distance_for_check_res_on_the_map: # Варианаты радиуса: 60, 90, 120, 150, 180, 210
                        cup_coordinates.append(list_coordinates[list_coordinates.index(item_1)])
                print(f"Координаты меньше 210м: {cup_coordinates}")

                copy_player_coordinates_x0 = float(player.player_coordinates_x0)
                copy_player_coordinates_y0 = float(player.player_coordinates_y0)

                "Расчет координат ресурса, найденного на миникарте"
                testic = []
                for item_dot in pix_coordinates:
                    res_pix_x = item_dot[0]
                    res_pix_y = item_dot[1]
                    player_pix_x = user["map_center"][0]
                    player_pix_y = user["map_center"][1]
                    where_x, where_y = abs(player_pix_x - res_pix_x), abs(player_pix_y - res_pix_y)
                    where_x, where_y = where_x * (self.distance_for_check_res_in_yard / 120), where_y * (self.distance_for_check_res_in_yard / 110)
                    where_x, where_y = where_x / player.multiplier_location_x, where_y / player.multiplier_location_y
                    testic.append([where_x, where_y])
                "Расчет координат ресурса, найденного на миникарте"
                if print_me == "yes":
                    print(f"Абсолютное смещение по X, Y: {testic}")

                delete_list = []
                number_circle = 0
                for coordinates in cup_coordinates:
                    coordinates_x, coordinates_y = coordinates[:5], coordinates[6:]
                    if coordinates_x <= player.player_coordinates_x0 and coordinates_y <= player.player_coordinates_y0: square = 1
                    elif coordinates_x > player.player_coordinates_x0 and coordinates_y < player.player_coordinates_y0: square = 2
                    elif coordinates_x < player.player_coordinates_x0 and coordinates_y > player.player_coordinates_y0: square = 3
                    elif coordinates_x > player.player_coordinates_x0 and coordinates_y > player.player_coordinates_y0: square = 4
                    else: square = 0

                    non = 0
                    if print_me == "yes":
                        print(f"Предполагаемая координата: {coordinates_x, coordinates_y}")
                        print(f"Список секторов: {cup_square}")
                        print(f"Сектор координаты: {square}")

                    if square in cup_square:
                        pass

                        for item_dot2 in testic:
                            where_x = item_dot2[0]
                            where_y = item_dot2[1]

                            if square == 1:
                                where_x, where_y = copy_player_coordinates_x0 - abs(where_x), copy_player_coordinates_y0 - abs(where_y)
                                if print_me == "yes":
                                    print(f"{name}: X от {where_x - self.scatter} до {where_x + self.scatter}, Y от {where_y - self.scatter} до {where_y + self.scatter}")

                            if square == 2:
                                where_x, where_y = copy_player_coordinates_x0 + abs(where_x), copy_player_coordinates_y0 - abs(where_y)
                                if print_me == "yes":
                                    print(f"{name}: X от {where_x - self.scatter} до {where_x + self.scatter}, Y от {where_y - self.scatter} до {where_y + self.scatter}")

                            if square == 3:
                                where_x, where_y = copy_player_coordinates_x0 - abs(where_x), copy_player_coordinates_y0 + abs(where_y)
                                if print_me == "yes":
                                    print(f"{name}: X от {where_x - self.scatter} до {where_x + self.scatter}, Y от {where_y - self.scatter} до {where_y + self.scatter}")

                            if square == 4:
                                where_x, where_y = copy_player_coordinates_x0 + abs(where_x), copy_player_coordinates_y0 + abs(where_y)
                                if print_me == "yes":
                                    print(f"{name}: X от {where_x - self.scatter} до {where_x + self.scatter}, Y от {where_y - self.scatter} до {where_y + self.scatter}")

                            coordinates_x, coordinates_y = float(coordinates_x), float(coordinates_y)
                            if (coordinates_x < (where_x + self.scatter) and (coordinates_x > where_x - self.scatter)
                                    and coordinates_y < (where_y + self.scatter) and coordinates_y > (where_y - self.scatter)):
                                if print_me == "yes":
                                    print(f"Ресурсы в указанной квадрате НАЙДЕН: {coordinates_x, coordinates_y}")
                                pass
                            else:
                                if print_me == "yes":
                                    print(f"Коррдината не подходит: {coordinates_x, coordinates_y}")
                                non += 1

                        if non == 0:
                            pass
                        if non > 0:
                            delete_list.append(number_circle)

                    else:
                        delete_list.append(number_circle)
                    if print_me == "yes":
                        print("\n")
                    number_circle += 1

                delete_list = sorted(delete_list, reverse=True)
                for del_coord in delete_list:
                    del cup_coordinates[del_coord]

                if name == "ERPD":
                    elusive_rich_progenium_deposit_temporary_list.append(cup_coordinates)
                    for item_del in cup_coordinates:
                        was = len(self.elusive_rich_progenium_deposit)
                        del self.elusive_rich_progenium_deposit[self.elusive_rich_progenium_deposit.index(item_del)]
                        print(f"ERPD was: {was} >>> became: {len(self.elusive_rich_progenium_deposit)}")
                if name == "EPD":
                    elusive_progenium_deposit_temporary_list.append(cup_coordinates)
                    for item_del in cup_coordinates:
                        was = len(self.elusive_progenium_deposit)
                        del self.elusive_progenium_deposit[self.elusive_progenium_deposit.index(item_del)]
                        print(f"EPD was: {was} >>> became: {len(self.elusive_progenium_deposit)}")
                if name == "RPD":
                    rich_progenium_deposit_temporary_list.append(cup_coordinates)
                    for item_del in cup_coordinates:
                        was = len(self.rich_progenium_deposit)
                        del self.rich_progenium_deposit[self.rich_progenium_deposit.index(item_del)]
                        print(f"RPD was: {was} >>> became: {len(self.rich_progenium_deposit)}")
                if name == "PD":
                    progenium_deposit_temporary_list.append(cup_coordinates)
                    for item_del in cup_coordinates:
                        was = len(self.progenium_deposit)
                        del self.progenium_deposit[self.progenium_deposit.index(item_del)]
                        print(f"PD was: {was} >>> became: {len(self.progenium_deposit)}")
                if name == "ERED":
                    elusive_rich_elethium_deposit_temporary_list.append(cup_coordinates)
                    for item_del in cup_coordinates:
                        was = len(self.elusive_rich_elethium_deposit)
                        del self.elusive_rich_elethium_deposit[self.elusive_rich_elethium_deposit.index(item_del)]
                        print(f"ERED was: {was} >>> became: {len(self.elusive_rich_elethium_deposit)}")
                if name == "RED":
                    rich_elethium_deposit_temporary_list.append(cup_coordinates)
                    for item_del in cup_coordinates:
                        was = len(self.rich_elethium_deposit)
                        del self.rich_elethium_deposit[self.rich_elethium_deposit.index(item_del)]
                        print(f"RED was: {was} >>> became: {len(self.rich_elethium_deposit)}")
                if name == "ED":
                    elethium_deposit_temporary_list.append(cup_coordinates)
                    for item_del in cup_coordinates:
                        was = len(self.elethium_deposit)
                        del self.elethium_deposit[self.elethium_deposit.index(item_del)]
                        print(f"ED: was: {was} >>> became: {len(self.elethium_deposit)}")
                if name == "FTV":
                    forgotten_treasure_vault_list.append(cup_coordinates)
                    for item_del in cup_coordinates:
                        was = len(self.forgotten_treasure_vault)
                        del self.forgotten_treasure_vault[self.forgotten_treasure_vault.index(item_del)]
                        print(f"FTV: was: {was} >>> became: {len(self.forgotten_treasure_vault)}")
                if name == "DAS":
                    discarded_automa_scrap_list.append(cup_coordinates)
                    for item_del in cup_coordinates:
                        was = len(self.discarded_automa_scrap)
                        del self.discarded_automa_scrap[self.discarded_automa_scrap.index(item_del)]
                        print(f"DAS: was: {was} >>> became: {len(self.discarded_automa_scrap)}")
                if name == "CBC":
                    cypher_bound_chest_list.append(cup_coordinates)
                    for item_del in cup_coordinates:
                        was = len(self.cypher_bound_chest)
                        del self.cypher_bound_chest[self.cypher_bound_chest.index(item_del)]
                        print(f"CBC: was: {was} >>> became: {len(self.cypher_bound_chest)}")
                if name == "TE":
                    tarachnid_eggs_list.append(cup_coordinates)
                    for item_del in cup_coordinates:
                        was = len(self.tarachnid_eggs)
                        del self.tarachnid_eggs[self.tarachnid_eggs.index(item_del)]
                        print(f"TE: was: {was} >>> became: {len(self.tarachnid_eggs)}")
                if name == "AN":
                    avian_nest_list.append(cup_coordinates)
                    for item_del in cup_coordinates:
                        was = len(self.avian_nest)
                        del self.avian_nest[self.avian_nest.index(item_del)]
                        print(f"AN: was: {was} >>> became: {len(self.avian_nest)}")
                if name == "MSC":
                    mawsworn_supply_chest.append(cup_coordinates)
                    for item_del in cup_coordinates:
                        was = len(self.mawsworn_supply_chest)
                        del self.mawsworn_supply_chest[self.mawsworn_supply_chest.index(item_del)]
                        print(f"MSC: was: {was} >>> became: {len(self.mawsworn_supply_chest)}")

            print(f"Лист имен: {list_name}")

            if "ERPD" in list_name: distance_for_res(self.elusive_rich_progenium_deposit, "ERPD")
            if "EPD" in list_name: distance_for_res(self.elusive_progenium_deposit, "EPD")
            if "RPD" in list_name: distance_for_res(self.rich_progenium_deposit, "RPD")
            if "PD" in list_name: distance_for_res(self.progenium_deposit, "PD")
            if "ERED" in list_name: distance_for_res(self.elusive_rich_elethium_deposit, "ERED")
            if "RED" in list_name: distance_for_res(self.rich_elethium_deposit, "RED")
            if "ED" in list_name: distance_for_res(self.elethium_deposit, "ED")
            if "FTV" in list_name: distance_for_res(self.forgotten_treasure_vault, "FTV")
            if "DAS" in list_name: distance_for_res(self.discarded_automa_scrap, "DAS")
            if "CBC" in list_name: distance_for_res(self.cypher_bound_chest, "CBC")
            if "TE" in list_name: distance_for_res(self.tarachnid_eggs, "TE")
            if "AN" in list_name: distance_for_res(self.avian_nest, "AN")
            if "MSC" in list_name: distance_for_res(self.mawsworn_supply_chest, "MSC")

            print(f"ПОЛОЖЕНИЕ ИГРОКА::: {player.player_coordinates_x0, player.player_coordinates_y0}")

            if len(elusive_rich_progenium_deposit_temporary_list) > 0: print(f"Лист координат после проверки на 210 м << ERPD >>  {elusive_rich_progenium_deposit_temporary_list}")
            if len(elusive_progenium_deposit_temporary_list) > 0: print(f"Лист координат после проверки на 210 м << EPD >>  {elusive_progenium_deposit_temporary_list}")
            if len(rich_progenium_deposit_temporary_list) > 0: print(f"Лист координат после проверки на 210 м << RPD >>  {rich_progenium_deposit_temporary_list}")
            if len(progenium_deposit_temporary_list) > 0: print(f"Лист координат после проверки на 210 м << PD >>  {progenium_deposit_temporary_list}")
            if len(elusive_rich_elethium_deposit_temporary_list) > 0: print(f"Лист координат после проверки на 210 м << ERED >>  {elusive_rich_elethium_deposit_temporary_list}")
            if len(rich_elethium_deposit_temporary_list) > 0:print(f"Лист координат после проверки на 210 м << RED >>  {rich_elethium_deposit_temporary_list}")
            if len(elethium_deposit_temporary_list) > 0:print(f"Лист координат после проверки на 210 м << ED >>  {elethium_deposit_temporary_list}")
            if len(forgotten_treasure_vault_list) > 0:print(f"Лист координат после проверки на 210 м << FTV >>  {forgotten_treasure_vault_list}")
            if len(discarded_automa_scrap_list) > 0:print(f"Лист координат после проверки на 210 м << DAS >>  {discarded_automa_scrap_list}")
            if len(cypher_bound_chest_list) > 0:print(f"Лист координат после проверки на 210 м << CBC >>  {cypher_bound_chest_list}")
            if len(tarachnid_eggs_list) > 0:print(f"Лист координат после проверки на 210 м << TE >>  {tarachnid_eggs_list}")
            if len(avian_nest_list) > 0:print(f"Лист координат после проверки на 210 м << AN >>  {avian_nest_list}")
            if len(mawsworn_supply_chest) > 0:print(f"Лист координат после проверки на 210 м << MSC >>  {mawsworn_supply_chest}")

            try:
                self.near_res_50 = []
                self.near_res_50 = list(np.hstack(elusive_rich_elethium_deposit_temporary_list + rich_elethium_deposit_temporary_list +
                elethium_deposit_temporary_list + forgotten_treasure_vault_list + discarded_automa_scrap_list +
                cypher_bound_chest_list + tarachnid_eggs_list + avian_nest_list + mawsworn_supply_chest + elusive_rich_progenium_deposit_temporary_list
                + elusive_progenium_deposit_temporary_list + rich_progenium_deposit_temporary_list + progenium_deposit_temporary_list))
                self.player_coordinates_x2, self.player_coordinates_y2 = player.pytesseract_player_target(self.near_res_50, 0)
                print(f"Все ресурсы в радиусе 210 м: {self.near_res_50}, длина: {len(self.near_res_50)}")
                print(f"Первые координаты из 210 м: {self.player_coordinates_x2}, {self.player_coordinates_y2}")
            except Exception as ex:
                self.near_res_50 = []
                print(f"Нет координат в радиусе 210 м: {ex}")

    def reconnect(self):
        keyboard.release("w")
        keyboard.release("s")
        keyboard.release("a")
        keyboard.release("d")
        keyboard.release("space")
        keyboard.release("x")
        time.sleep(1)
        os.system("TASKKILL /F /IM Wow.exe")
        time.sleep(10)
        os.startfile(str(user["way"]))
        disconnect = monitor.construct_gui(time_active=60, img=monitor.disconnect,
                                           similarity=0.8, offset_x=0, offset_y=0,
                                           region=(1700, 990, 200, 60), grayscale=False)
        time.sleep(1)
        keyboard.write(str(user["password"]), random.uniform(0.1, 0.2))
        keyboard.send("ENTER")
        enter_world = monitor.construct_gui(time_active=60, img=monitor.enter_world,
                                            similarity=0.8, offset_x=0, offset_y=0,
                                            region=(800, 950, 300, 75), grayscale=False)
        time.sleep(1)
        keyboard.send("ENTER")

        check_enter_world = monitor.construct_gui(time_active=60, img=monitor.check_enter_world,
                                                  similarity=0.8, offset_x=0, offset_y=0,
                                                  region=(690, 800, 70, 66), grayscale=False)
        keyboard.send("k")
        time.sleep(1.5)
        keyboard.send("k")
        keyboard.press("space")
        time.sleep(15)
        keyboard.release("space")
        normal = "non"
        m = mss()
        grab = m.grab({"left": user["hp_position"][0], "top": user["hp_position"][1], "width": 1, "height": 1})
        full_screen_array = np.array(grab)
        hp = (full_screen_array == (user["hp_color"][0], user["hp_color"][1], user["hp_color"][2], 255))
        if False in hp: normal = "not_normal"

        if normal != "not_normal":
            pyautogui.moveTo(725, 834)
            time.sleep(2)
            keyboard.send("0")
            start()
            player.one_class = 1
            player.two_class = 1
        keyboard.send("0")

    def reset(self):
        keyboard.release("w")
        keyboard.release("s")
        keyboard.release("a")
        keyboard.release("d")
        keyboard.release("space")
        keyboard.release("x")
        keyboard.send("0")
        time.sleep(1)

        position = monitor.mouse("moveTo", xy=monitor.construct_gui(time_active=10, img=monitor.dead_v3, similarity=0.7, offset_x=0, offset_y=0, region=(840, 100, 120, 240), grayscale=False))
        try:
            pyautogui.click(position[1], position[2])
        except: pass

        time.sleep(5)

        keyboard.press("w")
        time.sleep(0.4)
        keyboard.release("w")
        time.sleep(1)

        monitor.find_res_on_screen(2, circle=5, for_minimap=3)
        time.sleep(1)

        for x in range(2):
            position2 = monitor.mouse("moveTo", xy=monitor.construct_gui(time_active=10, img=monitor.dead_v4, similarity=0.7, offset_x=0, offset_y=0, region=(840, 100, 120, 240), grayscale=False))
            try:
                pyautogui.click(position2[1], position2[2])
            except: pass

            pyautogui.click()
            time.sleep(2)

        keyboard.press("s")
        time.sleep(1.5)
        keyboard.release("s")
        time.sleep(1)

        keyboard.send("j")
        time.sleep(2)
        pyautogui.moveTo(939, 570)
        pyautogui.click()
        time.sleep(2)

        pyautogui.moveTo(725, 834)
        pyautogui.click()
        time.sleep(2)

        monitor.form_sov(1)

        keyboard.press("space")
        time.sleep(15)
        keyboard.release("space")

        start()
        player.one_class = 1
        player.two_class = 1

class Monitor:

    def __init__(self):
        self.num_cycle = 0
        self.was_game = 0

        self.open_box = False

        self.massive_acc = []
        self.massive_json = None
        self.login_now = ""
        self.password_now = ""

        self.screen = 0
        self.screen_mask = None

        self.start_x = 0
        self.start_y = 0

        self.back = 0
        self.cycle = 0
        self.tru_or_false = None
        self.res = 0

        self.screen_v1 = None
        self.screen_v2 = None
        self.screen_v3 = None
        self.screen_v4 = None
        self.screen_v5 = None
        self.screen_v6 = None
        self.screen_v7 = None
        self.screen_v8 = None
        self.screen_v9 = None
        self.screen_v10 = None
        self.screen_v11 = None
        self.screen_v12 = None
        self.screen_v13 = None
        self.screen_v14 = None
        self.screen_v15 = None
        self.screen_v16 = None
        self.e_r_elethium_deposit = None
        self.r_elethium_deposit = None
        self.elethium_deposit = None

        self.e_r_progenium_deposit = None
        self.e_progenium_deposit = None
        self.r_progenium_deposit = None
        self.progenium_deposit = None

        self.forgotten_treasure_vault = None
        self.discarded_automa_scrap = None
        self.cypher_bound_chest = None
        self.tarachnid_eggs = None
        self.avian_nest = None
        self.mawsworn_supply_chest = None

        self.screen_v18 = None
        self.screen_v19 = None
        self.screen_v20 = None
        self.disconnect = None

        self.dead_v1 = None
        self.dead_v2 = None
        self.dead_v3 = None
        self.dead_v4 = None

        self.pocopoc_buff_v1 = None
        self.pocopoc_buff_v2 = None
        self.check_pocopoc = None

        self.enter_world = None
        self.check_enter_world = None

        self.all_info = []
        print(f"Инициализация класса: успех...")

    def __str__(self):
        print("Class:Monitor")

    def creation_img(self):
        self.screen_v1 = monitor.load_img("Masha/1.png", "BGR")
        self.screen_v2 = monitor.load_img("Masha/2.png", "BGR")
        self.screen_v3 = monitor.load_img("Masha/3.png", "BGR")
        self.screen_v4 = monitor.load_img("Masha/4.png", "BGR")
        self.screen_v5 = monitor.load_img("Masha/test2.png", "BGR")
        self.screen_v6 = monitor.load_img("Masha/6.png", "BGR")
        self.screen_v7 = monitor.load_img("Masha/7.png", "BGR")
        self.screen_v8 = monitor.load_img("Masha/8.png", "BGR")
        self.screen_v9 = monitor.load_img("Masha/9.png", "BGR")
        self.screen_v10 = monitor.load_img("Masha/10.png", "BGR")
        self.screen_v11 = monitor.load_img("Masha/11.png", "BGR")
        self.screen_v12 = monitor.load_img("Masha/12.png", "BGR")
        self.screen_v13 = monitor.load_img("Masha/13.png", "BGR")
        self.screen_v14 = monitor.load_img("Masha/14.png", "BGR")
        self.screen_v15 = monitor.load_img("Masha/15.png", "BGR")
        self.screen_v16 = monitor.load_img("Masha/16.png", "BGR")

        self.e_r_elethium_deposit = monitor.load_img("Masha/Elusive_Rich_Elethium_Deposit.png", "BGR")
        self.r_elethium_deposit = monitor.load_img("Masha/Rich_Elethium_Deposit.png", "BGR")
        self.elethium_deposit = monitor.load_img("Masha/Elethium_Deposit.png", "BGR")

        self.e_r_progenium_deposit = monitor.load_img("Masha/Elusive_Rich_Progenium_Deposit.png", "BGR")
        self.e_progenium_deposit = monitor.load_img("Masha/Elusive_Progenium_Deposit.png", "BGR")
        self.r_progenium_deposit = monitor.load_img("Masha/Rich_Progenium_Deposit.png", "BGR")
        self.progenium_deposit = monitor.load_img("Masha/Progenium_Deposit.png", "BGR")

        self.forgotten_treasure_vault = monitor.load_img("Masha/forgotten_treasure_vault.png", "BGR")
        self.discarded_automa_scrap = monitor.load_img("Masha/discarded_automa_scrap.png", "BGR")
        self.cypher_bound_chest = monitor.load_img("Masha/cypher_bound_chest.png", "BGR")
        self.tarachnid_eggs = monitor.load_img("Masha/tarachnid_eggs.png", "BGR")
        self.avian_nest = monitor.load_img("Masha/avian_nest.png", "BGR")
        self.mawsworn_supply_chest = monitor.load_img("Masha/mawsworn_supply_chest.png", "BGR")

        self.screen_v18 = monitor.load_img("Masha/form.png", "BGR")
        self.screen_v19 = monitor.load_img("Masha/convoke.png", "BGR")
        self.screen_v20 = monitor.load_img("Masha/celestial.png", "BGR")

        self.disconnect = monitor.load_img("Masha/disconnect.png", "BGR")

        self.dead_v1 = monitor.load_img("Masha/dead_1.png", "BGR")
        self.dead_v2 = monitor.load_img("Masha/dead_2.png", "BGR")
        self.dead_v3 = monitor.load_img("Masha/dead_3.png", "BGR")
        self.dead_v4 = monitor.load_img("Masha/dead_4.png", "BGR")

        self.pocopoc_buff_v1 = monitor.load_img("Masha/pocopoc_buff_1.png", "BGR")
        self.pocopoc_buff_v2 = monitor.load_img("Masha/pocopoc_buff_2.png", "BGR")
        self.check_pocopoc = monitor.load_img("Masha/check_pocopoc.png", "BGR")

        self.enter_world = monitor.load_img("Masha/enter_world.png", "BGR")
        self.check_enter_world = monitor.load_img("Masha/check_enter_world.png", "BGR")

    @staticmethod
    def load_img(name, color):
        item = cv2.imread(str(name))
        item = monitor.convector(item, color)
        item = np.array(item)
        print(f"Загружено изображение: {name}")
        return item

    @staticmethod
    def convector(massive, color):
        if color == "RGB":
            item = cv2.cvtColor(massive, cv2.COLOR_RGBA2BGR)
            return item

        if color == "BGR":
            item = cv2.cvtColor(massive, cv2.COLOR_RGBA2RGB)
            return item

        if color == "RGB_A":
            item = cv2.cvtColor(massive, cv2.COLOR_RGB2RGBA)
            return item

        if color == "HSV":
            item = cv2.cvtColor(massive, cv2.COLOR_BGR2HSV)
            return item

    def screen_monitor(self, x1, y1, x2, y2, mode="BGR"):
        """Скрин центральной части экрана, перевод RGB в BGR, создание массива"""
        monitor_window = {
            'left': x1,
            'top': y1,
            'width': x2,
            'height': y2,
        }
        m = mss()
        img = m.grab(monitor_window)

        self.screen = np.array(img)
        self.screen = monitor.convector(self.screen, color=mode)
        return self.screen

    @staticmethod
    def check_height():
        time0 = time.time()
        result = None
        keyboard.press("x")
        while result is not True:
            screen_1 = monitor.screen_monitor(590, 975, 40, 95)
            time.sleep(1)
            result = monitor.mouse("find", xy=monitor.construct_gui(time_active=0.01, img=screen_1,
                                                                               similarity=0.95, offset_x=0, offset_y=0,
                                                                               region=(580, 965, 60, 115),
                                                                               grayscale=False))
            time1 = time.time() - time0
            print(time1)
            if time1 > 8:
                print("Принудительно останавливаю спуск")
                keyboard.release("x")
                with open("Error.txt", "a", encoding="utf-8") as error:
                    error.write(f"{datetime.datetime.now().strftime(' %H: %M: %S')} >>> Принудительная остановка спуска" + "\n")
                return 5


            if result is None:
                print("Спускаюсь...")
                pass
            if result:
                print("Опустились")
                keyboard.release("x")
                if time1 <= 5: return time1
                else: return 5

    def form_sov(self, how):
        if how == 1:
            form = monitor.construct_gui(time_active=0.01, img=monitor.screen_v18, similarity=0.8, offset_x=0, offset_y=0, region=(930, 700, 60, 50), grayscale=False)
            if form is None:
                while form is None:
                    keyboard.send("k")
                    time.sleep(0.5)
                    combat.check_combat()
                    combat.telegram()
                    form = monitor.construct_gui(time_active=0.01, img=monitor.screen_v18, similarity=0.8, offset_x=0, offset_y=0, region=(930, 700, 60, 50), grayscale=False)

        if how == 2:
            form = monitor.construct_gui(time_active=0.01, img=monitor.screen_v18, similarity=0.8, offset_x=0, offset_y=0, region=(930, 700, 60, 50), grayscale=False)
            if form is None:
                m = mss()
                grab = m.grab(
                    {"left": user["combat_position"][0], "top": user["combat_position"][1], "width": 1, "height": 1})
                grab = np.array(grab)[0][0]
                if grab[0] == user["combat_color"][0] and grab[1] == user["combat_color"][1] and grab[2] == user["combat_color"][2]:  combat_bird = True
                else: combat_bird = False
                if combat_bird is False:
                    keyboard.send("k")
                    time.sleep(0.5)
                    combat.telegram()
                    #form = monitor.construct_gui(time_active=0.01, img=monitor.screen_v18, similarity=0.8, offset_x=0, offset_y=0, region=(930, 700, 60, 50), grayscale=False)
                    keyboard.press("space")
                    time.sleep(5)
                    keyboard.release("space")

    def find_load_img(self, img, similarity, x_offset, y_offset):
        """Поиск необходимого изображения на экране"""

        try:
            res = cv2.matchTemplate(self.screen_mask, img, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= similarity)
            xy = loc[1][0] + x_offset, loc[0][0] + y_offset
            return xy
        except Exception as ex:
            pass
            return None

    @staticmethod
    def construct_cv2(time_active, img, similarity, offset_x=0, offset_y=0, region=(0, 0, 1920, 1080)):
        """Объединяет функцию захвата изображения и поиска необходимого на нем"""
        time0 = time_active
        result = None
        while result is None and time0 > 0:
            time1 = time.time()

            monitor.screen_monitor(monitor.start_x + region[0], monitor.start_y + region[1], region[2], region[3])

            if type(img) is tuple:
                for item in img:
                    result = monitor.find_load_img(item, similarity, x_offset=offset_x, y_offset=offset_y)
                    if result is not None:
                        break
            else:
                result = monitor.find_load_img(img, similarity, x_offset=offset_x, y_offset=offset_y)
            time2 = time.time()
            time3 = time2 - time1
            time0 -= time3
        return result

    def mask(self,img):
        """
        Формирует маску определенного цвета и возвращает лишь цвет макси
        """
        low = np.array((0, 175, 204), np.uint8)
        upper = np.array((23, 230, 255), np.uint8)
        mask = cv2.inRange(img, low, upper)
        self.screen_mask = cv2.bitwise_and(img, img, mask=mask)

    @staticmethod
    def construct_gui(time_active, img, similarity=0.7, offset_x=0, offset_y=0, region=(0, 0, 1920, 1080),
                      grayscale=False, need_gui="no"):
        time0 = time_active
        result = None
        while result is None and time0 > 0:
            time1 = time.time()
            all_find_img = []
            num_circle = 0
            if type(img) is tuple:
                for item in img:
                    result = pyautogui.locateCenterOnScreen(item, region=(
                    monitor.start_x + region[0], monitor.start_y + region[1], region[2], region[3]),
                                                            grayscale=grayscale, confidence=similarity)
                    if result is not None:
                        if need_gui == "yes":
                            if num_circle < 7:
                                rectangles = [int(result[0]), int(result[1]), "dot"]
                            elif num_circle >= 7:
                                rectangles = [int(result[0]), int(result[1]), "box"]
                            all_find_img.append(rectangles)
                        else:
                            break
                    num_circle += 1
            else:
                result = pyautogui.locateCenterOnScreen(img, region=(
                monitor.start_x + region[0], monitor.start_y + region[1], region[2], region[3]), grayscale=grayscale,
                                                        confidence=similarity)
            time2 = time.time()
            time3 = time2 - time1
            time0 -= time3

        if need_gui == "yes":
            if len(all_find_img) > 1:
                return all_find_img
            else:
                return all_find_img
        else:
            return result

    def mouse(self, command, xy=(0, 0), xy2=(0, 0)):
        """Производит клик по координатам, если найдено изображение"""
        if xy:
            x, y = self.start_x + xy[0], self.start_y + xy[1]
            if command == "moveTo":
                pyautogui.moveTo(x, y, 0)
                return True, x, y

            if command == "move":
                pyautogui.moveTo(x, y)
                return True, x, y

            if command == "click":
                pyautogui.click(x, y)
                return True, x, y

            if command == "dragTo":
                pyautogui.dragTo(xy[0], xy[1], button='left')
                pyautogui.dragTo(xy2[0], xy2[1], 2, button='left')
                return True, x, y

            if command == "drag":
                pyautogui.dragTo(xy[0], xy[1], 2, button='left')
                return True, x, y

            if command == "scroll":
                pyautogui.scroll(-1000)
                return True, x, y

            if command == "find":
                return True, x, y
        else:
            self.back = 1000
            return None

    def check_minimap(self):
        if player.one_class == 0:
            all_find = []
            name_res_massive = []
            square = []
            self.all_info =[]
            def find_square(coordinates_xy):
                coordinates = coordinates_xy
                if coordinates[0] <= user["map_center"][0] and coordinates[1] <= user["map_center"][1]: square.append(1)
                if coordinates[0] > user["map_center"][0] and coordinates[1] < user["map_center"][1]: square.append(2)
                if coordinates[0] < user["map_center"][0] and coordinates[1] > user["map_center"][1]: square.append(3)
                if coordinates[0] > user["map_center"][0] and coordinates[1] > user["map_center"][1]: square.append(4)
                all_find.append(coordinates)

            res = monitor.construct_gui(time_active=0.01, img=(self.screen_v6,
                                                               self.screen_v7,
                                                               self.screen_v8,
                                                               self.screen_v9,
                                                               self.screen_v10,
                                                               self.screen_v11,
                                                               self.screen_v12,
                                                               self.screen_v1),
                                                               similarity=0.8, offset_x=0, offset_y=0,
                                                               region=(1585, 4, 335, 258),
                                                               grayscale=False,
                                                               need_gui="yes")
            circle = 0
            for item_box in res:
                if "box" in item_box:
                    monitor.screen_monitor(item_box[0] - 10, item_box[1] - 10, 20, 20)
                    low = np.array((100, 0, 154), np.uint8)
                    upper = np.array((255, 57, 255), np.uint8)
                    mask = cv2.inRange(monitor.screen, low, upper)
                    if 255 in mask:
                        pass
                    else:
                        del res[circle]
                circle += 1

            if len(res) > 0:
                for item in res:

                    pyautogui.moveTo(item[0], item[1], duration=0.0)
                    monitor.screen_monitor(1585, 4, 335, 258)
                    monitor.mask(monitor.screen)

                    find = None

                    if item[2] == "dot":
                        if find is None:
                            find = monitor.find_load_img(monitor.e_r_progenium_deposit, 0.9, 0, 0)
                            if find:
                                print(f"{find} - Нашел:::ERPD")
                                name_res_massive.append("ERPD")
                                find_square(item)

                        if find is None:
                            find = monitor.find_load_img(monitor.e_progenium_deposit, 0.9, 0, 0)
                            if find:
                                print(f"{find} - Нашел:::EPD")
                                name_res_massive.append("EPD")
                                find_square(item)

                        if find is None:
                            find = monitor.find_load_img(monitor.r_progenium_deposit, 0.9, 0, 0)
                            if find:
                                print(f"{find} - Нашел:::RPD")
                                name_res_massive.append("RPD")
                                find_square(item)

                        if find is None:
                            find = monitor.find_load_img(monitor.progenium_deposit, 0.9, 0, 0)
                            if find:
                                print(f"{find} - Нашел:::PD")
                                name_res_massive.append("PD")
                                find_square(item)

                        if find is None:
                            find = monitor.find_load_img(monitor.e_r_elethium_deposit, 0.9, 0, 0)
                            if find:
                                print(f"{find} - Нашел:::ERED")
                                name_res_massive.append("ERED")
                                find_square(item)

                        if find is None:
                            find = monitor.find_load_img(monitor.r_elethium_deposit, 0.9, 0, 0)
                            if find:
                                print(f"{find} - Нашел:::RED")
                                name_res_massive.append("RED")
                                find_square(item)

                        if find is None:
                            find = monitor.find_load_img(monitor.elethium_deposit, 0.9, 0, 0)
                            if find:
                                print(f"{find} - Нашел:::ED")
                                name_res_massive.append("ED")
                                find_square(item)


                    if item[2] == "box":
                        if find is None:
                            find = monitor.find_load_img(monitor.forgotten_treasure_vault, 0.9, 0, 0)
                            if find:
                                print(f"{find} - Нашел:::FTV")
                                name_res_massive.append("FTV")
                                find_square(item)

                        if find is None:
                            find = monitor.find_load_img(monitor.discarded_automa_scrap, 0.9, 0, 0)
                            if find:
                                print(f"{find} - Нашел:::DAS")
                                name_res_massive.append("DAS")
                                find_square(item)

                        if find is None:
                            find = monitor.find_load_img(monitor.cypher_bound_chest, 0.9, 0, 0)
                            if find:
                                print(f"{find} - Нашел:::CBC")
                                name_res_massive.append("CBC")
                                find_square(item)

                        if find is None:
                            find = monitor.find_load_img(monitor.tarachnid_eggs, 0.9, 0, 0)
                            if find:
                                print(f"{find} - Нашел:::TE")
                                name_res_massive.append("TE")
                                find_square(item)

                        if find is None:
                            find = monitor.find_load_img(monitor.avian_nest, 0.9, 0, 0)
                            if find:
                                print(f"{find} - Нашел:::AN")
                                name_res_massive.append("AN")
                                find_square(item)

                        if find is None:
                            find = monitor.find_load_img(monitor.mawsworn_supply_chest, 0.9, 0, 0)
                            if find:
                                print(f"{find} - Нашел:::MSC")
                                name_res_massive.append("MSC")
                                find_square(item)

                num = 0
                for x in square:
                    x =  [all_find[num], name_res_massive[num], x]
                    self.all_info.append(x)
                    num += 1
                if len(all_find) > 0:
                    return len(all_find)
                else:
                    return None
            else:
                return None

    def find_res_on_screen(self, how, x=960, y=520, step=20, circle=4, for_minimap=2):
        one = 1
        two = 1
        three = 2
        four = 2
        five = 2
        self.tru_or_false = None
        pyautogui.moveTo(x, y, duration=0.0)
        if how == 1:time.sleep(1)
        if how == 2:time.sleep(0.5)

        monitor.check_res(for_minimap)
        if self.tru_or_false is None:

            for item in range(circle):

                for item_1 in range(one): # right
                    x += step
                    pyautogui.moveTo(x, y)
                    monitor.check_res(for_minimap)
                    if self.tru_or_false:
                        break
                if self.tru_or_false:
                    break

                for item_2 in range(two): # down
                    y += step
                    pyautogui.moveTo(x, y)
                    monitor.check_res(for_minimap)
                    if self.tru_or_false:
                        break
                if self.tru_or_false:
                    break

                for item_3 in range(three):  # left
                    x -= step
                    pyautogui.moveTo(x, y)
                    monitor.check_res(for_minimap)
                    if self.tru_or_false:
                        break
                if self.tru_or_false:
                    break

                for item_4 in range(four):  # down
                    y -= step
                    pyautogui.moveTo(x, y)
                    monitor.check_res(for_minimap)
                    if self.tru_or_false:
                        break
                if self.tru_or_false:
                    break

                for item_5 in range(five):  # left
                    x += step
                    pyautogui.moveTo(x, y)
                    monitor.check_res(for_minimap)
                    if self.tru_or_false:
                        break
                if self.tru_or_false:
                    break

                two += 2
                three += 2
                four += 2
                five += 2

            if how == 1:
                pyautogui.click(x, y)

        else: pyautogui.click(x, y)
        if how == 2:
            if self.tru_or_false:
                pyautogui.click(x, y)
                time.sleep(0.5)
                self.res += 1
                with open("Grab_Resurses.txt", "w", encoding="utf-8") as dead:
                    dead.write(f"Время старта: {start_time} Время завершения: {datetime.datetime.now().strftime('%H:%M:%S')} = {self.res}" + "\n")
                    dead.close()
                pyautogui.click(x, y)
                time.sleep(2)

    def check_res(self, how=2):
        if how == 1:
            self.tru_or_false = monitor.mouse("find", xy=monitor.construct_gui(time_active=0.01, img=(self.screen_v3,
                                                                                                      self.screen_v4,
                                                                                                      self.screen_v5),
                                                                     similarity=0.8, offset_x=0, offset_y=0, region=(1750, 1015, 170, 65), grayscale=False)) # (1750, 1015, 170, 65)
        if how == 2:
            self.tru_or_false = monitor.mouse("find", xy=monitor.construct_gui(time_active=0.01, img=(self.screen_v4,
                                                                                                      self.screen_v5),
                                                                        similarity=0.8, offset_x=0, offset_y=0, region=(1750, 1020, 125, 60), grayscale=False)) # (1750, 1015, 170, 65)
        if how == 3:
            self.tru_or_false = monitor.mouse("find", xy=monitor.construct_gui(time_active=0.01, img=self.dead_v1,
                                                                               similarity=0.8, offset_x=0, offset_y=0,
                                                                               region=(1750, 1015, 170, 65),
                                                                               grayscale=False))

    def boarding_protocol(self, tactic="collection"):
        if tactic == "collection":
            print(f"Нашел руду и спускаюсь: {monitor.tru_or_false}")
            combat.pocopoc_funk(how="non_combat")
            time_up = monitor.check_height()
            combat.check_combat()
            monitor.find_res_on_screen(2, circle=5)
            combat.telegram()
            combat.check_combat()
            combat.telegram()
            if player.one_class == 0:
                monitor.form_sov(1)
            if player.one_class == 0:
                print(f"Время взлета: {time_up}")
                keyboard.press("space")
                time.sleep(time_up)
                keyboard.release("space")
        else:
            key2 = {'45.3838.78': ("red", "red", "start"),
                    '45.3838.79': ("red", "red", "route"),
                    '44.8829.77': ("green", "green", "start"),
                    '44.8829.78': ("green", "green", "route"),
                    '69.7533.54': ("green", "green", "route"),
                    '40.7932.11': ("poc", "poc"),
                    '62.5745.59': ("poc", "poc"),
                    '53.3652.94': ("4", "4"),
                    '58.8857.28': ("4", "5"),
                    '58.6535.95': ("5", "4"),
                    '66.7243.37': ("6", "1")
            }
            x, y = str(player.player_coordinates_x2), str(player.player_coordinates_y2)
            if len(x) < 5: x = str(x) + "0"
            if len(y) < 5: y = str(y) + "0"
            identifier = x + y
            try:
                down, up = (key2[identifier])[0], (key2[identifier])[1]
                print(f"Ключ координат в списке: {down}, {up}")

            except Exception as ex:
                down, up = 0, 0

            if down == "red":
                if player.one_class == 0:
                    t = 8
                    if key2[identifier][2] == "start": t = 17
                    else: pass
                    print(f"Сажусь брать красный бафф: {monitor.tru_or_false}")
                    combat.pocopoc_funk(how="non_combat")
                    keyboard.press("x")
                    time.sleep(t)
                    keyboard.release("x")

                    if player.one_class == 0:
                        monitor.find_res_on_screen(1, for_minimap=1)
                        time.sleep(1)
                        combat.telegram()
                        combat.check_combat()
                        combat.telegram()
                        combat.pocopoc_funk(how="non_combat")
                        combat.telegram()
                        combat.check_combat()
                        combat.telegram()

                    if player.one_class == 0:
                        monitor.form_sov(1)

                    if player.one_class == 0:
                        keyboard.press("space")
                        time.sleep(5)
                        keyboard.release("space")

            if down == "green":
                if player.one_class == 0:
                    t = 10
                    if key2[identifier][2] == "start": t = 17
                    else: pass
                    print(f"Сажусь брать зеленый бафф: {monitor.tru_or_false}")
                    combat.pocopoc_funk(how="non_combat")
                    keyboard.press("x")
                    time.sleep(t)
                    keyboard.release("x")

                    if player.one_class == 0:
                        for x in range(2):
                            monitor.find_res_on_screen(1, for_minimap=1)
                            time.sleep(2)
                            combat.telegram()
                            combat.check_combat()
                            combat.telegram()
                            combat.pocopoc_funk(how="non_combat")
                        combat.telegram()
                        combat.check_combat()
                        combat.telegram()

                    if player.one_class == 0:
                        monitor.form_sov(1)

                    if player.one_class == 0:
                        keyboard.press("space")
                        time.sleep(5)
                        keyboard.release("space")

            if down == "poc":
                buff = None
                buff = monitor.construct_gui(time_active=0.01, img=monitor.pocopoc_buff_v1,
                                             similarity=0.8, offset_x=0, offset_y=0,
                                             region=(1300, 0, 500, 150), grayscale=False)
                if buff:
                    pass
                else:
                    try:
                        time.sleep(10)
                        monitor.screen_monitor(640, 300, 640, 390)
                        low = np.array((255, 255, 86), np.uint8)
                        upper = np.array((255, 255, 119), np.uint8)
                        mask = cv2.inRange(monitor.screen, low, upper)
                        self.screen_mask_frame = cv2.bitwise_and(monitor.screen, monitor.screen, mask=mask)
                        self.screen_mask_frame = np.where(self.screen_mask_frame != 0)
                        self.screen_mask_frame = int(np.mean(self.screen_mask_frame[0])), int(np.mean(self.screen_mask_frame[1]))

                        pyautogui.moveTo(640 + self.screen_mask_frame[1], 300 + self.screen_mask_frame[0])
                        time.sleep(1)
                        pyautogui.click()
                        buff = monitor.construct_gui(time_active=5, img=monitor.pocopoc_buff_v2,
                                                     similarity=0.8, offset_x=0, offset_y=0,
                                                     region=(0, 0, 400, 400), grayscale=False)
                        pyautogui.moveTo(buff[0], buff[1])
                        time.sleep(1)
                        pyautogui.click()
                    except Exception as ex:
                        print(ex)
                        pass

            try:
                if player.one_class == 0:
                    int(down)
                    keyboard.press("x")
                    time.sleep(int(down))
                    keyboard.release("x")
                    int(up)
                    keyboard.press("space")
                    time.sleep(int(up))
                    keyboard.release("space")
            except:
                pass

    def clear(self, how):
        if how == 1:
            self.tru_or_false = None
            player.two_class = 0
        if how == 2:
            self.tru_or_false = None

class Combat:

    def __init__(self):
        self.combat = None
        self.fuck_pocopoc = None
        self.hp = None
        self.astral = None
        self.convoke = None
        self.convoke_kd = None
        self.celestial_kd = None
        self.celestial = None
        self.screen = None
        self.screen_spell = None
        self.cora = None
        self.revelation = None
        self.save = None
        self.enemy = None
        self.screen_mask_frame = None
        self.typhoon_kd = None

    def __str__(self):
        print(f"Статус боя: {self.combat}")
        print(f"Чертов Покопок: {self.fuck_pocopoc}")
        print(f"Здоровье: {self.hp}")
        print(f"Астральная энергия: {self.astral}")
        print(f"Конвок: {self.convoke}")
        print(f"Селестиал: {self.celestial}")
        print(f"Положение врагов: {self.screen_mask_frame}")

    def telegram(self, hp_ignore=False):
        m = mss()
        grab = m.grab({"left": user["hp_position"][0], "top": user["hp_position"][1], "width": 1, "height": 1})
        full_screen_array = np.array(grab)
        hp = (full_screen_array == (user["hp_color"][0], user["hp_color"][1], user["hp_color"][2], 255))
        if hp_ignore is True: hp = [False, False, False, False]
        if False in hp:
            time.sleep(5)
            error = player.find_error()
            if error == "disconnect": text = f"Здоровье игрока отсутствует >>> disconnect"
            if error == "dead": text = f"Здоровье игрока отсутствует >>> dead"
            if error == "unknown_hp_off": text = f"Здоровье игрока отсутствует >>> unknown"
            if error == "unknown_hp_on": text = f"Здоровье игрока присутствует >>> fly to the Sun"

            bot_token = "***"
            admin_id = int(user["telegram_id"])
            api_link = "https://api.telegram.org/bot" + bot_token
            requests.get(api_link + f"/sendMessage?chat_id={admin_id}&text={text}")
            print(text)

            if error == "disconnect": player.reconnect()
            if error == "dead": player.reset()
            if error == "unknown_hp_off": player.reconnect()
            if error == "unknown_hp_on": player.reconnect()
        else: return "all_normal"

    def pocopoc_funk(self, how="non_combat"):
        check_pocopoc = None
        check_pocopoc = monitor.construct_gui(time_active=0.01, img=monitor.check_pocopoc,
                                                  similarity=0.8, offset_x=0, offset_y=0,
                                                  region=(1080, 900, 100, 50), grayscale=False)
        if check_pocopoc:
            print("Выключаю Покапока")
            self.fuck_pocopoc = True
            if how == "non_combat":
                keyboard.send("esc")
            if how == "combat":
                keyboard.send("esc")
                keyboard.send("f")
        else:
            self.fuck_pocopoc = None
            print("pocopoc non")


    def check_combat(self):
        self.combat = None
        self.fuck_pocopoc = None
        self.hp = None
        self.astral = None
        self.convoke = None
        self.convoke_kd = 0
        self.celestial_kd = 0
        self.celestial = None
        self.screen = None
        self.screen_spell = None
        self.cora = None
        self.revelation = None
        self.save = None
        self.enemy = None
        self.screen_mask_frame = None
        self.typhoon_kd = 0

        m = mss()
        grab = m.grab({"left": user["combat_position"][0], "top": user["combat_position"][1], "width": 1, "height": 1})
        grab = np.array(grab)[0][0]
        if grab [0] == user["combat_color"][0] and grab[1] == user["combat_color"][1]  and grab[2] == user["combat_color"][2] : pix = True
        else: pix = False

        if pix is True:
            keyboard.send("u")
            time.sleep(1)
            while pix is True:
                combat.pocopoc_funk(how="combat")
                combat.get_info_in_combat()
                combat.corrector_position()
                combat.command()
                m = mss()
                grab = m.grab({"left": user["combat_position"][0], "top": user["combat_position"][1], "width": 1, "height": 1})
                grab = np.array(grab)[0][0]
                if grab [0] == user["combat_color"][0] and grab[1] == user["combat_color"][1]  and grab[2] == user["combat_color"][2] : pix = True
                else:
                    pix = False
                    try:
                        pyautogui.moveTo(self.screen_mask_frame[1], self.screen_mask_frame[0])
                        pyautogui.click()
                        time.sleep(0.5)
                    except:
                        pass
                    combat.get_info_in_combat()
                    combat.telegram()
                    with open("Dead_Logs.txt", "a", encoding="utf-8") as dead:
                        dead.write(f"{datetime.datetime.now().strftime('%H:%M:%S')} - Бой завершился: здоровье = {self.hp}" + "\n")

        else:
            pass

    def find_load_img(self, img, similarity, x_offset, y_offset):
        """Поиск необходимого изображения на экране"""
        try:
            res = cv2.matchTemplate(self.screen_spell, img, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= similarity)
            xy = loc[1][0] + x_offset, loc[0][0] + y_offset
            return xy
        except:
            return None

    def get_info_in_combat(self):
        m = mss()
        grab = m.grab({"left":0, "top":0, "width": 1920, "height": 1080})
        full_screen_array = np.array(grab)

        self.hp = (full_screen_array[user["hp_position2"][0]:user["hp_position2"][1], user["hp_position2"][2]:user["hp_position2"][3]])[0] \
                  == (user["hp_color"][0], user["hp_color"][1], user["hp_color"][2], 255)
        hh = 0
        for item in self.hp:
            if False in item: pass
            else: hh += 1
        self.hp = int(hh/(240/100))

        self.astral = (full_screen_array[user["astral_position"][0]:user["astral_position"][1], user["astral_position"][2]:user["astral_position"][3]])[0]\
                      == (user["astral_color"][0], user["astral_color"][1], user["astral_color"][2], 255)
        aa = 0
        for item in self.astral:
            if False in item: pass
            else: aa += 1
        self.astral = 100 - (int(aa/(192/100)))

        self.screen_spell = full_screen_array[700:825, 830:1100]
        self.screen_spell = monitor.convector(self.screen_spell, color="BGR")
        self.convoke = combat.find_load_img(monitor.screen_v19, 0.7, 0, 0)
        self.celestial = combat.find_load_img(monitor.screen_v20, 0.7, 0, 0)

        try:
            low = np.array((user["enemy_color"][0][0], user["enemy_color"][0][1], user["enemy_color"][0][2], 255), np.uint8)
            upper = np.array((user["enemy_color"][1][0], user["enemy_color"][1][1], user["enemy_color"][1][2], 255), np.uint8)
            mask = cv2.inRange(full_screen_array, low, upper)
            self.screen_mask_frame = cv2.bitwise_and(full_screen_array, full_screen_array, mask=mask)
            self.screen_mask_frame = np.where(self.screen_mask_frame != 0)
            self.screen_mask_frame = int(np.mean(self.screen_mask_frame[0])), int(np.mean(self.screen_mask_frame[1]))
            print(self.screen_mask_frame)
        except:
            self.screen_mask_frame = [540, 960]
            print(self.screen_mask_frame)

    def corrector_position(self):
        """Поворачивается в нужном направлении по отношению к цели в бою"""
        player_save_x, player_save_y = copy.copy(player.player_coordinates_x2), copy.copy(player.player_coordinates_y2)
        try:
            player.player_coordinates_x0 = 960
            player.player_coordinates_y0 = 1080
            player.player_coordinates_x1 = 960
            player.player_coordinates_y1 = 540
            player.player_coordinates_x2 = self.screen_mask_frame[1]
            player.player_coordinates_y2 = self.screen_mask_frame[0]
            player.distance_to_target(how=0)  # дистанция AC
            player.distance_to_target(how=1)  # дистанция AB
            player.distance_to_target(how=2)  # дистанция BC
            player.cosine_angle()
            player.exterior_angle()
            print(player.cosine_exterior_angle)
            if self.screen_mask_frame == [540, 960]:
                print(self.screen_mask_frame[0], self.screen_mask_frame[1])
                pass
            else:
                if self.screen_mask_frame[1] <= 940:
                    side = "a"
                else:
                    side = "d"
                print(self.screen_mask_frame[0], self.screen_mask_frame[1])

                rotation_sec = 0.0055555555555556 * player.cosine_exterior_angle
                keyboard.press(side)
                time.sleep(rotation_sec)
                keyboard.release(side)
            player.player_coordinates_x2, player.player_coordinates_y2 = player_save_x, player_save_y
        except Exception as ex:
            player.player_coordinates_x2, player.player_coordinates_y2 = player_save_x, player_save_y
            player.error(ex=ex, write="no")

    def command(self):
        print(combat.__str__())
        if self.hp < 20 and self.typhoon_kd != 1:
            keyboard.send("e")
            print("e")
            self.save = 1
            time.sleep(1.5)
            keyboard.send("r")
            print("r")

        elif self.hp < 20:
            keyboard.send("z")
            print("z")
            time.sleep(2.5)
            keyboard.send("b")
            print("b")
            time.sleep(1.5)
            keyboard.send("u")
            return 1

        elif self.hp < 40 and self.save != 1:
            keyboard.send("v")
            print("v")
            self.save = 1
            return 1

        elif self.hp < 50:
            keyboard.send("z")
            print("z")
            time.sleep(2.5)

            return 1

        elif self.hp < 70 and self.revelation != 1:
            keyboard.send("q")
            print("q")
            keyboard.send("n")
            self.revelation = 1
            print("n")
            time.sleep(1.5)
            keyboard.send("u")
            time.sleep(1)
            return 1

        elif self.celestial and self.celestial_kd != 1:
            keyboard.send("1")
            self.celestial_kd = 1
            print("1")

        elif self.convoke and self.convoke_kd != 1:
            time.sleep(0.3)
            keyboard.send("2")
            self.convoke_kd = 1
            print("2")
            time.sleep(4)

        elif self.astral > 32:
            keyboard.send("4")
            print("4")
            time.sleep(0.5)

        else:
            keyboard.send("5")
            print("5")

def start():
    pyautogui.moveTo(725, 834)
    pyautogui.click()
    time.sleep(2)
    player.elusive_rich_elethium_deposit = copy.copy(player.original_elusive_rich_elethium_deposit)
    player.rich_elethium_deposit = copy.copy(player.original_rich_elethium_deposit)
    player.elethium_deposit = copy.copy(player.original_elethium_deposit)

    player.elusive_rich_progenium_deposit = copy.copy(player.original_elusive_rich_progenium_deposit)
    player.elusive_progenium_deposit = copy.copy(player.original_elusive_progenium_deposit)
    player.rich_progenium_deposit = copy.copy(player.original_rich_progenium_deposit)
    player.progenium_deposit = copy.copy(player.original_progenium_deposit)

    player.forgotten_treasure_vault = copy.copy(player.original_forgotten_treasure_vault)
    player.discarded_automa_scrap = copy.copy(player.original_discarded_automa_scrap)
    player.cypher_bound_chest = copy.copy(player.original_cypher_bound_chest)
    player.tarachnid_eggs = copy.copy(player.original_tarachnid_eggs)
    player.avian_nest = copy.copy(player.original_avian_nest)
    player.mawsworn_supply_chest = copy.copy(player.original_mawsworn_supply_chest)
    print(f"Все координаты сброшены . . .")
    player.near_res_50 = ['45.38 38.78', '42.76 33.51', '44.88 29.77']
    player.player_coordinates_x2, player.player_coordinates_y2 = player.pytesseract_player_target(player.near_res_50, 0)

    combat.telegram()
    player.two_class = 0
    while player.two_class == 0:
        player.pytesseract_player_xy0(how=0)  # точка A
        keyboard.press('w')
        time.sleep(0.3)
        player.distance_to_target(how=0)  # дистанция AC
        if player.distanceAC < 50:
            keyboard.release("w")
        player.pytesseract_player_xy0(how=1)  # точка B
        player.distance_to_target(how=1)  # дистанция AB
        player.distance_to_target(how=2)  # дистанция BC
        player.cosine_angle()
        player.exterior_angle()
        player.left_or_right()
        player.movement()
        player.move(how=3, distance=3)
        monitor.clear(how=2)

        monitor.form_sov(2)

        print(datetime.datetime.now(), f" <<<start>>>  one_dot: {player.player_coordinates_x0}, {player.player_coordinates_y0}; two_dot: {player.player_coordinates_x1}, {player.player_coordinates_y1}", "\n")
    keyboard.release("w")
    player.near_res_50 = []
    player.player_coordinates_x2, player.player_coordinates_y2 = player.pytesseract_player_target(player.list_coordinates, 0)
    print(f"После смерти или старта >>> {player.player_coordinates_x2, player.player_coordinates_y2}")

def work():
    while True:
        player.one_class = 0
        player.pytesseract_player_xy0(how=0)  # точка A
        keyboard.press('w')
        # time.sleep(0.1)
        combat.telegram()
        check = monitor.construct_gui(time_active=0.01, img=(monitor.screen_v6, monitor.screen_v7, monitor.screen_v8, monitor.screen_v9,
                                                             monitor.screen_v10, monitor.screen_v11, monitor.screen_v12,monitor.screen_v1),
                                    similarity=0.8, offset_x=0, offset_y=0, region=(1465, 4, 455, 449), grayscale=False, need_gui="yes")
        circle = 0
        for item_box in check:
            if "box" in item_box:
                monitor.screen_monitor(item_box[0] - 10, item_box[1] - 10, 20, 20)
                low = np.array((100, 0, 154), np.uint8)
                upper = np.array((255, 57, 255), np.uint8)
                mask = cv2.inRange(monitor.screen, low, upper)
                if 255 in mask:
                    pass
                else:
                    del check[circle]
            circle += 1
        print(f"Проверил карту на наличие нужной руды: {check}")
        if check:
            keyboard.release("w")
            player.pytesseract_player_xy0(how=0)
            monitor.check_minimap()
            player_save_x, player_save_y = copy.copy(player.player_coordinates_x2), copy.copy(player.player_coordinates_y2)
            player.distance_near()

            if len(player.near_res_50) > 0:
                work50()
                combat.telegram()
                print("'\n'<<<ПОЛНОСТЬЮ ВЫШЕЛ ИЗ ЦИКЛА И ВОЗВРАЩАЮСЬ К МАРШРУТУ>>>''\n")
                player.pytesseract_player_xy0(how=0)
                keyboard.press('w')
                time.sleep(0.3)

                player.player_coordinates_x2, player.player_coordinates_y2 = player_save_x, player_save_y
                print(f"Вышел из цикла поиска ресурсов - текущие координаты назначения: {player.player_coordinates_x2, player.player_coordinates_y2}")
            else:
                player.pytesseract_player_xy0(how=0)
                keyboard.press('w')
                time.sleep(0.3)
                player.player_coordinates_x2, player.player_coordinates_y2 = player_save_x, player_save_y

        keyboard.press('w')
        player.distance_to_target(how=0) # дистанция AC
        if player.distanceAC < 50:
            keyboard.release("w")
        player.pytesseract_player_xy0(how=1) # точка B
        player.distance_to_target(how=1) # дистанция AB
        player.distance_to_target(how=2) # дистанция BC
        player.cosine_angle()
        player.exterior_angle()
        player.left_or_right()
        player.movement()
        player.move(how=1, distance=3)
        monitor.clear(how=1)

        monitor.form_sov(2)

        print(datetime.datetime.now(), f"<<<route>>>  one_dot: {player.player_coordinates_x0}, {player.player_coordinates_y0}; two_dot: {player.player_coordinates_x1}, {player.player_coordinates_y1}", "\n")
        if player.one_class == 1:
            player.player_coordinates_x2, player.player_coordinates_y2 = player.pytesseract_player_target(
                player.list_coordinates, 0)

def work50():
    combat.telegram()
    player.two_class = 0
    while player.two_class == 0:
        player.pytesseract_player_xy0(how=0)  # точка A
        keyboard.press('w')
        time.sleep(0.3)
        player.distance_to_target(how=0)  # дистанция AC
        if player.distanceAC < 50:
            keyboard.release("w")
        player.pytesseract_player_xy0(how=1)  # точка B
        player.distance_to_target(how=1)  # дистанция AB
        player.distance_to_target(how=2)  # дистанция BC
        player.cosine_angle()
        player.exterior_angle()
        player.left_or_right()
        player.movement()
        player.move(how=2, distance=3)
        monitor.clear(how=2)

        monitor.form_sov(2)

        print(datetime.datetime.now(),f" <<<resources>>>  one_dot: {player.player_coordinates_x0}, {player.player_coordinates_y0}; two_dot: {player.player_coordinates_x1}, {player.player_coordinates_y1}", "\n")
        if player.one_class == 1:
            player.player_coordinates_x2, player.player_coordinates_y2 = player.pytesseract_player_target(
                player.list_coordinates, 0)


user = load_profile()
player = Player(multiplier_location_x=49.4, multiplier_location_y=32.9, red=[63.12, 19.49],
                green=[69.74, 33.54], distance_map=210, distance_yard=210,scatter=0.5)
monitor = Monitor()
combat = Combat()
monitor.creation_img()
pytesseract.pytesseract.tesseract_cmd = user['tesseract']
keyboard.wait("p")
start_time = datetime.datetime.now().strftime('%H:%M:%S')
keyboard.send("0")
#start()
#work()
#
#player.for_check_coordinates_res()
""" ПАТЧ:
18.05.2022
- расположение тессеракта(Маша)
- добавление в старт сброс заблокированных координат
- поиск Покапока по картинке
- кнопка выравнивания камеры после дисконекта
- время старта
"""

""" ПАТЧ:
23.05.2022
- выбор пользователя в профиле
- повороты в бою
- уменьшение зоны поиска "mining"
- функция для отображения зоны ресурса>>>   player.for_check_coordinates_res()
- отступ при смерти, длительность реса
- 548 стр(таб)
- две точки игрока в отчетах
- точки центра карты в профиле
- еще одна точка чека бафа от покапока
- релиз и слип 256 стр
"""
def all_func():
    one_x = step_one_x(player_coordinates_x0, player_coordinates_y0, player_coordinates_x1)
    print(one_x)
    one_y = step_one_y(player_coordinates_x0, player_coordinates_y0, player_coordinates_y1)
    print(one_y)

    two_x_up = step_two_up_down(one_x[1], one_x[0])
    print(two_x_up)
    # two_x_down = step_two_down(one_x[1], one_x[0])
    # print(two_x_down)
    # result = how_way(one_x[1], one_x[0], two_x_up[1], two_x_up[0], two_x_down[1], two_x_down[0])
    # print(result)

def step_one_x(x, y, x1):
    circle = 0
    while x + circle != x1:
        circle += 1
        if massive[y][x + circle] == 0:
            #print(f"Двигаюсь по X: {y, x + circle}; {massive[y][x + circle]}")
            pass
        else:
            #print("STOP")
            #print(f"Двигаюсь по X: {y, x + circle}; {massive[y][x + circle]}")
            return y, x + (circle - 1)
    return y, x + circle

def step_one_y(x, y, y1):
    circle = 0
    while y - circle != y1:
        circle += 1
        if massive[y - circle][x] == 0:
            #print(f"Двигаюсь по Y: {y - circle, x}; {massive[y - circle][x]}")
            pass
        else:
            #print("STOP")
            #print(f"Двигаюсь по Y: {y - circle, x}; {massive[y - circle][x]}")
            return  y - (circle - 1), x
    return y - circle, x

def step_two_up_down(x, y):
    print(y, x)
    circle = 0
    circle_3 = 1
    circle_2 = 0
    circle_4 = 0

    while (massive[y - circle][x + 1] != 0) and (massive[y + circle][x + 1] != 0):

        if massive[y - circle][x] == 0:
            if massive[y - circle][x + 1] == 0:
                print("STOP1")
                return y - circle, x

        else:
            circle_2 += 1
            if massive[y - (circle + 1)][x - circle_2] == 0:
                if massive[y - circle][x - circle_2] == 0:
                    print("STOP2")
                    return y - circle, x - circle_2

        if massive[y + circle_3][x] == 0:
            if massive[y + circle_3][x + 1] == 0:
                print("STOP3")
                return y + circle_3, x

        else:
            circle_4 += 1
            if massive[y - (circle_3 - 1)][x - circle_4] == 0:
                if massive[y - circle_3][x - circle_4] == 0:
                    print("STOP4")
                    return y - circle_3, x - circle_4
        print(massive[y - circle_3][x - circle_4])

        if massive[y - circle][x] == 0: circle += 1
        if massive[y + circle_3][x] == 0: circle_3 += 1


def step_two_down(x, y):
    print(y, x)
    circle = 0
    print(massive[y + circle][x + 1])
    while massive[y + circle][x + 1] != 0:
        circle += 1
        if massive[y + circle][x] == 0:
            print(massive[y + circle][x])
            if massive[y + circle][x + 1] == 0:
                print("STOP")
                return y + circle, x
        else:
            circle_2 = 0
            while massive[y + circle][x - circle_2] != 0:
                circle_2 += 1
                if massive[y - (circle - 1)][x - circle_2] == 0:
                    if massive[y - circle][x - circle_2] == 0:
                        print("STOP1")
                        print(y - circle, x - circle_2)
                        return y - circle, x - circle_2
            print(massive[y - circle][x - circle_2])

def how_way(x, y, x1, y1, x2, y2):
    one = abs(x - x1) + abs(y - y1)
    two = abs(x - x2) + abs(y - y2)
    print(one)
    print(two)
    if one < two:
        return y1, x1
    else:
        return y2, x2

all_func()