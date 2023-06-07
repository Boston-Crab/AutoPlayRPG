#The Main AutoRPG python file
import sys
import pygame
import time
import pygame.mixer
from enum import Enum, auto

pygame.init()
pygame.mixer.init()

#>>>>>> Screen <<<<<<
screen_width = 480
screen_height = 784
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Auto Battler")
#>>>>>> End - Screen <<<<<<

#>>>>>> Game State/Progress tracking <<<<<<
game_finish_progress = {'crypts': False, 'orcish_valley': False, 'frozen_tundra': False, 'demon_world': False}
#crypts_scenes_completion = [0,0,0]
orcish_valley_scenes_completion = [0,0,0,0,0]
#>>>>>> End - Game State/Progress tracking <<<<<<

#>>>>>> Variables <<<<<<
#--- Hero:
hero_level = 1
hero_exp = 0
hero_total_hp = 300
hero_current_hp = 300
hero_damage = 10
hero_defence = 10
hero_unsed_stat_points = 0
hero_vitality = 0
hero_strength = 0
#--- Enemy:
enemy_total_hp = 50
enemy_current_hp = 50
enemy_damage = 20
enemy_defence = 0
#--- Colors:
color_black = 0,0,0
color_white = 255,255,255
color_red = 255,0,0
color_grey = 192,192,192
color_yellow = 255,255,0
color_green = 0,255,0
#--- range() numbers:
#For music mute button:
r_0_0 = 0,0
#>>>>>> End - Variables <<<<<<

#>>>>>> Custom Functions <<<<<<

def back_text_screen_blitting(screen, mp):
    text_back.blit_text(screen, mp)
    
def redraw_screen(current_menu, music_playing, screen, mp, assets, state):
    #Title screen:
    if current_menu == GameLoopState.MainMenu:
        state.title_screen_blit(mp)            
    #New game confirmation screen:
    elif current_menu == GameLoopState.NewGame:
        state.new_game_confirmation_screen_blit(mp)
    #About screen:
    elif current_menu == GameLoopState.AboutGame:
        state.about_screen_blit(mp)
    #Town screen:
    elif current_menu == GameLoopState.TownMainMenu:
        state.town_screen_blit(mp)
    #Faceless Man Screen:
    elif current_menu == GameLoopState.TownFacelessman:
        state.facelessman_screen_blit(mp)
    #Battle screen:
    elif current_menu == GameLoopState.TownBattle:
        state.battle_screen_blit(mp)   
    #Character screen
    elif current_menu == GameLoopState.TownCharacter:
        state.character_screen_blit(mp)
    #Shop screen
    elif current_menu == GameLoopState.TownShop:
        state.shop_screen_blit(mp)
    #Music buttons:
    if music_playing == True:
        screen.blit(assets.raw_music_on_bg, (r_0_0))
    elif music_playing == False:
        screen.blit(assets.raw_music_off_bg, (r_0_0))

def victory_blitting(assets):
    red_bar_x = 150
    red_bar_y = 200
    red_bar_width = 200
    red_bar_height = 10
    pygame.draw.rect(screen, color_yellow, [red_bar_x-2, red_bar_y-2, red_bar_width+4, red_bar_height+4], 2)
    pygame.draw.rect(screen, color_green, [red_bar_x, red_bar_y, red_bar_width, red_bar_height])
    text_victory = assets.font_62.render("VICTORY", True, color_white)
    text_victory_black = assets.font_62.render("VICTORY", True, color_black)
    screen.blit(text_victory_black, (157,222))
    screen.blit(text_victory, (155,220))
    pygame.draw.rect(screen, color_yellow, [red_bar_x-2, red_bar_y+66, red_bar_width+4, red_bar_height+4], 2)
    pygame.draw.rect(screen, color_green, [red_bar_x, red_bar_y+68, red_bar_width, red_bar_height])
    pygame.display.flip()

