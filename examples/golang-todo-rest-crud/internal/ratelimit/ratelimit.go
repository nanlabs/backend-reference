// ratelimit package include a method to perform rate limiting
package ratelimit

import (
	"encoding/json"
	"net/http"
	"time"

	"todo-api-golang/internal/config"
	"todo-api-golang/pkg/apierror"
	"todo-api-golang/pkg/logs"

	"github.com/didip/tollbooth/v7"
	"github.com/didip/tollbooth/v7/limiter"
)

// LimitHandler perform rate limiting on api requests.
func LimitHandler(router http.Handler, log *logs.Logs, config *config.Config) http.Handler {

	errorMessage := apierror.NewTooManyRequest()
	jsonBytes, err := json.Marshal(errorMessage)
	if err != nil {
		log.Logger.Error(err.Error())
	}

	var interval time.Duration

	switch config.HTTPRateInterval {
	case "second":
		interval = time.Second
	case "minute":
		interval = time.Minute
	case "hour":
		interval = time.Hour
	default:
		interval = time.Second
	}

	lmt := tollbooth.NewLimiter(config.HTTPRateLimit, &limiter.ExpirableOptions{DefaultExpirationTTL: interval})
	lmt.SetMessageContentType("application/json").
		SetMessage(string(jsonBytes)).
		SetMethods([]string{http.MethodPost, http.MethodPatch, http.MethodGet}).
		SetStatusCode(http.StatusTooManyRequests)

	lmth := tollbooth.LimitHandler(lmt, router)

	return lmth
}
