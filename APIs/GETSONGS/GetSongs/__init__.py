import logging
import azure.functions as func
from . import get_songs



def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    durationInMinutes = req.params.get('duration')
    song_genre = req.params.get('genre')
    song_mood = req.params.get('mood')
    if not durationInMinutes or not song_genre or not song_mood:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            durationInMinutes = req_body.get('duration')
            song_genre = req_body.get('genre')
            song_mood = req_body.get('mood')

    if durationInMinutes and song_genre and song_mood:
        durationInSeconds = int(durationInMinutes)*60
        respone = get_songs.retrieve_songs(durationInSeconds,song_genre,song_mood)
        if respone[0] == 200:
            return func.HttpResponse(body=respone[1],status_code=respone[0])
        else:
            return func.HttpResponse(
             "Unexpected Error Occured.  Please check log for more details.",
             status_code=respone[0]
        )

    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Missing Params",
             status_code=200
        )