class Combat:
    class CombatState(Enum):
        Start = 0
        AdvancePlayer = 1
        Slashing = 2

    def __init__(self, screen, enemy_current_hp, hero_current_hp, hero_damage, 
                 enemy_damage, hero_defence, enemy_defence, player_slash_img, enemy_slash_img, hero_total_hp, enemy_total_hp,
                 is_crypts_finished, is_orcish_valley_finished, assets):
        
        self.crypts_scenes_completion = [0,0,0]
        self.orcish_valley_scenes_completion = [0,0,0,0,0]
        self.is_crypts_finished = is_crypts_finished
        self.is_orcish_valley_finished = is_orcish_valley_finished
        self.combat_state = Combat.CombatState.Start
        #----
        self.desired_defender = None
        self.desired_attacker = None
        self.desired_defender_coord_xy = None
        self.desired_attacker_coord_x = None
        self.desired_attacker_coord_y = None
        self.desired_slash = None
        self.desired_slash_coord_xy = None
        #----
        self.assets = assets
        self.screen = screen
        self.enemy_current_hp = enemy_current_hp
        self.hero_current_hp = hero_current_hp
        self.hero_damage = hero_damage
        self.enemy_damage = enemy_damage
        self.hero_defence = hero_defence
        self.enemy_defence = enemy_defence
        self.player_slash_img = player_slash_img
        self.enemy_slash_img = enemy_slash_img
        self.hero_total_hp = hero_total_hp
        self.enemy_total_hp = enemy_total_hp
        self.move_coord = 0
        self.moving_forwards_or_backwards_switch = True
        self.attack_turn_switch = False
        self.hero_dmg_num_blit_x = 330
        self.hero_dmg_num_blit_y = 420
        self.enemy_dmg_num_blit_x = 150
        self.enemy_dmg_num_blit_y = 420
        self.combat_finished = False

    def update(self, mp, current_menu):
        self.current_menu = current_menu
        self.desired_bg = self.desired_bg_picking(self.assets, self.current_menu)
        self.desired_enemy = self.desired_enemy_picking(self.assets, self.current_menu)
        self.combat_finished = False
        self.mp = mp
        self.enemy_current_hp = 50

    def checking_if_enemy_moves(self, whose_move):
        if whose_move == "enemy":
            if self.move_coord == 0:
                self.move_coord = 80
            return 280

    def updating_attributes_depending_on_whose_turn(self, whose_move):
        if whose_move == "player":
            self.desired_defender = self.desired_enemy[0]
            self.desired_attacker = self.assets.scaled_player_char[0]
            self.desired_defender_coord_xy = 280,457
            self.desired_attacker_coord_x = self.move_coord
            self.desired_attacker_coord_y = 458
            self.desired_slash = self.player_slash_img
            self.desired_slash_coord_xy = 276,533
            self.whose_damage = self.hero_damage
            self.whose_defence = self.enemy_defence
            self.whose_dmg_coord_x = self.hero_dmg_num_blit_x
            self.whose_dmg_coord_y = self.hero_dmg_num_blit_y
            self.whose_current_hp = self.enemy_current_hp
        elif whose_move == "enemy":
            self.desired_defender = self.assets.scaled_player_char[0]
            self.desired_attacker = self.desired_enemy[0]
            self.desired_defender_coord_xy = 0,458
            self.desired_attacker_coord_x = 280 - self.move_coord
            self.desired_attacker_coord_y = 457
            self.desired_slash = self.enemy_slash_img
            self.desired_slash_coord_xy = 67,534
            self.whose_damage = self.enemy_damage
            self.whose_defence = self.hero_defence
            self.whose_dmg_coord_x = self.enemy_dmg_num_blit_x
            self.whose_dmg_coord_y = self.enemy_dmg_num_blit_y
            self.whose_current_hp = self.hero_current_hp
    
    def updating_remaining_hp(self, whose_move):
        if whose_move == 'enemy':
            self.hero_current_hp = self.whose_current_hp
        else:
            self.enemy_current_hp = self.whose_current_hp

    def all_characters_combat_movement_blitting(self, whose_move):
        self.updating_attributes_depending_on_whose_turn(whose_move)
        self.screen.blit(self.desired_bg[0], self.desired_bg[1])
        self.screen.blit(self.desired_defender, (self.desired_defender_coord_xy))
        #--- HP Bar Blitting:
        text_hero_current_hp.blit_text(self.screen, self.mp)
        text_enemy_current_hp.blit_text(self.screen, self.mp)
        self.hp_bar_blitting() 
        #------------------------
        if self.combat_state == Combat.CombatState.Start:
            self.player_advance_start_time = pygame.time.get_ticks()
            self.combat_state = Combat.CombatState.AdvancePlayer
        current_time = pygame.time.get_ticks()
        #Character moves forward:
        if self.moving_forwards_or_backwards_switch == True: 
            self.screen.blit(self.desired_attacker, (self.desired_attacker_coord_x, self.desired_attacker_coord_y))
            if self.combat_state == Combat.CombatState.AdvancePlayer:
                if (current_time - self.player_advance_start_time) >= 5:
                    self.move_coord = self.move_coord +1
                    if self.move_coord == 80:
                        self.combat_state = Combat.CombatState.Slashing
                        self.slash_start_time = current_time
                    self.player_advance_start_time = current_time
            #Attacking Image/sound:
            if self.combat_state == Combat.CombatState.Slashing:
                self.screen.blit(self.desired_slash, (self.desired_slash_coord_xy))
                if (current_time - self.slash_start_time) >= 150:
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound(self.assets.sound_sword_slash))
                    #Damage inflicted calculation:
                    self.whose_current_hp = self.whose_current_hp - self.whose_damage
                    self.updating_remaining_hp(whose_move)
                #Move forward is off:
                    self.moving_forwards_or_backwards_switch = False
                    self.combat_state = Combat.CombatState.AdvancePlayer
        #------------------------  
        #Character moves backwards:
        elif self.moving_forwards_or_backwards_switch == False: 
            self.screen.blit(self.desired_attacker, (self.desired_attacker_coord_x,self.desired_attacker_coord_y))
            if self.combat_state == Combat.CombatState.AdvancePlayer:
                self.move_coord = self.move_coord - 1
                if self.move_coord == 0:
            
                    self.moving_forwards_or_backwards_switch = True
                    self.whose_dmg_coord_y = 420 #Resetting damage coordinates
                    
                    self.attack_turn_switching_inside_class(whose_move)
                    self.victory_checking(whose_move)
                #Blit of damage inflicted:
                else:
                    if self.whose_dmg_coord_y > 380:
                        self.damage_numbers_appearing(self.whose_damage, self.whose_defence, self.whose_dmg_coord_x, self.whose_dmg_coord_y)
                        self.whose_dmg_coord_y = self.whose_dmg_coord_y - 1                  
    
    def hp_bar_blitting(self):
        #--- Player HP Bar coordinates:
        player_hp_bar_x = 30
        player_hp_bar_y = 50
        hp_bar_width = 180
        hp_bar_height = 20
        #--- Player HP calculation:
        hero_hp_percent = self.hero_current_hp / self.hero_total_hp
        #--- Enemy HP Bar coordinates:
        enemy_hp_bar_x = 270
        enemy_hp_bar_y = 50
        hp_bar_width = 180
        hp_bar_height = 20
        #--- Enemy HP calculation:
        enemy_hp_percent = self.enemy_current_hp / self.enemy_total_hp

        #------------------------------------------------------------------
        #--- Player HP Bar Border:
        pygame.draw.rect(self.screen, color_black, [player_hp_bar_x, player_hp_bar_y, hp_bar_width, hp_bar_height], 2)
        #--- Player HP:
        pygame.draw.rect(self.screen, color_red, [player_hp_bar_x + 2, player_hp_bar_y + 2, hero_hp_percent * (hp_bar_width - 4), hp_bar_height - 4])
        #--- Player HP number representation:
        text_player_hp_bar_numbers = self.assets.text_font_30.render((str(self.hero_current_hp)+"/"+str(self.hero_total_hp)), True, (color_white))
        text_player_hp_bar_numbers_border = self.assets.text_font_30.render((str(self.hero_current_hp)+"/"+str(self.hero_total_hp)), True, (color_black))
        self.screen.blit(text_player_hp_bar_numbers_border, (31,71))
        self.screen.blit(text_player_hp_bar_numbers, (30,70))

        #------------------------------------------------------------------
        #--- Enemy HP Bar Border:
        pygame.draw.rect(self.screen, color_black, [enemy_hp_bar_x, enemy_hp_bar_y, hp_bar_width, hp_bar_height], 2)
        #--- Enemy HP:
        pygame.draw.rect(self.screen, color_red, [enemy_hp_bar_x + 2, enemy_hp_bar_y + 2, enemy_hp_percent * (hp_bar_width - 4), hp_bar_height - 4])
        #--- Enemy HP number representation:
        text_enemy_hp_bar_numbers = self.assets.text_font_30.render((str(self.enemy_current_hp)+"/"+str(self.enemy_total_hp)), True, (color_white))
        text_enemy_hp_bar_numbers_border = self.assets.text_font_30.render((str(self.enemy_current_hp)+"/"+str(self.enemy_total_hp)), True, (color_black))
        self.screen.blit(text_enemy_hp_bar_numbers_border, (271,71))
        self.screen.blit(text_enemy_hp_bar_numbers, (270,70))

    def damage_numbers_appearing(self, whose_dmg, whose_def, dmg_num_x, dmg_num_y):
        damage_to_do = whose_dmg - whose_def
        if damage_to_do <= 0:
                damage_to_do = 0
        text_damage_number_border = self.assets.text_font_40.render(("-"+str(damage_to_do)), True, (color_black))
        screen.blit(text_damage_number_border, (dmg_num_x +1, dmg_num_y +1))
        text_damage_number = self.assets.text_font_40.render(("-"+str(damage_to_do)), True, (color_red))
        screen.blit(text_damage_number, (dmg_num_x, dmg_num_y))
    
    def victory_checking(self, whose_winning):
        if self.enemy_current_hp <= 0:
            self.hp_bar_blitting()
            print(whose_winning)
            pygame.mixer.Channel(0).stop()
            victory_blitting(self.assets)
            pygame.mixer.Channel(1).play(pygame.mixer.Sound(self.assets.sound_leveling_up))
            time.sleep(3)
            self.updating_game_progress_after_fight_outcome(whose_winning, self.current_menu)
            self.combat_finished = True
        elif self.hero_current_hp <= 0:
            self.hp_bar_blitting()
            print(whose_winning)
            pygame.mixer.Channel(1).play(pygame.mixer.Sound(self.assets.sound_leveling_up))
            time.sleep(3)
            self.updating_game_progress_after_fight_outcome(whose_winning, self.current_menu)
            self.combat_finished = True
    
    def updating_game_progress_after_fight_outcome(self, whose_winning, current_menu):
        global is_crypts_finished, is_orcish_valley_finished
        if whose_winning == "player":
            if current_menu == GameLoopState.CryptsFighting:
                index_finding = self.crypts_scenes_completion.index(0)
                self.crypts_scenes_completion[index_finding] = 1
                if self.crypts_scenes_completion[2] == 1:
                    is_crypts_finished = True
                    self.crypts_scenes_completion = [0,0,0]
            elif current_menu == GameLoopState.OrcishValleyFighting:
                index_finding = self.orcish_valley_scenes_completion.index(0)
                self.orcish_valley_scenes_completion[index_finding] = 1
                if self.orcish_valley_scenes_completion[4] == 1:
                    is_orcish_valley_finished = True
                    self.orcish_valley_scenes_completion = [0,0,0,0,0]
                #--- Temp ----:
        elif whose_winning == "enemy":
            if current_menu == GameLoopState.CryptsFighting:
                self.crypts_scenes_completion = [0,0,0]
            if current_menu == GameLoopState.OrcishValleyFighting:
                self.orcish_valley_scenes_completion = [0,0,0,0,0]
     
    def desired_bg_picking(self, assets, current_menu):
        if current_menu == GameLoopState.CryptsFighting:
            if self.crypts_scenes_completion[0] == 0:
                return assets.scaled_ud_0_bg
            elif self.crypts_scenes_completion[1] == 0:
                return assets.scaled_ud_1_bg
            elif self.crypts_scenes_completion[2] == 0:
                return assets.scaled_ud_4_bg
        elif current_menu == GameLoopState.OrcishValleyFighting:
            if self.orcish_valley_scenes_completion[0] == 0:
                return assets.scaled_orc_1_bg
            elif self.orcish_valley_scenes_completion[1] == 0:
                return assets.scaled_orc_2_bg
            elif self.orcish_valley_scenes_completion[2] == 0:
                return assets.scaled_orc_5_bg
            elif self.orcish_valley_scenes_completion[3] == 0:
                return assets.scaled_orc_4_bg
            elif self.orcish_valley_scenes_completion[4] == 0:
                return assets.scaled_orc_3_bg
    
    def desired_enemy_picking(self, assets, current_menu):
        if current_menu == GameLoopState.CryptsFighting:
            if self.crypts_scenes_completion[0] == 0:
                return assets.scaled_undead_1
            elif self.crypts_scenes_completion[1] == 0:
                return assets.scaled_undead_3
            elif self.crypts_scenes_completion[2] == 0:
                return assets.scaled_undead_2
        elif current_menu == GameLoopState.OrcishValleyFighting:
            if self.orcish_valley_scenes_completion[0] == 0:
                return assets.scaled_orc_1
            elif self.orcish_valley_scenes_completion[1] == 0:
                return assets.scaled_orc_2
            elif self.orcish_valley_scenes_completion[2] == 0:
                return assets.scaled_orc_3
            elif self.orcish_valley_scenes_completion[3] == 0:
                return assets.scaled_orc_4
            elif self.orcish_valley_scenes_completion[4] == 0:
                return assets.scaled_orc_5
    
    def returning_to_town_after_combat_conclusion(self):
        if self.combat_finished == True:
            return True
        else:
            return False

    def attack_turn_switching_inside_class(self, whose_move):
        if whose_move == "player":
            self.attack_turn_switch = True
        else:
            self.attack_turn_switch = False

    def main_game_loop_attack_turn_switcher(self):
        whose_turn = self.attack_turn_switch
        return whose_turn    
    
