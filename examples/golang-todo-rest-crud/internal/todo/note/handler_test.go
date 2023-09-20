// note package include application logic related with the note sub feature.
package note

import (
	"encoding/json"
	"io"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"

	"github.com/go-playground/validator"
	"github.com/google/uuid"
	"github.com/gorilla/mux"
	mock "github.com/stretchr/testify/mock"
	"github.com/stretchr/testify/suite"
)

type CreateNoteHandlerTestSuite struct {
	suite.Suite
	router          *mux.Router
	noteHandlerTest Handler
	mockService     *MockService
}

func TestCreateNoteHandlerTestSuite(t *testing.T) {
	suite.Run(t, &CreateNoteHandlerTestSuite{})
}

func (suite *CreateNoteHandlerTestSuite) SetupSuite() {
	validator := validator.New()
	_ = validator.RegisterValidation("enum", ValidateEnum)
	suite.mockService = NewMockService(suite.T())
	suite.noteHandlerTest = NewHandler(suite.mockService, validator)
	suite.router = mux.NewRouter()
	suite.router.HandleFunc("/notes", suite.noteHandlerTest.GetAll).Methods(http.MethodGet)
	suite.router.HandleFunc("/notes", suite.noteHandlerTest.Create).Methods(http.MethodPost)
	suite.router.HandleFunc("/notes/{noteId}", suite.noteHandlerTest.GetById).Methods(http.MethodGet)
	suite.router.HandleFunc("/notes/{noteId}", suite.noteHandlerTest.Update).Methods(http.MethodPatch)
}

func (suite *CreateNoteHandlerTestSuite) TestCreateNote_ValidTestInput_ShouldReturn201Created() {
	// Arrange
	var request = strings.NewReader(`{
		"name": "Go shopping",
		"description": "Buy groceries for the week"
	}`)

	suite.mockService.On("Create", mock.Anything, mock.Anything).Return(&Note{
		ID:          uuid.New(),
		Name:        "Go shopping",
		Description: "Buy groceries for the week",
		Status:      "To Do",
		CreatedAt:   time.Now(),
	}, nil).Once()

	// Act
	req, _ := http.NewRequest(http.MethodPost, "/notes", request)
	res := suite.ExecuteRequest(req, suite.router)

	// Assert
	suite.Equal(http.StatusCreated, res.StatusCode)
}

func (suite *CreateNoteHandlerTestSuite) TestCreateNote_InvalidInputWithMissingDescription_ShouldReturn400BadRequest() {
	// Arrange
	var request = strings.NewReader(`{
		"name": "test"
	}`)

	// Act
	req, _ := http.NewRequest(http.MethodPost, "/notes", request)
	res := suite.ExecuteRequest(req, suite.router)

	// Assert
	suite.Equal(http.StatusBadRequest, res.StatusCode)
}

func (suite *CreateNoteHandlerTestSuite) TestCreateNote_InvalidInputWithWrongJsonFormat_ShouldReturn422UnprocessableEntity() {
	// Arrange
	var request = strings.NewReader(`{
		"name": ["test"]
	}`)

	// Act
	req, _ := http.NewRequest(http.MethodPost, "/notes", request)
	res := suite.ExecuteRequest(req, suite.router)

	// Assert
	suite.Equal(http.StatusUnprocessableEntity, res.StatusCode)
}

func (suite *CreateNoteHandlerTestSuite) TestUpdateNote_ValidInput_ShouldReturn204NoContent() {
	// Arrange
	var request = strings.NewReader(`{
		"name": "Go shopping",
		"description":"Buy groceries for the week",
		"status" : "In Progress"
	}`)
	suite.mockService.On("Update", mock.Anything, mock.Anything).Return(&Note{
		ID:          uuid.New(),
		Name:        "Go shopping",
		Description: "Buy groceries for the week",
		Status:      "In Progress",
		CreatedAt:   time.Now(),
		UpdatedAt:   time.Now(),
	}, nil).Once()

	// Act
	req, _ := http.NewRequest(http.MethodPatch, "/notes/67dde89f-2dbc-4e9e-91dd-a1ef1a8a6ca3", request)
	res := suite.ExecuteRequest(req, suite.router)

	// Assert
	suite.Equal(http.StatusNoContent, res.StatusCode)
}

