from __future__ import division
from Parser import parse_all
import os
from config import *
from Indexer import index
import multiprocessing

# Request all the cores as Processors
MAX_PROCESSES = multiprocessing.cpu_count()


def worker(files):
    """
    :param files: a list of filenames that are to be used by the worker process
    :return: Void
    """
    # Parse XML docs + add features
    parsed_docs = parse_all(files)

    # Index parsed docs with Elastic search
    index(parsed_docs)


def chunk(data):
    """
    :param data: All the files containing the blog entries in the data folder
    :return: List of List containing files chunked based on the number of
             processes available
    """
    chunks = []
    chunk_size = int(len(data) / MAX_PROCESSES)

    for i in range(0, len(data), chunk_size):
        chunks.append(data[i:i + chunk_size])
    return chunks


if __name__ == '__main__':
    all_files = os.listdir(DATASET_PATH)
    chunks = chunk(all_files)
    jobs = []

    # Spawn processes to start processing the data
    for i in range(0, MAX_PROCESSES):
        p = multiprocessing.Process(target=worker, args=([chunks[i]]))
        jobs.append(p)
        p.start()

    # Wait for all the processes to finish
    [job.join() for job in jobs]