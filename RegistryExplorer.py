#!/usr/bin/env python3

import argparse
import requests

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def main():
    parser = argparse.ArgumentParser(description='Docker Registry Explorer')
    parser.add_argument('--show-images', '-si', action='store_true', help='Show Images Repositories in the Registry')
    parser.add_argument('--show-tags-list', '-stl', action='store_true', help='Show Tag Lists in the Image Repository')
    parser.add_argument('--image', '-i', type=str, help='Image Repository Name')
    parser.add_argument('--password', '-p', type=str, help='Password of the Docker Registry (Basic Authentication)')
    parser.add_argument('--show-manifests', '-sm', action='store_true', help='Show Manifests for Tag/Image in the Repository')
    parser.add_argument('--tag', '-t', type=str, help='Tag of the Image')
    parser.add_argument('--download-blob', '-db', action='store_true', help='Download the Blob in the Image Repository')
    parser.add_argument('--blob', '-b', type=str, help='Blob to Download from the Image Repository')
    parser.add_argument('--download-all-blobs', '-dab', action='store_true', help='Download all the Blobs in the Tag/Image')
    parser.add_argument('--username', '-u', type=str, help='Username of the Docker Registry (Basic Authentication)')
    parser.add_argument('--ssl-disable-verify', '-sdv', action='store_false', help='Disable the SSL Certificate Verification')
    parser.add_argument('url', type=str, help='Base URL of the Docker Registry')

    args = parser.parse_args()
    showImages = args.show_images
    showTagsList = args.show_tags_list
    image = args.image
    showManifests = args.show_manifests
    tag = args.tag
    downloadBlob = args.download_blob
    blob = args.blob
    downloadAllBlobs = args.download_all_blobs
    url = args.url
    username = args.username
    password = args.password
    sslDisableVerify = args.ssl_disable_verify
    
    def dumpUrl(url, username='', password='', verify=True):
        print('Dumping:') 
        print('URL: ' + url)
        print(('SSL Verification Enabled' if verify else 'SSL Verification Disabled'))
        
        if username:
            print('Username: ' + username)
            print('Password: ' + password)
            auth = (username, password)
        else:
            auth = ()

        try:
            return requests.get(url, auth=auth, verify=verify)
        except requests.exceptions.SSLError:
            print('Error, could not dump url.')
            print('SSL Error Throw, try including --ssl-disable-verify to ignore certificate verification')
        except:
            print('Error, could not dump url.')
            print('Verify connection')
        sys.exit()

    def getImageList(url, username, password, verify):
        url = url + '/_catalog'
        processImageListResponse(dumpUrl(url, username, password, verify))

    def getTagsList(url, image, username, password, verify):
        url = url + '/' + image + '/tags/list'
        processTagListResponse(dumpUrl(url, username, password, verify))

    def getManifestsList(url, image, tag, username, password, verify):
        url = url + '/' + image + '/manifests/' + tag
        processManifestListResponse(dumpUrl(url, username, password, verify))

    def processManifestListResponse(resp):
        if resp.status_code == 200:
            j=resp.json()
            print('\n\nLayers Available for ' + j['name'] + ' / ' + j['tag'])
            for l in j['fsLayers']:
                print(bcolors.OKGREEN + l['blobSum'])

    def processTagListResponse(resp):
        if resp.status_code == 200:
            j=resp.json()
            print('\n\nTags Available for ' + j['name'])
            print(bcolors.OKGREEN + '\n'.join(j['tags']))

    def processImageListResponse(resp):
        if resp.status_code == 200:
            print('\n\nImages Repositories Available:')
            j=resp.json()
            print(bcolors.OKGREEN + "\n".join(j['repositories']))

    def getDownloadBlob(url, image, blob, username, password, verify):
        print('Download Blob ' + blob)
        url = url + image + '/blobs/' + blob
        filename = blob[blob.find(':')+1:] + '.tar.gz'
        download(dumpUrl(url, username, password, verify), filename)

    def getDownloadAllBlobs(url, image, tag, username, password, verify):
        print('Downloading all Blobs for ' + image + ' / ' + tag)
        urlRepo = url + '/' + image + '/manifests/' + tag
        resp = dumpUrl(urlRepo, username, password, verify)
        if resp.status_code == 200:
            j = resp.json()
            for l in j['fsLayers']:
                getDownloadBlob(url, image, l['blobSum'], username, password, verify)

    def download(response, file_name):
        with open(file_name, "wb") as file:
            print('writing to ' + file_name)
            file.write(response.content)

    if showImages:
        getImageList(url, username, password, sslDisableVerify)
    elif showTagsList:
        getTagsList(url, image, username, password, sslDisableVerify)
    elif showManifests:
        getManifestsList(url, image, tag, username, password, sslDisableVerify)
    elif downloadBlob:
        getDownloadBlob(url, image, blob, username, password, sslDisableVerify)
    elif downloadAllBlobs:
        getDownloadAllBlobs(url, image, tag, username, password, sslDisableVerify)

if __name__ == "__main__":
    main()
