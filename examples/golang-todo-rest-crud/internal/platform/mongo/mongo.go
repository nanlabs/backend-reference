// mongo package include mongo db client related methods.
package mongo

import (
	"context"
	"fmt"
	"time"
	"todo-api-golang/internal/config"
	"todo-api-golang/pkg/logs"

	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

// NewDbClient takes mongodb configuration and returns a mongo client.
func NewDbClient(config *config.Config, logs *logs.Logs) (ClientHelper, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	url := fmt.Sprintf("mongodb://%s:%s@%s:%s", config.MongoUsername, config.MongoPassword, config.MongoHost, config.MongoPort)
	clientOptions := options.Client().ApplyURI(url).SetRegistry(mongoRegistry)

	// Connect to MongoDB
	client, err := mongo.Connect(ctx, clientOptions)
	if err != nil {
		logs.Logger.Error("Failed to connect to MongoDB")
		return nil, err
	}

	ctx, cancel = context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel()

	// Check the connection
	if err = client.Ping(ctx, nil); err != nil {
		logs.Logger.Error("Ping command to MongoDB client failed")
		return nil, err
	}
	logs.Logger.Info("MongoDB client connected")

	return &mongoClient{cl: client}, err

}

//go:generate mockery --name=DatabaseHelper --output=mongo --inpackage=true --filename=mongo_database_helper_mock.go
type DatabaseHelper interface {
	Collection(name string) CollectionHelper
	Client() ClientHelper
}

//go:generate mockery --name=CollectionHelper --output=mongo --inpackage=true --filename=mongo_collection_helper_mock.go
type CollectionHelper interface {
	FindOne(context.Context, interface{}) SingleResultHelper
	InsertOne(context.Context, interface{}) (interface{}, error)
	DeleteOne(ctx context.Context, filter interface{}) (int64, error)
	UpdateOne(ctx context.Context, filter interface{}, update interface{}, opts ...*options.UpdateOptions) (UpdateResultHelper, error)
	Find(ctx context.Context, filter interface{}, opts ...*options.FindOptions) (cur CursorHelper, err error)
}

//go:generate mockery --name=SingleResultHelper --output=mongo --inpackage=true --filename=single_result_helper_mock.go
type SingleResultHelper interface {
	Decode(v interface{}) error
}

//go:generate mockery --name=ClientHelper --output=mongo --inpackage=true --filename=mongo_client_helper_mock.go
type ClientHelper interface {
	Database(string) DatabaseHelper
	Connect() error
	StartSession() (mongo.Session, error)
}

//go:generate mockery --name=CursorHelper --output=mongo --inpackage=true --filename=mongo_cursor_helper_mock.go
type CursorHelper interface {
	Close(ctx context.Context) error
	Decode(val interface{}) error
	Err() error
	ID() int64
	Next(ctx context.Context) bool
	RemainingBatchLength() int
	TryNext(ctx context.Context) bool
}

//go:generate mockery --name=UpdateResultHelper --output=mongo --inpackage=true --filename=mongo_update_result_helper_mock.go
type UpdateResultHelper interface {
	UnmarshalBSON(b []byte) error
}

type mongoClient struct {
	cl *mongo.Client
}
type mongoDatabase struct {
	db *mongo.Database
}
type mongoCollection struct {
	coll *mongo.Collection
}
type mongoCursor struct {
	cur *mongo.Cursor
}

type mongoSingleResult struct {
	sr *mongo.SingleResult
}

type mongoSession struct {
	mongo.Session
}

func NewDatabase(cnf *config.Config, client ClientHelper) DatabaseHelper {
	return client.Database(cnf.MongoDatabase)
}

func (mc *mongoClient) Database(dbName string) DatabaseHelper {
	db := mc.cl.Database(dbName)
	return &mongoDatabase{db: db}
}

func (mc *mongoClient) StartSession() (mongo.Session, error) {
	session, err := mc.cl.StartSession()
	return &mongoSession{session}, err
}

func (mc *mongoClient) Connect() error {
	return mc.cl.Connect(context.TODO())
}

func (md *mongoDatabase) Collection(colName string) CollectionHelper {
	collection := md.db.Collection(colName)
	return &mongoCollection{coll: collection}
}

func (md *mongoDatabase) Client() ClientHelper {
	client := md.db.Client()
	return &mongoClient{cl: client}
}
func (mc *mongoCollection) Find(ctx context.Context, filter interface{}, opts ...*options.FindOptions) (cur CursorHelper, err error) {
	cursor, err := mc.coll.Find(ctx, filter, opts...)
	return &mongoCursor{cur: cursor}, err
}
func (mc *mongoCollection) FindOne(ctx context.Context, filter interface{}) SingleResultHelper {
	singleResult := mc.coll.FindOne(ctx, filter)
	return &mongoSingleResult{sr: singleResult}
}

func (mc *mongoCollection) InsertOne(ctx context.Context, document interface{}) (interface{}, error) {
	id, err := mc.coll.InsertOne(ctx, document)
	return id.InsertedID, err
}

func (mc *mongoCollection) DeleteOne(ctx context.Context, filter interface{}) (int64, error) {
	count, err := mc.coll.DeleteOne(ctx, filter)
	return count.DeletedCount, err
}

func (mc *mongoCollection) UpdateOne(ctx context.Context, filter interface{}, update interface{},
	opts ...*options.UpdateOptions) (UpdateResultHelper, error) {
	return mc.coll.UpdateOne(ctx, filter, update, opts...)
}

func (sr *mongoSingleResult) Decode(v interface{}) error {
	return sr.sr.Decode(v)
}

// Close implements CursorHelper
func (mc *mongoCursor) Close(ctx context.Context) error {
	return mc.cur.Close(ctx)
}

// Decode implements CursorHelper
func (mc *mongoCursor) Decode(val interface{}) error {
	return mc.cur.Decode(val)
}

// Err implements CursorHelper
func (mc *mongoCursor) Err() error {
	return mc.cur.Err()
}

// ID implements CursorHelper
func (mc *mongoCursor) ID() int64 {
	return mc.cur.ID()
}

// Next implements CursorHelper
func (mc *mongoCursor) Next(ctx context.Context) bool {
	return mc.cur.Next(ctx)
}

// RemainingBatchLength implements CursorHelper
func (mc *mongoCursor) RemainingBatchLength() int {
	return mc.cur.RemainingBatchLength()
}

// TryNext implements CursorHelper
func (mc *mongoCursor) TryNext(ctx context.Context) bool {
	return mc.cur.TryNext(ctx)
}
