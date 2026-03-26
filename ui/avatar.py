import pygame
import os
from PIL import Image 

class AtlasAvatar:
    def __init__(self, gif_path="ui/assets/scifiui2.gif"):
        self.screen = pygame.display.set_mode((800, 800), pygame.NOFRAME | pygame.SRCALPHA | pygame.DOUBLEBUF)
        self.screen.set_colorkey((0, 0, 0)) 

        self.current_state = "idle"
        self.is_talking = False
        self.frame_index = 0
        self.animation_speed = 0.5 
        
        self.frames = self._load_gif_frames(gif_path)

    def _load_gif_frames(self, path):
        frames = []
        if os.path.exists(path):
            try:
                img_gif = Image.open(path)
                for frame_num in range(img_gif.n_frames):
                    img_gif.seek(frame_num)
                    
                    frame_rgba = img_gif.convert("RGBA")
                    data = frame_rgba.tobytes()
                    size = frame_rgba.size
                    
                    pygame_surface = pygame.image.fromstring(data, size, "RGBA").convert_alpha()
                    frames.append(pygame_surface)
                print(f">>> {len(frames)} frames carregados do GIF.")
            except Exception as e:
                print(f"[!] Erro ao carregar GIF: {e}")
        
        return frames if frames else [pygame.Surface((800, 800), pygame.SRCALPHA)]

    def draw(self):
            """Renderiza o frame atual com efeito de pulsação quando fala."""
            self.screen.fill((0, 0, 0, 0)) 
            
            speed = self.animation_speed * 1.5 if self.is_talking else self.animation_speed
            self.frame_index = (self.frame_index + speed) % len(self.frames)
            img = self.frames[int(self.frame_index)]
            
            if self.is_talking:
                import math
                import time
                
                pulse = 1.0 + (math.sin(time.time() * 15) * 0.05) 
                
                new_size = (int(800 * pulse), int(800 * pulse))
                img = pygame.transform.smoothscale(img, new_size)
                
                offset_x = (new_size[0] - 800) // 2
                offset_y = (new_size[1] - 800) // 2
                self.screen.blit(img, (-offset_x, -offset_y))
                
            else:
                self.screen.blit(img, (0, 0))
                
            pygame.display.flip()

    def set_talking(self, state: bool):
        """Altera o estado para quando a Atlas estiver falando."""
        self.is_talking = state
