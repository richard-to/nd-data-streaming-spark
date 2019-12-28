import json

from kafka import KafkaConsumer

import settings


def main():
    consumer = KafkaConsumer(
        settings.KAFKA_TOPIC,
        auto_offset_reset="earliest",
        bootstrap_servers=[settings.KAFKA_BOOTSTRAP_SERVERS],
        enable_auto_commit=False,
        group_id=settings.KAFKA_CLIENT_ID,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )

    for message in consumer:
        print(message.value)


if __name__ == "__main__":
    main()
