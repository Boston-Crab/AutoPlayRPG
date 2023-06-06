#The Main Menu of the game
import sys
import pygame
import time
import pygame.mixer
from enum import Enum

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
crypts_scenes_completion = [0,0,0]
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
def scaling_bg_images(image):
    new_size = (480,784)
    changed_size = pygame.transform.scale(image, new_size)
    image_rect = changed_size.get_rect()
    new_size_and_rect_in_a_lists = [changed_size, image_rect]
    return new_size_and_rect_in_a_lists

def scaling_most_characters(img):
    new_size = (200, 327)
    changed_size = pygame.transform.scale(img, new_size)
    image_rect = changed_size.get_rect()
    new_size_and_rect_in_a_lists = [changed_size, image_rect]
    return new_size_and_rect_in_a_lists

def back_text_screen_blitting(screen, mp):
    text_back.blit_text(screen, mp)

def redraw_screen(current_menu, music_playing, screen, mp):
    state = ScreenBlittedState(screen, mp)
    #Title screen:
    if current_menu == GameLoopState.MainMenu:
        state.title_screen_blit()            
    #New game confirmation screen:
    elif current_menu == GameLoopState.NewGame:
        state.new_game_confirmation_screen_blit()
    #About screen:
    elif current_menu == GameLoopState.AboutGame:
        state.about_screen_blit()
    #Town screen:
    elif current_menu == GameLoopState.TownMainMenu:
        state.town_screen_blit()
    #Faceless Man Screen:
    elif current_menu == GameLoopState.TownFacelessman:
        state.facelessman_screen_blit()
    #Battle screen:
    elif current_menu == GameLoopState.TownBattle:
        state.battle_screen_blit()   
    #Character screen
    elif current_menu == GameLoopState.TownCharacter:
        state.character_screen_blit()
    #Shop screen
    elif current_menu == GameLoopState.TownShop:
        state.shop_screen_blit()
    #Crypts fighting scenes:
    elif current_menu == GameLoopState.CryptsFighting:
        if crypts_scenes_completion[0] == 0:
            combat_scene_loops(mp, screen, scaled_ud_0_bg, scaled_undead_1, current_menu)
        elif crypts_scenes_completion[1] == 0:
            combat_scene_loops(mp, screen, scaled_ud_1_bg, scaled_undead_3, current_menu)
        elif crypts_scenes_completion[2] == 0:
            combat_scene_loops(mp, screen, scaled_ud_4_bg, scaled_undead_2, current_menu)
    #Orcish Valley fighting scenes:       
    elif current_menu == GameLoopState.OrcishValleyFighting:
        if orcish_valley_scenes_completion[0] == 0:
            combat_scene_loops(mp, screen, scaled_orc_1_bg, scaled_orc_1, current_menu)
        elif orcish_valley_scenes_completion[1] == 0:
            combat_scene_loops(mp, screen, scaled_orc_2_bg, scaled_orc_2, current_menu)
        elif orcish_valley_scenes_completion[2] == 0:
            combat_scene_loops(mp, screen, scaled_orc_3_bg, scaled_orc_5, current_menu)
        elif orcish_valley_scenes_completion[3] == 0:
            combat_scene_loops(mp, screen, scaled_orc_4_bg, scaled_orc_4, current_menu)
        elif orcish_valley_scenes_completion[4] == 0:
            combat_scene_loops(mp, screen, scaled_orc_5_bg, scaled_orc_3, current_menu)
    #Music buttons:
    if music_playing == True:
        screen.blit(raw_music_on_bg, (r_0_0))
    elif music_playing == False:
        screen.blit(raw_music_off_bg, (r_0_0))

def victory_blitting():
    red_bar_x = 150
    red_bar_y = 200
    red_bar_width = 200
    red_bar_height = 10
    pygame.draw.rect(screen, color_yellow, [red_bar_x-2, red_bar_y-2, red_bar_width+4, red_bar_height+4], 2)
    pygame.draw.rect(screen, color_green, [red_bar_x, red_bar_y, red_bar_width, red_bar_height])
    text_victory = font_62.render("VICTORY", True, color_white)
    text_victory_black = font_62.render("VICTORY", True, color_black)
    screen.blit(text_victory_black, (157,222))
    screen.blit(text_victory, (155,220))
    pygame.draw.rect(screen, color_yellow, [red_bar_x-2, red_bar_y+66, red_bar_width+4, red_bar_height+4], 2)
    pygame.draw.rect(screen, color_green, [red_bar_x, red_bar_y+68, red_bar_width, red_bar_height])
    pygame.display.flip()