def exit_game_actions(screen, assets):
    screen.blit(assets.scaled_exit_game_bg[0], assets.scaled_exit_game_bg[1])
    pygame.display.flip()
    pygame.mixer.stop()
    time.sleep(1)
    pygame.quit()
    sys.exit()

def loading_screen(screen, mp, assets):
    screen.blit(assets.scaled_loading_bg[0], assets.scaled_loading_bg[1])
    text_loading.blit_text(screen, mp)
    pygame.display.flip()
    time.sleep(0.5)
#>>>>>> End - Custom Functions <<<<<<

#>>>>>> Custom Classes <<<<<<
class ScreenBlittedState:

    def __init__(self, screen, assets):
        self.screen = screen
        self.assets = assets
        self.back_text_for_many_places = MenuText("BACK", 170,720, assets.font_72)
        self.title_screen_text_items = [(MenuText("NEW GAME", 100,200, assets.font_72), GameLoopState.NewGame),
                                        (MenuText("??????????", 88,259, assets.font_72), GameLoopState.MainMenu), #Supose to be "LOAD GAME"
                                        (MenuText("ABOUT", 154,318, assets.font_72), GameLoopState.AboutGame),
                                        (MenuText("EXIT", 179,377, assets.font_72), GameLoopState.Exit)]
        self.new_game_screen_text_items = [(MenuText("START NEW GAME?", 33,200, assets.font_62), None), 
                                            (MenuText("YES", 191,259, assets.font_62), GameLoopState.TownMainMenu),
                                            (MenuText('NO', 204,318, assets.font_62), GameLoopState.MainMenu)]
        self.about_screen_text_items = [(MenuText("BACK", 180,540, assets.font_72), GameLoopState.MainMenu)]
        self.town_screen_text_items = [(MenuText("FACELESS MAN", 45,200, assets.font_72), GameLoopState.TownFacelessman), 
                                       (MenuText("BATTLE", 144,259, assets.font_72), GameLoopState.TownBattle), 
                                       (MenuText("CHARACTER", 81,318, assets.font_72), GameLoopState.TownCharacter), 
                                       (MenuText("SHOP", 168,378, assets.font_72), GameLoopState.TownShop), 
                                       (MenuText("MAIN MENU", 96,436, assets.font_72), GameLoopState.MainMenu)]
        self.facelessman_screen_text_items = [((self.back_text_for_many_places), GameLoopState.TownMainMenu)]
        self.battle_screen_text_items = [(MenuText("CRYPTS", 141,320, assets.font_72), GameLoopState.CryptsFighting), 
                                         (MenuText("ORCISH VALLEY", 38,379, assets.font_72), GameLoopState.OrcishValleyFighting), 
                                         (MenuText("FROZEN TUNDRA", 28,438, assets.font_72), GameLoopState.FrozenTundraFighting), 
                                         (MenuText("DEMON WORLD", 46,497, assets.font_72), GameLoopState.DemonWorldFighting),
                                         (self.back_text_for_many_places, GameLoopState.TownMainMenu),  
                                         (MenuText("??????", 150,379, assets.font_72), GameLoopState.TownBattle), 
                                         (MenuText("??????", 150,438, assets.font_72), GameLoopState.TownBattle), 
                                         (MenuText("??????", 150,497, assets.font_72), GameLoopState.TownBattle)]
        self.character_screen_text_items = [(MenuText("STATS", 187,370, assets.font_50), None), 
                                            (MenuText("LEVEL", 60,416, assets.font_40), None), 
                                            (MenuText("EXP", 60,447, assets.font_40), None), 
                                            (MenuText("HEALTH", 60,478, assets.font_40), None), 
                                            (MenuText("DAMAGE", 60,509, assets.font_40), None), 
                                            (MenuText("DEFENCE", 60,540, assets.font_40), None), 
                                            (MenuText("FREE POINTS", 60,571, assets.font_40), None), 
                                            (MenuText("VITALITY", 60,602, assets.font_40), None), 
                                            (MenuText("STRENGTH", 60,633, assets.font_40), None), 
                                            ((self.back_text_for_many_places), GameLoopState.TownMainMenu)]
        self.shop_screen_text_items = [((self.back_text_for_many_places), GameLoopState.TownMainMenu)]

    #Method which goes thought the lists of texts and blits them:
    def blit_text_items(self, text_items, mp):
        for (text_item, _) in text_items:
            text_item.blit_text(self.screen, mp)

    def title_screen_blit(self, mp):
            screen.blit(self.assets.scaled_main_menu_bg[0], self.assets.scaled_main_menu_bg[1]) #Background
            self.blit_text_items(self.title_screen_text_items, mp) #Texts
    
    def new_game_confirmation_screen_blit(self, mp):
        screen.blit(self.assets.scaled_main_menu_bg[0], self.assets.scaled_main_menu_bg[1]) #Background
        self.blit_text_items(self.new_game_screen_text_items, mp) #Texts
    
    def about_screen_blit(self, mp):
        screen.blit(self.assets.scaled_about_bg[0], self.assets.scaled_about_bg[1]) #Background
        self.blit_text_items(self.about_screen_text_items, mp) #Texts
    
    def town_screen_blit(self, mp):
        screen.blit(self.assets.scaled_town_bg_1[0], self.assets.scaled_town_bg_1[1]) #Background
        self.blit_text_items(self.town_screen_text_items, mp) #Texts

    def facelessman_screen_blit(self, mp):
        screen.blit(self.assets.scaled_faceless_man_bg[0], self.assets.scaled_faceless_man_bg[1]) #Background
        self.blit_text_items(self.facelessman_screen_text_items, mp) #Texts
    
    def battle_screen_blit(self, mp):
        #--- Background
        screen.blit(self.assets.scaled_gate_guard_bg[0], self.assets.scaled_gate_guard_bg[1])
        #--- Crypts
        self.battle_screen_text_items[0][0].blit_text(self.screen, mp)
        #--- Orcish Valley
        if is_crypts_finished == True:  
            self.battle_screen_text_items[1][0].blit_text(self.screen, mp)
        else:
            self.battle_screen_text_items[5][0].blit_text(self.screen, mp)
        #--- Frozen Tundra
        if is_orcish_valley_finished == True:
            self.battle_screen_text_items[2][0].blit_text(self.screen, mp)
        else:
            self.battle_screen_text_items[6][0].blit_text(self.screen, mp)
        #--- Demon World
        if is_frozen_tundra_finished == True:
            self.battle_screen_text_items[3][0].blit_text(self.screen, mp)
        else:
            self.battle_screen_text_items[7][0].blit_text(self.screen, mp)
        #--- Back
        self.battle_screen_text_items[4][0].blit_text(self.screen, mp)

    def character_screen_blit(self, mp):
        screen.blit(self.assets.scaled_human_3_bg[0], self.assets.scaled_human_3_bg[1]) #Backgrounds
        self.blit_text_items(self.character_screen_text_items, mp) #Texts
    
    def shop_screen_blit(self, mp):
        screen.blit(self.assets.scaled_shop_bg[0], self.assets.scaled_shop_bg[1]) #Backgrounds
        self.blit_text_items(self.shop_screen_text_items, mp) #Texts

