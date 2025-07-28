from futdle import create_app
from futdle.models import Time

app = create_app()

with app.app_context():
    times = Time.query.limit(8).all()
    for time in times:
        print(f"{time.nome}: {time.cores}")
