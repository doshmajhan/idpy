from flask_restful import Resource


class Index(Resource):
    def get(self) -> str:
        return "hello world"
