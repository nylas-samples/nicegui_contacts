# nicegui_contacts

This sample will show you to create manage your contacts using NiceGUI.

You can follow along step-by-step in our blog post ["How to manage your contacts using NiceGUI"](https://www.nylas.com/blog/how-to-manage-your-contacts-using-nicegui/).

## Setup

### System dependencies

- Python v3.x

### Gather environment variables

You'll need the following values:

```text
CLIENT_ID = ""
CLIENT_SECRET = ""
ACCESS_TOKEN = ""
```

Add the above values to a new `.env` file:

```bash
$ touch .env # Then add your env variables
```

### Install dependencies

```bash
$ pip3 install nicegui # Nylas API SDK
$ pip3 install python-dotenv # Environment variables
```

## Usage

Run the file **nicegui_contacts.py**:

```bash
$ python3 nicegui_contacts.py
```

NiceGUI will open up your browser on port 8080.

## Learn more

Visit our [Nylas Python SDK documentation](https://developer.nylas.com/docs/developer-tools/sdk/python-sdk/) to learn more.
