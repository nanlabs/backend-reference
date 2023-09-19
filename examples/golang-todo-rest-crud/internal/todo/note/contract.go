// note package include application logic related with the note sub feature.
package note

// Create a note request
type CreateNoteRequest struct {
	// required: true
	Name string `json:"name" validate:"required"`
	// required: true
	Description string `json:"description" validate:"required"`
}

// Update a note request
type UpdateNoteRequest struct {
	Name        string `json:"name"`
	Description string `json:"description"`
	Status      Status `json:"status" validate:"enum"`
}

// Create a note response
// swagger:model CreateNoteResponse
type CreateNoteResponse struct {
	ID          string `json:"id"`
	Name        string `json:"name"`
	Description string `json:"description"`
	Status      Status `json:"status"`
}

// A single note returns in the response
// swagger:model GetNoteResponse
type GetNoteResponse struct {
	ID          string `json:"id"`
	Name        string `json:"name"`
	Description string `json:"description"`
	Status      Status `json:"status"`
}

// List notes returns
// swagger:model GetNotesResponse
type GetNotesResponse []GetNoteResponse
