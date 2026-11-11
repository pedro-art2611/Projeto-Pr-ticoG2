"""Verifica referências locais, âncoras e extensão normativa do resumo."""
import re
from html.parser import HTMLParser
from pathlib import Path
root = Path(__file__).resolve().parents[1]


class ArticleParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids = []; self.links = []; self.images = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs: self.ids.append(attrs["id"])
        for key in ["href", "src"]:
            if key in attrs: self.links.append(attrs[key])
        if tag == "img": self.images.append(attrs)


text = (root / "docs/index.html").read_text(encoding="utf-8")
p = ArticleParser(); p.feed(text)
assert len(p.ids) == len(set(p.ids)), "IDs duplicados"
for link in p.links:
    if link.startswith("#"): assert link[1:] in p.ids, link
    elif not re.match(r"[a-z]+:", link): assert (root / "docs" / link).is_file(), link
assert all(image.get("alt") for image in p.images), "Figura sem descrição alternativa"
summary = re.search(r'<h2 id="resumo">Resumo</h2>\s*<p>(.*?)</p>', text, re.S)[1]
words = len(summary.split())
assert 150 <= words <= 250, f"Resumo: {words} palavras"
assert "${" not in text, "Placeholder não substituído"
assert "Pedro Artur Brandão Murillo e Daniel de Oliveira Teixeira Silva" in text
assert all(section in p.ids for section in ["introducao", "metodologia", "resultados", "conclusao", "fair", "referencias"])
assert "Pearson r =" in text and "Spearman ρ =" in text
assert "Decreto nº 8.777/2016" in text
assert all(character not in text for character in [chr(0x2013), chr(0x2014)]), "Travessão em texto autoral"
print(f"Artigo: {words} palavras no resumo; {len(p.images)} figuras; referências locais e âncoras válidas.")
