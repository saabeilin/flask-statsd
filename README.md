Gotta get get some metrics!
===========================

Easily collect call metrics for Flask.

The common way to get the metrics is collect them via StatsD protocol
to Grafana or DataDog. It's relatively easy to measure every endpoint
by decorating it with `@statsd.timed()`, but why not automate it?

So once you've configured your statsd client, just pass it to this
extension and get the generic metrics automagically.


## Usage example


```python
from flask import Flask

from flask_statsd import FlaskStatsD

from yourapp.stats import configured_statsd_client as statsd

app = Flask()
FlaskStatsD(app, statsd=statsd, tags=['app:{}'.format(__name__)])


@app.route("/")
async def index():
    return "Ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
```

And that's, basically, it!


-----

TODO:

 [ ] Document init parameters and implement examples of using of

 [ ] Implement support for statsd

