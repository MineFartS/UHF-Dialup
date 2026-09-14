# UHF Dialup
### Dialup over UHF Radios
*(Unfinished)*

---
### Requirements

- **2x** Computer running debian linux (Ubuntu, Rasbian, etc.)
- **2x** 2-way RX/TX radio
- **2x** 1-way RX radio
- **4x** Compatible Aux Cable

---
### Usage

- Clone the Repository
    ```
    git clone https://github.com/MineFartS/UHF-Dialup
    cd UHF-Dialup
    ```

- Start the Service
    ```
    sudo bash start.sh <local_octet> <remote_octet> <audio_card_index>
    ```

    - **local_octet:** The last number of your local IP address configuration for this link (e.g., if you want your IP to be 10.0.0.1, enter 1).

    - **remote_octet:** The last number of the remote peer's IP address configuration (e.g., if their IP is 10.0.0.2, enter 2).

    - **audio_card_index:** The system index number of the sound card you are using for the audio interface. Run `aplay -l` to list cards.


