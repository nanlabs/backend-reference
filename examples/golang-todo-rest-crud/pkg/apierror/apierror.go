// apierror package include a set of functions to handle common http responses.
package apierror

import (
	"fmt"
	"net/http"

	"github.com/go-playground/validator"
)

// Type define a custom type for handling error type message.
type Type string

// Define the a generic list of validation types.
const (
	Authorization        Type = "AUTHORIZATION"          // Authentication Failures
	BadRequest           Type = "BAD_REQUEST"            // Validation errors / BadInput
	Conflict             Type = "CONFLICT"               // Resource already exists 409
	Internal             Type = "INTERNAL"               // Server 500 errors
	NotFound             Type = "NOT_FOUND"              // For not finding resource
	TooManyRequest       Type = "TOO_MANY_REQUEST"       // For too many requests
	UnprocessableEntity  Type = "UNPROCESSABLE_ENTITY"   // Not able to decode the JSON request 422
	PayloadTooLarge      Type = "PAYLOAD_TOO_LARGE"      // For uploading tons of JSON, or an image over the limit 413
	ServiceUnavailable   Type = "SERVICE_UNAVAILABLE"    // For long running handlers
	UnsupportedMediaType Type = "UNSUPPORTED_MEDIA_TYPE" // For wrong media type
)

// ErrorResponse is a generic error response for an api.
type ErrorResponse struct {
	Type    Type              `json:"type"`
	Message string            `json:"message"`
	Code    int               `json:"code"`
	Detail  string            `json:"detail,omitempty"`
	Errors  []validationError `json:"errors,omitempty"`
}

// NewAuthorization creates a default response with status code 401.
func NewAuthorization(reason string) *ErrorResponse {
	return &ErrorResponse{
		Type:    Authorization,
		Message: reason,
		Code:    http.StatusUnauthorized,
	}
}

// NewBadRequest creates a default response with status code 400.
func NewBadRequest(reason string) *ErrorResponse {
	return &ErrorResponse{
		Type:    BadRequest,
		Message: reason,
		Code:    http.StatusBadRequest,
	}
}

// validationError contains keys for a validation error.
type validationError struct {
	Field string `json:"field"`
	Error string `json:"error"`
}

// NewValidationBadRequest creates a validation default response with status code 400.
func NewValidationBadRequest(ve validator.ValidationErrors) *ErrorResponse {
	var validationErrors []validationError
	for _, fe := range ve {
		validationErrors = append(validationErrors, validationError{fe.Field(), msgForTag(fe.Tag())})
	}

	return &ErrorResponse{
		Type:    BadRequest,
		Message: "One of the request inputs is not valid.",
		Code:    http.StatusBadRequest,
		Errors:  validationErrors,
	}
}

// msgForTag create a simple mapper from the validators tags to a custom message.
func msgForTag(tag string) string {
	switch tag {
	case "required":
		return "This field is required."
	case "enum":
		return "Invalid enum value."
	default:
		return tag
	}
}

// NewConflict creates a default response with status code 409.
func NewConflict(name string, value string) *ErrorResponse {
	return &ErrorResponse{
		Type:    Conflict,
		Message: fmt.Sprintf("Resource: %v with value: %v already exists.", name, value),
		Code:    http.StatusConflict,
	}
}

// NewUnprocessableEntity creates a default response with status code 422.
func NewUnprocessableEntity() *ErrorResponse {
	return &ErrorResponse{
		Type:    UnprocessableEntity,
		Message: "Unable to process the request.",
		Code:    http.StatusUnprocessableEntity,
	}
}

// NewInternal creates a default response with status code 500.
func NewInternal(detail string) *ErrorResponse {
	return &ErrorResponse{
		Type:    Internal,
		Message: "Internal server error.",
		Detail:  detail,
		Code:    http.StatusInternalServerError,
	}
}

// NewNotFound creates a default response with status code 404.
func NewNotFound() *ErrorResponse {
	return &ErrorResponse{
		Type:    NotFound,
		Message: "The specified resource does not exist.",
		Code:    http.StatusNotFound,
	}
}

// NewPayloadTooLarge creates a default response with status code 413.
func NewPayloadTooLarge(maxBodySize int64, contentLength int64) *ErrorResponse {
	return &ErrorResponse{
		Type:    PayloadTooLarge,
		Message: fmt.Sprintf("Max payload size of %v exceeded. Actual payload size: %v.", maxBodySize, contentLength),
		Code:    http.StatusRequestEntityTooLarge,
	}
}

// NewServiceUnavailable creates a default response with status code 503.
func NewServiceUnavailable() *ErrorResponse {
	return &ErrorResponse{
		Type:    ServiceUnavailable,
		Message: "Service unavailable or timed out.",
		Code:    http.StatusServiceUnavailable,
	}
}

// NewUnsupportedMediaType creates a default response with status code 415.
func NewUnsupportedMediaType(reason string) *ErrorResponse {
	return &ErrorResponse{
		Type:    UnsupportedMediaType,
		Message: reason,
		Code:    http.StatusUnsupportedMediaType,
	}
}

// NewTooManyRequest creates a default response with status code 429.
func NewTooManyRequest() *ErrorResponse {
	return &ErrorResponse{
		Type:    TooManyRequest,
		Message: "You have reached maximum request limit.",
		Code:    http.StatusTooManyRequests,
	}
}
