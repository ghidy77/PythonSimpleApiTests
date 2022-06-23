import http
import requests
import unittest

class ApiClient:
    def post(body):
        BASE_URL = "https://some-api-example.com/v1/tests/" # //{stationId}
        headers = {"Content-Type": "application/json", "Accept": "*/*"}

        # loop through stationIds, perform a request for each station between 1-5 and save the responses in a dict
        responseMap = {}
        for i in range(1, 6):
            responseMap.update({i: requests.post(BASE_URL + str(i), body, headers)})

        return responseMap

# Test Suite that contains the 3 Test cases
class APITests(unittest.TestCase):

    def testGetVersion(self):
        print("Start test for: getVersion")
        body = {"command": "getVersion", "payload": None}
        responseMap = ApiClient.post(body)
        errorsMap = {}
        for stationId in responseMap:
            response = responseMap[stationId]
            # If Response code != 200, print it as WARNING as save it in errorsMap
            if response.status_code != http.HTTPStatus.OK:
                print("WARNING: Invalid response code for station " + str(stationId))
                errorsMap.update({stationId: "STATUS CODE: " + str(response.status_code)})
                continue
            responseBody = response.json()
            #print(responseBody["result"])
            minimumVersion = 1.6
            # Expect the result to be greater than minumum version, so only > 1.6 is valid
            if float(responseBody["result"]) <= minimumVersion:
                errorsMap.update({stationId: responseBody["result"]})

        # If there are no errors saved, mark test as passed
        self.assertDictEqual(errorsMap, {}, "Errors found on stations ! " + errorsMap.__str__())

        print("Test getVersion passed !")

    def testGetInterval(self):
        print("Start test for: getInterval")
        body = {"command": "getInterval", "payload": None}
        responseMap = ApiClient.post(body)
        errorsMap = {}
        for stationId in responseMap:
            response = responseMap[stationId]
            # If Response code != 200, print it as WARNING as save it in errorsMap
            if response.status_code != http.HTTPStatus.OK:
                print("WARNING: Invalid response code for station " + str(stationId))
                errorsMap.update({stationId: "STATUS CODE: " + str(response.status_code)})
                continue
            responseBody = response.json()
            #print(responseBody["result"])

            # Check conditions. Result is valid only if it's between 1-60
            if int(responseBody["result"]) < 1 or int(responseBody["result"]) > 60:
                errorsMap.update({stationId: responseBody["result"]})

        # If there are no errors saved, mark test as passed
        self.assertDictEqual(errorsMap, {}, "Errors found on stations ! " + errorsMap.__str__())
        print("Test getInterval passed !")

    def testSetValues(self):
        # Define the Payload for the scenarios to be validated
        payloadScenariosList = [0,1,2,9,10,11]
        scenariosWithErrors = {}
        # for each scenario, execute the requests on all stationIds
        for payload in payloadScenariosList:
            print("Start test for: setValues using Payload: " + str(payload))
            body = {"command": "setValues", "payload": payload}
            responseMap = ApiClient.post(body)
            errorsMap = {}
            for stationId in responseMap:
                response = responseMap[stationId]
                # If Response code != 200, print it as WARNING as save it in errorsMap
                if response.status_code != http.HTTPStatus.OK:
                    print("WARNING: Invalid response code for station " + str(stationId))
                    errorsMap.update({stationId: "STATUS CODE: " + str(response.status_code)})
                    continue
                responseBody = response.json()

                # Set the Expected Response, according to the specifications
                expectedResponse = "FAILED"
                # any payload greater than 1 and smaller than 10 should respond with OK
                if payload in range(2, 10):
                    expectedResponse = "OK"

                # force cast to string for Result because of a corner case: one of the results was a Boolean: True
                if responseBody["result"] != expectedResponse:
                    errorsMap.update({stationId: str(responseBody["result"]) + " for payload: " + str(payload)})

            # If there is an error in this scenario, save it in a dict with Payload as key
            if errorsMap != {}:
                scenariosWithErrors.update({payload: errorsMap})

        # If there is no error present, the test is marked as Passed
        self.assertDictEqual(scenariosWithErrors, {}, "Errors found on stations ! " + errorsMap.__str__())

        print("Test setValues passed !")

# Execute all tests
if __name__ == '__main__':
    unittest.main()

