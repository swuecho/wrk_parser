from pprint import pprint
from .lib.wrk_parser import wrk_parser, TreeToJson
import requests


text = """
Running 30s test @ https://www.bestqa.net/sr/icu996
  8 threads and 20 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.28s   155.11ms   1.67s    87.95%
    Req/Sec     1.98      2.49    10.00     91.46%
    366 requests in 30.07s, 1.50MB read
Socket errors: connect 0, read 0, write 0, timeout 1
Requests/sec:     12.17
Transfer/sec:     51.01KB
"""
tree = wrk_parser.parse(text.strip())

pprint(TreeToJson(visit_tokens=True).transform(tree))
result = TreeToJson(visit_tokens=True).transform(tree)
pprint(result)

