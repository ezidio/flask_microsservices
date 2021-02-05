from flask_restplus import Api

from .consulta import api as consulta_ns
from .infrastructure import api as infrastructure_ns

api = Api(
    title='API de Consulta Médica',
    version='1.0',
    description='APIs de manutenção de consulta'
)

api.add_namespace(consulta_ns)
api.add_namespace(infrastructure_ns)