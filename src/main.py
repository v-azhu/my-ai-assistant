from chat import chat_manager


def main():
    """
    Application entry point.
    """

    print("=" * 50)
    print("My AI Assistant")
    print("Long-term memory AI assistant")
    print("Type 'exit' to quit")
    print("=" * 50)


    while True:

        user_input = input("\nYou: ")


        if user_input.lower() in [
            "exit",
            "quit",
            "bye"
        ]:
            print(
                "Assistant: Goodbye!"
            )
            break


        try:

            response = chat_manager.send_message(
                user_input
            )

            print(
                "\nAssistant:",
                response
            )


        except Exception as e:

            print(
                "\nError:",
                str(e)
            )


if __name__ == "__main__":
    main()