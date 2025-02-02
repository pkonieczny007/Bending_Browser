import xml.etree.ElementTree as ET
import base64
from io import BytesIO
from PIL import Image, ImageTk
import tkinter as tk

def parse_dld_file(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Inicjalizacja zmiennych
        workpiece_name = None
        material_thickness = None
        tool_name = None
        bend_segments = []

        # Parsowanie danych z pliku
        for workpiece in root.iter('Workpiece'):
            workpiece_name = workpiece.find('WorkpieceName').get('value')
            material_thickness = workpiece.find('WorkpieceThickness').get('value')
            material = workpiece.find('WorkpieceMaterial')
            material_name = material.find('MaterialName').get('value')
            tool_name = material_name  # Zakładamy, że nazwa materiału to nazwa narzędzia

        for bend_sequence in root.iter('BendSequence'):
            for bend_step in bend_sequence.iter('BendStep'):
                deformation = bend_step.find('Deformation').get('value')
                bend_angle = bend_step.find('DeformableSystemState').find('BendAngle').get('value')
                bend_length = bend_step.find('DeformableSystemState').find('BendLength').get('value')
                bend_segments.append({'deformation': deformation, 'angle': bend_angle, 'length': bend_length})

        # Wyświetlanie wyników
        print(f"Nazwa produktu: {workpiece_name}")
        print(f"Grubość materiału: {material_thickness} mm")
        print(f"Narzędzie: {tool_name}")
        print("Segmenty gięcia:")
        for i, segment in enumerate(bend_segments, start=1):
            print(f"  Segment {i}: Deformacja = {segment['deformation']}, Kąt = {segment['angle']}°, Długość = {segment['length']} mm")

        # Wyświetlanie miniaturki
        display_thumbnail(root)

    except ET.ParseError as e:
        print(f"Błąd parsowania pliku XML: {e}")
    except FileNotFoundError:
        print(f"Plik {file_path} nie został znaleziony.")
    except Exception as e:
        print(f"Wystąpił nieoczekiwany błąd: {e}")

def display_thumbnail(root):
    try:
        # Znalezienie sekcji WorkpiecePreview
        workpiece_preview = root.find('.//WorkpiecePreview')

        # Pobranie danych obrazu
        image_data = workpiece_preview.find('Image').get('value')

        # Dekodowanie danych Base64
        image_bytes = base64.b64decode(image_data)

        # Otwieranie obrazu za pomocą PIL
        image = Image.open(BytesIO(image_bytes))

        # Tworzenie interfejsu graficznego
        window = tk.Tk()
        window.title("Podgląd elementu")

        # Konwersja obrazu do formatu kompatybilnego z tkinter
        tk_image = ImageTk.PhotoImage(image)

        # Wyświetlanie obrazu w oknie
        label = tk.Label(window, image=tk_image)
        label.pack()

        # Uruchomienie aplikacji
        window.mainloop()

    except Exception as e:
        print(f"Nie udało się wyświetlić miniaturki: {e}")

# Ścieżka do pliku .dld
file_path = 'prd.sl40034305.dld'
parse_dld_file(file_path)
