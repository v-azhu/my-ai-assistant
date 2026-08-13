from config import config
from providers import LLMError

EXIT_COMMANDS = ("exit", "quit", "bye")


def main():
    """Application entry point."""
    try:
        config.validate()
    except ValueError as e:
        print(f"Configuration error:\n{e}")
        return

    # Imported after config validation so a missing API key fails
    # fast with a clear message instead of a raw exception.
    from chat import chat_manager

    print("=" * 50)
    print("My AI Assistant")
    print(f"Provider: {config.LLM_PROVIDER}")
    print("Long-term memory AI assistant")
    print("Type 'exit' to quit")
    print("=" * 50)

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nAssistant: Goodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in EXIT_COMMANDS:
            print("Assistant: Goodbye!")
            break

        try:
            response = chat_manager.send_message(user_input)
            print(f"\nAssistant: {response}")
        except LLMError as e:
            print(f"\n[Assistant unavailable] {e}")
        except Exception as e:
            # Unexpected bug rather than a known provider failure —
            # surface it clearly instead of silently degrading.
            print(f"\n[Unexpected error] {e}")


if __name__ == "__main__":
    main()
