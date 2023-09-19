// Package classification Todo API
//
// # Documentation for Todo API
//
// Schemes: http, https
// Host: localhost:8080
// BasePath: /api/v1
// Version: 1.0.0
//
// Consumes:
// - application/json
//
// Produces:
// - application/json
//
// swagger:meta

// note package include application logic related with the note sub feature.
package note

// swagger:parameters CreateNoteRequestWrapper
type CreateNoteRequestWrapper struct {
	// in: body
	// required: true
	Body CreateNoteRequest
}

// swagger:parameters UpdateNoteRequestWrapper
type UpdateNoteRequestWrapper struct {
	// The id of the note for which the operation relates
	// in: path
	// required: true
	ID string `json:"noteId"`
	// in: body
	// required: true
	Body UpdateNoteRequest
}

// swagger:parameters NoteIdQueryParamWrapper
type NoteIdQueryParamWrapper struct {
	// The id of the note for which the operation relates
	// in: path
	// required: true
	ID string `json:"noteId"`
}

// No content is returned by this API endpoint
// swagger:response NoContentResponseWrapper
type NoContentResponseWrapper struct {
}

// swagger:response ErrorResponseWrapper
type ErrorResponseWrapper struct {
	// in: body
	Body struct {
		Type    string `json:"type"`
		Message string `json:"message"`
		Code    int    `json:"code"`
	}
}

// swagger:response ValidationErrorResponseWrapper
type ValidationErrorResponseWrapper struct {
	// in: body
	Body struct {
		Type    string            `json:"type"`
		Message string            `json:"message"`
		Detail  string            `json:"detail"`
		Code    int               `json:"code"`
		Errors  []ValidationError `json:"errors"`
	}
}
type ValidationError struct {
	Field string `json:"field"`
	Error string `json:"error"`
}