class MenuText:
    
    def __init__(self, text, xPos, yPos, font):
        self.colorBlack = (0,0,0)
        self.colorWhite = (255,255,255)
        self.colorRed = (255,0,0)
        self.font = font
        self.text_shadow = self.colorBlack
        self.text_white = self.colorWhite
        self.text_red = self.colorRed
        #Making text with different colors:
        self.text_shadow = self.font.render(text, True, self.colorBlack), (xPos+2,yPos+2)
        self.text_white = self.font.render(text, True, self.colorWhite), (xPos,yPos)
        self.text_red = self.font.render(text, True, self.colorRed), (xPos,yPos)
        #getting text rect value:
        text_rect = self.text_white[0].get_rect()
        #calculating range values for x and y:
        self.xPos_r = (xPos, (xPos + text_rect[2]))
        self.yPos_r = (yPos, (yPos + text_rect[3]))

    def blit_text(self, screen, mp):
        #blitting text
        self.blit_shadow = screen.blit(self.text_shadow[0], self.text_shadow[1])
        self.blit_white = screen.blit(self.text_white[0], self.text_white[1])
        if self.is_mouse_over(mp): #checking if mouse is over text
            screen.blit(self.text_red[0], self.text_white[1]) #if True, bliting red text over white
    
    def is_mouse_over(self, mp):
        return (mp[0] in range(self.xPos_r[0], self.xPos_r[1]) and mp[1] in range(self.yPos_r[0], self.yPos_r[1]))

