// note package include application logic related with the note sub feature.
package note

import (
	"context"
	"testing"
	"time"

	"github.com/google/uuid"
	mock "github.com/stretchr/testify/mock"
	"github.com/stretchr/testify/suite"
)

type CreateNoteServiceTestSuite struct {
	suite.Suite
	noteService        Service
	mockNoteRepository *MockRepository
}

func TestCreateNoteServiceTestSuite(t *testing.T) {
	suite.Run(t, &CreateNoteServiceTestSuite{})
}

func (suite *CreateNoteServiceTestSuite) SetupSuite() {
	suite.mockNoteRepository = NewMockRepository(suite.T())
	suite.noteService = NewService(suite.mockNoteRepository)
}

func (suite *CreateNoteServiceTestSuite) TestCreateNote_ValidTestInput_ShouldReturnCreatedNoteWithoutError() {
	note := &Note{
		ID:          uuid.New(),
		Name:        "Go shopping",
		Description: "Buy groceries for the week",
	}
	newNote := &Note{
		ID:          uuid.New(),
		Name:        "Go shopping",
		Description: "Buy groceries for the week",
		Status:      "To Do",
		CreatedAt:   time.Now(),
	}

	suite.mockNoteRepository.On("Create", mock.Anything, mock.Anything).Return(newNote, nil).Once()

	newNote, err := suite.noteService.Create(note, context.TODO())

	suite.Nil(err)
	suite.NotNil(newNote)
}

func (suite *CreateNoteServiceTestSuite) TestCreateNote_ValidTestInput_ShouldReturnError() {
	note := &Note{
		Name:        "note",
		Description: "note description",
	}

	suite.mockNoteRepository.On("Create", mock.Anything, mock.Anything).Return(nil, ErrCreatingNote).Once()

	newNote, err := suite.noteService.Create(note, context.TODO())

	suite.Equal(ErrCreatingNote, err)
	suite.Nil(newNote)
}
func (suite *CreateNoteServiceTestSuite) TestUpdateNote_ValidTestInput_ShouldReturnUpdatedNoteWithoutError() {
	note := &Note{
		ID:          uuid.New(),
		Name:        "Go shopping",
		Description: "Buy groceries for the week",
		Status:      "In Progress",
	}
	updatedNote := &Note{
		ID:          uuid.New(),
		Name:        "Go shopping",
		Description: "Buy groceries for the week",
		Status:      "In Progress",
		CreatedAt:   time.Now(),
		UpdatedAt:   time.Now(),
	}

	suite.mockNoteRepository.On("Update", mock.Anything, mock.Anything).Return(updatedNote, nil).Once()

	updatedNote, err := suite.noteService.Update(note, context.TODO())

	suite.Nil(err)
	suite.NotNil(updatedNote)
}

func (suite *CreateNoteServiceTestSuite) TestUpdateNote_ValidTestInput_ShouldReturnError() {
	note := &Note{
		ID:          uuid.New(),
		Name:        "Go shopping",
		Description: "Buy groceries for the week",
		Status:      "In Progress",
	}

	suite.mockNoteRepository.On("Update", mock.Anything, mock.Anything).Return(nil, ErrFoundingNote).Once()

	newNote, err := suite.noteService.Update(note, context.TODO())

	suite.Equal(ErrFoundingNote, err)
	suite.Nil(newNote)
}

func (suite *CreateNoteServiceTestSuite) TestGetNote_ValidTestInput_ShouldReturnNoteWithoutError() {
	note := &Note{
		ID:          uuid.New(),
		Name:        "Go shopping",
		Description: "Buy groceries for the week",
		Status:      "In Progress",
		CreatedAt:   time.Now(),
		UpdatedAt:   time.Now(),
	}

	suite.mockNoteRepository.On("GetById", mock.Anything, mock.Anything).Return(note, nil).Once()

	retrievedNote, err := suite.noteService.GetById(uuid.New(), context.TODO())

	suite.Nil(err)
	suite.NotNil(retrievedNote)
}

func (suite *CreateNoteServiceTestSuite) TestGetNotes_ValidTestInput_ShouldReturnError() {

	suite.mockNoteRepository.On("GetAll", mock.Anything).Return(nil, ErrFoundingNote).Once()

	retrievedNotes, err := suite.noteService.GetAll(context.TODO())

	suite.Equal(ErrFoundingNote, err)
	suite.Nil(retrievedNotes)
}
func (suite *CreateNoteServiceTestSuite) TestGetNotes_ValidTestInput_ShouldReturnNoteWithoutError() {
	notes := []Note{
		{
			ID:          uuid.New(),
			Name:        "Go shopping",
			Description: "Buy groceries for the week",
			Status:      "In Progress",
			CreatedAt:   time.Now(),
			UpdatedAt:   time.Now(),
		}}

	suite.mockNoteRepository.On("GetAll", mock.Anything, mock.Anything).Return(notes, nil).Once()

	retrievedNotes, err := suite.noteService.GetAll(context.TODO())

	suite.Nil(err)
	suite.NotNil(retrievedNotes)
}

func (suite *CreateNoteServiceTestSuite) TestGetNote_ValidTestInput_ShouldReturnError() {

	suite.mockNoteRepository.On("GetById", mock.Anything, mock.Anything).Return(nil, ErrFoundingNote).Once()

	retrievedNote, err := suite.noteService.GetById(uuid.New(), nil)

	suite.Equal(ErrFoundingNote, err)
	suite.Nil(retrievedNote)
}
