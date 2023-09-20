// trace package include a middleware to add X-Request-Id and X-Trace-Id to context used and http responses headers.
package trace

import (
	"context"
	"net/http"
	"todo-api-golang/pkg/logs"

	"github.com/google/uuid"
	"github.com/gorilla/mux"
	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
)

// ContextKeyID is used as a type for store context trace and request ids.
type ContextKeyID string

// ContextKeyRequestID is the ContextKeyID for X-Request-Id.
const ContextKeyRequestID ContextKeyID = "X-Request-Id"

// ContextKeyTraceID is the ContextKeyID for X-Trace-Id.
const ContextKeyTraceID ContextKeyID = "X-Trace-Id"

// GetContextKey will get context key id and return it as a string.
func GetContextKey(ctx context.Context, contextKey ContextKeyID) string {

	id := ctx.Value(contextKey)

	if ret, ok := id.(string); ok {
		return ret
	}
	return ""
}

// ContextIDMiddleware store request and trace id in the request context, response header and logger.
func ContextIDMiddleware(log *logs.Logs) mux.MiddlewareFunc {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(rw http.ResponseWriter, r *http.Request) {

			ctx := r.Context()

			id, err := uuid.NewRandom()
			if err != nil {
				log.Logger.Error("Error creating request id.", zap.String("detail", err.Error()))
			}

			traceIdHeader := r.Header.Get(string(ContextKeyTraceID))
			if traceIdHeader == "" {
				traceIdHeader = id.String()
			}

			ctx = context.WithValue(ctx, ContextKeyTraceID, traceIdHeader)
			ctx = context.WithValue(ctx, ContextKeyRequestID, id.String())

			rw.Header().Add(string(ContextKeyTraceID), traceIdHeader)
			rw.Header().Add(string(ContextKeyRequestID), id.String())

			ids := []zapcore.Field{
				zap.String("traceId", traceIdHeader),
				zap.String("requestId", id.String()),
			}

			log.Logger = log.Logger.With(ids...)

			r = r.WithContext(ctx)

			next.ServeHTTP(rw, r)
		})
	}
}