def hp_bar_blitting():
    global color_black, color_red, screen, hero_current_hp, enemy_current_hp, hero_total_hp, enemy_total_hp
    #--- Player HP Bar coordinates:
    player_hp_bar_x = 30
    player_hp_bar_y = 50
    hp_bar_width = 180
    hp_bar_height = 20
    #--- Player HP calculation:
    hero_hp_percent = hero_current_hp / hero_total_hp
    #--- Enemy HP Bar coordinates:
    enemy_hp_bar_x = 270
    enemy_hp_bar_y = 50
    hp_bar_width = 180
    hp_bar_height = 20
    #--- Enemy HP calculation:
    enemy_hp_percent = enemy_current_hp / enemy_total_hp

    #------------------------------------------------------------------
    #--- Player HP Bar Border:
    pygame.draw.rect(screen, color_black, [player_hp_bar_x, player_hp_bar_y, hp_bar_width, hp_bar_height], 2)
    #--- Player HP:
    pygame.draw.rect(screen, color_red, [player_hp_bar_x + 2, player_hp_bar_y + 2, hero_hp_percent * (hp_bar_width - 4), hp_bar_height - 4])
    #--- Player HP number representation:
    text_player_hp_bar_numbers = text_font_30.render((str(hero_current_hp)+"/"+str(hero_total_hp)), True, (color_white))
    text_player_hp_bar_numbers_border = text_font_30.render((str(hero_current_hp)+"/"+str(hero_total_hp)), True, (color_black))
    screen.blit(text_player_hp_bar_numbers_border, (31,71))
    screen.blit(text_player_hp_bar_numbers, (30,70))

    #------------------------------------------------------------------
    #--- Enemy HP Bar Border:
    pygame.draw.rect(screen, color_black, [enemy_hp_bar_x, enemy_hp_bar_y, hp_bar_width, hp_bar_height], 2)
    #--- Enemy HP:
    pygame.draw.rect(screen, color_red, [enemy_hp_bar_x + 2, enemy_hp_bar_y + 2, enemy_hp_percent * (hp_bar_width - 4), hp_bar_height - 4])
    #--- Enemy HP number representation:
    text_enemy_hp_bar_numbers = text_font_30.render((str(enemy_current_hp)+"/"+str(enemy_total_hp)), True, (color_white))
    text_enemy_hp_bar_numbers_border = text_font_30.render((str(enemy_current_hp)+"/"+str(enemy_total_hp)), True, (color_black))
    screen.blit(text_enemy_hp_bar_numbers_border, (271,71))
    screen.blit(text_enemy_hp_bar_numbers, (270,70))

def damage_numbers_appearing(whose_dmg, whose_def, dmg_num_x, dmg_num_y):
    damage_to_do = whose_dmg - whose_def
    if damage_to_do <= 0:
            damage_to_do = 0
    text_damage_number_border = text_font_40.render(("-"+str(damage_to_do)), True, (color_black))
    screen.blit(text_damage_number_border, (dmg_num_x +1, dmg_num_y +1))
    text_damage_number = text_font_40.render(("-"+str(damage_to_do)), True, (color_red))
    screen.blit(text_damage_number, (dmg_num_x, dmg_num_y))

def updating_game_progress_after_fight_outcome(whose_winning, current_menu):
    global enemy_current_hp, crypts_scenes_completion, is_crypts_finished
    global is_orcish_valley_finished, orcish_valley_scenes_completion
    if whose_winning == "player":
        if current_menu == GameLoopState.CryptsFighting:
            index_finding = crypts_scenes_completion.index(0)
            crypts_scenes_completion[index_finding] = 1
            if crypts_scenes_completion[2] == 1:
                is_crypts_finished = True
                crypts_scenes_completion = [0,0,0]
        elif current_menu == GameLoopState.OrcishValleyFighting:
            index_finding = orcish_valley_scenes_completion.index(0)
            orcish_valley_scenes_completion[index_finding] = 1
            if orcish_valley_scenes_completion[4] == 1:
                is_orcish_valley_finished = True
                orcish_valley_scenes_completion = [0,0,0,0,0]
            #--- Temp ----:
            enemy_current_hp = 50
    elif whose_winning == "enemy":
        if current_menu == GameLoopState.CryptsFighting:
            crypts_scenes_completion = [0,0,0]
        if current_menu == GameLoopState.OrcishValleyFighting:
            orcish_valley_scenes_completion = [0,0,0,0,0]

