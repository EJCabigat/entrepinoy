
import pygame
from game.sprite.button import Button

from game.sprite.menu_background import MenuBackground
from game.sprite.message import Message


class ConfirmMenu():
    """
    This class displays a confirmation menu when certain actions have been taken.
    """
    def __init__(self, main):
        self.main = main
        self.callback = None
        
        # Sprite groups
        self.objects = pygame.sprite.Group()
        self.hoverable_buttons = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        
        # Screen objects
        self.background = MenuBackground(
            self.main.screen, 0.40,
            image=self.main.data.meta_images["menu_background"])
        self.background.add(self.objects, self.buttons)
        
        self.canvas_rect = self.background.rect
        self.confirmation_message = Message(
            self.main.screen, 
            ["No message has been set"],
            self.main.data.medium_font,
            self.main.data.colors["white"],
            outline_thickness=2,
            center_coordinates=(
                int(self.canvas_rect.width * 0.50) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.175) + self.canvas_rect.y
            )
        )
        self.confirmation_message.add(self.objects)
        
        self.confirm_button = Button(
            self.main.screen, self.confirm,
            center_coordinates=(
                int(self.canvas_rect.width * 0.32) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.77) + self.canvas_rect.y
            ),
            **{
                "idle" : self.main.data.meta_images["confirm_button_idle"],
                "outline" : self.main.data.meta_images["confirm_button_hovered"]
            }
        )
        self.confirm_button.add(self.objects, self.buttons, self.hoverable_buttons)
        
        self.cancel_button = Button(
            self.main.screen, self.cancel,
            center_coordinates=(
                int(self.canvas_rect.width * 0.73) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.77) + self.canvas_rect.y
            ),
            **{
                "idle" : self.main.data.meta_images["cancel_button_idle"],
                "outline" : self.main.data.meta_images["cancel_button_hovered"]
            },
        )
        self.cancel_button.add(self.objects, self.buttons, self.hoverable_buttons)
        
        
    # Inner functions just for the functionality of the buttons
    def confirm(self, *args):
        self.background.enable = False
        self.callback()
        
        
    def cancel(self, *args):
        self.background.enable = False
        
        
    def run(self):
        # Screen dimming
        self.main.display_surface.set_alpha(128)
        self.main.screen.blit(self.main.display_surface, (0, 0)) 
        
        self.background.enable = True
        while self.background.enable:
            self.objects.update()
            
            # Event processing
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    # Closing the game properly
                    self.close_game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.background.enable = False
                elif event.type == pygame.MOUSEMOTION: 
                    for button in self.hoverable_buttons:
                        button.check_hovered(event.pos)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = event.pos
                        for button in self.buttons:
                            button.check_clicked(mouse_pos)
            
            # Updating the display
            self.main.refresh_display()
        
        
    def set_message_and_callback(self, message, callback):
        self.confirmation_message.set_message(message)
        self.callback = callback