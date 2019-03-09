package main

import (
	"encoding/json"
	"fmt"
	"log"
	"math/rand"
	"net/http"
	"strconv"

	"github.com/gorilla/mux"
)

// RandomNumber structure
type RandomNumber struct {
	FirstNumber int `json:"first_number"`
	LastNumber  int `json:"last_number"`
}

func getHealthStatus(w http.ResponseWriter, r *http.Request) {
	var version = "0.0.1"
	var status = "healthy"
	var serviceName = "get-random-number"
	healthCheck := map[string]string{
		"Application version": version,
		"Application status":  status,
		"Service Name":        serviceName,
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(healthCheck)
}

func getRandomNumber(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	var randNum RandomNumber
	_ = json.NewDecoder(r.Body).Decode(&randNum)
	calculation := (rand.Intn(randNum.LastNumber-randNum.FirstNumber) + randNum.FirstNumber)
	log.Print("Random number: " + strconv.Itoa(calculation))
	calculationResponse := map[string]int{
		"random_number": calculation,
	}
	json.NewEncoder(w).Encode(calculationResponse)
}

func main() {
	// Init Router
	serverPort := 8000
	r := mux.NewRouter()

	// Router Handler / Endpoints
	r.HandleFunc("/health-check", getHealthStatus).Methods("GET")
	r.HandleFunc("/api/random-number", getRandomNumber).Methods("POST")

	fmt.Println("Starting web server on port " + strconv.Itoa(serverPort))
	log.Fatal(http.ListenAndServe(":"+strconv.Itoa(serverPort), r))
}
