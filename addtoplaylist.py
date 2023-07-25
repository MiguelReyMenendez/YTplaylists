from youtube import YouTube

def list_playlist_items(service, playlist_id):
    response = service.playlistItems().list(
        part='contentDetails',
        playlistId=playlist_id,
        maxResults=50
    ).execute()

    playlistItems = response['items']
    nextPageToken = response.get('nextPageToken')

    while nextPageToken:
        response = service.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=nextPageToken
        ).execute()

        playlistItems.extend(response['items'])
        nextPageToken = response.get('nextPageToken')
    return playlistItems

client_file = 'client-secret.json'
yt = YouTube(client_file)
yt.init_service()


source_playlist_ids = ['PL_XJF7k8UP4EIZspnnaL2nmXbqrxnqyBf']
target_playlist_id = 'PL_XJF7k8UP4EIZspnnaL2nmXbqrxnqyBf'

for source_playlist_id in source_playlist_ids:
    playlist_items = list_playlist_items(yt.service, source_playlist_id)
   
    for playlist_item in playlist_items:
        video_id = playlist_item['contentDetails']['videoId']
        request_body = {
            'snippet': {
                'playlistId': target_playlist_id,
                'resourceId': {
                    'kind': 'youtube#video',
                    'videoId': video_id
                }
            }
        }
        response = yt.service.playlistItems().insert(
            part='snippet',
            body=request_body
        ).execute()
        video_title = response['snippet']['title']
        print(f'Video "{video_title}" inserted to {target_playlist_id} playlist')