def combat_scene_loops(mp, screen, desired_bg, desired_enemy, current_menu):
    global enemy_current_hp, enemy_damage, hero_current_hp, hero_damage, hero_defence
    fight = True
    i = 0
    while fight:
        screen.blit(desired_bg[0], desired_bg[1])
        screen.blit(scaled_player_char[0], (0,458))
        screen.blit(desired_enemy[0], (280,457))
        #Player attacks:
        for i in range(81):
            screen.blit(desired_bg[0], desired_bg[1])
            #--- HP Bar Blitting:
            text_hero_current_hp.blit_text(screen, mp)
            text_enemy_current_hp.blit_text(screen, mp)
            hp_bar_blitting()
            #--------------------
            screen.blit(desired_enemy[0], (280,457))
            screen.blit(scaled_player_char[0], ((0+i),458))
            i = i +20
            pygame.display.flip()
            time.sleep(0.002)
        screen.blit(scaled_player_attack_slash, (276,533))
        #Enemy HP counting:
        enemy_current_hp = enemy_current_hp - hero_damage
        #------------------
        pygame.display.flip()
        pygame.mixer.Channel(0).play(pygame.mixer.Sound(sound_sword_slash))
        time.sleep(0.07)

        #Player goes back:
        #--- damage number coordinates:
        hero_dmg_num_x = 330
        hero_dmg_num_y = 420
        for i in range(81):    
            screen.blit(desired_bg[0], desired_bg[1])
            damage_numbers_appearing(hero_damage, enemy_defence, hero_dmg_num_x, hero_dmg_num_y)
            hero_dmg_num_y = hero_dmg_num_y - 1
            #--- HP Bar Blitting:
            text_hero_current_hp.blit_text(screen, mp)
            text_enemy_current_hp.blit_text(screen, mp)
            hp_bar_blitting()
            #--------------------
            screen.blit(desired_enemy[0], (280,457))
            screen.blit(scaled_player_char[0], (80-i,458))
            i = i +20
            pygame.display.flip()
            time.sleep(0.002)
        #--- Player Win Checking:
        if enemy_current_hp <= 0:
            print("Player Wins")
            pygame.mixer.Channel(0).stop()
            victory_blitting()
            pygame.mixer.Channel(1).play(pygame.mixer.Sound(sound_leveling_up))
            time.sleep(3)
            updating_game_progress_after_fight_outcome("player", current_menu)
            current_menu = GameLoopState.TownMainMenu
            fight = False
            break
        #-----------------------------------------------------------------------
        #Enemy attacks:
        for i in range(81):
            screen.blit(desired_bg[0], desired_bg[1])
            text_hero_current_hp.blit_text(screen, mp)
            text_enemy_current_hp.blit_text(screen, mp)
            hp_bar_blitting()
            screen.blit(desired_enemy[0], (280-i,457))
            screen.blit(scaled_player_char[0], (0,458))
            i = i +20
            pygame.display.flip()
            time.sleep(0.002)
        screen.blit(scaled_enemy_attack_slash, (67,534))
        pygame.display.flip()
        pygame.mixer.Channel(0).play(pygame.mixer.Sound(sound_sword_slash))
        #Player HP counting:
        hero_current_hp = hero_current_hp - (enemy_damage - hero_defence)
        #------------------
        time.sleep(0.07)

        #Enemy goes back:
        #--- damage number coordinates:
        enemy_dmg_num_x = 150
        enemy_dmg_num_y = 420
        for i in range(81):
            screen.blit(desired_bg[0], desired_bg[1])
            damage_numbers_appearing(enemy_damage, hero_defence, enemy_dmg_num_x, enemy_dmg_num_y)
            enemy_dmg_num_y = enemy_dmg_num_y - 1
            #--- HP Bar Blitting:
            text_hero_current_hp.blit_text(screen, mp)
            text_enemy_current_hp.blit_text(screen, mp)
            hp_bar_blitting()
            #--- End ---
            screen.blit(desired_enemy[0], (200+i,457))
            screen.blit(scaled_player_char[0], (0,458))
            i = i +20
            pygame.display.flip()
            time.sleep(0.002)
        #--- Enemy Win Checking:
        if hero_current_hp <= 0:
            print("Enemy Wins")
            pygame.mixer.Channel(0).stop()
            updating_game_progress_after_fight_outcome("enemy", current_menu)
            print(crypts_scenes_completion)
            current_menu = GameLoopState.TownMainMenu
            fight = False
            break      
    
