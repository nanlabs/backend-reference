// logs package include the configuration for the loggers of the application
package logs

import (
	"go.uber.org/zap"
)

type Logs struct {
	Logger *zap.Logger
}

// New creates the default logger configuration
func New() (*Logs, error) {
	logger, err := zap.NewProduction()
	if err != nil {
		return nil, err
	}

	return &Logs{
		Logger: logger,
	}, nil
}
