from prometheus_client import start_http_server


def init_metrics_exporter(port=8888):
    """Initialize the Prometheus metrics exporter"""
    start_http_server(port)
