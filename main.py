import pygame, os, random

pygame.font.init()

WIDTH, HEIGHT = (300, 500)
BIRD_VEL = 25
GRAVITY = 2
PIPE_VEL = 2
FPS = 60

BACKGROUND = pygame.image.load(os.path.join("Assets", "background.png"))
BIRD_PNG = pygame.image.load(os.path.join("Assets", "flappy_bird.png"))
PIPE_PNG = pygame.image.load(os.path.join("Assets", "pipe.png"))

LOST_FONT = pygame.font.SysFont("comicsans", 50)
SCORE_FONT = pygame.font.SysFont("comicsans", 30)


class FlappyBird:
    def __init__(self) -> None:
        self.running = True
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Flappy Bird.")
        self.BIRD = pygame.Rect(WIDTH / 2 - 25, HEIGHT / 2 - 25, 50, 50)
        self.points = 0
        self.scored = False
        self.main()

    def draw_pipes(self) -> None:
        place = random.randint(0, 200)
        self.current_pipe1_location_y = 0 - place
        self.current_pipe2_location_y = HEIGHT - place - 50
        self.pipe1 = self.WIN.blit(
            pygame.transform.rotate(PIPE_PNG, 180),
            (WIDTH, self.current_pipe1_location_y),
        )
        self.pipe2 = self.WIN.blit(
            PIPE_PNG,
            (WIDTH, self.current_pipe2_location_y),
        )

    def lost_screen(self) -> None:
        drawtext = LOST_FONT.render("You Lost!", 1, (255, 255, 255))
        self.WIN.blit(drawtext, (WIDTH / 2 - drawtext.get_width() / 2, HEIGHT / 2))
        pygame.display.update()
        pygame.time.delay(5000)

    def update_score(self, score) -> None:
        drawtext = SCORE_FONT.render(f"Score: {score}", 1, (255, 255, 255))
        self.WIN.blit(drawtext, (WIDTH / 2 - drawtext.get_width() / 2, 10))
        pygame.display.update()

    def handle_pipes(self) -> None:
        if self.pipe1.x > 0:
            self.pipe1.x -= PIPE_VEL
            self.pipe2.x -= PIPE_VEL
            self.pipe1 = self.WIN.blit(
                pygame.transform.rotate(PIPE_PNG, 180),
                (self.pipe1.x, self.current_pipe1_location_y),
            )
            self.pipe2 = self.WIN.blit(
                PIPE_PNG,
                (self.pipe2.x, self.current_pipe2_location_y),
            )
            scorerect = pygame.Rect(
                self.pipe1.x,
                HEIGHT / 2 + 50,
                1,
                100,
            )
            if self.BIRD.colliderect(scorerect):
                if not self.scored:
                    self.points += 1
                    self.scored = True
            else:
                self.scored = False
            self.update_score(self.points)

            if self.BIRD.colliderect(self.pipe1) or self.BIRD.colliderect(self.pipe2):
                self.running = False
                self.lost_screen()
        else:
            self.draw_pipes()

    def draw_window(self, bird: pygame.Rect) -> None:

        self.WIN.blit(BACKGROUND, (0, 0))
        self.WIN.blit(BIRD_PNG, (bird.x, bird.y))
        self.handle_pipes()
        self.update_score(self.points)
        pygame.display.update()

    def main(self) -> None:
        self.draw_pipes()
        self.update_score(self.points)
        while self.running:
            self.BIRD.y += (
                GRAVITY if self.BIRD.y + self.BIRD.height < HEIGHT - 15 else 0
            )
            pygame.time.Clock().tick(FPS)

            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        self.running = False
                        pygame.quit()
                    case pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_SPACE:
                                self.BIRD.y -= BIRD_VEL if self.BIRD.y > 0 else 0
                            case pygame.K_ESCAPE:
                                self.running = False
                                pygame.quit()

            self.draw_window(self.BIRD)

        FlappyBird()


if __name__ == "__main__":
    FlappyBird()
