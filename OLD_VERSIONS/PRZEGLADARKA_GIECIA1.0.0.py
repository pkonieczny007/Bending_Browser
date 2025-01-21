import base64
import xml.etree.ElementTree as ET
from io import BytesIO
from PIL import Image, ImageTk
import tkinter as tk

# Parsowanie pliku XML
tree = ET.parse('prd.sl40034305.dld')
root = tree.getroot()

# Znalezienie sekcji WorkpiecePreview
workpiece_preview = root.find('.//WorkpiecePreview')

# Pobranie danych obrazu
image_data = workpiece_preview.find('Image').get('value')

# Dekodowanie danych Base64
image_bytes = base64.b64decode(image_data)

# Otwieranie obrazu za pomocą PIL
image = Image.open(BytesIO(image_bytes))

# Tworzenie interfejsu graficznego
root = tk.Tk()
root.title("Podgląd elementu")

# Konwersja obrazu do formatu kompatybilnego z tkinter
tk_image = ImageTk.PhotoImage(image)

# Wyświetlanie obrazu w oknie
label = tk.Label(root, image=tk_image)
label.pack()

# Uruchomienie aplikacji
root.mainloop()
