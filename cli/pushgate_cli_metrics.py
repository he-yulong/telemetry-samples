from prometheus_client import CollectorRegistry, Gauge, push_to_gateway, pushadd_to_gateway
from prometheus_client import Counter

# Create a registry for your metrics
registry = CollectorRegistry()

# Define your metric (a gauge in this case)
# g = Gauge('example_metric_name', 'Description of the metric', registry=registry)
# g = Gauge('foo', 'Gauge example', ['env_name', 'clearmode'], registry=registry)


# Define your counter metric
c = Counter('xxx_counter_metric', 'Example counter metric', registry=registry)

# Set the metric value (example: 5)
# g.set(5)
# Add values with specific labels
# g.labels(env_name="prod", clearmode="aggregate").set(300)

# Increment the counter by 1
c.inc()

# Define the Pushgateway URL (the one you provided)
pushgateway_url = 'localhost:4278'

# Push the metric to the Pushgateway
# push_to_gateway(pushgateway_url, job='example_job', registry=registry)
push_to_gateway(pushgateway_url, job='example_job', registry=registry)

print("Metric pushed to the Pushgateway successfully.")
