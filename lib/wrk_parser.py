from collections import ChainMap

from lark import Lark, Transformer

wrk_parser = Lark('''start: config \
_NEWLINE  "Thread Stats   Avg      Stdev     Max   +/- Stdev" \
latency_stat \
request_stat \
total \
socket_error? \
avg_req \
avg_size

config: "Running" opt_time  "test" "@" URL _NEWLINE INT "threads" "and" INT "connections"
opt_time: time
latency_stat: _NEWLINE "Latency" time time time percent
request_stat: _NEWLINE "Req/Sec" NUMBER NUMBER NUMBER percent
total: _NEWLINE total_requests "requests in" time "," size "read"
socket_error: _NEWLINE  "Socket errors:" "connect" INT ", read" INT ", write" INT ", timeout" INT
avg_req: _NEWLINE "Requests/sec:" NUMBER
avg_size: _NEWLINE "Transfer/sec:" size

total_requests: INT
time: NUMBER TIME_UNIT
TIME_UNIT: /s|ms|m|h/

size: NUMBER SIZE_UNIT
percent: NUMBER "%"

SIZE_UNIT: /KB|MB|GB/
URL:  /\S+/

_NEWLINE: NEWLINE

%import common.INT
%import common.DECIMAL
%import common.NUMBER
%import common.NEWLINE
%ignore " "
''', parser="lalr")


class TreeToJson(Transformer):
    NUMBER = float
    INT = int
    URL = str

    # def INT(self, tok):
    #    return int(tok)

    # def NUMBER(self, tok):
    #    return float(tok)

    def start(self, children):
        return dict(ChainMap({}, *filter(lambda x: x, children)))

    def config(self, children):
        [opt_time, url, threads, connection] = children
        return {**opt_time, 'url': url, 'threads': threads, 'connection': connection}

    def latency_stat(self, children):
        result = {}
        for idx, stat_name in enumerate(['avg', 'stdev', 'max', 'stdev_percent']):
            result['latency_' + stat_name.lower()] = children[idx]
        return result

    def request_stat(self, children):
        result = {}
        for idx, stat_name in enumerate(['avg', 'stdev', 'max', 'stdev_percent']):
            child = children[idx]
            result['request_' + stat_name.lower()] = child
        return result

    def total_requests(self, children):
        return children[0]

    def total(self, children):
        result = {}
        for idx, stat_name in enumerate(['requests', 'time', 'size']):
            child = children[idx]
            result['total_' + stat_name.lower()] = child

        return result

    def avg_req(self, children):
        # default rule for tokem?
        return {'avg_req': children[0]}

    def avg_size(self, children):
        # default rule for tokem?
        return {'avg_size': children[0]}

    def time(self, children):
        [number, unit] = children
        return {'time': number, 'unit': str(unit)}

    def opt_time(self, children):
        return {'opt_time': children[0]}

    def size(self, children):
        [number, unit] = children
        return {'size': number, 'unit': str(unit)}

    def percent(self, children):
        return {'percent': children[0]}

    def socket_error(self, children):
        result = {}
        for idx, stat_name in enumerate(['connect', 'read', 'write', 'timeout']):
            result['socket_error_' + stat_name.lower()] = children[idx]
        return result
