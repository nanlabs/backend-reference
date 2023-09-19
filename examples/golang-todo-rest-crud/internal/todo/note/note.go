// note package include application logic related with the note sub feature.
package note

import (
	"errors"
	"time"

	"github.com/google/uuid"
)

// Note defines the fields of a note.
type Note struct {
	ID          uuid.UUID `bson:"_id,omitempty"`
	Name        string    `bson:"name,omitempty"`
	Description string    `bson:"description,omitempty"`
	Status      Status    `bson:"status,omitempty"`
	CreatedAt   time.Time `bson:"createdAt,omitempty"`
	UpdatedAt   time.Time `bson:"updatedAt,omitempty"`
}

// List of all possible errors managed by the note package.
var (
	ErrInvalidNoteId  = errors.New("error invalid id")
	ErrCreatingNoteId = errors.New("error creating note id")
	ErrDecodingNote   = errors.New("error decoding note")
	ErrUpdatingNote   = errors.New("error updating note")
	ErrCreatingNote   = errors.New("error creating note")
	ErrFoundingNote   = errors.New("error founding note")
)

// swagger:enum Status
// State is a type that defines all possible states of a note.
type Status string

const (
	Todo       Status = "To Do"
	InProgress Status = "In Progress"
	Done       Status = "Done"
)

// IsValid defines when a status is a valid value.
func (s Status) IsValid() bool {
	switch s {
	case Todo, InProgress, Done:
		return true
	default:
		return false
	}
}
