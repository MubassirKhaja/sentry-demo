import os
import sentry_sdk
from flask import Flask

sentry_sdk.init(
    dsn=os.environ["SENTRY_DSN"],
    environment="dev",
    release="my-sentry-app@1.0.0",
    traces_sample_rate=1.0,
    send_default_pii=False,
)

app = Flask(__name__)

@app.route("/")
def home():
    return "yolo! Try /zerotrust_crash to get some stupid divvv error or maybe /notrust_huh"

@app.route("/zerotrust_crash")
def crash():
    return 1 / 0

@app.route("/notrust_huh")
def notrust():
    try:
        int("abc")
    except ValueError as e:
        sentry_sdk.set_tag("demo", "route")
        sentry_sdk.set_context("ctx", {"dattaa": "bla", "bla": 69})
        sentry_sdk.capture_exception(e)
    return "Error thrown 😒😏, but you aint gonna see no crash cuz good engineering design it should be no? pfft"

if __name__ == "__main__":
    app.run(port=5000)
