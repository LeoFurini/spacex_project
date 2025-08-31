from google.cloud import storage, bigquery

def get_storage_client():
    return storage.Client()

def get_bigquery_client(project=None):
    return bigquery.Client(project=project)


# if __name__ == "__main__":
#     print(get_storage_client())