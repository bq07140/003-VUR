package lateral_acceleration

import (
	"encoding/json"
	"fmt"
	"math/rand"
	"time"
)

type Data struct {
	UserId        string                 `json:"userId"`
	VehicleId     string                 `json:"vehicleId"`
	SchemaId      string                 `json:"schemaId"`
	UserMessageId string                 `json:"userMessageId"`
	UseCaseIds    []string               `json:"useCaseIds"`
	Time          string                 `json:"time"`
	Payload       map[string]interface{} `json:"payload"`
}

func generateData() Data {

	minSpeed := 0.001
	maxSpeed := 0.1

	return Data{
		UserId:        "393b4915-8a1a-43c9-a5e1-2710057fdf8b",
		VehicleId:     "b9487cfbc0c74499a970d5d08d2878c1",
		SchemaId:      "Schema-363a2145-3c28-41cb-9255-806722709cee",
		UserMessageId: "FUM-1153",
		UseCaseIds:    []string{"UseCase-1f8fc8bb-a824-46d3-972a-8492da542b4a"},
		Time:          time.Now().Format(time.RFC3339),
		Payload: map[string]interface{}{
			"mdc_id":            180940,
			"g_id":              1,
			"name":              "Lateral acceleration",
			"value":             minSpeed + rand.Float64()*(maxSpeed-minSpeed),
			"unit":              "",
			"timestamp":         time.Now().UnixMilli(),
			"containerMsgId":    4,
			"orderId":           "5a7dada3-5a54-4d21-8c9a-7061cf3599b3",
			"containerId":       "6d5a9a65-ed4e-4524-9690-23df17473a4b",
			"containerMsgCount": 4,
			"ingest_timestamp":  time.Now().UnixMilli(),
			"orderVersion":      0,
			"correlationId":     "",
		},
	}
}

func Main() {
	for {
		data := generateData()
		jsonBytes, _ := json.MarshalIndent(data, "", "    ")
		fmt.Println(string(jsonBytes))
		kafkaSpeedMain()
		time.Sleep(3 * time.Second)
	}
}
