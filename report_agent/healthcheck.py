from models import PostgresDatabase, report_generation

def main_loop():
    instance = PostgresDatabase()
    report = instance.get_all_metrics()
    report_generation(report)

if __name__ == "__main__":

    main_loop()
