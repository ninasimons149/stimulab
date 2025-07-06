import json, re, os

VALID_LANG = {"es"}
VALID_FORMATS = {"Paperback", "Ebook", "Audiobook", "Hardcover"}

books = [
    {
        "title": "Mientras vivimos",
        "summary": "Judit, joven escritora en Barcelona, se enfrenta al dolor de crecer.",
        "image": "data/assets/portadas/mientras_vivimos.jpg",
        "file": "data/libros/mientras_vivimos.pdf",
        "isbn": "9788408041234",
        "asin": "B000ABCDE1",
        "language": "es",
        "format": "Paperback",
        "authors": [
            {
                "author_id": 1,
                "name": "Maruja Torres",
                "photo": "https://example.com/authors/torres.jpg",
                "verified": True
            }
        ],
        "tags": "drama, crecimiento personal",
        "public": True,
        "seen": 127,
        "verified": True
    }
]

def validate(book, seen_isbn, seen_asin):
    assert 5 <= len(book["title"]) <= 500
    assert len(book["summary"]) <= 1500
    assert re.match(r"^\d{13}$", book["isbn"].replace("-", ""))
    assert book["isbn"] not in seen_isbn
    seen_isbn.add(book["isbn"])
    assert re.match(r"^[A-Za-z0-9]{10}$", book["asin"])
    assert book["asin"] not in seen_asin
    seen_asin.add(book["asin"])
    assert book["language"] in VALID_LANG
    assert book["format"] in VALID_FORMATS

seen_isbn, seen_asin = set(), set()
for b in books:
    validate(b, seen_isbn, seen_asin)

os.makedirs("data", exist_ok=True)
output_path = "data/premio_planeta_2000_2025.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, indent=2)

print(f"✅ {len(books)} libros guardados en {output_path}")