func (suite *CreateNoteHandlerTestSuite) TestUpdateNote_InvalidInputWithWrongJsonFormat_ShouldReturn422UnprocessableEntity() {
	// Arrange
	var request = strings.NewReader(`{
		"name": ["test"]
	}`)

	// Act
	req, _ := http.NewRequest(http.MethodPatch, "/notes/67dde89f-2dbc-4e9e-91dd-a1ef1a8a6ca3", request)
	res := suite.ExecuteRequest(req, suite.router)

	// Assert
	suite.Equal(http.StatusUnprocessableEntity, res.StatusCode)
}

func (suite *CreateNoteHandlerTestSuite) TestUpdateNote_InvalidInputWithInvalidId_ShouldReturn400BadRequest() {
	// Arrange
	var request = strings.NewReader(`{
		"name": "Go shopping",
		"description":"Buy groceries for the week",
		"status" : "In Progress"
	}`)

	// Act
	req, _ := http.NewRequest(http.MethodPatch, "/notes/12", request)
	res := suite.ExecuteRequest(req, suite.router)

	// Assert
	suite.Equal(http.StatusBadRequest, res.StatusCode)
}
func (suite *CreateNoteHandlerTestSuite) TestUpdateNote_InvalidInputWithInvalidStatus_ShouldReturn400BadRequest() {
	// Arrange
	var request = strings.NewReader(`{
		"name": "Go shopping",
		"description":"Buy groceries for the week",
		"status" : "status"
	}`)

	// Act
	req, _ := http.NewRequest(http.MethodPatch, "/notes/67dde89f-2dbc-4e9e-91dd-a1ef1a8a6ca3", request)
	res := suite.ExecuteRequest(req, suite.router)

	// Assert
	suite.Equal(http.StatusBadRequest, res.StatusCode)
}

func (suite *CreateNoteHandlerTestSuite) TestUpdateNote_ValidInputWithIdNotFound_ShouldReturn404NotFound() {
	// Arrange
	var request = strings.NewReader(`{
		"name": "Go shopping",
		"description":"Buy groceries for the week",
		"status" : "In Progress"
	}`)
	suite.mockService.On("Update", mock.Anything, mock.Anything).Return(nil, ErrFoundingNote).Once()

	// Act
	req, _ := http.NewRequest(http.MethodPatch, "/notes/67dde89f-2dbc-4e9e-91dd-a1ef1a8a6ca3", request)
	res := suite.ExecuteRequest(req, suite.router)

	// Assert
	suite.Equal(http.StatusNotFound, res.StatusCode)
}
func (suite *CreateNoteHandlerTestSuite) TestUpdateNote_ValidInputWithUnexpectedError_ShouldReturn500InternalServerError() {
	// Arrange
	var request = strings.NewReader(`{
		"name": "Go shopping",
		"description":"Buy groceries for the week",
		"status" : "In Progress"
	}`)
	suite.mockService.On("Update", mock.Anything, mock.Anything).Return(nil, ErrDecodingNote).Once()

	// Act
	req, _ := http.NewRequest(http.MethodPatch, "/notes/67dde89f-2dbc-4e9e-91dd-a1ef1a8a6ca3", request)
	res := suite.ExecuteRequest(req, suite.router)

	// Assert
	suite.Equal(http.StatusInternalServerError, res.StatusCode)
}