class GameLoopState(Enum):
    #Main Menu loop:
    MainMenu = auto()
    NewGame = auto()
    LoadGame = auto()
    AboutGame = auto()
    Exit = auto()
    #Town loops:
    TownMainMenu = auto()
    TownFacelessman = auto()
    TownBattle = auto()
    TownCharacter = auto()
    TownShop = auto()
    #Fighting loops:
    CryptsFighting = auto()
    OrcishValleyFighting = auto()
    FrozenTundraFighting = auto()
    DemonWorldFighting = auto()

class Assets:

    def __init__(self):
        self.fonts_init()
        self.sounds_init()
        self.background_imgs_init()
        self.background_imgs_size_change()
        self.character_imgs_init()
        self.character_imgs_size_change()
        self.attack_effect_imgs_init_and_size_change()

    def fonts_init(self):
        #Fonts:
        self.text_font_72 = pygame.font.Font(None, 72)
        self.text_font_62 = pygame.font.Font(None, 62)
        self.text_font_50 = pygame.font.Font(None, 50)
        self.text_font_40 = pygame.font.Font(None, 40)
        self.text_font_30 = pygame.font.Font(None, 30)
        self.text_font_20 = pygame.font.Font(None, 20)

        self.font_72 = pygame.font.Font(None, 72)
        self.font_62 = pygame.font.Font(None, 62)
        self.font_50 = pygame.font.Font(None, 50)
        self.font_40 = pygame.font.Font(None, 40)
    
    def sounds_init(self):
        self.town_music = pygame.mixer.Sound('assets/music/town_music.wav')
        self.main_menu_music = pygame.mixer.Sound('assets/music/main_menu_loop.mp3')
        self.sound_sword_slash = pygame.mixer.Sound('assets/music/sword_slash.mp3')
        self.sound_leveling_up = pygame.mixer.Sound('assets/music/leveling_up.wav')

    def background_imgs_init(self):
        #Backgrounds:
        self.raw_main_menu_bg = pygame.image.load('assets/painted/main_menu_1.jpg')
        self.raw_exit_game_bg = pygame.image.load('assets/painted/main_menu_0.jpg')
        self.raw_about_bg = pygame.image.load('assets/painted/about_game.jpg')
        self.raw_town_bg_1 = pygame.image.load('assets/painted/town_1.jpg')
        self.raw_loading_bg = pygame.image.load('assets/painted/loading_bg.jpg')
        self.raw_music_on_bg = pygame.image.load('assets/music/music_on.png')
        self.raw_music_off_bg = pygame.image.load('assets/music/music_off.png')
        self.raw_faceless_man_bg = pygame.image.load('assets/painted/faceless_man.jpg')
        self.raw_gate_guard_magic_ball_bg = pygame.image.load('assets/painted/gate_guard_magic_ball.jpg')
        self.raw_shop_bg = pygame.image.load('assets/painted/shop_0.jpg')
        self.raw_portal_0_bg = pygame.image.load('assets/painted/portal_0.jpg')
        self.raw_portal_1_bg = pygame.image.load('assets/painted/portal_1.jpg')
        self.raw_portal_2_bg = pygame.image.load('assets/painted/portal_2.jpg')
        self.raw_portal_3_bg = pygame.image.load('assets/painted/portal_3.jpg')
        self.raw_human_3_bg = pygame.image.load('assets/painted/human_3_bg.png')
        #--- For Crypts
        self.raw_ud_0_bg = pygame.image.load('assets/painted/ud_bg_0.jpg')
        self.raw_ud_1_bg = pygame.image.load('assets/painted/ud_bg_1.jpg')
        self.raw_ud_4_bg = pygame.image.load('assets/painted/ud_bg_4.jpg')
        #--- For Orcish Valley:
        self.raw_orc_1_bg = pygame.image.load('assets/painted/orc_bg_0.jpg')
        self.raw_orc_2_bg = pygame.image.load('assets/painted/orc_bg_1.jpg')
        self.raw_orc_3_bg = pygame.image.load('assets/painted/orc_bg_2.jpg')
        self.raw_orc_4_bg = pygame.image.load('assets/painted/orc_bg_3.jpg')
        self.raw_orc_5_bg = pygame.image.load('assets/painted/orc_bg_4.jpg')

    def background_imgs_size_change(self):
        #>>>>>> Rescaling: <<<<<<
        self.scaled_main_menu_bg = self.scaling_bg_images(self.raw_main_menu_bg)
        self.scaled_exit_game_bg = self.scaling_bg_images(self.raw_exit_game_bg)
        self.scaled_about_bg = self.scaling_bg_images(self.raw_about_bg)
        self.scaled_town_bg_1 = self.scaling_bg_images(self.raw_town_bg_1)
        self.scaled_loading_bg = self.scaling_bg_images(self.raw_loading_bg)
        self.scaled_faceless_man_bg = self.scaling_bg_images(self.raw_faceless_man_bg)
        self.scaled_gate_guard_bg = self.scaling_bg_images(self.raw_gate_guard_magic_ball_bg)
        self.scaled_shop_bg = self.scaling_bg_images(self.raw_shop_bg)
        self.scaled_portal_0_bg = self.scaling_bg_images(self.raw_portal_0_bg)
        self.scaled_portal_1_bg = self.scaling_bg_images(self.raw_portal_1_bg)
        self.scaled_portal_2_bg = self.scaling_bg_images(self.raw_portal_2_bg)
        self.scaled_portal_3_bg = self.scaling_bg_images(self.raw_portal_3_bg)
        self.scaled_human_3_bg = self.scaling_bg_images(self.raw_human_3_bg)
        #--- For Crypts:
        self.scaled_ud_0_bg = self.scaling_bg_images(self.raw_ud_0_bg)
        self.scaled_ud_1_bg = self.scaling_bg_images(self.raw_ud_1_bg)
        self.scaled_ud_4_bg = self.scaling_bg_images(self.raw_ud_4_bg)
        #--- For Orcish Valley:
        self.scaled_orc_1_bg = self.scaling_bg_images(self.raw_orc_1_bg)
        self.scaled_orc_2_bg = self.scaling_bg_images(self.raw_orc_2_bg)
        self.scaled_orc_3_bg = self.scaling_bg_images(self.raw_orc_3_bg)
        self.scaled_orc_4_bg = self.scaling_bg_images(self.raw_orc_4_bg)
        self.scaled_orc_5_bg = self.scaling_bg_images(self.raw_orc_5_bg)

    def character_imgs_init(self):
        #--- Player:
        self.raw_player_char = pygame.image.load('assets/painted/transparent/human_3_trans.png')
        #--- For Crypts:
        self.raw_undead_1 = pygame.image.load('assets/painted/transparent/undead_0.png')
        self.raw_undead_2 = pygame.image.load('assets/painted/transparent/undead_1.png')
        self.raw_undead_3 = pygame.image.load('assets/painted/transparent/undead_2.png')
        #--- For Orcish Valley:
        self.raw_orc_1 = pygame.image.load('assets/painted/transparent/orc_0.png')
        self.raw_orc_2 = pygame.image.load('assets/painted/transparent/orc_1.png')
        self.raw_orc_3 = pygame.image.load('assets/painted/transparent/orc_2.png')
        self.raw_orc_4 = pygame.image.load('assets/painted/transparent/orc_3.png')
        self.raw_orc_5 = pygame.image.load('assets/painted/transparent/orc_4.png')
        self.raw_orc_6 = pygame.image.load('assets/painted/transparent/orc_5.png')

    def character_imgs_size_change(self):
        #>>>>>> Rescaling: <<<<<<
        self.scaled_player_char = self.scaling_most_characters(self.raw_player_char)
        #--- For Crypts
        self.scaled_undead_1 = self.scaling_most_characters(self.raw_undead_1)
        self.scaled_undead_2 = self.scaling_most_characters(self.raw_undead_2)
        self.scaled_undead_3 = self.scaling_most_characters(self.raw_undead_3)
        #--- For Orcish Valley:
        self.scaled_orc_1 = self.scaling_most_characters(self.raw_orc_1)
        self.scaled_orc_2 = self.scaling_most_characters(self.raw_orc_2)
        self.scaled_orc_3 = self.scaling_most_characters(self.raw_orc_3)
        self.scaled_orc_4 = self.scaling_most_characters(self.raw_orc_4)
        self.scaled_orc_5 = self.scaling_most_characters(self.raw_orc_5)
        self.scaled_orc_6 = self.scaling_most_characters(self.raw_orc_6)

    def attack_effect_imgs_init_and_size_change(self):
        #--- Attacks:
        self.raw_player_attack_slash = pygame.image.load('assets/painted/transparent/slash_on_enemy_trans.png')
        self.raw_enemy_attack_slash = pygame.image.load('assets/painted/transparent/slash_on_player_trans.png')
        self.raw_savage_attack = pygame.image.load('assets/painted/transparent/slash_attack.png')

        #>>>>>> Size change: <<<<<<
        self.scaled_player_attack_slash = pygame.transform.scale(self.raw_player_attack_slash, (150,89))
        self.scaled_enemy_attack_slash = pygame.transform.scale(self.raw_enemy_attack_slash, (150,89))
        self.scaled_slash_attack = pygame.transform.scale(self.raw_savage_attack, (130,168)) #blit it at (53,499)

    def scaling_bg_images(self, image):
        new_size = (480,784)
        changed_size = pygame.transform.scale(image, new_size)
        image_rect = changed_size.get_rect()
        new_size_and_rect_in_a_lists = [changed_size, image_rect]
        return new_size_and_rect_in_a_lists
    
    def scaling_most_characters(self, img):
        new_size = (200, 327)
        changed_size = pygame.transform.scale(img, new_size)
        image_rect = changed_size.get_rect()
        new_size_and_rect_in_a_lists = [changed_size, image_rect]
        return new_size_and_rect_in_a_lists

