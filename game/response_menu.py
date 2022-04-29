
import pygame
from game.sprite.button import Button

from game.sprite.menu_background import MenuBackground
from game.sprite.message import Message


class ResponseMenu():
    """
    This class displays a message response of the system feedback.
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
            self.main.screen, 0.45,
            image=self.main.data.meta_images["menu_background"])
        self.background.add(self.objects, self.buttons)
        
        self.canvas_rect = self.background.rect
        self.confirmation_message = Message(
            self.main.screen, 
            ["No message has been set"],
            self.main.data.large_font,
            self.main.data.colors["white"],
            outline_thickness=2,
            center_coordinates=(
                int(self.canvas_rect.width * 0.50) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.22) + self.canvas_rect.y
            )
        )
        self.confirmation_message.add(self.objects)
        
        self.confirm_button = Button(
            self.main.screen, self.confirm,
            center_coordinates=(
                int(self.canvas_rect.width * 0.52) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.77) + self.canvas_rect.y
            ),
            **{
                "idle" : self.main.data.meta_images["confirm_button_idle"],
                "outline" : self.main.data.meta_images["confirm_button_hovered"]
            }
        )
        self.confirm_button.add(self.objects, self.buttons, self.hoverable_buttons)
        
    
    def confirm(self, *args):
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
        
        
    def set_message(self, message):
        self.confirmation_message.set_message(message)