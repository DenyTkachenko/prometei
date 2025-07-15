def exit_handler(_, address_book, storage):
    print("💾 Saving data...")
    storage.save(address_book)
    print("👋 Good bye!")
    exit(0)