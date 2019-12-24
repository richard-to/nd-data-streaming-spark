import producer_server


def run_kafka_server():
    # TODO get the json file path (DONE)
    input_file = "../data/police-department-calls-for-service.json"

    # TODO fill in blanks (DONE)
    producer = producer_server.ProducerServer(
        input_file=input_file,
        topic="org.datasf.crime_data",
        bootstrap_servers="localhost:9092",
        client_id="0",
    )

    return producer


def feed():
    producer = run_kafka_server()
    producer.generate_data()


if __name__ == "__main__":
    feed()
