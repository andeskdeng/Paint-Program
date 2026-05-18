import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
BUTTON_HEIGHT = 40
CANVAS_HEIGHT = SCREEN_HEIGHT - BUTTON_HEIGHT

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

class PaintProgram:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Paint Program")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Canvas
        self.canvas = pygame.Surface((SCREEN_WIDTH, CANVAS_HEIGHT))
        self.canvas.fill(WHITE)
        
        # Drawing state
        self.drawing = False
        self.current_color = BLACK
        self.brush_size = 5
        self.last_pos = None
        
        # Colors palette
        self.colors = [BLACK, RED, GREEN, BLUE, YELLOW, WHITE]
        self.color_buttons = []
        self.setup_color_buttons()
        
        # Font for labels
        self.font = pygame.font.Font(None, 24)
    
    def setup_color_buttons(self):
        """Setup color selection buttons"""
        button_width = 50
        button_x = 10
        button_y = CANVAS_HEIGHT + 5
        
        for color in self.colors:
            rect = pygame.Rect(button_x, button_y, button_width, BUTTON_HEIGHT - 10)
            self.color_buttons.append((rect, color))
            button_x += button_width + 5
    
    def handle_events(self):
        """Handle user input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if event.pos[1] < CANVAS_HEIGHT:  # Drawing area
                        self.drawing = True
                        self.last_pos = event.pos
                    else:  # Toolbar area
                        self.handle_toolbar_click(event.pos)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.drawing = False
                    self.last_pos = None
            
            elif event.type == pygame.MOUSEMOTION:
                if self.drawing and event.pos[1] < CANVAS_HEIGHT:
                    self.draw_line(self.last_pos, event.pos)
                    self.last_pos = event.pos
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:  # Clear canvas with 'C'
                    self.canvas.fill(WHITE)
                elif event.key == pygame.K_UP:  # Increase brush size
                    self.brush_size = min(self.brush_size + 1, 30)
                elif event.key == pygame.K_DOWN:  # Decrease brush size
                    self.brush_size = max(self.brush_size - 1, 1)
    
    def handle_toolbar_click(self, pos):
        """Handle toolbar clicks for color selection"""
        for rect, color in self.color_buttons:
            if rect.collidepoint(pos):
                self.current_color = color
                break
    
    def draw_line(self, start_pos, end_pos):
        """Draw a line on the canvas"""
        if start_pos and end_pos:
            pygame.draw.line(self.canvas, self.current_color, start_pos, end_pos, self.brush_size)
    
    def draw_ui(self):
        """Draw the user interface"""
        # Draw toolbar background
        toolbar_rect = pygame.Rect(0, CANVAS_HEIGHT, SCREEN_WIDTH, BUTTON_HEIGHT)
        pygame.draw.rect(self.screen, LIGHT_GRAY, toolbar_rect)
        
        # Draw color buttons
        for rect, color in self.color_buttons:
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, BLACK, rect, 2)
            
            # Highlight current color
            if color == self.current_color:
                pygame.draw.rect(self.screen, BLACK, rect, 3)
        
        # Draw brush size indicator
        size_text = self.font.render(f"Size: {self.brush_size}", True, BLACK)
        self.screen.blit(size_text, (350, CANVAS_HEIGHT + 8))
        
        # Draw instructions
        instr_text = self.font.render("C: Clear  |  ↑↓: Size  |  Click color to select", True, BLACK)
        self.screen.blit(instr_text, (500, CANVAS_HEIGHT + 8))
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            
            # Draw canvas
            self.screen.blit(self.canvas, (0, 0))
            
            # Draw UI
            self.draw_ui()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = PaintProgram()
    app.run()
