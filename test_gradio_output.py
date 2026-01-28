from gradio_client import Client

try:
    client = Client("Willie999/obalapalava-demo")
    result = client.predict(
        text="Hello!!",
        api_name="/translate_pidgin"
    )
    print(f"Result Type: {type(result)}")
    print(f"Result: {result}")
except Exception as e:
    print(f"Error: {e}")
