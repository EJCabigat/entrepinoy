import pygame
from game.sprite.button import Button

from game.sprite.menu_background import MenuBackground
from game.sprite.message import Message


class ResponseMenu:
    """
    This class displays a message response of the system feedback.
    """

    def __init__(self, main):
        self.enable = False

        self.main = main
        self.callback = None

        # Sprite groups
        self.objects = pygame.sprite.Group()
        self.hoverable_buttons = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()

        # Screen objects
        self.background = MenuBackground(
            self.main.screen, 0.3, image=self.main.data.meta_images["menu_background"]
        )

        self.canvas_rect = self.background.rect
        self.confirmation_message = Message(
            self.main.screen,
            ["No message has been set"],
            self.main.data.medium_font,
            self.main.data.colors["white"],
            outline_thickness=2,
            center_coordinates=(
                int(self.canvas_rect.width * 0.50) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.22) + self.canvas_rect.y,
            ),
        )

        self.confirm_button = Button(
            self.main,
            self.confirm,
            center_coordinates=(
                int(self.canvas_rect.width * 0.5) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.79) + self.canvas_rect.y,
            ),
            **{
                "idle": self.main.data.meta_images["confirm_button_idle"],
                "outline": self.main.data.meta_images["confirm_button_hovered"],
            }
        )

    def confirm(self, *args):
        self.background.enable = False

    def set_message(self, message):
        self.confirmation_message.set_message(message)

        self.background.add(self.objects, self.buttons)
        self.confirmation_message.add(self.objects)
        self.confirm_button.add(self.objects, self.buttons, self.hoverable_buttons)

        self.background.enable = True

    def handle_event(self, event):
        if not self.enable:
            return

        if event.type == pygame.QUIT:
            # Closing the game properly
            self.main.close_game()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.background.enable = False
            if (
                event.key == pygame.K_RETURN
                or event.key == pygame.K_KP_ENTER
                or event.key == pygame.K_SPACE
            ):
                self.confirm()
        elif event.type == pygame.MOUSEMOTION:
            for button in self.hoverable_buttons:
                button.check_hovered(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos
                for button in self.buttons:
                    button.check_clicked(mouse_pos)

        if not self.background.enable:
            self.close()

    def update(self):
        if not self.enable:
            return

        if self.background.enable:
            # Screen dimming
            self.main.display_surface.set_alpha(128)
            self.main.screen.blit(self.main.display_surface, (0, 0))
            self.objects.update()

    def clear(self):
        self.objects.empty()
        self.hoverable_buttons.empty()
        self.buttons.empty()

    def close(self):
        self.clear()
        self.enable = False
