// note package include application logic related with the note sub feature.
package note

import (
	"context"

	"github.com/google/uuid"
)

// Service is a common interface to perform operations related to notes.
//
//go:generate mockery --name=Service --output=note --inpackage=true --filename=service_mock.go
type Service interface {
	Create(note *Note, ctx context.Context) (*Note, error)
	GetById(id uuid.UUID, ctx context.Context) (*Note, error)
	GetAll(ctx context.Context) ([]Note, error)
	Update(note *Note, ctx context.Context) (*Note, error)
}

// service represents the service used for interacting with notes.
type service struct {
	repository Repository
}

// NewService instantiates the note service.
func NewService(repository Repository) Service {
	return &service{
		repository: repository,
	}
}

// Create handles create note business logic.
func (s *service) Create(note *Note, ctx context.Context) (*Note, error) {
	newNote, err := s.repository.Create(note, ctx)

	if err != nil {
		return nil, err
	}

	return newNote, nil
}

// Create handles the note update business logic.
func (s *service) Update(note *Note, ctx context.Context) (*Note, error) {
	updatedNote, err := s.repository.Update(note, ctx)

	if err != nil {
		return nil, err
	}

	return updatedNote, nil
}

// GetById handles the business logic requesting a note.
func (s *service) GetById(id uuid.UUID, ctx context.Context) (*Note, error) {

	note, err := s.repository.GetById(id, ctx)

	if err != nil {
		return nil, err
	}

	return note, nil
}

// GetAll handles the business logic requesting multiple notes.
func (s *service) GetAll(ctx context.Context) ([]Note, error) {

	notes, err := s.repository.GetAll(ctx)

	if err != nil {
		return nil, err
	}

	return notes, nil
}
