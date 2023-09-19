// todo package include application logic related with the todo feature.
package todo

import (
	"net/http"
	"time"
	"todo-api-golang/pkg/logs"

	"github.com/gorilla/mux"
	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
)

// ResponseRecorder is a wrapper of the standard http.ResponseWriter.
type ResponseRecorder struct {
	http.ResponseWriter
	StatusCode int
	Body       []byte
}

// WriteHeader writes an HTTP response header.
func (rec *ResponseRecorder) WriteHeader(statusCode int) {
	rec.StatusCode = statusCode
	rec.ResponseWriter.WriteHeader(statusCode)
}

// Write writes the body of an HTTP Response.
func (rec *ResponseRecorder) Write(body []byte) (int, error) {
	rec.Body = body
	return rec.ResponseWriter.Write(body)
}

// IsServerErrorStatusCode return a true if the response recorder has an 50x status code.
func (rec *ResponseRecorder) IsServerErrorStatusCode() bool {
	switch rec.StatusCode {
	case
		http.StatusInternalServerError,
		http.StatusNotImplemented,
		http.StatusBadGateway,
		http.StatusServiceUnavailable,
		http.StatusGatewayTimeout,
		http.StatusHTTPVersionNotSupported,
		http.StatusVariantAlsoNegotiates,
		http.StatusInsufficientStorage,
		http.StatusLoopDetected,
		http.StatusNotExtended,
		http.StatusNetworkAuthenticationRequired:
		return true
	default:
		return false
	}
}

// LogMiddleware is a middleware to include logging in http calls.
func LogMiddleware(log *logs.Logs) mux.MiddlewareFunc {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			startTime := time.Now()

			rec := &ResponseRecorder{
				ResponseWriter: w,
				StatusCode:     http.StatusOK,
			}
			log.Logger.Info(
				"Start http request",
				zap.String("method", r.Method),
				zap.String("url", r.URL.String()),
			)

			next.ServeHTTP(rec, r)
			duration := time.Since(startTime)

			responseMsg := "Finish http request"
			responseLog := []zapcore.Field{
				zap.String("method", r.Method),
				zap.String("url", r.URL.String()),
				zap.Int("statusCode", rec.StatusCode),
				zap.Duration("duration", duration),
			}

			ok := rec.IsServerErrorStatusCode()
			if ok {
				responseLogWithBody := append(responseLog, zap.ByteString("body", rec.Body))
				log.Logger.Error(responseMsg, responseLogWithBody...)
				return
			}
			log.Logger.Info(responseMsg, responseLog...)
		})
	}
}
