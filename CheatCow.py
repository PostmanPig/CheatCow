import dearpygui.dearpygui as dpg
import pymem
import sys

pm = pymem.Pymem()

back = 0x005AF9D4
task = 0x005AF9D8
keysCollected = 0x00517504
coinsCollected = 0x005174F4
monstersKilled = 0x005174FC
gemsCollected = 0x005174F8
garbageCleared = 0x00517508
secretsFound = 0x00517500
showFps = 0x00A79E18
points = 0x00517544
pointsDisplayed = 0x00517548
percent = 0x01432E4C
cowLives = 0x004CE28C
cowHealth = 0x01433E68
megaJump = 0x01433FA0
horseShoe = 0x01433FA4
firmness = 0x01433FA8
objectCount = 0x5CBA40
objectPool = 0x5C7A40
cowX = 0x01433B9C
cowY = 0x01433BA0

backgrounds = []
tasks = ['pass to exit', 'find keys', 'kill monsters', 'find gems', 'clear garbage', 'kill boss']
objects_blacklist = []

with open('data/backgrounds.txt', 'r') as backs:
    line = backs.readlines()
    length = len(line)
    for lines in range(length):
        line_toread = line[lines]
        if line_toread[0:1] == '[' and line_toread[0:2] != '[/':
            backgrounds.append(line_toread.replace('[','').replace(']','').replace('/',''))


class background():
    num = 0

try:
    pm.open_process_from_name('supercow.exe')
except pymem.exception.ProcessNotFound:
    try:
        pm.open_process_from_name('old.exe')
    except pymem.exception.ProcessNotFound:
        try:
            pm.open_process_from_name('editor.exe')
        except pymem.exception.ProcessNotFound:
            sys.exit()

def nextback():
    pm.write_int(back, (pm.read_int(back) + 1))

def prevback():
    pm.write_int(back, (pm.read_int(back) - 1))

def show_current_back():
    dpg.set_value(current_back, f"Current back: {backgrounds[pm.read_int(back)]}")

def back_change(sender, data, user_data):
    pm.write_int(back, user_data)

def nexttask():
    pm.write_int(task, (pm.read_int(task) + 1))

def prevtask():
    pm.write_int(task, (pm.read_int(task) - 1))

def show_current_task():
    dpg.set_value(current_task, f"Current task: {tasks[pm.read_int(task)]}")

def task_change(sender, data, user_data):
    pm.write_int(task, user_data)

def keys_collected_changed():
    amount = dpg.get_value(keys_collected)
    pm.write_int(keysCollected, amount)

def coins_collected_changed():
    amount = dpg.get_value(coins_collected)
    pm.write_int(coinsCollected, amount)

def monsters_killed_changed():
    amount = dpg.get_value(monsters_killed)
    pm.write_int(monstersKilled, amount)

def gems_collected_changed():
    amount = dpg.get_value(gems_collected)
    pm.write_int(gemsCollected, amount)

def garbage_cleared_changed():
    amount = dpg.get_value(garbage_cleared)
    pm.write_int(garbageCleared, amount)

def secrets_found_changed():
    amount = dpg.get_value(secrets_found)
    pm.write_int(secretsFound, amount)

def points_changed():
    amount = dpg.get_value(change_points)
    pm.write_int(points, amount)
    pm.write_int(pointsDisplayed, amount)

def percent_changed():
    amount = dpg.get_value(completeness)
    pm.write_int(percent, amount)

def lives_changed():
    amount = dpg.get_value(change_lives)
    pm.write_int(cowLives, amount)

def health_changed():
    amount = dpg.get_value(change_health)
    pm.write_float(cowHealth, float(amount))

def firmness_changed():
    amount = dpg.get_value(change_firmness)
    pm.write_float(firmness, float(str(amount) + '000'))

def megajump_changed():
    amount = dpg.get_value(change_megajump)
    pm.write_float(megaJump, float(str(amount) + '000'))

def horseshoe_changed():
    amount = dpg.get_value(change_horseshoe)
    pm.write_float(horseShoe, float(str(amount) + '000'))

def fps_show():
    fps = dpg.get_value(show_fps)
    if fps == True:
        pm.write_int(showFps, 1)
    else:
        pm.write_int(showFps, 0)

