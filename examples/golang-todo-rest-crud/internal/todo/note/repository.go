// note package include application logic related with the note sub feature.
package note

import (
	"context"
	"time"
	"todo-api-golang/internal/config"

	"github.com/google/uuid"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"

	cmongo "todo-api-golang/internal/platform/mongo"
)

// Repository is a common interface to perform operations related to notes and infrastructure layer.
//
//go:generate mockery --name=Repository --output=note --inpackage=true --filename=repository_mock.go
type Repository interface {
	Create(note *Note, ctx context.Context) (*Note, error)
	GetById(id uuid.UUID, ctx context.Context) (*Note, error)
	GetAll(ctx context.Context) ([]Note, error)
	Update(note *Note, ctx context.Context) (*Note, error)
}

// repository represents the repository used for interacting with notes records.
type repository struct {
	client cmongo.ClientHelper
	config *config.Config
}

// NewRepository instantiates the note repository.
func NewRepository(client cmongo.ClientHelper, config *config.Config) Repository {
	return &repository{
		client: client,
		config: config,
	}
}

// getCollection retrieve a mongo collection.
func (r *repository) getCollection() cmongo.CollectionHelper {
	database := r.client.Database(r.config.MongoDatabase)

	return database.Collection(r.config.MongoCollection)
}

// Create inserts a new note record.
func (r *repository) Create(note *Note, ctx context.Context) (*Note, error) {

	collection := r.getCollection()

	id, err := uuid.NewRandom()
	if err != nil {
		return nil, ErrCreatingNoteId
	}
	note.ID = id
	note.CreatedAt = time.Now().UTC()
	note.Status = "To Do"

	_, err = collection.InsertOne(ctx, note)

	if err != nil {
		return nil, ErrCreatingNote
	}

	return note, nil
}

// GetById returns the requested note by searching its id.
func (r *repository) GetById(id uuid.UUID, ctx context.Context) (*Note, error) {
	var note Note

	collection := r.getCollection()
	filter := bson.M{"_id": id}

	err := collection.FindOne(ctx, filter).Decode(&note)
	if err != nil {
		return nil, ErrFoundingNote
	}

	return &note, nil
}

// GetAll returns all notes.
func (r *repository) GetAll(ctx context.Context) ([]Note, error) {
	var notes []Note

	findOptions := options.Find()
	findOptions.SetLimit(100)

	collection := r.getCollection()

	cur, err := collection.Find(ctx, bson.D{{}}, findOptions)
	if err != nil {
		return nil, ErrFoundingNote
	}

	for cur.Next(ctx) {
		var note Note
		if err := cur.Decode(&note); err != nil {
			return nil, ErrDecodingNote
		}

		notes = append(notes, note)
	}
	cur.Close(ctx)

	if notes == nil {
		return nil, ErrFoundingNote
	}

	return notes, nil
}

// Update updates the existing record with new value.
func (r *repository) Update(note *Note, ctx context.Context) (*Note, error) {
	collection := r.getCollection()
	filter := bson.M{"_id": note.ID}

	note.UpdatedAt = time.Now().UTC()

	update := bson.M{
		"$set": note,
	}

	result, err := collection.UpdateOne(ctx, filter, update)

	if result.(*mongo.UpdateResult).MatchedCount == 0 {
		return nil, ErrFoundingNote
	}

	if err != nil {
		return nil, ErrUpdatingNote
	}

	return note, nil
}
