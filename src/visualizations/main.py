'''
The main menu to select the visualisation
'''
import pygame
from .utils import Label, Button
from .visualizers import APPS, Visualizer
pygame.init()

class MainApp:
    WIDTH: int = 1280
    HEIGHT: int = 720
    COLORS: dict = {"bg": pygame.Color("purple")}

    def __init__(self, fullscreen: bool = False) -> None:
        '''Initializing the main app'''
        if fullscreen:
            self.WIN: pygame.Surface = pygame.display.set_mode((MainApp.WIDTH, MainApp.HEIGHT), pygame.FULLSCREEN)
        else:
            self.WIN: pygame.Surface = pygame.display.set_mode((MainApp.WIDTH, MainApp.HEIGHT))
        pygame.display.set_caption("Visualisations")
        
        self.run: bool = True
        self.app: Visualizer | None = None

        self.loadUIElements()

    
    def clearScreen(self, update: bool = False) -> None:
        '''Clears the window by filling it the background color'''
        self.WIN.fill(self.COLORS["bg"])
        if update:
            pygame.display.update()

    def draw(self) -> None:
        self.clearScreen()
        self.drawUIElements()
        pygame.display.update()
    
    def loadUIElements(self) -> None:
        '''Loads the UI elements like Labels and Buttons'''
        # Sets the default values of the UI elements for this project.
        Label.setDefault(foreground=(255, 0, 0), background=(50, 50, 50), borderRadius = 10)

        # Adding the Labels
        self.labels: list[Label] = []
        self.labels.append(Label("Visualizations", (MainApp.WIDTH//2, MainApp.WIDTH//10), size = 80))

        # Adding the Buttons
        cols: int = 4
        self.buttons: list[Button] = [
                Button(name, (2*(i%cols + 1)*MainApp.WIDTH//10, 2*(2 + i//cols)*MainApp.HEIGHT//10), 
                                self.setApp, funcArgs = (cls,))
                for i, (name, cls) in enumerate(APPS.items())
            ]
        self.buttons.append(Button("Quit", (MainApp.WIDTH//2, 9*MainApp.HEIGHT//10), self.quit, size = 30))

    
    def drawUIElements(self) -> None:
        '''Draws the UI elements like Labels and Buttons'''
        # Drawing the labels
        for label in self.labels:
            label.draw(self.WIN)
        
        # Drawing the buttons
        for button in self.buttons:
            button.checkHover(pygame.mouse.get_pos())
            button.draw(self.WIN)

    def setApp(self, cls) -> None:
        '''Sets the app for visualization'''
        self.clearScreen(update=True)
        self.app = cls(self.WIN)
    
    def quitApp(self) -> None:
        self.app.quit()
    
    def quit(self) -> None:
        self.run = False
    
    def mainloop(self) -> None:
        while self.run:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        self.quit()
                    case pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_ESCAPE:
                                self.quit()
                    case pygame.MOUSEBUTTONDOWN:
                        for b in self.buttons:
                            if b.checkPress():
                                break

            # Starting the app if it is set
            if self.app is not None:
                self.run = self.app.mainloop()
                self.app = None
            
            self.draw()
        
        pygame.quit()

def main() -> None:
    mainApp: MainApp = MainApp()
    mainApp.mainloop()

if __name__ == "__main__":
    main()