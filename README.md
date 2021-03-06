# RegistryExplorer
A Docker Registry Explorer

## Help
```
usage: RegistryExplorer.py [-h] [--show-images] [--show-tags-list]
                           [--image IMAGE] [--password PASSWORD]
                           [--show-manifests] [--tag TAG] [--download-blob]
                           [--blob BLOB] [--download-all-blobs]
                           [--username USERNAME] [--ssl-disable-verify]
                           url

Docker Registry Explorer

positional arguments:
  url                   Base URL of the Docker Registry

optional arguments:
  -h, --help            show this help message and exit
  --show-images, -si    Show Images Repositories in the Registry
  --show-tags-list, -stl
                        Show Tag Lists in the Image Repository
  --image IMAGE, -i IMAGE
                        Image Repository Name
  --password PASSWORD, -p PASSWORD
                        Password of the Docker Registry (Basic Authentication)
  --show-manifests, -sm
                        Show Manifests for Tag/Image in the Repository
  --tag TAG, -t TAG     Tag of the Image
  --download-blob, -db  Download the Blob in the Image Repository
  --blob BLOB, -b BLOB  Blob to Download from the Image Repository
  --download-all-blobs, -dab
                        Download all the Blobs in the Tag/Image
  --username USERNAME, -u USERNAME
                        Username of the Docker Registry (Basic Authentication)
  --ssl-disable-verify, -sdv
                        Disable the SSL Certificate Verification
```

### Getting the Image List
```RegistryExplorer.py --show-images --username username --password password --ssl-disable https://dockerregistrypath/v2/```

### Getting the Tags List
```RegistryExplorer.py --show-tags-list --image imagename --username username --password password --ssl-disable https://dockerregistrypath/v2/```

### Getting Manifest for Blobs
```RegistryExplorer.py --show-manifests --image imagename --tag tagname --username username --password password --ssl-disable https://dockerregistrypath/v2/```

### Getting Specific Blob
```RegistryExplorer.py --download-blob --image imagename  --blob 'sha256:blobhash' --username username --password password --ssl-disable https://dockerregistrypath/v2/```


### Getting All Blobs for an Image
```RegistryExplorer.py --download-all-blob --image imagename --tag tagname --username username --password password --ssl-disable https://dockerregistrypath/v2/```