def exit_game_actions(screen):
    screen.blit(scaled_exit_game_bg[0], scaled_exit_game_bg[1])
    pygame.display.flip()
    pygame.mixer.stop()
    time.sleep(1)
    pygame.quit()
    sys.exit()

def loading_screen(screen, mp):
    screen.blit(scaled_loading_bg[0], scaled_loading_bg[1])
    text_loading.blit_text(screen, mp)
    pygame.display.flip()
    time.sleep(0.5)
#>>>>>> End - Custom Functions <<<<<<

#>>>>>> Sounds <<<<<<
town_music = pygame.mixer.Sound('assets/music/town_music.wav')
main_menu_music = pygame.mixer.Sound('assets/music/main_menu_loop2.wav')
sound_sword_slash = pygame.mixer.Sound('assets/music/sword_slash.mp3')
sound_leveling_up = pygame.mixer.Sound('assets/music/leveling_up.wav')
#>>>>>> End - Sounds <<<<<<

#>>>>>> Images <<<<<<
#--- Loading: ---
#Backgrounds:
raw_main_menu_bg = pygame.image.load('assets/painted/main_menu_1.jpg')
raw_exit_game_bg = pygame.image.load('assets/painted/main_menu_0.jpg')
raw_about_bg = pygame.image.load('assets/painted/about_game.jpg')
raw_town_bg_1 = pygame.image.load('assets/painted/town_1.jpg')
raw_loading_bg = pygame.image.load('assets/painted/loading_bg.jpg')
raw_music_on_bg = pygame.image.load('assets/music/music_on.png')
raw_music_off_bg = pygame.image.load('assets/music/music_off.png')
raw_faceless_man_bg = pygame.image.load('assets/painted/faceless_man.jpg')
raw_gate_guard_magic_ball_bg = pygame.image.load('assets/painted/gate_guard_magic_ball.jpg')
raw_shop_bg = pygame.image.load('assets/painted/shop_0.jpg')
raw_portal_0_bg = pygame.image.load('assets/painted/portal_0.jpg')
raw_portal_1_bg = pygame.image.load('assets/painted/portal_1.jpg')
raw_portal_2_bg = pygame.image.load('assets/painted/portal_2.jpg')
raw_portal_3_bg = pygame.image.load('assets/painted/portal_3.jpg')
raw_human_3_bg = pygame.image.load('assets/painted/human_3_bg.png')
#--- For Crypts
raw_ud_0_bg = pygame.image.load('assets/painted/ud_bg_0.jpg')
raw_ud_1_bg = pygame.image.load('assets/painted/ud_bg_1.jpg')
raw_ud_4_bg = pygame.image.load('assets/painted/ud_bg_4.jpg')
#--- For Orcish Valley:
raw_orc_1_bg = pygame.image.load('assets/painted/orc_bg_0.jpg')
raw_orc_2_bg = pygame.image.load('assets/painted/orc_bg_1.jpg')
raw_orc_3_bg = pygame.image.load('assets/painted/orc_bg_2.jpg')
raw_orc_4_bg = pygame.image.load('assets/painted/orc_bg_3.jpg')
raw_orc_5_bg = pygame.image.load('assets/painted/orc_bg_4.jpg')
#Characters:
raw_player_char = pygame.image.load('assets/painted/transparent/human_3_trans.png')
#--- For Crypts:
raw_undead_1 = pygame.image.load('assets/painted/transparent/undead_0.png')
raw_undead_2 = pygame.image.load('assets/painted/transparent/undead_1.png')
raw_undead_3 = pygame.image.load('assets/painted/transparent/undead_2.png')
#--- For Orcish Valley:
raw_orc_1 = pygame.image.load('assets/painted/transparent/orc_0.png')
raw_orc_2 = pygame.image.load('assets/painted/transparent/orc_1.png')
raw_orc_3 = pygame.image.load('assets/painted/transparent/orc_2.png')
raw_orc_4 = pygame.image.load('assets/painted/transparent/orc_3.png')
raw_orc_5 = pygame.image.load('assets/painted/transparent/orc_4.png')
raw_orc_6 = pygame.image.load('assets/painted/transparent/orc_5.png')
#--- Attacks:
raw_player_attack_slash = pygame.image.load('assets/painted/transparent/slash_on_enemy_trans.png')
raw_enemy_attack_slash = pygame.image.load('assets/painted/transparent/slash_on_player_trans.png')
raw_savage_attack = pygame.image.load('assets/painted/transparent/slash_attack.png')

