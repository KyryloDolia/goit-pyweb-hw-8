from models import Quote

def search_by_name(name):
    quotes = Quote.objects(author__name=name)
    return [quote.quote for quote in quotes]

def search_by_tag(tag):
    quotes = Quote.objects(tags=tag)
    return [quote.quote for quote in quotes]

def search_by_tags(tags):
    tags_list = tags.split(",")
    quotes = Quote.objects(tags__in=tags_list)
    return [quote.quote for quote in quotes]

def main():
    print("Welcome to Quote Finder. Enter your command:")
    while True:
        command = input(">> ").strip()
        if command.lower() == "exit":
            print("Exiting...")
            break
        try:
            action, value = command.split(":", 1)
            value = value.strip()
            if action == "name":
                results = search_by_name(value)
            elif action == "tag":
                results = search_by_tag(value)
            elif action == "tags":
                results = search_by_tags(value)
            else:
                print("Unknown command. Use name, tag, tags, or exit.")
                continue

            if results:
                print("\n".join(results))
            else:
                print("No quotes found.")
        except ValueError:
            print("Invalid command format. Use action:value.")

if __name__ == "__main__":
    main()
