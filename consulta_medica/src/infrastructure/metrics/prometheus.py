import time
import prometheus_client
from prometheus_client import CollectorRegistry, Histogram, make_wsgi_app, multiprocess

from flask import request
from werkzeug.middleware.dispatcher import DispatcherMiddleware

registry = CollectorRegistry()
multiprocess.MultiProcessCollector(registry)

REQUEST = Histogram(
    "http_requests",
    "Time spent processing request and number of requests along with its methods and " "responses",
    ["method", "endpoint", "http_status"],
    registry=registry,
)


def before_requests():
    request.start_time = time.time()


def after_requests(response):
    request_latency = time.time() - request.start_time
    REQUEST.labels(request.method, request.path, response.status_code).observe(request_latency)
    return response


def setup_metrics(app):
#    return "opa"
    import uwsgi

    prometheus_client.values.ValueClass = prometheus_client.values.MultiProcessValue(
        _pidFunc=uwsgi.worker_id
    )
    app.before_request(before_requests)
    app.after_request(after_requests)

    return DispatcherMiddleware(app, {"/metrics": make_wsgi_app(registry=registry)})