func (suite *CreateNoteHandlerTestSuite) TestGetAllNotes_ValidInput_ShouldReturn200OK() {
	// Arrange
	suite.mockService.On("GetAll", mock.Anything, mock.Anything).Return([]Note{
		{
			ID:          uuid.New(),
			Name:        "Go shopping",
			Description: "Buy groceries for the week",
			Status:      "In Progress",
			CreatedAt:   time.Now(),
			UpdatedAt:   time.Now(),
		},
		{
			ID:          uuid.New(),
			Name:        "Go to the bank",
			Description: "Schedule an appointment to the bank",
			Status:      "In Progress",
			CreatedAt:   time.Now(),
			UpdatedAt:   time.Now(),
		},
	}, nil).Once()

	// Act
	req, _ := http.NewRequest(http.MethodGet, "/notes", nil)
	res := suite.ExecuteRequest(req, suite.router)

	// Assert
	suite.Equal(http.StatusOK, res.StatusCode)
}
func (suite *CreateNoteHandlerTestSuite) TestGetAllNotes_ValidInputWithNoRecordsSaved_ShouldReturn200OK() {
	// Arrange
	suite.mockService.On("GetAll", mock.Anything, mock.Anything).Return(nil, ErrFoundingNote).Once()

	// Act
	req, _ := http.NewRequest(http.MethodGet, "/notes", nil)
	res := suite.ExecuteRequest(req, suite.router)

	// Assert
	suite.Equal(http.StatusOK, res.StatusCode)
}
func (suite *CreateNoteHandlerTestSuite) TestGetAllNotes_ValidInputWithUnexpectedError_ShouldReturn500InternalServerError() {
	// Arrange
	suite.mockService.On("GetAll", mock.Anything, mock.Anything).Return(nil, ErrDecodingNote).Once()

	// Act
	req, _ := http.NewRequest(http.MethodGet, "/notes", nil)
	res := suite.ExecuteRequest(req, suite.router)

	// Assert
	suite.Equal(http.StatusInternalServerError, res.StatusCode)
}

func (suite *CreateNoteHandlerTestSuite) TestGetNote_ValidInput_ShouldReturn200OK() {
	// Arrange
	suite.mockService.On("GetById", mock.Anything, mock.Anything).Return(&Note{

		ID:          uuid.New(),
		Name:        "Go shopping",
		Description: "Buy groceries for the week",
		Status:      "In Progress",
		CreatedAt:   time.Now(),
		UpdatedAt:   time.Now(),
	}, nil).Once()

	// Act
	req, _ := http.NewRequest(http.MethodGet, "/notes/67dde89f-2dbc-4e9e-91dd-a1ef1a8a6ca3", nil)
	res := suite.ExecuteRequest(req, suite.router)

	// Assert
	suite.Equal(http.StatusOK, res.StatusCode)
}
func (suite *CreateNoteHandlerTestSuite) TestGetNote_InvalidInputWithInvalidId_ShouldReturn400BadRequest() {
	// Act
	req, _ := http.NewRequest(http.MethodGet, "/notes/123", nil)
	res := suite.ExecuteRequest(req, suite.router)

	// Assert
	suite.Equal(http.StatusBadRequest, res.StatusCode)
}
func (suite *CreateNoteHandlerTestSuite) TestGetNote_ValidInputWithIdNotFound_ShouldReturn404NotFound() {
	// Arrange
	suite.mockService.On("GetById", mock.Anything, mock.Anything).Return(nil, ErrFoundingNote).Once()

	// Act
	req, _ := http.NewRequest(http.MethodGet, "/notes/67dde89f-2dbc-4e9e-91dd-a1ef1a8a6ca3", nil)
	res := suite.ExecuteRequest(req, suite.router)

	// Assert
	suite.Equal(http.StatusNotFound, res.StatusCode)
}
func (suite *CreateNoteHandlerTestSuite) TestGetNote_ValidInputWithUnexpectedError_ShouldReturn500InternalServerError() {
	// Arrange
	suite.mockService.On("GetById", mock.Anything, mock.Anything).Return(nil, ErrDecodingNote).Once()

	// Act
	req, _ := http.NewRequest(http.MethodGet, "/notes/67dde89f-2dbc-4e9e-91dd-a1ef1a8a6ca3", nil)
	res := suite.ExecuteRequest(req, suite.router)

	// Assert
	suite.Equal(http.StatusInternalServerError, res.StatusCode)
}

func (suite *CreateNoteHandlerTestSuite) ExecuteRequest(req *http.Request, router *mux.Router) *http.Response {
	recorder := httptest.NewRecorder()
	router.ServeHTTP(recorder, req)
	res := recorder.Result()
	return res
}

func (suite *CreateNoteHandlerTestSuite) GetResponseBody(res *http.Response, data any) {
	_ = json.NewDecoder(io.Reader(res.Body)).Decode(&data)
}
