from prometheus_client import CollectorRegistry, Gauge, push_to_gateway, pushadd_to_gateway
from prometheus_client import Counter
import os
import requests
from typing import Callable, List, Tuple, Optional, Any

# Create a registry for your metrics
registry = CollectorRegistry()

# Define your counter metric
c = Counter('xxx_counter_metric', 'Example counter metric', registry=registry)

# Set the metric value (example: 5)
# g.set(5)
# Add values with specific labels
# g.labels(env_name="prod", clearmode="aggregate").set(300)

# Increment the counter by 1
c.inc()

# Define the Pushgateway URL (the one you provided)
# Extract environment variable
pushgateway_url = os.getenv("PROMETHEUS_PUSH_API")

if pushgateway_url:
    print(f"The value of PROMETHEUS_PUSH_API is: {pushgateway_url}")
else:
    print("PROMETHEUS_PUSH_API is not set.")
    raise IOError(f"PROMETHEUS_PUSH_API is not set: {pushgateway_url}")


# Define a noop (no operation) function as a callable
def noop_callable():
    print("This is a no-operation callable that does nothing.")


# Define the handler as a Callable with the correct signature

def my_https_handler(
        url: str,
        method: str,
        timeout: Optional[float],
        headers: List[Tuple[str, str]],
        data: bytes
) -> Callable[[], None]:  # Return a callable that does nothing:
    # Convert headers list of tuples to a dictionary
    headers_dict = {key: value for key, value in headers}

    # Print headers and URL for debugging
    print(f"Sending {method} request to {url} with headers {headers_dict} and content {data}")

    # Send the HTTPS request and raise an exception on failure
    url = pushgateway_url  # The lib will add some strings which will result in 404, so just workaround it
    response = requests.request(
        method=method,
        url=url,
        data=data,
        headers=headers_dict,
        timeout=timeout,
        verify=True  # Ensure server certificate is validated
    )

    # Check for errors in the response and raise an exception if needed
    if not response.ok:
        print(f"Failed to push metrics: {response.status_code} {response.text}")
        # raise IOError(f"Failed to push metrics: {response.status_code} {response.text}")

    print(f"Response status: {response.status_code}")
    print(f"Response content: {response.text}")
    return noop_callable


# Push the metric to the Pushgateway using the HTTPS handler
try:
    push_to_gateway(pushgateway_url, job='example_job', registry=registry, handler=my_https_handler)
    print("Metric pushed to the Pushgateway successfully.")
except Exception as e:
    print(f"Error: {e}")
