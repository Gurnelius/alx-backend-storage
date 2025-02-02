#!/usr/bin/env python3
from pymongo import MongoClient

def log_stats():
    client = MongoClient('mongodb://127.0.0.1:27017')
    collection = client.logs.nginx

    print(f"{collection.count_documents({})} logs")
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = collection.count_documents({ "method": method })
        print(f"\tmethod {method}: {count}")
    
    status_check = collection.count_documents({ "method": "GET", "path": "/status" })
    print(f"{status_check} status check")

if __name__ == "__main__":
    log_stats()
