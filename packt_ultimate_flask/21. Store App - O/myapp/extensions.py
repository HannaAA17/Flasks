from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask_migrate import Migrate
migrate = Migrate()

from flask_uploads import UploadSet, IMAGES
photos = UploadSet('photos', IMAGES)

