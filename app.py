import tkinter as tk
from PIL import ImageGrab
import pytesseract
import pyperclip
import threading

# Configuração básica do pytesseract (descomente e ajuste se necessário)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class ScreenCaptureTool:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        self.root.wait_visibility(self.root)
        self.root.attributes("-alpha", 0.3)
        self.selection = None
        self.start_x = None
        self.start_y = None
        self.canvas = tk.Canvas(self.root, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.selection = self.canvas.create_rectangle(
            self.start_x, self.start_y, 0, 0, outline="red"
        )

    def on_move_press(self, event):
        self.canvas.coords(self.selection, self.start_x, self.start_y, event.x, event.y)

    def on_button_release(self, event):
        self.capture_screen_area(self.canvas.coords(self.selection))
        self.root.quit()

    def capture_screen_area(self, coords):
        x1, y1, x2, y2 = sorted(coords[:2]) + sorted(coords[2:])
        screenshot = ImageGrab.grab((x1, y1, x2, y2))
        texto = pytesseract.image_to_string(screenshot)
        pyperclip.copy(texto)
        print("Texto copiado para a área de transferência.")

    def run(self):
        self.root.mainloop()


def iniciar_captura():
    captura = ScreenCaptureTool()
    captura.run()


# Executar em uma thread separada
threading.Thread(target=iniciar_captura).start()
