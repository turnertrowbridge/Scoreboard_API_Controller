import requests
import json
from states import state_1, state_2, state_3, state_4


api_url = "https://dnvjlmuy5f.execute-api.us-west-2.amazonaws.com/prod"


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
    # Convert the payload data to JSON (if needed)
    payload_json = json.dumps(payload_data)

    # Set the HTTP headers (if needed)
    headers = {
        "Content-Type": "application/json",  # Set the appropriate content type
        # "Authorization": "Bearer YourAccessToken"  # Include authorization headers if required
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


# def post_score(away_score, home_score):
#     payload_data = {
#         "away-team": "Dodgers",
#         "home-team": "Padres",
#         "away-score": 2,
#         "home-score": 7,
#         "inning": 7,
#         "outs": 2,
#         "batter": "Soto",
#         "pitcher": "Kershaw",
#         "pitch_count": 12,
#         "count": [0, 0],
#         "on_base": ["Machado", "Tatis", "", ""],
#         "last-play": "",
#     }
#     post_data(payload_data)

def load_states():
    states = {
        "1": state_1,
        "2": state_2,
        "3": state_3,
        "4": state_4,
    }
    return states

def main():
    cur_state_num = 1
    states = load_states()
    while True:
        user_input = input("Type get, score, state, or exit:\n-> ").lower()
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
                cur_state_num = answer
            if cur_state_num == str(len(states) + 1) or cur_state_num == "0":
                cur_state_num = "1"
            post_data(states[cur_state_num])
        print("\n")


if __name__ == "__main__":
    main()
