import tkinter as tk
from PIL import ImageGrab, ImageEnhance, ImageFilter
import pytesseract
import pyperclip
import threading

# Descomente e ajuste o caminho abaixo se o Tesseract não estiver no PATH do seu sistema
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

custom_config = r"--oem 3 --psm 6"


def preprocess_image(image):
    image = image.convert("L")
    image = image.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)
    image = image.point(lambda x: 0 if x < 140 else 255)
    return image


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
            self.start_x, self.start_y, self.start_x, self.start_y, outline="red"
        )

    def on_move_press(self, event):
        self.canvas.coords(self.selection, self.start_x, self.start_y, event.x, event.y)

    def on_button_release(self, event):
        x1, y1, x2, y2 = self.canvas.coords(self.selection)
        self.capture_screen_area(x1, y1, x2, y2)
        self.root.quit()

    def capture_screen_area(self, x1, y1, x2, y2):
        screenshot = ImageGrab.grab((x1, y1, x2, y2))
        processed_image = preprocess_image(screenshot)
        texto = pytesseract.image_to_string(processed_image, config=custom_config)
        pyperclip.copy(texto)
        print("Texto copiado para a área de transferência.")

    def run(self):
        self.root.mainloop()


def iniciar_captura():
    captura = ScreenCaptureTool()
    captura.run()


threading.Thread(target=iniciar_captura).start()
