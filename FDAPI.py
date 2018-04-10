#!/usr/bin/env python3

import requests
from typing import Dict

class FDAPI:
    def __init__(self, app_key='xupp86vZE75OwsAdZW0KQVG06kTweGvAfondP6cA'):
        self.base_url = "https://api.nal.usda.gov/ndb/"
        self.search_endpoint = "search/?"
        self.app_key = app_key

    #Getting items without using upc search
    def search(self, phrase: str):
        url = f'{self.base_url}{self.search_endpoint}'
        params = {"q": phrase, "api_key": self.app_key}
        response = requests.get(url, params = params, data = {"q": phrase}, headers = {"Content-Type": "application/json"})

        #print(response.url)
        #print(response.status_code)
        return self.error_handling(response)


    #To check what errors occured from a search
    def error_handling(self, response: requests) -> requests:
        # Exceptions description from https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#5xx_Server_errors
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            raise BadRequestException("The server cannot or will not process the request"
                                        "due to an apparent client error.")
        elif response.status_code == 401:
            raise UnauthorizedException("Authentication is required and has failed or has not yet been provided.")
        elif response.status_code == 403:
            raise ForbiddenException("The request was valid, but the server is refusing action.")
        elif response.status_code == 404:
            raise NotFoundException("The requested resource could not be found.")
        elif response.status_code == 408:
            raise RequestTimeoutException("The server timed out waiting for the request.")
        elif response.status_code == 410:
            raise GoneException("The resource requested is no longer available.")
        elif response.status_code == 421:
            raise MisdirectedRequestException("The request was directed at a server that is"
                                             "not able to produce a response.")
        elif response.status_code == 429:
            raise TooManyRequestException("The user has sent too many requests in a given amount of time.")
        elif response.status_code == 451:
            raise LegalException("A server operator has received a legal demand to deny access"
                                     "to a resource or to a set of resources.")
        elif response.status_code == 500:
            raise ServerErrorException("The server gave an error message.")
        elif response.status_code == 501:
            raise NotImplementedException("The server does not recognize the request method or"
                                            "it lacks the ability to fufill the request.")
        elif response.status_code == 502:
            raise BadGatewayException("The server was acting as a gateway or proxy and received"
                                    "an invalid response from the upstream server.")
        elif response.status_code == 503:
            raise ServiceUnavailableException("The server is currently unavailable.")
        elif response.status_code == 504:
            raise GatewayTimeoutException("The server was acting as a gateway or proxy and did not receive"
                                        "a timely response from the upstream server.")
        elif response.status_code == 505:
            raise HTTPVersionNotSupportedException("The server does not support the HTTP protocol"
                                                    "version used in the request.")
        elif response.status_code == 506:
            raise VariantAlsoNegotiatesException("Transparent content negotiation for the request"
                                                 "results in a circular reference.")
        elif response.status_code == 507:
            raise InsufficientStorageException("The server is unable to store the representation"
                                                "needed to complete the request.")
        elif response.status_code == 508:
            raise LoopDetectedException("The server detected an infinite loop while processing the request.")
        elif response.status_code == 510:
            raise NotExtendedException("Further extensions to the request are required for the server to fulfil it.")
        elif response.status_code == 511:
            raise NetworkAuthenticationRequiredException("The client needs to authenticate to gain network access.")
        else:
            raise Exception("Unknown Error.")

#All the exceptions:
class UpcFormatException(Exception):
    pass

class BadRequestException(Exception):
    pass

class UnauthorizedException(Exception):
    pass

class ForbiddenException(Exception):
    pass

class NotFoundException(Exception):
    pass

class RequestTimeoutException(Exception):
    pass

class GoneException(Exception):
    pass

class MisdirectedRequestException(Exception):
    pass

class TooManyRequestException(Exception):
    pass

class LegalException(Exception):
    pass

class ServerErrorException(Exception):
    pass

class NotImplementedException(Exception):
    pass

class BadGatewayException(Exception):
    pass

class ServiceUnavailableException(Exception):
    pass

class GatewayTimeoutException(Exception):
    pass

class HTTPVersionNotSupportedException(Exception):
    pass

class VariantAlsoNegotiatesException(Exception):
    pass

class InsufficientStorageException(Exception):
    pass

class LoopDetectedException(Exception):
    pass

class NotExtendedException(Exception):
    pass

class NetworkAuthenticationRequiredException(Exception):
    pass