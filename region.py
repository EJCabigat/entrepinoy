from game.sprite.scene_background import SceneBackground
from game.sprite.button import Button

import pygame


class Map:
    """
    Displays the whole region to traverse between different cities
    """

    def __init__(self, main):
        self.main = main
        self.running = False

        # Sprite groups
        self.objects = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        self.hoverable_buttons = pygame.sprite.Group()

        self.background = SceneBackground(
            self.main.screen,
            self.main.scene_window.time,
            **self.main.data.map["region"],
        )
        self.transition_background = self.main.data.meta_images[
            "window_background"
        ].convert_alpha()

        # Location overlays
        self.location_a_button = Button(
            self.main,
            self.location_a_callback,
            top_left_coordinates=(0, 0),
            collide_rect=[0.116, 0.112, 0.219, 0.265],
            **{
                "idle": self.main.data.map["base_hover"],
                "hovered": self.main.data.map["outline"]["location_a"],
            },
        )
        self.location_b_button = Button(
            self.main,
            self.location_b_callback,
            top_left_coordinates=(0, 0),
            collide_rect=[0.335, 0.134, 0.25, 0.328],
            **{
                "idle": self.main.data.map["base_hover"],
                "hovered": self.main.data.map["outline"]["location_b"],
            },
        )
        self.location_c_button = Button(
            self.main,
            self.location_c_callback,
            top_left_coordinates=(0, 0),
            collide_rect=[0.584, 0.072, 0.306, 0.285],
            **{
                "idle": self.main.data.map["base_hover"],
                "hovered": self.main.data.map["outline"]["location_c"],
            },
        )
        self.location_d_button = Button(
            self.main,
            self.location_d_callback,
            top_left_coordinates=(0, 0),
            collide_rect=[0.584, 0.356, 0.309, 0.288],
            **{
                "idle": self.main.data.map["base_hover"],
                "hovered": self.main.data.map["outline"]["location_d"],
            },
        )
        self.location_e_button = Button(
            self.main,
            self.location_e_callback,
            top_left_coordinates=(0, 0),
            collide_rect=[0.335, 0.462, 0.25, 0.344],
            **{
                "idle": self.main.data.map["base_hover"],
                "hovered": self.main.data.map["outline"]["location_e"],
            },
        )
        self.location_f_button = Button(
            self.main,
            self.location_f_callback,
            top_left_coordinates=(0, 0),
            collide_rect=[0.126, 0.445, 0.209, 0.344],
            **{
                "idle": self.main.data.map["base_hover"],
                "hovered": self.main.data.map["outline"]["location_f"],
            },
        )

        # Objects Add
        self.main.sliding_menu.sliding_menu_button.add(self.buttons)
        self.location_a_button.add(self.objects, self.buttons, self.hoverable_buttons)
        self.location_b_button.add(self.objects, self.buttons, self.hoverable_buttons)
        self.location_c_button.add(self.objects, self.buttons, self.hoverable_buttons)
        self.location_d_button.add(self.objects, self.buttons, self.hoverable_buttons)
        self.location_e_button.add(self.objects, self.buttons, self.hoverable_buttons)
        self.location_f_button.add(self.objects, self.buttons, self.hoverable_buttons)

    def location_a_callback(self, *args):
        self.location_changer("location_a")

    def location_b_callback(self, *args):
        self.location_changer("location_b")

    def location_c_callback(self, *args):
        self.location_changer("location_c")

    def location_d_callback(self, *args):
        self.location_changer("location_d")

    def location_e_callback(self, *args):
        self.location_changer("location_e")

    def location_f_callback(self, *args):
        self.location_changer("location_f")

    def location_changer(self, new_location):
        if self.main.data.progress["last_location"] != new_location:
            self.main.data.progress["last_location"] = new_location

            self.main.sliding_menu.tuck()
            self.main.scene_window.update_data()

            self.main.transition.setup_and_run(
                transition_length=0.5,
                duration_length=3,
                display_image=self.transition_background,
                hold_sfx=self.main.data.music["engine_start"],
                center_message=[
                    f"Travelling to {self.main.data.city[new_location]}..."
                ],
            )

            self.main.scene_window.reconstruct(self.main)

        self.running = False

    def mouse_click_events(self, event):
        click_coordinates = event.pos

        # If the user clicked on left mouse button
        if event.button == 1:
            for button in self.buttons:
                # Adding halting statement to prevent other buttons to
                #   react the same way/overlap reactions
                if button.check_clicked(click_coordinates):
                    break

        # If the user clicked on the right mouse button
        if event.button == 3:
            pass

        # If the user scrolls the mouse wheel upward
        if event.button == 4:
            pass

        # If the user scrolls the mouse wheel downward
        if event.button == 5:
            pass

    def mouse_drag_events(self, event):
        # This variable always saves the last mouse location to be used by the
        #   key_events() function, because we can't always get the location
        #   of the mouse if the only event is key press
        self.last_mouse_pos = event.pos

        # Making sure the user only holds one button at a time
        if event.buttons[0] + event.buttons[1] + event.buttons[2] == 1:
            # If the user is dragging the mouse with left mouse button
            if event.buttons[0] == 1:
                pass

            # If the user is dragging the mouse with the right mouse button
            if event.buttons[2] == 1:
                pass

        # Hovering through display check
        else:
            overlapped = False
            for button in self.buttons:
                # Adding halting statement to prevent other buttons to
                #   react the same way/overlap reactions
                if overlapped:
                    button.state = "idle"
                    button.set_image_and_rect()
                elif button.check_hovered(self.last_mouse_pos):
                    overlapped = True

    def key_down_events(self, key):
        self.main.global_key_down_events(key)

        if key == pygame.K_F1:
            self.show_debug_info = not self.show_debug_info
            if self.show_debug_info:
                self.debug_message.add(self.ui_components)
                self.main.debug.log("Debug details shown")
            else:
                self.debug_message.kill()
                self.main.debug.log("Debug details hidden")

        elif key == pygame.K_F2:
            pass

        elif key == pygame.K_F3:
            pass

        elif key == pygame.K_F4:
            self.location_changer("test_location")

    def key_hold_events(self, keys):
        # If the user pressed the "del" key, (enter explanation here)
        if keys[pygame.K_DELETE]:
            pass

        # If the user pressed the "a" key, (enter explanation here)
        if keys[pygame.K_a]:
            pass

        # If the user pressed the "d" key, (enter explanation here)
        if keys[pygame.K_d]:
            pass

    def run(self):
        self.main.debug.memory_log()
        self.main.debug.new_line()

        # Check if the sliding button is in the scene yet
        if self.buttons not in self.main.sliding_menu.sliding_menu_button.groups():
            self.main.sliding_menu.sliding_menu_button.add(self.buttons)

        self.running = True
        while self.running:
            # Rendering sprites
            self.background.update()
            self.objects.update()
            self.main.sliding_menu.update()

            # Event processing
            for event in pygame.event.get():
                if self.main.confirm_menu.enable:
                    self.main.confirm_menu.handle_event(event)
                elif not self.main.sliding_menu.is_tucked:
                    self.main.sliding_menu.handle_event(event)
                else:
                    if event.type == pygame.QUIT:
                        self.running = False
                        self.main.close_game()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.mouse_click_events(event)
                    elif event.type == pygame.MOUSEMOTION:
                        self.mouse_drag_events(event)
                    elif event.type == pygame.KEYDOWN:
                        self.key_down_events(event.key)

            # Key pressing events (holding keys applicable)
            keys = pygame.key.get_pressed()
            self.key_hold_events(keys)

            # Updating the display
            self.main.scene_window.refresh_display()
