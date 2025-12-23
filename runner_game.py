import pygame
import random
import sys
import traceback

# Initialize pygame
pygame.init()

# Screen
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Runner Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()


def draw_player_man(surface, x, y, width, height, color):
    """Draw a simple stick-figure 'man' inside the given bounding box.

    x, y is the top-left of the box (matching the previous player rect).
    """
    cx = x + width // 2

    # Head
    head_radius = max(4, min(width, height) // 6)
    head_center = (cx, y + head_radius + 2)
    pygame.draw.circle(surface, color, head_center, head_radius)

    # Body
    body_top = head_center[1] + head_radius
    body_bottom = y + height - 8
    pygame.draw.line(surface, color, (cx, body_top), (cx, body_bottom), 3)

    # Arms
    arm_y = body_top + (body_bottom - body_top) // 3
    arm_length = width // 2
    pygame.draw.line(surface, color, (cx - arm_length // 2, arm_y), (cx + arm_length // 2, arm_y), 3)

    # Legs
    leg_y_start = body_bottom
    leg_length = max(8, height // 3)
    pygame.draw.line(surface, color, (cx, leg_y_start), (cx - leg_length // 1, leg_y_start + leg_length), 3)
    pygame.draw.line(surface, color, (cx, leg_y_start), (cx + leg_length // 1, leg_y_start + leg_length), 3)


def run_game():
    font = pygame.font.SysFont(None, 40)

    while True:
        # Reset / initialize runtime state for a new game
        player_x = 100
        player_y = 300
        player_width = 40
        player_height = 40
        player_jump = False
        y_velocity = 0

        obstacle_x = WIDTH
        obstacle_y = 300
        obstacle_width = 40
        obstacle_height = 40
        obstacle_speed = 5

        score = 0
        running = True

        while running:
            screen.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Jump
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not player_jump:
                        player_jump = True
                        y_velocity = -10

            # Player jump logic
            if player_jump:
                player_y += y_velocity
                y_velocity += 0.5
                if player_y >= 300:
                    player_y = 300
                    player_jump = False

            # Move obstacle
            obstacle_x -= obstacle_speed
            if obstacle_x < -obstacle_width:
                obstacle_x = WIDTH
                score += 1

            # Collision detection
            player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
            obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)

            if player_rect.colliderect(obstacle_rect):
                # Show lose overlay and ask for restart (Y) or quit (N)
                waiting = True
                restart = False
                while waiting:
                    # draw translucent overlay
                    overlay = pygame.Surface((WIDTH, HEIGHT))
                    overlay.set_alpha(200)
                    overlay.fill((255, 255, 255))
                    screen.blit(overlay, (0, 0))

                    lost_text = font.render("You Lost the Game", True, BLACK)
                    prompt_text = font.render("Press Y to restart or N to quit", True, BLACK)
                    screen.blit(lost_text, ((WIDTH - lost_text.get_width()) // 2, HEIGHT // 2 - 40))
                    screen.blit(prompt_text, ((WIDTH - prompt_text.get_width()) // 2, HEIGHT // 2 + 10))
                    pygame.display.update()

                    for ev in pygame.event.get():
                        if ev.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if ev.type == pygame.KEYDOWN:
                            if ev.key == pygame.K_y:
                                waiting = False
                                restart = True
                            elif ev.key == pygame.K_n:
                                pygame.quit()
                                sys.exit()

                    clock.tick(30)

                # break the running loop to restart if requested
                if restart:
                    running = False
                    break

            # Draw player and obstacle
            draw_player_man(screen, player_rect.x, player_rect.y, player_rect.width, player_rect.height, BLACK)
            pygame.draw.rect(screen, BLACK, obstacle_rect)

            # Draw score
            score_text = font.render(f"Score: {score}", True, BLACK)
            screen.blit(score_text, (10, 10))

            pygame.display.update()
            clock.tick(60)


if __name__ == '__main__':
    try:
        run_game()
    except Exception:
        tb = traceback.format_exc()
        print(tb)
        try:
            with open('error.log', 'w', encoding='utf-8') as f:
                f.write(tb)
        except Exception:
            pass

        # show a brief on-screen error message if possible
        try:
            font = pygame.font.SysFont(None, 36)
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(220)
            overlay.fill((255, 200, 200))
            screen.blit(overlay, (0, 0))
            err_text = font.render("An error occurred; see error.log", True, BLACK)
            screen.blit(err_text, ((WIDTH - err_text.get_width()) // 2, HEIGHT // 2))
            pygame.display.update()
            pygame.time.wait(2500)
        except Exception:
            pass
    finally:
        try:
            pygame.quit()
        except Exception:
            pass
