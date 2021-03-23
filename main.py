
from app import create_app, db
# from app.models import Role


flask_app = create_app()
flask_app.run("0.0.0.0", 5000, debug=True)
flask_app.app_context().push()

# db.drop_all(app=flask_app)
db.create_all(app=flask_app)