#--- Changing sizes: ---
#Backgrounds:
scaled_main_menu_bg = scaling_bg_images(raw_main_menu_bg)
scaled_exit_game_bg = scaling_bg_images(raw_exit_game_bg)
scaled_about_bg = scaling_bg_images(raw_about_bg)
scaled_town_bg_1 = scaling_bg_images(raw_town_bg_1)
scaled_loading_bg = scaling_bg_images(raw_loading_bg)
scaled_faceless_man_bg = scaling_bg_images(raw_faceless_man_bg)
scaled_gate_guard_bg = scaling_bg_images(raw_gate_guard_magic_ball_bg)
scaled_shop_bg = scaling_bg_images(raw_shop_bg)
scaled_portal_0_bg = scaling_bg_images(raw_portal_0_bg)
scaled_portal_1_bg = scaling_bg_images(raw_portal_1_bg)
scaled_portal_2_bg = scaling_bg_images(raw_portal_2_bg)
scaled_portal_3_bg = scaling_bg_images(raw_portal_3_bg)
scaled_human_3_bg = scaling_bg_images(raw_human_3_bg)
#--- For Crypts:
scaled_ud_0_bg = scaling_bg_images(raw_ud_0_bg)
scaled_ud_1_bg = scaling_bg_images(raw_ud_1_bg)
scaled_ud_4_bg = scaling_bg_images(raw_ud_4_bg)
#--- For Orcish Valley:
scaled_orc_1_bg = scaling_bg_images(raw_orc_1_bg)
scaled_orc_2_bg = scaling_bg_images(raw_orc_2_bg)
scaled_orc_3_bg = scaling_bg_images(raw_orc_3_bg)
scaled_orc_4_bg = scaling_bg_images(raw_orc_4_bg)
scaled_orc_5_bg = scaling_bg_images(raw_orc_5_bg)
#Characters:
scaled_player_char = scaling_most_characters(raw_player_char)
#--- For Crypts
scaled_undead_1 = scaling_most_characters(raw_undead_1)
scaled_undead_2 = scaling_most_characters(raw_undead_2)
scaled_undead_3 = scaling_most_characters(raw_undead_3)
#--- For Orcish Valley:
scaled_orc_1 = scaling_most_characters(raw_orc_1)
scaled_orc_2 = scaling_most_characters(raw_orc_2)
scaled_orc_3 = scaling_most_characters(raw_orc_3)
scaled_orc_4 = scaling_most_characters(raw_orc_4)
scaled_orc_5 = scaling_most_characters(raw_orc_5)
scaled_orc_6 = scaling_most_characters(raw_orc_6)
#--- Attacks:
scaled_player_attack_slash = pygame.transform.scale(raw_player_attack_slash, (150,89))
scaled_enemy_attack_slash = pygame.transform.scale(raw_enemy_attack_slash, (150,89))
scaled_slash_attack = pygame.transform.scale(raw_savage_attack, (130,168)) #blit it at (53,499)
#>>>>>> End - Images <<<<<<

