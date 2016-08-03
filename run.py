from __future__ import division
from Parser import parse_all
import os
from config import *
from Indexer import index
import multiprocessing


MAX_PROCESSES = multiprocessing.cpu_count()


def worker(files):
    # Parse XML docs + add features
    parsed_docs = parse_all(files)

    # Index parsed docs with Elastic search
    index(parsed_docs)


def chunk(data):
    chunks = []
    chunk_size = int(len(data) / MAX_PROCESSES)

    for i in range(0, len(data), chunk_size):
        chunks.append(data[i:i + chunk_size])
    return chunks


all_files = os.listdir(DATASET_PATH)
chunks = chunk(all_files)
jobs = []

for i in range(0, MAX_PROCESSES):
    p = multiprocessing.Process(target=worker, args=([chunks[i]]))
    jobs.append(p)
    p.start()

# Wait for all the processes to finish
[job.join() for job in jobs]