def object_find():
    for index in range(pm.read_int(objectCount)):
        objectAddr = pm.read_int(objectPool + 4 * index)
        objName = pm.read_string(objectAddr + 0x4)
        objX = pm.read_float(objectAddr + 0x24)
        objY = pm.read_float(objectAddr + 0x28)
        if objName == dpg.get_value(object_tofind):
            if index not in objects_blacklist:
                if dpg.get_value(teleport_to_found_objs) == True:
                    pm.write_float(cowX, objX)
                    pm.write_float(cowY, objY)
                if dpg.get_value(teleport_setting) == True:
                    objects_blacklist.append(index)
                dpg.set_value(x, f'Object X: {objX}')
                dpg.set_value(y, f'Object Y: {objY}')
                break

def cowUp():
    pm.write_float(cowY, pm.read_float(cowY)+10)

def cowDown():
    pm.write_float(cowY, pm.read_float(cowY)-10)

def cowRight():
    pm.write_float(cowX, pm.read_float(cowX)+10)

def cowLeft():
    pm.write_float(cowX, pm.read_float(cowX)-10)
 
def set_checkpoint():
    dpg.set_value(checkpoint_x, f'Checkpoint X: {pm.read_float(cowX)}')
    dpg.set_value(checkpoint_y, f'Checkpoint Y: {pm.read_float(cowY)}')

def checkpoint_teleport():
    pm.write_float(cowX, float(dpg.get_value(checkpoint_x).replace('Checkpoint X: ', '')))
    pm.write_float(cowY, float(dpg.get_value(checkpoint_y).replace('Checkpoint Y: ', '')))

def pos_show():
    dpg.set_value(cow_x, f'Cow X: {pm.read_float(cowX)}')
    dpg.set_value(cow_y, f'Cow Y: {pm.read_float(cowY)}')

def teleport_to_entered_cords():
    try:
        pm.write_float(cowX, float(dpg.get_value(x_to_teleport)))
        pm.write_float(cowY, float(dpg.get_value(y_to_teleport)))
    except ValueError:
        pass

def show_objects():
    for index in range(pm.read_int(objectCount)):
        objectAddr = pm.read_int(objectPool + 4 * index)
        objName = pm.read_string(objectAddr + 0x4)
        objX = pm.read_float(objectAddr + 0x24)
        objY = pm.read_float(objectAddr + 0x28)
        exec(f"dpg.set_value(a_{index}_name, f'Object {index} name: {objName}')")
        exec(f"dpg.set_value(a_{index}_x, f'Object {index} X: {objX}')")
        exec(f"dpg.set_value(a_{index}_y, f'Object {index} Y: {objY}')")

dpg.create_context()
dpg.create_viewport(title='CheatCow', width=600, height=300)

background = background()

