from flask import Blueprint, Response, url_for
from datetime import datetime

sitemap_bp = Blueprint('sitemap', __name__)

@sitemap_bp.route('/sitemap.xml', methods=['GET'])
def sitemap():
    pages = [
        ('main.home', 'daily', 1.0),
        ('main.classico', 'daily', 0.9),
        ('main.escudo', 'daily', 0.9),
        ('main.sobre', 'monthly', 0.5),
        ('main.como_jogar', 'monthly', 0.5),
        ('main.politica_privacidade', 'yearly', 0.3),
        ('main.contato', 'yearly', 0.3),
        ('main.atualizacoes', 'weekly', 0.7)
    ]

    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    today = datetime.utcnow().date().isoformat()
    for page, freq, priority in pages:
        xml.append("  <url>")
        xml.append(f"    <loc>{url_for(page, _external=True)}</loc>")
        xml.append(f"    <lastmod>{today}</lastmod>")
        xml.append(f"    <changefreq>{freq}</changefreq>")
        xml.append(f"    <priority>{priority}</priority>")
        xml.append("  </url>")
    xml.append('</urlset>')
    return Response('\n'.join(xml), mimetype='application/xml')
