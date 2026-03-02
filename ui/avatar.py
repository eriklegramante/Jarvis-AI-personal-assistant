import pygame
import os

class JarvisAvatar:
    def __init__(self, base_path="ui/assets/avatar"):
        self.screen = pygame.display.set_mode((300, 300), pygame.NOFRAME | pygame.SRCALPHA)
        
        # Atributos de controle
        self.current_state = "idle"
        self.is_talking = False
        self.frame_index = 0
        
        # Carregamento dos Ativos
        self.assets = {
            "idle": self._load_frames(f"{base_path}/idle"),
            "talking": self._load_frames(f"{base_path}/talking"),
            "listening": self._load_frames(f"{base_path}/listening")
        }

    def _load_frames(self, path):
        """Carrega PNGs garantindo transparência."""
        frames = []
        if os.path.exists(path):
            files = sorted([f for f in os.listdir(path) if f.endswith('.png')])
            for f in files:
                img = pygame.image.load(os.path.join(path, f)).convert_alpha()
                frames.append(img)
        return frames if frames else [pygame.Surface((300, 300), pygame.SRCALPHA)]

    def play_idle(self):
        """Animação de repouso: respiração suave e piscadas."""
        self.current_state = "idle"
        self._animate(speed=0.1) 

    def play_talking(self):
        """Animação de fala: sincronizada com a saída de áudio."""
        self.current_state = "talking"
        self._animate(speed=0.25) 

    def play_listening(self):
        """Animação de escuta: sinaliza que o microfone está ativo."""
        self.current_state = "listening"
        self._animate(speed=0.15)

    def _animate(self, speed):
        """Lógica interna para girar os frames do estado atual."""
        frames = self.assets.get(self.current_state)
        self.frame_index = (self.frame_index + speed) % len(frames)
        img = frames[int(self.frame_index)]
        
        self.screen.fill((0, 0, 0, 0))
        self.screen.blit(img, (0, 0))
        pygame.display.flip()

    def draw(self):
        """O Loop principal decide qual ação executar."""
        if self.is_talking:
            self.play_talking()
        elif self.current_state == "listening":
            self.play_listening()
        else:
            self.play_idle()

    def set_talking(self, state: bool):
        """Interface para o main.py controlar a fala."""
        self.is_talking = state
        if not state: self.frame_index = 0 