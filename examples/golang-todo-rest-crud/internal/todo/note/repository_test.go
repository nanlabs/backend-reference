// note package include application logic related with the note sub feature.
package note

import (
	"context"
	"testing"
	"time"
	"todo-api-golang/internal/config"
	"todo-api-golang/internal/platform/mongo"

	m "go.mongodb.org/mongo-driver/mongo"

	"github.com/google/uuid"
	mock "github.com/stretchr/testify/mock"
	"github.com/stretchr/testify/suite"
)

type CreateNoteRepositoryTestSuite struct {
	suite.Suite
	mockMongoClient       *mongo.MockClientHelper
	mockMongoDatabase     *mongo.MockDatabaseHelper
	mockMongoCollection   *mongo.MockCollectionHelper
	mockMongoSingleResult *mongo.MockSingleResultHelper
	noteRepository        Repository
}

func TestCreateNoteRepositoryTestSuite(t *testing.T) {
	suite.Run(t, &CreateNoteRepositoryTestSuite{})
}

func (suite *CreateNoteRepositoryTestSuite) SetupSuite() {
	suite.mockMongoClient = mongo.NewMockClientHelper(suite.T())
	suite.mockMongoCollection = mongo.NewMockCollectionHelper(suite.T())
	suite.mockMongoSingleResult = mongo.NewMockSingleResultHelper(suite.T())
	suite.mockMongoDatabase = mongo.NewMockDatabaseHelper(suite.T())
	suite.noteRepository = NewRepository(suite.mockMongoClient, &config.Config{
		HTTPServerHost:   "",
		HTTPServerPort:   "",
		HTTPRateLimit:    0,
		HTTPRateInterval: "",
		MongoHost:        "",
		MongoPort:        "",
		MongoDatabase:    "",
		MongoCollection:  "",
		MongoUsername:    "",
		MongoPassword:    "",
	})

	suite.mockMongoClient.On("Database", mock.Anything).Return(suite.mockMongoDatabase)
	suite.mockMongoDatabase.On("Collection", mock.Anything).Return(suite.mockMongoCollection)
}

func (suite *CreateNoteRepositoryTestSuite) TestCreateNote_ValidTestInput_ShouldReturnCreatedNoteWithoutError() {
	note := &Note{
		Name:        "Go shopping",
		Description: "Buy groceries for the week",
	}
	newNote := &Note{
		ID:          uuid.New(),
		Name:        "Go shopping",
		Description: "Buy groceries for the week",
		Status:      Todo,
		CreatedAt:   time.Now(),
	}

	suite.mockMongoCollection.On("InsertOne", mock.Anything, mock.Anything).Return(newNote, nil).Once()

	newNote, err := suite.noteRepository.Create(note, context.TODO())

	suite.Nil(err)
	suite.NotNil(newNote)
}
func (suite *CreateNoteRepositoryTestSuite) TestUpdateNote_ValidTestInput_ShouldReturnUpdatedNoteWithoutError() {
	note := &Note{
		Name:        "Go shopping",
		Description: "Buy groceries for the week",
	}
	suite.mockMongoCollection.On("UpdateOne", mock.Anything, mock.Anything, mock.Anything).Return(&m.UpdateResult{MatchedCount: 1}, nil).Once()

	newNote, err := suite.noteRepository.Update(note, context.TODO())

	suite.Nil(err)
	suite.NotNil(newNote)
}

func (suite *CreateNoteRepositoryTestSuite) TestGetNote_ValidTestInput_ShouldReturnNoteWithoutError() {

	suite.mockMongoCollection.On("FindOne", mock.Anything, mock.Anything).Return(suite.mockMongoSingleResult).Once()
	suite.mockMongoSingleResult.On("Decode", mock.Anything).Return(nil)
	note, err := suite.noteRepository.GetById(uuid.New(), context.TODO())

	suite.Nil(err)
	suite.NotNil(note)
}
