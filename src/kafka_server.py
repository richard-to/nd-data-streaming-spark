import producer_server
import settings


def run_kafka_server():
    # TODO get the json file path (DONE)
    input_file = settings.CRIME_DATA

    # TODO fill in blanks (DONE)
    producer = producer_server.ProducerServer(
        input_file=input_file,
        topic=settings.KAFKA_TOPIC,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        client_id=settings.KAFKA_CLIENT_ID,
    )

    return producer


def feed():
    producer = run_kafka_server()
    producer.generate_data()


if __name__ == "__main__":
    feed()
