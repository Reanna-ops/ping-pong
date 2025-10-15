import pygame
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)

        # Default winning score
        self.win_score = 5

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        # Move the ball
        self.ball.move()

        # --- Collision detection with paddles ---
        ball_rect = self.ball.rect()
        player_rect = self.player.rect()
        ai_rect = self.ai.rect()

        if ball_rect.colliderect(player_rect):
            self.ball.velocity_x = abs(self.ball.velocity_x)  # move right
        elif ball_rect.colliderect(ai_rect):
            self.ball.velocity_x = -abs(self.ball.velocity_x)  # move left

        # Bounce off top/bottom walls
        if self.ball.y <= 0 or self.ball.y + self.ball.size >= self.height:
            self.ball.velocity_y *= -1

        # Check for scoring
        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.x + self.ball.size >= self.width:
            self.player_score += 1
            self.ball.reset()

        # Simple AI movement
        self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

    def check_game_over(self, screen):
        """Check if either player reached win_score and handle replay menu."""
        if self.player_score >= self.win_score or self.ai_score >= self.win_score:
            # Display winner
            winner_text = "Player Wins!" if self.player_score >= self.win_score else "AI Wins!"
            text_surface = self.font.render(winner_text, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2 - 50))
            screen.blit(text_surface, text_rect)

            # Replay options
            options = [
                "Press 3 for Best of 3",
                "Press 5 for Best of 5",
                "Press 7 for Best of 7",
                "Press ESC to Exit"
            ]
            for i, option in enumerate(options):
                opt_surface = self.font.render(option, True, WHITE)
                opt_rect = opt_surface.get_rect(center=(self.width // 2, self.height // 2 + 40 + i * 40))
                screen.blit(opt_surface, opt_rect)

            pygame.display.flip()

            # Wait for user choice
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return True  # Exit game
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            return True  # Exit
                        elif event.key == pygame.K_3:
                            self.win_score = 2  # Best of 3 → first to 2 wins
                            waiting = False
                        elif event.key == pygame.K_5:
                            self.win_score = 3  # Best of 5 → first to 3 wins
                            waiting = False
                        elif event.key == pygame.K_7:
                            self.win_score = 4  # Best of 7 → first to 4 wins
                            waiting = False

            # Reset scores and ball
            self.player_score = 0
            self.ai_score = 0
            self.ball.reset()
            return False  # Continue game
        return False
