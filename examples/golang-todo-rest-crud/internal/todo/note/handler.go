// note package include application logic related with the note sub feature.
package note

import (
	"errors"
	"net/http"
	"todo-api-golang/pkg/apierror"
	"todo-api-golang/pkg/encode"

	"github.com/google/uuid"

	"github.com/go-playground/validator"
)

// Handler is a common interface to perform operations related to notes and http.
type Handler interface {
	Create(rw http.ResponseWriter, r *http.Request)
	GetById(rw http.ResponseWriter, r *http.Request)
	GetAll(rw http.ResponseWriter, r *http.Request)
	Update(rw http.ResponseWriter, r *http.Request)
}

// handler is the implementation of the operations related to notes.
type handler struct {
	service  Service
	validate *validator.Validate
}

// NewHandler creates a note handler which have operations related to notes.
func NewHandler(service Service, validator *validator.Validate) Handler {
	return &handler{
		service:  service,
		validate: validator,
	}
}

// swagger:route POST /notes Notes CreateNoteRequestWrapper
// Creates a new note
//
// Create a new note in a database
//
// responses:
// 201: CreateNoteResponse
// 400: ValidationErrorResponseWrapper
// 422: ErrorResponseWrapper
// 500: ErrorResponseWrapper

// Create handles POST requests and create a note into the data store.
func (h *handler) Create(rw http.ResponseWriter, r *http.Request) {
	var createNoteRequest CreateNoteRequest

	if err := encode.ReadRequestBody(r, &createNoteRequest); err != nil {
		encode.WriteError(rw, apierror.NewUnprocessableEntity())
		return
	}

	if err := h.validate.Struct(&createNoteRequest); err != nil {
		encode.WriteError(rw, apierror.NewValidationBadRequest(err.(validator.ValidationErrors)))
		return
	}

	newNote := &Note{
		Name:        createNoteRequest.Name,
		Description: createNoteRequest.Description,
	}

	note, err := h.service.Create(newNote, r.Context())

	if err != nil {
		encode.WriteError(rw, apierror.NewInternal(err.Error()))
		return
	}

	noteResponse := &CreateNoteResponse{
		ID:          note.ID.String(),
		Name:        note.Name,
		Description: note.Description,
		Status:      note.Status,
	}

	encode.WriteResponse(rw, http.StatusCreated, noteResponse)
}

// swagger:route GET /notes Notes Notes
// Returns a list of notes
//
// Returns a list of notes from the database
// responses:
// 200: GetNotesResponse
// 500: ErrorResponseWrapper

// GetAll handles GET requests and returns all the notes from the data store.
func (h *handler) GetAll(rw http.ResponseWriter, r *http.Request) {
	notes, err := h.service.GetAll(r.Context())

	if err != nil {
		switch {
		case errors.Is(err, ErrFoundingNote):
			encode.WriteResponse(rw, http.StatusOK, &GetNotesResponse{})
		default:
			encode.WriteError(rw, apierror.NewInternal(err.Error()))
		}
		return
	}

	var notesResponse GetNotesResponse

	for _, note := range notes {
		noteResponse := GetNoteResponse{
			ID:          note.ID.String(),
			Name:        note.Name,
			Description: note.Description,
			Status:      note.Status,
		}
		notesResponse = append(notesResponse, noteResponse)
	}

	encode.WriteResponse(rw, http.StatusOK, &notesResponse)
}

// swagger:route GET /notes/{noteId} Notes NoteIdQueryParamWrapper
// Returns a single note
//
// Returns a single note from the database
// responses:
// 200: GetNoteResponse
// 500: ErrorResponseWrapper

// GetNote handles GET/{noteId} requests and returns a note from the data store.
func (h *handler) GetById(rw http.ResponseWriter, r *http.Request) {
	noteId, err := encode.GetUriParam(r, "noteId")
	if err != nil {
		encode.WriteError(rw, apierror.NewBadRequest(ErrInvalidNoteId.Error()))
		return
	}

	uid, err := uuid.Parse(noteId)
	if err != nil {
		encode.WriteError(rw, apierror.NewBadRequest(ErrInvalidNoteId.Error()))
		return
	}

	note, err := h.service.GetById(uid, r.Context())

	if err != nil {
		switch {
		case errors.Is(err, ErrFoundingNote):
			encode.WriteError(rw, apierror.NewNotFound())
		default:
			encode.WriteError(rw, apierror.NewInternal(err.Error()))
		}
		return
	}

	noteResponse := &GetNoteResponse{
		ID:          note.ID.String(),
		Name:        note.Name,
		Description: note.Description,
		Status:      note.Status,
	}

	encode.WriteResponse(rw, http.StatusOK, noteResponse)
}

// swagger:route PATCH /notes/{noteId} Notes UpdateNoteRequestWrapper
// Update an existing note
//
// Update a new note in a database
//
// responses:
// 204: NoContentResponseWrapper
// 400: ValidationErrorResponseWrapper
// 422: ErrorResponseWrapper
// 500: ErrorResponseWrapper

// Update handles PATCH requests and updates a note into the data store.
func (h *handler) Update(rw http.ResponseWriter, r *http.Request) {
	var updateNoteRequest UpdateNoteRequest
	noteId, err := encode.GetUriParam(r, "noteId")
	if err != nil {
		encode.WriteError(rw, apierror.NewBadRequest(ErrInvalidNoteId.Error()))
		return
	}

	uid, err := uuid.Parse(noteId)
	if err != nil {
		encode.WriteError(rw, apierror.NewBadRequest(ErrInvalidNoteId.Error()))
		return
	}

	if err := encode.ReadRequestBody(r, &updateNoteRequest); err != nil {
		encode.WriteError(rw, apierror.NewUnprocessableEntity())
		return
	}

	if err := h.validate.Struct(&updateNoteRequest); err != nil {
		encode.WriteError(rw, apierror.NewValidationBadRequest(err.(validator.ValidationErrors)))
		return
	}

	updatedNote := &Note{
		ID:          uid,
		Name:        updateNoteRequest.Name,
		Description: updateNoteRequest.Description,
		Status:      updateNoteRequest.Status,
	}

	_, err = h.service.Update(updatedNote, r.Context())

	if err != nil {
		switch {
		case errors.Is(err, ErrFoundingNote):
			encode.WriteError(rw, apierror.NewNotFound())
		default:
			encode.WriteError(rw, apierror.NewInternal(err.Error()))
		}
		return
	}

	rw.WriteHeader(http.StatusNoContent)
}