with dpg.window(label="CheatCow", width=800, height=800, pos=(100, 100), tag='CheatCow'):
    hello = dpg.add_text(label='')
    dpg.set_value(hello, 'Welcome to CheatCow v1.0!')
    with dpg.tree_node(label='Level'):
        with dpg.tree_node(label='Background'):
            with dpg.group(horizontal=True):
                dpg.add_button(label='Next background', callback=nextback)
                dpg.add_button(label='Previous background', callback=prevback)
            current_back = dpg.add_text(label='')
            dpg.set_value(current_back, f"Current back:")
            dpg.add_button(label='Show current background', callback=show_current_back, user_data=current_back)
            with dpg.menu(label='Chose background'):
                for i in range(len(backgrounds)):
                    change_back = dpg.add_menu_item(label=backgrounds[i], callback=back_change, user_data=i)

        with dpg.tree_node(label='Task'):
            with dpg.group(horizontal=True):
                dpg.add_button(label='Next task', callback=nexttask)
                dpg.add_button(label='Previous task', callback=prevtask)
            current_task = dpg.add_text(label='')
            dpg.set_value(current_task, f"Current task:")
            dpg.add_button(label='Show current task', callback=show_current_task, user_data=current_task)
            with dpg.menu(label='Chose task'):
                for i in range(len(tasks)):
                    change_task = dpg.add_menu_item(label=tasks[i], callback=task_change, user_data=i)
            with dpg.tree_node(label='Adjust values'):
                keys_collected = dpg.add_input_int(label='Keys', callback=keys_collected_changed)
                monsters_killed = dpg.add_slider_int(label='Monsters killed', min_value=-5000, max_value=5000, callback=monsters_killed_changed)
                gems_collected = dpg.add_slider_int(label='Gems collected', min_value=-5000, max_value=5000, callback=gems_collected_changed)
                garbage_cleared = dpg.add_slider_int(label='Garbage cleared', min_value=-5000, max_value=5000, callback=garbage_cleared_changed)
                completeness = dpg.add_slider_int(label='Completeness percent', min_value=-300, max_value=300, callback=percent_changed)

        with dpg.tree_node(label='Objects'):
            object_tofind = dpg.add_input_text(label='Object to find')
            find_object = dpg.add_button(label='Find object', callback=object_find)
            x = dpg.add_text(label='')
            dpg.set_value(x, 'Object X:')
            y = dpg.add_text(label='')
            dpg.set_value(y, 'Object Y:')
            teleport_to_found_objs = dpg.add_checkbox(label='Teleport to found objects', default_value=True)
            teleport_setting = dpg.add_checkbox(label='Do not teleport to objects you have already teleported to', default_value=True)
            with dpg.tree_node(label='Objects'):
                dpg.add_button(label='Show all objects', callback=show_objects)
                for j in range(4096):
                    exec(f"with dpg.tree_node(label='Object {j}'):\n    a_{j}_name = dpg.add_text(label='')\n    a_{j}_x = dpg.add_text(label='')\n    a_{j}_y = dpg.add_text(label='')")

    with dpg.tree_node(label='Stats'):
        change_points = dpg.add_slider_int(label='Points', min_value=-10000000, max_value=10000000,callback=points_changed)
        coins_collected = dpg.add_slider_int(label='Coins collected', min_value=-5000, max_value=5000, callback=coins_collected_changed)
        secrets_found = dpg.add_input_int(label='Secrets found', callback=secrets_found_changed)

    with dpg.tree_node(label='Cow'):
        change_lives = dpg.add_input_int(label='Lives', callback=lives_changed, default_value=pm.read_int(cowLives))
        change_health = dpg.add_slider_int(label='Health', min_value=0, max_value=100, callback=health_changed, default_value=100)
        with dpg.tree_node(label='Powerups'):
            change_firmness = dpg.add_slider_int(label='Firmness (seconds)', min_value=0, max_value=3600, callback=firmness_changed)
            change_megajump = dpg.add_slider_int(label='Megajump (seconds)', min_value=0, max_value=3600, callback=megajump_changed)
            change_horseshoe = dpg.add_slider_int(label='Horseshoe (seconds)', min_value=0, max_value=3600, callback=horseshoe_changed)
        with dpg.tree_node(label='Position'):
            with dpg.group(horizontal=True):
                dpg.add_spacer(width=12)
                up = dpg.add_button(arrow=True, direction=dpg.mvDir_Up, callback=cowUp)
            with dpg.group(horizontal=True):
                left = dpg.add_button(arrow=True, direction=dpg.mvDir_Left, callback=cowLeft)
                dpg.add_spacer(width=6)
                right = dpg.add_button(arrow=True, direction=dpg.mvDir_Right, callback=cowRight)
            with dpg.group(horizontal=True):
                dpg.add_spacer(width=12)
                down = dpg.add_button(arrow=True, direction=dpg.mvDir_Down, callback=cowDown)
            show_pos = dpg.add_button(label='Show Cow position', callback=pos_show)
            cow_x = dpg.add_text(label='')
            dpg.set_value(cow_x, 'Cow X: ')
            cow_y = dpg.add_text(label='')
            dpg.set_value(cow_y, 'Cow Y: ')
            x_to_teleport = dpg.add_input_text(label='X to teleport')
            y_to_teleport = dpg.add_input_text(label='Y to teleport')
            dpg.add_button(label='Teleport to the entered coordinates', callback=teleport_to_entered_cords)
            with dpg.tree_node(label='Checkpoints'):
                checkpoint_set = dpg.add_button(label='Set checkpoint', callback=set_checkpoint)
                checkpoint_x = dpg.add_text('')
                dpg.set_value(checkpoint_x, 'Checkpoint X:')
                checkpoint_y = dpg.add_text('')
                dpg.set_value(checkpoint_y, 'Checkpoint Y:')
                teleport_checkpoint = dpg.add_button(label='Teleport to checkpoint', callback=checkpoint_teleport)

    with dpg.tree_node(label='Other'):
        show_fps = dpg.add_checkbox(label='Show FPS?', callback=fps_show)

dpg.set_primary_window("CheatCow", True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()