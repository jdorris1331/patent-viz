import sys
import json

message = sys.argv[1]

test = {"id": "0924123", "title": "test"}

print json.dumps(test)
