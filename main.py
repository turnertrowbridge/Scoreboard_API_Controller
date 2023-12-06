from time import sleep

import requests
import json
import states

api_url = "https://w1fyv4m4j3.execute-api.us-west-2.amazonaws.com/prod"


def call_get_request():
    try:
        # make a GET request to the API
        response = requests.get(api_url)

        # check if the request was successful
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"API request failed with status code {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")


def post_data(payload_data):
    # Convert the payload data to JSON
    payload_json = json.dumps(payload_data)

    # Set the HTTP headers
    headers = {
        "Content-Type": "application/json",  # Set the appropriate content type
    }

    try:
        # Make the POST request
        response = requests.post(api_url, data=payload_json, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response (if the response contains JSON data)
            response_data = response.json()
            print("Response:", response_data)
        else:
            print(f"POST request failed with status code {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")


def load_states():
    game_states = {
        "none": states.state_none,
        "0": states.state_0,
        "1": states.state_1,
        "2": states.state_2,
        "3": states.state_3,
        "4": states.state_4,
        "5": states.state_5,
        "6": states.state_6,
        "7": states.state_7,
        "8": states.state_8,
        "9": states.state_9,
        "10": states.state_10,
        "11": states.state_11,
        "12": states.state_12,
        "13": states.state_13,
        "14": states.state_14,
        "15": states.state_15,
        "16": states.state_16,
    }
    return game_states


def main():
    cur_state_num = 1
    game_states = load_states()
    while True:
        user_input = input("Type get, score, state, demo, reset, or exit:\n-> ").lower()
        if user_input == "get":
            response = call_get_request()
            print(response)
        elif user_input == "exit":
            break
        elif user_input == "score":
            response = call_get_request()
            print(f"{response['away-team']} {response['away-score']}, {response['home-team']} {response['home-score']}"
                  f" -- {response['inning-half']} of the {response['inning']} st/nd/th inning -- {response['outs']} outs")
        elif user_input == "state":
            answer = input("Enter state number or next: ")
            if answer == "next":
                cur_state_num = str(int(cur_state_num) + 1)
            else:
                cur_state_num = str(answer)
            if int(cur_state_num) > (len(game_states)) or int(cur_state_num) < 1:
                cur_state_num = "1"
            post_data(game_states[cur_state_num])
        elif user_input == "demo":
            post_data(states.state_none)
            print()
            for i in range(len(game_states) - 1):
                print(f"Display state {i}?")
                input("Press enter to continue")
                post_data(game_states[str(i)])
                print()
        elif user_input == "reset":
            post_data(states.state_none)

        print("\n")


if __name__ == "__main__":
    main()
