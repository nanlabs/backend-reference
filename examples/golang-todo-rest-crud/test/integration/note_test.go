//go:build integration

// integration package include logic related to todo api integration tests
package integration

import (
	"fmt"
	"log"
	"net/http"
	"testing"
	"todo-api-golang/internal/config"
	"todo-api-golang/internal/todo/note"
	"todo-api-golang/pkg/apierror"
	"todo-api-golang/pkg/encode"
	"todo-api-golang/pkg/health"

	"github.com/ory/dockertest/v3"
	"github.com/stretchr/testify/assert"
)

var basePath string

func TestMain(m *testing.M) {
	config, err := config.LoadIntegrationConfig("./../..")
	if err != nil {
		log.Fatal("cannot load config:", err)
	}

	pool, err := dockertest.NewPool("")
	if err != nil {
		log.Fatalf("Could not construct pool: %s", err)
	}

	network, err := pool.CreateNetwork("integrationtest")
	if err != nil {
		log.Fatalf("Could not create Network to docker: %s \n", err)
	}

	integrationTest := NewIntegrationTest(pool, network, config)
	err = integrationTest.StartMongoDB("5.0.9")
	if err != nil {
		integrationTest.CleanUp(1)
	}

	basePath, err = integrationTest.StartTodoAPI()
	if err != nil {
		integrationTest.CleanUp(1)
	}

	println("Starting tests")
	code := m.Run()
	println("Stopping tests")

	integrationTest.CleanUp(code)
}
func createNote(t *testing.T) note.CreateNoteResponse {
	createNoteRequest := &note.CreateNoteRequest{
		Name:        "Go to the bank",
		Description: "Schedule an appointment to the bank",
	}
	request, err := encode.CreateRequest(createNoteRequest)
	assert.NoError(t, err)

	req, err := http.NewRequest(http.MethodPost, fmt.Sprintf("%s/notes", basePath), request)
	assert.NoError(t, err)

	client := http.Client{}
	response, err := client.Do(req)
	assert.NoError(t, err)
	defer response.Body.Close()

	var createNoteResponse note.CreateNoteResponse
	err = encode.ReadResponseBody(response, &createNoteResponse)
	assert.NoError(t, err)
	return createNoteResponse
}
func getNoteById(t *testing.T, id string) note.GetNoteResponse {
	req, err := http.NewRequest(http.MethodGet, fmt.Sprintf("%s/notes/%s", basePath, id), nil)
	assert.NoError(t, err)

	client := http.Client{}
	response, err := client.Do(req)
	assert.NoError(t, err)
	defer response.Body.Close()

	var getNoteResponse note.GetNoteResponse
	err = encode.ReadResponseBody(response, &getNoteResponse)
	assert.NoError(t, err)
	return getNoteResponse
}
func TestRetrieveHealth_InputIsValid_ShouldReturnStatus200WithHealthyResponse(t *testing.T) {
	req, err := http.NewRequest(http.MethodGet, fmt.Sprintf("%s/health", basePath), nil)
	assert.NoError(t, err)

	client := http.Client{}
	response, err := client.Do(req)
	assert.NoError(t, err)
	defer response.Body.Close()

	var healthResponse health.HealthResponse
	err = encode.ReadResponseBody(response, &healthResponse)
	assert.NoError(t, err)

	assert.Equal(t, http.StatusOK, response.StatusCode)
	assert.Equal(t, "Healthy", healthResponse.Status)
}

func TestCreateNote_InputIsValid_ShouldReturnStatus201WithResourceCreated(t *testing.T) {
	createNoteRequest := &note.CreateNoteRequest{
		Name:        "Go to the bank",
		Description: "Schedule an appointment to the bank",
	}
	newRequest, err := encode.CreateRequest(createNoteRequest)
	assert.NoError(t, err)

	fmt.Println(basePath)
	req, err := http.NewRequest(http.MethodPost, fmt.Sprintf("%s/notes", basePath), newRequest)
	assert.NoError(t, err)

	client := http.Client{}
	response, err := client.Do(req)
	assert.NoError(t, err)

	var createNoteResponse note.CreateNoteResponse
	err = encode.ReadResponseBody(response, &createNoteResponse)
	assert.NoError(t, err)
	defer response.Body.Close()

	assert.Equal(t, http.StatusCreated, response.StatusCode)
	assert.Equal(t, createNoteRequest.Name, createNoteResponse.Name)
	assert.Equal(t, createNoteRequest.Description, createNoteResponse.Description)
	assert.Equal(t, "To Do", string(createNoteResponse.Status))
	assert.NotEmpty(t, createNoteResponse.ID)
}
func TestUpdateNote_InputIsValid_ShouldReturnStatus204NoContent(t *testing.T) {
	createNoteResponse := createNote(t)
	updateNoteRequest := &note.UpdateNoteRequest{
		Name:        "Go to the bank",
		Description: "Schedule an appointment to the bank",
		Status:      "In Progress",
	}
	updateRequest, err := encode.CreateRequest(updateNoteRequest)
	assert.NoError(t, err)

	newUpdateRequest, err := http.NewRequest(http.MethodPatch, fmt.Sprintf("%s/notes/%s", basePath, createNoteResponse.ID), updateRequest)
	assert.NoError(t, err)

	client := http.Client{}
	updateResponse, err := client.Do(newUpdateRequest)
	assert.NoError(t, err)
	defer updateResponse.Body.Close()

	updatedNote := getNoteById(t, createNoteResponse.ID)

	assert.Equal(t, http.StatusNoContent, updateResponse.StatusCode)
	assert.Equal(t, updateNoteRequest.Status, updatedNote.Status)
}
func TestUpdateNote_InputIsInvalidStatus_ShouldReturnStatus400BadRequest(t *testing.T) {
	createNoteResponse := createNote(t)
	updateNoteRequest := &note.UpdateNoteRequest{
		Name:        "Go to the bank",
		Description: "Schedule an appointment to the bank",
		Status:      "Invalid status",
	}
	updateRequest, err := encode.CreateRequest(updateNoteRequest)
	assert.NoError(t, err)

	newUpdateRequest, err := http.NewRequest(http.MethodPatch, fmt.Sprintf("%s/notes/%s", basePath, createNoteResponse.ID), updateRequest)
	assert.NoError(t, err)

	client := http.Client{}
	updateResponse, err := client.Do(newUpdateRequest)
	assert.NoError(t, err)
	defer updateResponse.Body.Close()

	var errorResponse apierror.ErrorResponse
	err = encode.ReadResponseBody(updateResponse, &errorResponse)
	assert.NoError(t, err)

	assert.Equal(t, http.StatusBadRequest, updateResponse.StatusCode)
	assert.Equal(t, http.StatusBadRequest, errorResponse.Code)
	assert.Equal(t, "One of the request inputs is not valid.", errorResponse.Message)
}
func TestRetrieveNoteById_InputIsValidId_ShouldReturnStatus200OK(t *testing.T) {
	createNoteResponse := createNote(t)

	req, err := http.NewRequest(http.MethodGet, fmt.Sprintf("%s/notes/%s", basePath, createNoteResponse.ID), nil)
	assert.NoError(t, err)

	client := http.Client{}
	response, err := client.Do(req)
	assert.NoError(t, err)
	defer response.Body.Close()

	var getNoteResponse note.GetNoteResponse
	err = encode.ReadResponseBody(response, &getNoteResponse)
	assert.NoError(t, err)

	assert.EqualValues(t, createNoteResponse, getNoteResponse)
	assert.Equal(t, http.StatusOK, response.StatusCode)
}