#>>>>>> Custom Classes <<<<<<
class ScreenBlittedState:

    def __init__(self, screen, mp):
        self.screen = screen
        self.mp = mp

    def title_screen_blit(self):
        #--- Background
            screen.blit(scaled_main_menu_bg[0], scaled_main_menu_bg[1])
            #--- New Game
            text_new_game.blit_text(self.screen, self.mp)
            #--- Load Game
            text_load_game.blit_text(self.screen, self.mp)
            #--- About
            text_about.blit_text(self.screen, self.mp)
            #--- Exit
            text_exit.blit_text(self.screen, self.mp)
    
    def new_game_confirmation_screen_blit(self):
        #--- Background
        screen.blit(scaled_main_menu_bg[0], scaled_main_menu_bg[1])
        #--- Start New Game?
        text_start_newgame.blit_text(self.screen, self.mp)
        #--- Yes
        text_yes.blit_text(self.screen, self.mp)
        #--- No
        text_no.blit_text(self.screen, self.mp)   
    
    def about_screen_blit(self):
        #--- Background
        screen.blit(scaled_about_bg[0], scaled_about_bg[1])
        #--- Back
        text_back_about_screen_special.blit_text(self.screen, self.mp)
    
    def town_screen_blit(self):
        #--- Background
        screen.blit(scaled_town_bg_1[0], scaled_town_bg_1[1])
        #--- Faceless Man
        text_faceless_man.blit_text(self.screen, self.mp)
        #--- Battle
        text_battle.blit_text(self.screen, self.mp)
        #--- Character
        text_character.blit_text(self.screen, self.mp)
        #--- Shop
        text_shop.blit_text(self.screen, self.mp)
        #--- Main Menu
        text_main_menu.blit_text(self.screen, self.mp)

    def facelessman_screen_blit(self):
        #--- Background
        screen.blit(scaled_faceless_man_bg[0], scaled_faceless_man_bg[1])
        #--- Back
        back_text_screen_blitting(self.screen, self.mp)
    
    def battle_screen_blit(self):
        #--- Background
        screen.blit(scaled_gate_guard_bg[0], scaled_gate_guard_bg[1])
        #--- Crypts
        text_crypts.blit_text(self.screen, self.mp)
        #--- Orcish Valley
        if is_crypts_finished == True:  
            text_orcish_valley.blit_text(self.screen, self.mp)
        else:
            text_question_marks_OrcVal.blit_text(self.screen, self.mp)
        #--- Frozen Tundra
        if is_orcish_valley_finished == True:
            text_frozen_tundra.blit_text(self.screen, self.mp)
        else:
            text_question_marks_FroTund.blit_text(self.screen, self.mp)
        #--- Demon World
        if is_frozen_tundra_finished == True:
            text_demon_world.blit_text(self.screen, self.mp)
        else:
            text_question_marks_DemWorl.blit_text(self.screen, self.mp)
        #--- Back
        back_text_screen_blitting(self.screen, self.mp)

    def character_screen_blit(self):
        #--- Background
        screen.blit(scaled_human_3_bg[0], scaled_human_3_bg[1])
        #--- Stats
        text_stats.blit_text(self.screen, self.mp)
        #--- Level
        text_level.blit_text(self.screen, self.mp)
        #--- Exp
        text_exp.blit_text(self.screen, self.mp)
        #--- Health
        text_health.blit_text(self.screen, self.mp)
        #--- Damage
        text_damage.blit_text(self.screen, self.mp)
        #--- Defence
        text_defence.blit_text(self.screen, self.mp)
        #--- Free Points
        text_free_points.blit_text(self.screen, self.mp)
        #--- Vitality
        text_vitality.blit_text(self.screen, self.mp)
        #--- Strength
        text_strength.blit_text(self.screen, self.mp)
        #--- Back
        back_text_screen_blitting(self.screen, self.mp) 
    
    def shop_screen_blit(self):
        #--- Background
        screen.blit(scaled_shop_bg[0], scaled_shop_bg[1]) 
        #--- Back
        back_text_screen_blitting(self.screen, self.mp) 

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
        #checking if mouse is over text
        if mp[0] in range(self.xPos_r[0], self.xPos_r[1]) and mp[1] in range(self.yPos_r[0], self.yPos_r[1]):
            #if True, bliting red text over white
            screen.blit(self.text_red[0], self.text_white[1])

class GameLoopState(Enum):
    #Main Menu loop:
    MainMenu = 1
    NewGame = 2
    AboutGame = 3
    #Town loops:
    TownMainMenu = 4
    TownFacelessman = 5
    TownBattle = 6
    TownCharacter = 7
    TownShop = 8
    #Fighting loops:
    CryptsFighting = 9
    OrcishValleyFighting = 10
    FrozenTundraFighting = 11
    DemonWorldFighting = 12
#>>>>>> End - Custom Classes <<<<<<   

#>>>>>> Texts: <<<<<<
#Fonts:
text_font_72 = pygame.font.Font(None, 72)
text_font_62 = pygame.font.Font(None, 62)
text_font_50 = pygame.font.Font(None, 50)
text_font_40 = pygame.font.Font(None, 40)
text_font_30 = pygame.font.Font(None, 30)
text_font_20 = pygame.font.Font(None, 20)

