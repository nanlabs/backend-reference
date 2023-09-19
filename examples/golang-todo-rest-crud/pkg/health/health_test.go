// health package include a reusable health check handler
package health

import (
	"encoding/json"
	"io"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/gorilla/mux"
	"gopkg.in/go-playground/assert.v1"
)

type healthCheck struct {
	Status string `status:"name"`
}

func TestHealthCheck(t *testing.T) {
	expectedBody := &healthCheck{
		Status: "Healthy",
	}
	router := mux.NewRouter()
	router.HandleFunc("/health", HealthCheck).Methods(http.MethodGet)

	req, _ := http.NewRequest(http.MethodGet, "/health", nil)
	recorder := httptest.NewRecorder()
	router.ServeHTTP(recorder, req)
	res := recorder.Result()

	var responseBody healthCheck
	_ = json.NewDecoder(io.Reader(res.Body)).Decode(&responseBody)

	assert.Equal(t, http.StatusOK, res.StatusCode)
	assert.Equal(t, expectedBody, responseBody)
}
