from flask.ext.testing import TestCase
from pikaia import app, db
from pikaia.models.models import User, Songs, Ratings

class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.add(User("public id", "admin", "ad@min.com", False))
        db.session.add(Songs("name", "link", "author", "cover"))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