font_72 = pygame.font.Font(None, 72)
font_62 = pygame.font.Font(None, 62)
font_50 = pygame.font.Font(None, 50)
font_40 = pygame.font.Font(None, 40)

#Creating texts, setting coordinates and fonts:
#--- New Game
text_new_game = MenuText("NEW GAME", 100,200, font_72)
#--- Load Game
text_load_game = MenuText("LOAD GAME", 88,259, font_72)
#--- About
text_about = MenuText("ABOUT", 154,318, font_72)
#--- Exit
text_exit = MenuText("EXIT", 179,377, font_72)
#--- Start New Game?
text_start_newgame = MenuText("START NEW GAME?", 33,200, font_62)
#--- Yes
text_yes = MenuText("YES", 191,259, font_62)
#--- No
text_no = MenuText('NO', 204,318, font_62)
#-!- Back -> about screen special
text_back_about_screen_special = MenuText("BACK", 180,540, font_72)
#-!- Back -> for general use
text_back = MenuText("BACK", 170,720, font_72)
#--- Loading..
text_loading = MenuText("LOADING..", 10, 726, font_72)
#--- Faceless Man
text_faceless_man = MenuText("FACELESS MAN", 45,200, font_72)
#--- Battle
text_battle = MenuText("BATTLE", 144,259, font_72)
#--- Character
text_character = MenuText("CHARACTER", 81,318, font_72)
#--- Shop
text_shop = MenuText("SHOP", 168,378, font_72)
#--- Main Menu
text_main_menu = MenuText("MAIN MENU", 96,436,    font_72)
#--- Crypts
text_crypts = MenuText("CRYPTS", 141,320, font_72)
#--- Orcish Valley
text_orcish_valley = MenuText("ORCISH VALLEY", 38,379, font_72)
#--- Frozen Tundra
text_frozen_tundra = MenuText("FROZEN TUNDRA", 28,438, font_72)
#--- Demon World
text_demon_world = MenuText("DEMON WORLD", 46,497, font_72)
#--- ??????
text_question_marks_OrcVal = MenuText("??????", 150,379, font_72)
text_question_marks_FroTund = MenuText("??????", 150,438, font_72)
text_question_marks_DemWorl = MenuText("??????", 150,497, font_72)
#--- Stats
text_stats = MenuText("STATS", 187,370, font_50)
#--- Level
text_level = MenuText("LEVEL", 60,416, font_40)
#--- Exp
text_exp = MenuText("EXP", 60,447, font_40)
#--- Health
text_health = MenuText("HEALTH", 60,478, font_40)
#--- Damage
text_damage = MenuText("DAMAGE", 60,509, font_40)
#--- Defence
text_defence = MenuText("DEFENCE", 60,540, font_40)
#--- Free Points
text_free_points = MenuText("FREE POINTS", 60,571, font_40)
#--- Vitality
text_vitality = MenuText("VITALITY", 60,602, font_40)
#--- Strength
text_strength = MenuText("STRENGTH", 60,633, font_40)
#--- Hero Health bar
text_hero_current_hp = MenuText("HERO HP", 58,20, font_40)
#--- Enemey Health bar
text_enemy_current_hp = MenuText("ENEMY HP", 285,20, font_40)
#Getting text rect size example:
#test = font_72.render("ORCISH VALLEY", True, (color_black))
#print(test.get_size())
#>>>>>> End - Texts <<<<<<

#>>>>>> Game Progresion Switches <<<<<<
is_crypts_finished = False
is_orcish_valley_finished = False
is_frozen_tundra_finished = False
is_demon_world_finished = False
#>>>>>> End - Game Progresion Switches <<<<<<

#>>>>>> Loops <<<<<<
#Main loop:
program_running_loop = True
#Music on/off:
music_playing = True
#Game menu/scenes changing/control:
current_menu = GameLoopState.MainMenu
#>>>>>> End - Loops <<<<<<

