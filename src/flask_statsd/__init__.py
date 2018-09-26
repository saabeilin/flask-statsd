import time

from flask import g, request


class StatsD(object):
    def __init__(self, app=None, statsd=None):
        self.statsd = statsd
        self.metric = metric
        # If an app was provided, then call `init_app` for them
        if app is not None:
            self.init_app(app)
        else:
            self.app = None

    def init_app(self, app):
        """
        Installs plugin middleware
        """
        self.app = app
        self.setup_middleware()

    def setup_middleware(self):
        """
        (really) installs plugin middleware
        """
        self.app.before_request(self.statsd_start_timers)
        self.app.after_request(self.statsd_submit_timers)

    def statsd_start_timers(self):
        g.request_started_at = time.time()

    def statsd_submit_timers(self, response):
        def _make_stat_name(req):
            url_rule = getattr(req.url_rule, 'rule', '')
            return (
                url_rule
                    .lstrip("/")  # drop leading slash
                    .replace("/", ".")  # use traditional statsd delimiter
            )
        elapsed = time.time() - g.request_started_at
        self.statsd.timing(stat=_make_stat_name(request),
                           delta=elapsed,
                           rate=1)


class StatsDDog(StatsD):
    def __init__(self, app=None, tags=None, statsd=None, metric='api.response.time'):
        StatsD.__init__(self, app=app, statsd=statsd)
        self.metric = metric
        self.tags = tags

    def statsd_submit_timers(self, response):
        elapsed = time.time() - g.request_started_at
        tags = [
            'method:{}'.format(request.method.lower()),
            'uri_template:{}'.format(getattr(request.url_rule, 'rule', ''))
        ]
        if self.tags:
            tags.extend(self.tags)
        self.statsd.histogram(self.metric, elapsed, tags=tags)
        return response