#>>>>>> End - Custom Classes <<<<<< 

#>>>>>> Game Progresion Switches <<<<<<
is_crypts_finished = False
is_orcish_valley_finished = False
is_frozen_tundra_finished = False
is_demon_world_finished = False
attack_turn = 0
#>>>>>> End - Game Progresion Switches <<<<<<  

#>>>>>> Instances <<<<<<
assets = Assets()
state = ScreenBlittedState(screen, assets)
combat_instance = Combat(screen, enemy_current_hp, 
                        hero_current_hp, hero_damage, enemy_damage, hero_defence, enemy_defence, 
                        assets.scaled_player_attack_slash, assets.scaled_enemy_attack_slash, hero_total_hp, enemy_total_hp,
                        is_crypts_finished, is_orcish_valley_finished, assets)
#>>>>>> End - Instances <<<<<<

#>>>>>> Texts: <<<<<<
#Creating texts, setting coordinates and fonts:
#-!- Back -> for general use
text_back = MenuText("BACK", 170,720, assets.font_72)
#--- Loading..
text_loading = MenuText("LOADING..", 10, 726, assets.font_72)
#--- Hero Health bar
text_hero_current_hp = MenuText("HERO HP", 58,20, assets.font_40)
#--- Enemey Health bar
text_enemy_current_hp = MenuText("ENEMY HP", 285,20, assets.font_40)
#Getting text rect size example:
#test = assets.font_72.render("ORCISH VALLEY", True, (color_black))
#print(test.get_size())
#>>>>>> End - Texts <<<<<<

