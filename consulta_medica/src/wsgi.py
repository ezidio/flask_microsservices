from infrastructure.metrics.prometheus import setup_metrics
from app import make_app

application = make_app()

# Adiciona configuração do prometheus
app_dispatch = setup_metrics(application)
