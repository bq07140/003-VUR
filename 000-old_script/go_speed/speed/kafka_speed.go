package speed

import (
	"context"
	"encoding/json"
	"fmt"
	"github.com/segmentio/kafka-go"
)

func connectKafka() *kafka.Writer {

	config := kafka.WriterConfig{
		Brokers: []string{"119.96.173.17:9092"},
		Topic:   "zcw",
	}

	writer := kafka.NewWriter(config)

	return writer
}

func sendToKafka(writer *kafka.Writer, data interface{}) error {

	jsonBytes, err := json.Marshal(data)
	if err != nil {
		return err
	}

	msg := kafka.Message{
		Value: jsonBytes,
	}

	err = writer.WriteMessages(context.Background(), msg)
	return err
}

func kafkaSpeedMain() {

	writer := connectKafka()
	for {
		data := generateData()
		err := sendToKafka(writer, data)
		if err != nil {
			fmt.Printf("Error: %+v\n", err)
			return
		}
	}
}
