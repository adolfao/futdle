from futdle import create_app
from futdle.models import Time

app = create_app()

with app.app_context():
    times = Time.query.all()
    nomes_times = [time.nome for time in times]
    print(f"Total de times: {len(nomes_times)}")
    print("Times na base de dados:")
    for nome in sorted(nomes_times):
        print(f"- {nome}")
