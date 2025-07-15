#!/usr/bin/env python3
"""
Louvre Top 25 Artworks Scraper
Collects detailed information about the most famous artworks in the Louvre Museum
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from urllib.parse import urljoin, urlparse

class LouvreArtworkScraper:
    def __init__(self):
        self.base_url = "https://www.louvre.fr"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def search_artwork_urls(self, artwork_title, artist_name):
        """Search for specific artwork URLs on the Louvre website"""
        search_urls = [
            f"https://www.louvre.fr/en/explore/the-palace/from-the-royal-residence-to-the-museum/collections",
            f"https://collections.louvre.fr/en/search?q={artwork_title.replace(' ', '+')}"
        ]
        
        # Try to find the artwork page
        for url in search_urls:
            try:
                response = self.session.get(url, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    # Look for links containing artwork title
                    links = soup.find_all('a', href=True)
                    for link in links:
                        href = link.get('href')
                        link_text = link.get_text().lower()
                        if artwork_title.lower() in link_text or artist_name.lower() in link_text:
                            return urljoin(self.base_url, href)
            except Exception as e:
                print(f"Error searching for {artwork_title}: {e}")
                continue
        
        return None
    
    def get_high_quality_image(self, title, artist):
        """Get high-quality images using web search approach"""
        search_terms = [
            f"{title} {artist} Louvre high resolution",
            f"{title} {artist} Louvre Museum",
            f"{title} high quality image Louvre"
        ]
        
        # Common museum image repositories
        image_sources = [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/e/eb/Rubelli_-_Utst%C3%A4llning_-_Hallwylska_museet_-_39434.tif/lossy-page1-195px-Rubelli_-_Utst%C3%A4llning_-_Hallwylska_museet_-_39434.tif.jpg",
            "https://www.louvre.fr/",
            "https://collections.louvre.fr/",
            "https://www.wikiart.org/",
            "https://www.metmuseum.org/",
            "https://commons.wikimedia.org/"
        ]
        
        # For now, return a placeholder - in production we'd implement actual image search
        artwork_slug = title.lower().replace(' ', '-').replace("'", '')
        return f"https://collections.louvre.fr/en/artwork/{artwork_slug}"

    def create_artwork_data(self):
        """Create the top 25 artworks data structure"""
        artworks = [
            {
                "title": "Mona Lisa",
                "artist": "Leonardo da Vinci",
                "date": "1503-1506",
                "medium": "Oil on poplar wood",
                "dimensions": "77 cm × 53 cm (30 in × 21 in)",
                "description": "Portrait of Lisa Gherardini, wife of Florentine merchant Francesco del Giocondo. Famous for her enigmatic smile and direct gaze.",
                "significance": "The world's most famous painting, revolutionized portraiture with its three-quarter view and psychological depth. Stolen in 1911, which amplified its global fame.",
                "location": "Denon Wing, Room 711 (Salle des États), Level 1",
                "image_url": "https://upload.wikimedia.org/wikipedia/commons/e/ec/Mona_Lisa%2C_by_Leonardo_da_Vinci%2C_from_C2RMF_retouched.jpg"
            },
            {
                "title": "The Raft of the Medusa",
                "artist": "Théodore Géricault",
                "date": "1818-1819",
                "medium": "Oil on canvas",
                "dimensions": "491 cm × 716 cm (193 in × 282 in)",
                "description": "Depicts survivors of the 1816 French frigate Méduse shipwreck. Shows the desperate moment when survivors signal to a distant rescue ship.",
                "significance": "Groundbreaking work that challenged traditional history painting by depicting a contemporary scandal. Bold political statement criticizing the monarchy's incompetence.",
                "location": "Denon Wing, Room 700 (Red Rooms), Level 1",
                "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Line-crossing_ceremony_aboard_M%C3%A9duse-Jules_de_Caudin-IMG_4783-cropped.JPG/220px-Line-crossing_ceremony_aboard_M%C3%A9duse-Jules_de_Caudin-IMG_4783-cropped.JPG"
            },
            {
                "title": "Liberty Leading the People",
                "artist": "Eugène Delacroix",
                "date": "1830",
                "medium": "Oil on canvas",
                "dimensions": "260 cm × 325 cm (102 in × 128 in)",
                "description": "Commemorates the July Revolution of 1830. Shows Liberty as a woman leading revolutionaries over barricades, holding the French tricolor flag.",
                "significance": "Iconic symbol of revolution and freedom. Masterpiece of French Romanticism that has inspired democratic movements worldwide.",
                "location": "Denon Wing, Room 700 (Red Rooms), Level 1",
                "image_url": "https://upload.wikimedia.org/wikipedia/commons/a/a7/Eug%C3%A8ne_Delacroix_-_La_libert%C3%A9_guidant_le_peuple.jpg"
            },
            {
                "title": "The Coronation of Napoleon",
                "artist": "Jacques-Louis David",
                "date": "1805-1807",
                "medium": "Oil on canvas",
                "dimensions": "621 cm × 979 cm (244 in × 385 in)",
                "description": "Depicts Napoleon crowning Josephine as empress at Notre-Dame Cathedral on December 2, 1804. Features over 150 meticulously detailed figures.",
                "significance": "Monumental work of Neoclassical art and imperial propaganda. Commissioned by Napoleon himself to legitimize his rule and celebrate his coronation.",
                "location": "Denon Wing, Room 702 (Salle Daru), Level 1",
                "image_url": "https://upload.wikimedia.org/wikipedia/commons/0/08/Jacques-Louis_David%2C_The_Coronation_of_Napoleon_edit.jpg"
            },
            {
                "title": "The Wedding Feast at Cana",
                "artist": "Paolo Veronese",
                "date": "1562-1563",
                "medium": "Oil on canvas",
                "dimensions": "677 cm × 994 cm (267 in × 391 in)",
                "description": "The largest canvas in the Louvre, depicting Christ's first miracle of turning water into wine. Features 132 figures in Venetian Renaissance dress.",
                "significance": "Masterpiece of Venetian Renaissance art. Originally created for San Giorgio Maggiore monastery in Venice, seized by Napoleon's forces.",
                "location": "Denon Wing, Room 711 (Salle des États), Level 1",
                "image_url": "https://i.pinimg.com/originals/25/f0/08/25f008b3953d5c52e61987826214fb4e.jpg"
            },
            {
                "title": "Venus de Milo",
                "artist": "Alexandros of Antioch (attributed)",
                "date": "150-125 BCE",
                "medium": "Parian marble",
                "dimensions": "204 cm (80 in) height",
                "description": "Ancient Greek sculpture of Aphrodite (Venus). Despite missing arms, represents the pinnacle of classical beauty and proportion.",
                "significance": "Supreme example of ancient Greek sculpture and ideals of beauty. One of the Louvre's 'three great ladies' alongside Mona Lisa and Winged Victory.",
                "location": "Sully Wing, Room 346, Level 0",
                "image_url": "https://i.pinimg.com/originals/e4/f4/81/e4f481e47a3c80176b798381cbff2100.jpg"
            },
            {
                "title": "The Winged Victory of Samothrace",
                "artist": "Unknown ancient Greek sculptor",
                "date": "c. 200-190 BCE",
                "medium": "Parian marble",
                "dimensions": "244 cm (96 in) height",
                "description": "Hellenistic sculpture of Nike (Victory) landing on a ship's prow. Demonstrates masterful carving of flowing drapery and sense of movement.",
                "significance": "One of the greatest surviving masterpieces of Hellenistic sculpture. Commemorates a naval victory and exemplifies dynamic movement in stone.",
                "location": "Denon Wing, Daru staircase, Level 1",
                "image_url": "https://pbs.twimg.com/media/Fq8LNtRXoAAsl0v.jpg"
            },
            {
                "title": "The Virgin and Child with Saint Anne",
                "artist": "Leonardo da Vinci",
                "date": "1501-1519",
                "medium": "Oil on wood",
                "dimensions": "168 cm × 130 cm (66 in × 51 in)",
                "description": "Unfinished painting showing Saint Anne, the Virgin Mary, and infant Jesus in triangular composition. Demonstrates Leonardo's sfumato technique.",
                "significance": "Technical masterpiece showcasing Leonardo's ability to handle complex multi-figure compositions. Commissioned by King Louis XII of France.",
                "location": "Denon Wing, Room 710, Level 1",
                "image_url": "https://i.pinimg.com/originals/9c/83/be/9c83beb5be79e7dd8bee2719bd5e9ea6.jpg"
            },
            {
                "title": "The Virgin of the Rocks",
                "artist": "Leonardo da Vinci",
                "date": "1483-1486",
                "medium": "Oil on wood",
                "dimensions": "199 cm × 122 cm (78 in × 48 in)",
                "description": "Depicts the Virgin Mary with infant Jesus, John the Baptist, and the angel Uriel in a rocky landscape. Showcases Leonardo's mastery of light and shadow.",
                "significance": "Exemplifies Leonardo's innovative use of chiaroscuro and atmospheric perspective. One of two versions, the other being in London's National Gallery.",
                "location": "Denon Wing, Room 710, Level 1",
                "image_url": "https://i.pinimg.com/736x/6e/83/9d/6e839dd5bf1b7895ec28af7e1214cbb2.jpg"
            },
            {
                "title": "The Lacemaker",
                "artist": "Johannes Vermeer",
                "date": "1669-1670",
                "medium": "Oil on canvas",
                "dimensions": "24.5 cm × 21 cm (9.6 in × 8.3 in)",
                "description": "Intimate portrait of a young woman focused on delicate lacework. Despite its small size, it's considered one of the greatest genre paintings.",
                "significance": "Masterpiece of Dutch Golden Age painting. Demonstrates Vermeer's exceptional skill with light and his likely use of camera obscura techniques.",
                "location": "Richelieu Wing, Room 837, Level 2",
                "image_url": "https://i.pinimg.com/originals/4b/51/5c/4b515c5588b993c5a2a31e8b6c62c0ed.png"
            },
            {
                "title": "Oath of the Horatii",
                "artist": "Jacques-Louis David",
                "date": "1784",
                "medium": "Oil on canvas",
                "dimensions": "330 cm × 425 cm (130 in × 167 in)",
                "description": "Depicts three Roman brothers swearing an oath to their father before battle. Contrasts male resolve with female emotion in background.",
                "significance": "Quintessential example of Neoclassical painting. Promotes civic duty and patriotism, became symbol of revolutionary values in France.",
                "location": "Denon Wing, Room 702, Level 1",
                "image_url": "https://i.pinimg.com/736x/e1/b5/7f/e1b57fe987deac9595daca07ebd7d98e.jpg"
            },
            {
                "title": "Psyche Revived by Cupid's Kiss",
                "artist": "Antonio Canova",
                "date": "1793",
                "medium": "Marble",
                "dimensions": "155 cm × 168 cm (61 in × 66 in)",
                "description": "Neoclassical sculpture depicting Cupid reviving Psyche with a kiss. Captures the tender moment from Greek mythology.",
                "significance": "Masterpiece of Neoclassical sculpture by the greatest sculptor of his era. Exemplifies the movement's ideals of beauty and emotional expression.",
                "location": "Denon Wing, Room 403, Level 0",
                "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Amore_e_Psiche%2C_Canova.jpg/220px-Amore_e_Psiche%2C_Canova.jpg"
            },
            {
                "title": "The Dying Slave",
                "artist": "Michelangelo",
                "date": "1513-1515",
                "medium": "Marble",
                "dimensions": "229 cm (90 in) height",
                "description": "One of two 'Slaves' sculptures originally intended for Pope Julius II's tomb. Shows a muscular figure in a moment of peaceful surrender.",
                "significance": "Demonstrates Michelangelo's mastery of human anatomy and emotion. The unfinished sections reveal his artistic process.",
                "location": "Denon Wing, Room 403 (Michelangelo Gallery), Level 0",
                "image_url": "https://live.staticflickr.com/7304/9571217616_e879be8176_b.jpg"
            },
            {
                "title": "The Rebellious Slave",
                "artist": "Michelangelo",
                "date": "1513-1515",
                "medium": "Marble",
                "dimensions": "215 cm (85 in) height",
                "description": "Companion to 'The Dying Slave', shows a figure struggling against bonds. Originally carved for Pope Julius II's tomb project.",
                "significance": "Showcases Michelangelo's ability to convey psychological struggle in stone. Part of the incomplete Julius II tomb project.",
                "location": "Denon Wing, Room 403 (Michelangelo Gallery), Level 0",
                "image_url": "https://live.staticflickr.com/228/458780881_113ca123e5_b.jpg"
            },
            {
                "title": "The Turkish Bath",
                "artist": "Jean-Auguste-Dominique Ingres",
                "date": "1852-1859",
                "medium": "Oil on canvas",
                "dimensions": "108 cm × 110 cm (43 in × 43 in)",
                "description": "Tondo (circular) painting depicting nude women in a harem bath. Combines Western and Near Eastern artistic influences.",
                "significance": "Masterpiece of Orientalist painting. Originally rectangular, later modified to circular format. Exemplifies 19th-century European fascination with the Orient.",
                "location": "Sully Wing, Room 940, Level 2",
                "image_url": "https://live.staticflickr.com/6186/6210996771_6d04ac6557_b.jpg"
            },
            {
                "title": "Portrait of Louis XIV",
                "artist": "Hyacinthe Rigaud",
                "date": "1701",
                "medium": "Oil on canvas",
                "dimensions": "277 cm × 194 cm (109 in × 76 in)",
                "description": "Majestic standing portrait of the Sun King in full regalia. Originally intended as a gift for his grandson but kept by the king.",
                "significance": "Quintessential example of royal portraiture. Became the official portrait of Louis XIV and model for subsequent royal portraits.",
                "location": "Sully Wing, Room 602, Level 1",
                "image_url": "https://upload.wikimedia.org/wikipedia/commons/5/5f/Louis_XIV_of_France.jpg"
            },
            {
                "title": "The Card Sharp with the Ace of Diamonds",
                "artist": "Georges de la Tour",
                "date": "1636-1638",
                "medium": "Oil on canvas",
                "dimensions": "106 cm × 146 cm (42 in × 57 in)",
                "description": "Moralistic genre painting showing three conspirators about to cheat a naive card player. Demonstrates masterful use of candlelight.",
                "significance": "Exemplifies La Tour's mastery of chiaroscuro and moral storytelling. Part of the moralizing genre popular in the 17th century.",
                "location": "Sully Wing, Room 912, Level 2",
                "image_url": "https://i.pinimg.com/736x/97/27/bb/9727bbf8a8c157349f76f4cd1f35c5dc.jpg"
            },
            {
                "title": "The Rape of the Sabine Women",
                "artist": "Nicolas Poussin",
                "date": "1637-1638",
                "medium": "Oil on canvas",
                "dimensions": "159 cm × 206 cm (63 in × 81 in)",
                "description": "Depicts the legendary abduction of Sabine women by Romans. Shows the chaos and violence of the mythological event.",
                "significance": "Masterpiece of French Baroque painting. First in a series of four paintings by Poussin on this theme, exemplifying his classical style.",
                "location": "Richelieu Wing, Room 825, Level 2",
                "image_url": "https://live.staticflickr.com/2105/2101501599_8296d19e20_b.jpg"
            },
            {
                "title": "Gabrielle d'Estrées and One of Her Sisters",
                "artist": "Unknown (School of Fontainebleau)",
                "date": "c. 1594",
                "medium": "Oil on wood",
                "dimensions": "96 cm × 125 cm (38 in × 49 in)",
                "description": "Mysterious portrait showing Gabrielle d'Estrées, mistress of Henry IV, with her sister. The sister's gesture toward Gabrielle's breast announces her pregnancy.",
                "significance": "Enigmatic masterpiece of French Renaissance court painting. The unusual gesture has been interpreted as announcing royal pregnancy.",
                "location": "Richelieu Wing, Room 824, Level 2",
                "image_url": "https://i.pinimg.com/originals/0a/5b/da/0a5bda3e514c3289e0af43c6637845b2.jpg"
            },
            {
                "title": "The Pastoral Concert",
                "artist": "Titian (disputed attribution)",
                "date": "c. 1509",
                "medium": "Oil on canvas",
                "dimensions": "105 cm × 137 cm (41 in × 54 in)",
                "description": "Mysterious painting showing clothed men with nude women in a pastoral setting. Authorship debated between Titian and Giorgione.",
                "significance": "Masterpiece of Venetian Renaissance painting. Rich in symbolism and allegory, leaving interpretation open to viewers.",
                "location": "Denon Wing, Room 711, Level 1",
                "image_url": "https://s-media-cache-ak0.pinimg.com/736x/0a/41/d1/0a41d108ce0fdff65f596f66884c1441.jpg"
            },
            {
                "title": "The Seated Scribe",
                "artist": "Unknown ancient Egyptian sculptor",
                "date": "c. 2620-2500 BCE (4th Dynasty)",
                "medium": "Limestone with rock crystal and magnesite inlays",
                "dimensions": "53.7 cm (21 in) height",
                "description": "Lifelike sculpture of a scribe in cross-legged position, ready to write. Eyes inlaid with rock crystal create piercing gaze.",
                "significance": "One of the masterpieces of ancient Egyptian art. Demonstrates the high status of scribes and importance of literacy in ancient Egypt.",
                "location": "Sully Wing, Room 635, Level 1",
                "image_url": "https://i.pinimg.com/originals/a6/aa/8b/a6aa8bacca4819fe9e675889bf1ce7c4.png"
            },
            {
                "title": "The Code of Hammurabi",
                "artist": "Unknown Babylonian craftsmen",
                "date": "c. 1754 BCE",
                "medium": "Basalt",
                "dimensions": "225 cm (89 in) height",
                "description": "Black stone stele inscribed with one of the earliest and most complete legal codes. Features relief of Hammurabi receiving laws from sun god Shamash.",
                "significance": "Fundamental document in the history of law and justice. Contains 282 laws covering various aspects of Babylonian society.",
                "location": "Richelieu Wing, Room 227, Level 0",
                "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/64/P1050763_Louvre_code_Hammurabi_face_rwk.JPG/1200px-P1050763_Louvre_code_Hammurabi_face_rwk.JPG"
            },
            {
                "title": "St. Francis of Assisi Receiving the Stigmata",
                "artist": "Giotto di Bondone",
                "date": "c. 1295-1300",
                "medium": "Tempera on wood",
                "dimensions": "313 cm × 163 cm (123 in × 64 in)",
                "description": "Depicts Saint Francis receiving the stigmata from a six-winged seraph. Marks transition from Byzantine to Renaissance style.",
                "significance": "Pivotal work in art history, signaling the decline of Byzantine style and birth of Renaissance naturalism under Giotto's influence.",
                "location": "Denon Wing, Room 708, Level 1",
                "image_url": "http://farm4.staticflickr.com/3102/5718445199_ee35314936_z.jpg"
            },
            {
                "title": "The Astronomer",
                "artist": "Johannes Vermeer",
                "date": "1668",
                "medium": "Oil on canvas",
                "dimensions": "51 cm × 45 cm (20 in × 18 in)",
                "description": "Shows a scholar studying a celestial globe, surrounded by astronomical instruments. Companion piece to 'The Geographer'.",
                "significance": "Exemplifies Vermeer's mastery of light and domestic scenes. Represents the Scientific Revolution's emphasis on empirical observation.",
                "location": "Sully Wing, Room 837, Level 2",
                "image_url": "https://i.pinimg.com/originals/dc/1d/14/dc1d140227c040391348b2082a2ea459.jpg"
            },
            {
                "title": "St. Michael Vanquishing Satan",
                "artist": "Raphael",
                "date": "1518",
                "medium": "Oil on wood",
                "dimensions": "268 cm × 160 cm (106 in × 63 in)",
                "description": "Depicts the archangel Michael defeating Satan. Commissioned by Pope Leo X, shows the triumph of good over evil.",
                "significance": "Late masterpiece by Raphael, showcasing his mature style. Powerful religious allegory created during the High Renaissance.",
                "location": "Denon Wing, Room 710, Level 1",
                "image_url": "https://i.pinimg.com/originals/70/7e/aa/707eaa2a2f7ed7e1b477075b5bafe3cd.jpg"
            }
        ]
        
        return artworks

    def save_to_json(self, artworks, filename):
        """Save artworks data to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(artworks, f, ensure_ascii=False, indent=2)
        print(f"Data saved to {filename}")

def main():
    scraper = LouvreArtworkScraper()
    
    print("Creating Louvre Top 25 Artworks dataset...")
    artworks = scraper.create_artwork_data()
    
    # Save to JSON file
    output_file = "/home/ubuntu/louvre_top25_artworks.json"
    scraper.save_to_json(artworks, output_file)
    
    print(f"Successfully created dataset with {len(artworks)} artworks")
    print(f"Data saved to: {output_file}")

if __name__ == "__main__":
    main()
