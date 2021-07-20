from flask import Response, make_response, render_template
from flask_restful import Resource


class Index(Resource):
    def get(self) -> Response:
        return make_response(
            render_template("index.html"), 200, {"Content-Type": "text/html"}
        )
