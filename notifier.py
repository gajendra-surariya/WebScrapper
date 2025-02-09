class Notifier:
    def notify(self, scraped: int, updated: int) -> None:
        raise NotImplementedError

class ConsoleNotifier(Notifier):
    def notify(self, scraped: int, updated: int) -> None:
        print(f"Scraping complete. Total products scraped: {scraped}. Updated in DB: {updated}.")
