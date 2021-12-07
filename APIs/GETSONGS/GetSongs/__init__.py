import logging
import azure.functions as func
from . import get_songs



def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    durationInMinutes = req.params.get('duration')
    if not durationInMinutes:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            durationInMinutes = req_body.get('duration')

    if durationInMinutes:
        durationInSeconds = int(durationInMinutes)*60
        respone = get_songs.retrieve_songs(durationInSeconds)
        if respone[0] == 200:
            return func.HttpResponse(body=respone[1],status_code=respone[0])
        else:
            return func.HttpResponse(
             "Unexpected Error Occured.  Please check log for more details.",
             status_code=respone[0]
        )

    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a duration in the query string or in the request body for a personalized response.",
             status_code=200
        )
