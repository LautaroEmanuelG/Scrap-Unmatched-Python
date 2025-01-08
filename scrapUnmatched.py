from playwright.sync_api import sync_playwright
import os
import requests
from collections import defaultdict
import re
from PIL import Image

def sanitize_filename(filename):
    """Reemplaza o elimina caracteres especiales en el nombre del archivo."""
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def download_image(url, filename, folder):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            os.makedirs(folder, exist_ok=True)  # Crear la carpeta si no existe
            file_path = os.path.join(folder, filename)
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"[✔] Imagen descargada: {filename}")
            convert_webp_to_png(file_path)  # Convertir la imagen a PNG
        else:
            print(f"[✘] Error al descargar la imagen: {url}")
    except Exception as e:
        print(f"[✘] Error durante la descarga de la imagen: {e}")

def convert_webp_to_png(file_path):
    """Convierte una imagen de formato webp a png."""
    try:
        img = Image.open(file_path)
        png_path = file_path.replace('.webp', '.png')
        img.save(png_path, 'PNG')
        os.remove(file_path)  # Eliminar el archivo webp original
        print(f"[✔] Imagen convertida a PNG: {png_path}")
    except Exception as e:
        print(f"[✘] Error al convertir la imagen a PNG: {e}")

def scrape_hero_page(hero_name, page_url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        print(f"[INFO] Accediendo a la página: {page_url}")
        page.goto(page_url)

        # Carpeta base donde se guardarán las imágenes
        base_folder = f"{hero_name.replace(' ', '_')}"
        hero_folder = os.path.join(base_folder, "hero")
        cards_folder = os.path.join(base_folder, "cards")

        try:
            # Procesar sección 'hero-heading'
            print("[INFO] Procesando sección 'hero-heading'.")
            hero_heading_section = page.locator("section[aria-labelledby='hero-heading']")
            hero_images = hero_heading_section.locator("img")
            hero_image_count = hero_images.count()
            print(f"[INFO] Se encontraron {hero_image_count} imágenes en 'hero-heading'.")

            hero_image_names = defaultdict(int)

            for i in range(hero_image_count):
                img_url = hero_images.nth(i).get_attribute("src")
                img_alt = hero_images.nth(i).get_attribute("alt") or f"hero_image_{i}"

                # Asignar nombre 'Shakespeare' si no hay 'alt' o 'token' en el nombre
                if 'token' in img_alt.lower():
                    img_alt = "Actor_token"
                elif 'cover' in img_alt.lower() or img_alt == f"hero_image_{i}":
                    img_alt = f"cover_{hero_name} x10"
                else:
                    img_alt = hero_name

                # Incrementar el contador si el nombre de la imagen es repetido
                hero_image_names[img_alt] += 1
                if hero_image_names[img_alt] > 1:
                    img_alt = f"{img_alt}{hero_image_names[img_alt] - 1}"

                filename = sanitize_filename(f"{img_alt.replace(' ', '_')}.webp")
                download_image(img_url, filename, hero_folder)

            # Procesar sección 'deck-cards-list'
            print(f"[INFO] Procesando sección 'deck-cards-list'.")
            cards_section = page.locator("section[aria-labelledby='deck-cards-list']")
            cards = cards_section.locator("div.card[role='banner']")

            card_count = cards.count()
            print(f"[INFO] Se encontraron {card_count} tarjetas.")
            card_names = defaultdict(int)

            for i in range(card_count):
                card = cards.nth(i)
                img_url = card.locator("img").get_attribute("src")
                card_name = card.locator("img").get_attribute("alt") or f"card_{i}"

                # Buscar el elemento <p> correspondiente para obtener la cantidad
                p_tag = card.locator("xpath=following-sibling::p").first
                p_text = p_tag.inner_text().strip() if p_tag else ""
                parts = p_text.split(' x')
                quantity = parts[0].strip() if len(parts) == 2 else "1"

                # Incrementar el contador si el nombre de la carta es repetido
                card_names[card_name] += 1
                if card_names[card_name] > 1:
                    card_name = f"{card_name}{card_names[card_name] - 1}"

                filename = sanitize_filename(f"{card_name.replace(' ', '_')} x{quantity}.webp")
                download_image(img_url, filename, cards_folder)

        except Exception as e:
            print(f"[✘] Error procesando 'deck-cards-list': {e}")

        print("[✔] Proceso de scraping completado.")
        browser.close()

if __name__ == "__main__":
    # Hardcoded values Nombre y URL
    hero_name = "Eredin"
    page_url = "https://www.the-unmatched.club/heroes/eredin"
    scrape_hero_page(hero_name, page_url)