import os
import pygame
from constants import *


class HighScore:
    def __init__(self):
        self.scores = self.load_scores()
    
    def load_scores(self):
        """Load high scores from file"""
        scores = []
        if os.path.exists(HIGH_SCORE_FILE):
            try:
                with open(HIGH_SCORE_FILE, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            parts = line.split(',')
                            if len(parts) == 2:
                                name = parts[0]
                                score = int(parts[1])
                                scores.append((name, score))
            except:
                pass
        
        # Sort by score (highest first) and keep only top 3
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:TOP_SCORES_COUNT]
    
    def save_scores(self):
        """Save high scores to file"""
        try:
            with open(HIGH_SCORE_FILE, 'w') as f:
                for name, score in self.scores:
                    f.write(f"{name},{score}\n")
        except:
            pass
    
    def is_high_score(self, score):
        """Check if a score qualifies for the top 3"""
        if len(self.scores) < TOP_SCORES_COUNT:
            return True
        return score > self.scores[-1][1]
    
    def add_score(self, name, score):
        """Add a new high score"""
        self.scores.append((name, score))
        self.scores.sort(key=lambda x: x[1], reverse=True)
        self.scores = self.scores[:TOP_SCORES_COUNT]
        self.save_scores()
    
    def get_name_input(self, screen, score):
        """Get player name input for new high score"""
        name = ""
        input_active = True
        
        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and name.strip():
                        return name.strip()
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        return None
                    elif len(name) < MAX_NAME_LENGTH and event.unicode.isprintable():
                        name += event.unicode
            
            # Draw the input screen
            screen.fill((0, 0, 0))
            
            # Draw title
            font_large = pygame.font.SysFont(None, 72)
            title_text = font_large.render("NEW HIGH SCORE!", True, (255, 215, 0))
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
            screen.blit(title_text, title_rect)
            
            # Draw score
            font_medium = pygame.font.SysFont(None, 48)
            score_text = font_medium.render(f"Score: {score}", True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
            screen.blit(score_text, score_rect)
            
            # Draw input prompt
            prompt_text = font_medium.render("Enter your name:", True, (255, 255, 255))
            prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
            screen.blit(prompt_text, prompt_rect)
            
            # Draw input box
            font_input = pygame.font.SysFont(None, 36)
            input_text = font_input.render(name + "|", True, (255, 255, 255))
            input_rect = input_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
            screen.blit(input_text, input_rect)
            
            # Draw instructions
            font_small = pygame.font.SysFont(None, 24)
            instructions = [
                "Press ENTER to save",
                "Press ESC to cancel"
            ]
            for i, instruction in enumerate(instructions):
                inst_text = font_small.render(instruction, True, (128, 128, 128))
                inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80 + i * 25))
                screen.blit(inst_text, inst_rect)
            
            pygame.display.flip()
    
    def draw_high_scores(self, screen, x, y):
        """Draw the high scores list"""
        font_title = pygame.font.SysFont(None, 36)
        font_score = pygame.font.SysFont(None, 28)
        
        # Draw title
        title_text = font_title.render("HIGH SCORES", True, (255, 215, 0))
        title_rect = title_text.get_rect(midleft=(x, y))
        screen.blit(title_text, title_rect)
        
        # Draw scores
        for i, (name, score) in enumerate(self.scores):
            score_text = font_score.render(f"{i+1}. {name}: {score}", True, (255, 255, 255))
            score_rect = score_text.get_rect(midleft=(x, y + 40 + i * 25))
            screen.blit(score_text, score_rect)
        
        # Fill remaining slots with dashes
        for i in range(len(self.scores), TOP_SCORES_COUNT):
            score_text = font_score.render(f"{i+1}. ---: 0", True, (128, 128, 128))
            score_rect = score_text.get_rect(midleft=(x, y + 40 + i * 25))
            screen.blit(score_text, score_rect) 