#>>>>>> Loops <<<<<<
#Main loop:
program_running_loop = True
#Music on/off:
music_playing = True
#Game menu/scenes changing/control:
current_menu = GameLoopState.MainMenu
#>>>>>> End - Loops <<<<<<

#>>>>>> Time/FPS tracking/settting <<<<<<
my_event = pygame.USEREVENT + 1
#counts game "fps":
pygame.time.set_timer(my_event, 5)
start_time = pygame.time.get_ticks()
#>>>>>> End - Time/FPS tracking/settting <<<<<<

#>>>>>> Programs logic Loop <<<<<<
while program_running_loop:
    #---- Music ----
    if music_playing == True:
        if current_menu == GameLoopState.TownMainMenu:
            assets.town_music.set_volume(0.1)
            assets.town_music.play(-1)
        #elif current_menu == GameLoopState.TownMainMenu:
        #    main_menu_music.set_volume(0.1)
        #    main_menu_music.play(-1)
    for event in pygame.event.get():
        #Constant mouse position tracking:
        mouse_hovering_pos = pygame.mouse.get_pos()
        mp = mouse_hovering_pos
        current_time = pygame.time.get_ticks()
        if event.type == pygame.QUIT:
            exit_game_actions(screen, assets)
        elif current_menu == GameLoopState.Exit:
            exit_game_actions(screen, assets)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            exit_game_actions(screen, assets)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #Mouse clicks tracking:
            m_c_p = pygame.mouse.get_pos()
            #---- Music/Sound mute buttons:
            if music_playing == True:
                if m_c_p[0] in range(0,50) and m_c_p[1] in range(0,50):
                    music_playing = False
                    pygame.mixer.pause()
            elif music_playing == False:
                if m_c_p[0] in range(0,50) and m_c_p[1] in range(0,50):
                    music_playing = True
                    pygame.mixer.unpause()
            #>>>>>> Main Menu screen clicking <<<<<< ----------------------------------
            if current_menu == GameLoopState.MainMenu:
                for (text_item, menu_state) in state.title_screen_text_items:
                    if text_item.is_mouse_over(m_c_p):
                        current_menu = menu_state
            #---- New Game Y/N confirmation screen ----
            elif current_menu == GameLoopState.NewGame:
                for (text_item, menu_state) in state.new_game_screen_text_items:
                    if text_item.is_mouse_over(m_c_p):
                        current_menu = menu_state
            #---- About screen ----        
            elif current_menu == GameLoopState.AboutGame:
                for (text_item, menu_state) in state.about_screen_text_items:
                    if text_item.is_mouse_over(m_c_p):
                        current_menu = menu_state
            #>>>>>> Town Screen clicking <<<<<< ---------------------------------------
            elif current_menu == GameLoopState.TownMainMenu:
                for (text_item, menu_state) in state.town_screen_text_items:
                    if text_item.is_mouse_over(m_c_p):
                        current_menu = menu_state
            #--- Faceless Man screen clicking ---
            elif current_menu == GameLoopState.TownFacelessman:
                for (text_item, menu_state) in state.facelessman_screen_text_items:
                    if text_item.is_mouse_over(m_c_p):
                        current_menu = menu_state
            #--- Battle screen clicking: ---
            elif current_menu == GameLoopState.TownBattle:
                for (text_item, menu_state) in state.battle_screen_text_items[:5]:
                    if text_item.is_mouse_over(m_c_p):
                        if menu_state == GameLoopState.OrcishValleyFighting and is_crypts_finished == False:
                            current_menu = GameLoopState.TownBattle
                        elif menu_state == GameLoopState.FrozenTundraFighting and is_orcish_valley_finished == False:
                            current_menu = GameLoopState.TownBattle
                        elif menu_state == GameLoopState.DemonWorldFighting and is_frozen_tundra_finished == False:
                            current_menu = GameLoopState.TownBattle
                        else:
                            current_menu = menu_state
                combat_instance.update(mp, current_menu)
            #--- Character screen clicking: ---
            elif current_menu == GameLoopState.TownCharacter:
                for (text_item, menu_state) in state.character_screen_text_items:
                    if text_item.is_mouse_over(m_c_p):
                        current_menu = menu_state
            #--- Shop screen clicking ---
            elif current_menu == GameLoopState.TownShop:
                for (text_item, menu_state) in state.shop_screen_text_items:
                    if text_item.is_mouse_over(m_c_p):
                        current_menu = menu_state
        #--- All fights logic and blitting -----------------------------------------------<<<<<<
        if event.type == my_event:
            #--- Crypts fighting ---
            if current_menu == GameLoopState.CryptsFighting or current_menu == GameLoopState.OrcishValleyFighting:
                if (current_time - start_time) >= 5:
                    #resseting start time value:
                    start_time = pygame.time.get_ticks()    
                    if combat_instance.main_game_loop_attack_turn_switcher() == False:
                        combat_instance.all_characters_combat_movement_blitting('player')
                        if combat_instance.returning_to_town_after_combat_conclusion() == True:
                            current_menu = GameLoopState.TownMainMenu                    
                    elif combat_instance.main_game_loop_attack_turn_switcher() == True:
                        combat_instance.all_characters_combat_movement_blitting('enemy')
                        if combat_instance.returning_to_town_after_combat_conclusion() == True:
                            current_menu = GameLoopState.TownMainMenu
    redraw_screen(current_menu, music_playing, screen, mp, assets, state)
    pygame.display.flip()
#>>>>>> End - Programs logic Loop <<<<<<
