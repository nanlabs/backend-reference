// todo package include application logic related with the todo feature.
package todo

import (
	"context"
	"fmt"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"
	"todo-api-golang/internal/config"
	"todo-api-golang/internal/platform/mongo"
	"todo-api-golang/internal/ratelimit"
	"todo-api-golang/internal/todo/note"
	"todo-api-golang/internal/trace"
	"todo-api-golang/pkg/health"
	"todo-api-golang/pkg/logs"

	"github.com/go-playground/validator"
	"github.com/gorilla/handlers"
	"github.com/gorilla/mux"
	"github.com/pkg/errors"
	"go.uber.org/zap"
)

// APIServer is the handles the setup of a todo api.
type APIServer struct {
	noteHandler note.Handler
	router      *mux.Router
	logs        *logs.Logs
	config      *config.Config
	mongoClient mongo.ClientHelper
}

// newApi creates the default configuration for the http server and set up routing.
func NewApi(config *config.Config, logs *logs.Logs, mongoClient mongo.ClientHelper) (*APIServer, error) {

	noteRepository := note.NewRepository(mongoClient, config)
	noteService := note.NewService(noteRepository)
	validator := validator.New()
	if err := validator.RegisterValidation("enum", note.ValidateEnum); err != nil {
		return nil, errors.Wrap(err, "Failed registering validators for handlers")
	}
	noteHandler := note.NewHandler(noteService, validator)

	router := setupRoutes(noteHandler, logs, config)

	return &APIServer{
		noteHandler: noteHandler,
		router:      router,
		logs:        logs,
		config:      config,
		mongoClient: mongoClient,
	}, nil
}

// setupRoutes create the routes for the todo api.
func setupRoutes(noteHandler note.Handler, logs *logs.Logs, config *config.Config) *mux.Router {
	router := mux.NewRouter()
	base := router.PathPrefix("/api/v1").Subrouter()

	base.Use(trace.ContextIDMiddleware(logs))
	base.Use(LogMiddleware(logs))

	base.HandleFunc("/health", health.HealthCheck).Methods(http.MethodGet)
	base.HandleFunc("/notes", noteHandler.GetAll).Methods(http.MethodGet)
	base.HandleFunc("/notes", noteHandler.Create).Methods(http.MethodPost)
	base.HandleFunc("/notes/{noteId}", noteHandler.GetById).Methods(http.MethodGet)
	base.HandleFunc("/notes/{noteId}", noteHandler.Update).Methods(http.MethodPatch)

	return base
}

// Start initialize the server http.
func (api *APIServer) Start() (<-chan error, error) {

	// swagger
	api.router.PathPrefix("/swagger/").Handler(http.StripPrefix("/api/v1/swagger/", http.FileServer(http.Dir("./third_party/swagger-ui-4.11.1"))))

	// CORS
	cors := handlers.CORS(handlers.AllowedOrigins([]string{"*"}))

	// // Rate limit
	ratel := ratelimit.LimitHandler(api.router, api.logs, api.config)

	// create a new server
	serverAddress := fmt.Sprintf("%s:%s", api.config.HTTPServerHost, api.config.HTTPServerPort)
	server := http.Server{
		Addr:         serverAddress,     // configure the bind address
		Handler:      cors(ratel),       // set the default handler
		ReadTimeout:  5 * time.Second,   // max time to read request from the client
		WriteTimeout: 10 * time.Second,  // max time to write response to the client
		IdleTimeout:  120 * time.Second, // max time for connections using TCP Keep-Alive
	}

	// start the server
	api.logs.Logger.Info("Starting ToDo API server", zap.String("address", serverAddress))

	errC := make(chan error, 1)

	// ListenAndServe always returns a non-nil error. After Shutdown or Close, the returned error is ErrServerClosed
	go func() {
		if err := server.ListenAndServe(); err != nil && !errors.Is(err, http.ErrServerClosed) {
			errC <- err
		}
	}()

	// trap sigterm or interrupt and gracefully shutdown the server
	ch := make(chan os.Signal, 1)
	signal.Notify(ch, os.Interrupt, syscall.SIGTERM, syscall.SIGINT)

	// block until a signal is received.
	sig := <-ch
	api.logs.Logger.Info("Shutdown signal received", zap.String("detail", sig.String()))

	// gracefully shutdown the server, waiting max 30 seconds for current operations to complete
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	if err := server.Shutdown(ctx); err != nil {
		return nil, errors.Wrap(err, "Error doing the shutdown")
	}

	api.logs.Logger.Info("Server shutdown completed")

	return errC, nil
}
