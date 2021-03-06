from flask import Flask, jsonify
from .model import configure as config_db
from .serializer import configure as config_ma


def create_app():
    app = Flask(__name__)
    app.config.from_object("project.config.Config")

    config_db(app)
    config_ma(app)

    from .blueprint.token_blueprint import bp_token
    from .blueprint.github_user_blueprint import bp_github_user
    from .blueprint.github_repository_blueprint import bp_github_repository
    from .blueprint.github_pull_request_blueprint import bp_github_pull_request
    from .blueprint.extractor_blueprint import bp_extractor
    from .blueprint.metrics_blueprint import bp_metrics
    app.register_blueprint(bp_token)
    app.register_blueprint(bp_github_user)
    app.register_blueprint(bp_github_repository)
    app.register_blueprint(bp_github_pull_request)
    app.register_blueprint(bp_extractor)
    app.register_blueprint(bp_metrics)
    return app

app = create_app()

@app.route("/status")
def hello_world():
    return jsonify(status="OK")