#>>>>>> Programs logic Loop <<<<<<
while program_running_loop:
    #---- Music ----
    if music_playing == True:
        if current_menu == GameLoopState.TownMainMenu:
            town_music.set_volume(0.1)
            town_music.play(-1)
        #elif current_menu == GameLoopState.TownMainMenu:
        #    main_menu_music.set_volume(0.1)
        #    main_menu_music.play(-1)
    for event in pygame.event.get():
        #Constant mouse position tracking:
        mouse_hovering_pos = pygame.mouse.get_pos()
        mp = mouse_hovering_pos
        if event.type == pygame.QUIT:
            exit_game_actions(screen)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            exit_game_actions(screen)
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
                #New Game:
                if m_c_p[0] in range(102,380) and m_c_p[1] in range(200,243):
                    current_menu = GameLoopState.NewGame
                #Load Game:
                elif m_c_p[0] in range(90,394) and m_c_p[1] in range(259,302):
                    print("Not Fisnished Feature")
                #About:
                elif m_c_p[0] in range(154,327) and m_c_p[1] in range(318,361):
                    current_menu = GameLoopState.AboutGame
                #Exit:
                elif m_c_p[0] in range(179,301) and m_c_p[1] in range(377,420):
                    exit_game_actions(screen)
            #---- New Game Y/N confirmation screen ----
            elif current_menu == GameLoopState.NewGame:
                #Yes:
                if m_c_p[0] in range(193,292) and m_c_p[1] in range(259,302):
                    loading_screen(screen, mp)
                    current_menu = GameLoopState.TownMainMenu
                #No:
                elif m_c_p[0] in range(204,277) and m_c_p[1] in range(318,361):
                    current_menu = GameLoopState.MainMenu
            #---- About screen ----        
            elif current_menu == GameLoopState.AboutGame:
                #Back:
                if m_c_p[0] in range(180,321) and m_c_p[1] in range(540,583):
                    current_menu = GameLoopState.MainMenu
            #>>>>>> Town Screen clicking <<<<<< ---------------------------------------
            elif current_menu == GameLoopState.TownMainMenu:
                #Faceless Man:
                if m_c_p[0] in range(45,435) and m_c_p[1] in range(200,243):
                    current_menu = GameLoopState.TownFacelessman
                #Battle:
                elif m_c_p[0] in range(144,336) and m_c_p[1] in range(259,302):
                    current_menu = GameLoopState.TownBattle
                #Character:
                elif m_c_p[0] in range(81,400) and m_c_p[1] in range(318,361):
                    current_menu = GameLoopState.TownCharacter
                #Shop:
                elif m_c_p[0] in range(168,312) and m_c_p[1] in range(378,421):
                    current_menu = GameLoopState.TownShop
                #Main Menu:
                elif m_c_p[0] in range(96,385) and m_c_p[1] in range(436,479):
                    pygame.mixer.stop()
                    loading_screen(screen, mp)
                    current_menu = GameLoopState.MainMenu
            #--- Faceless Man screen clicking ---
            elif current_menu == GameLoopState.TownFacelessman:
                #Back:
                if m_c_p[0] in range(170,311) and m_c_p[1] in range(720,763):
                    current_menu = GameLoopState.TownMainMenu
            #--- Battle screen clicking: ---
            elif current_menu == GameLoopState.TownBattle:
                #Crypts:
                if m_c_p[0] in range(141,340) and m_c_p[1] in range(320,369):
                    screen.blit(scaled_portal_3_bg[0], scaled_portal_3_bg[1])
                    pygame.display.flip()
                    time.sleep(0.7)
                    current_menu = GameLoopState.CryptsFighting
                #Orcish Valley:
                elif is_crypts_finished == True:
                    if m_c_p[0] in range(38,442) and m_c_p[1] in range(379,428):
                        screen.blit(scaled_portal_0_bg[0], scaled_portal_0_bg[1])
                        pygame.display.flip()
                        time.sleep(0.7)
                        current_menu = GameLoopState.OrcishValleyFighting
                #Back:
                elif m_c_p[0] in range(170,311) and m_c_p[1] in range(720,763):
                    current_menu = GameLoopState.TownMainMenu
            #--- Character screen clicking: ---
            elif current_menu == GameLoopState.TownCharacter:
                #Back:
                if m_c_p[0] in range(170,311) and m_c_p[1] in range(720,763):
                    current_menu = GameLoopState.TownMainMenu
            #--- Shop screen clicking ---
            elif current_menu == GameLoopState.TownShop:
                #Back
                if m_c_p[0] in range(170,311) and m_c_p[1] in range(720,763):
                    current_menu = GameLoopState.TownMainMenu
    redraw_screen(current_menu, music_playing, screen, mp)
    pygame.display.flip()
#>>>>>> End - Programs logic Loop <<<<<<
